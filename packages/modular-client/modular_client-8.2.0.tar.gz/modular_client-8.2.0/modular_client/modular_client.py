from __future__ import print_function, division
import serial
import time
import atexit
import json
import functools
import operator
import platform
import os
import inflection
import sre_yield

from serial_interface import SerialInterface, SerialInterfaces, find_serial_interface_ports, WriteFrequencyError

try:
    from pkg_resources import get_distribution, DistributionNotFound
    _dist = get_distribution('modular_client')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'modular_client')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False
BAUDRATE = 115200

class ModularClient(object):
    '''ModularClient contains an instance of serial_interface.SerialInterface and
    adds methods to it, like auto discovery of available modular devices in
    Linux, Windows, and Mac OS X. This class automatically creates methods from
    available functions reported by the modular device when it is running the
    appropriate firmware. This is the modular device client library for
    communicating with and calling remote methods on modular device servers.

    Example Usage:

    from modular_client import ModularClient
    dev = ModularClient()
    # Will try to automatically find device if one available. This may be slow if it
    # needs to search many serial ports. If it is not found automatically or to
    # speed up, specify port directly.
    dev = ModularClient(port='/dev/ttyACM0') # Linux specific port
    dev = ModularClient(port='/dev/tty.usbmodem262471') # Mac OS X specific port
    dev = ModularClient(port='COM3') # Windows specific port
    dev.get_device_id()
    dev.get_methods()
    '''
    _TIMEOUT = 0.05
    _WRITE_READ_DELAY = 0.001
    _WRITE_WRITE_DELAY = 0.005
    _METHOD_ID_GET_METHOD_IDS = 0

    def __init__(self,*args,**kwargs):
        name = None
        form_factor = None
        serial_number = None
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        if 'try_ports' in kwargs:
            try_ports = kwargs.pop('try_ports')
        else:
            try_ports = None
        if 'baudrate' not in kwargs:
            kwargs.update({'baudrate': BAUDRATE})
        elif (kwargs['baudrate'] is None) or (str(kwargs['baudrate']).lower() == 'default'):
            kwargs.update({'baudrate': BAUDRATE})
        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self._TIMEOUT})
        if 'write_read_delay' not in kwargs:
            kwargs.update({'write_read_delay': self._WRITE_READ_DELAY})
        if 'write_write_delay' not in kwargs:
            kwargs.update({'write_write_delay': self._WRITE_WRITE_DELAY})
        if 'name' in kwargs:
            name = kwargs.pop('name')
        if 'form_factor' in kwargs:
            form_factor = kwargs.pop('form_factor')
        if 'serial_number' in kwargs:
            serial_number = kwargs.pop('serial_number')
        if ('port' not in kwargs) or (kwargs['port'] is None):
            port =  find_modular_device_port(baudrate=kwargs['baudrate'],
                                             name=name,
                                             form_factor=form_factor,
                                             serial_number=serial_number,
                                             try_ports=try_ports,
                                             debug=kwargs['debug'])
            kwargs.update({'port': port})

        t_start = time.time()
        self._serial_interface = SerialInterface(*args,**kwargs)
        atexit.register(self._exit_modular_client)
        self._method_dict = self._get_method_dict()
        try:
            self._method_dict_inv = dict([(v,k) for (k,v) in self._method_dict.items()])
        except AttributeError:
            self._method_dict_inv = dict([(v,k) for (k,v) in self._method_dict.iteritems()])
        self._create_methods()
        t_end = time.time()
        self._debug_print('Initialization time =', (t_end - t_start))

    def _debug_print(self, *args):
        if self.debug:
            print(*args)

    def _exit_modular_client(self):
        pass

    def _args_to_request(self,*args):
        request = json.dumps(args,separators=(',',':'))
        request += '\n';
        return request

    def _handle_response(self,response,request_id):
        if response is None:
            error_message = 'Did not receive server response.'
            raise IOError(error_message)
        try:
            response_dict = json_string_to_dict(response)
        except Exception as e:
            error_message = 'Error:\n{0}\nUnable to parse server response:\n{1}'.format(str(e),response)
            raise IOError(error_message)
        try:
            response_id  = response_dict.pop('id')
        except KeyError:
            error_message = 'Server response does not contain id member:\n{0}'.format(response)
            raise IOError(error_message)
        if not response_id == request_id:
            error_message = 'Response id:\n{0}\nDoes not match request id:\n{1}\nin response:{2}'.format(response_id,request_id,response)
            raise IOError(error_message)
        try:
            error = response_dict.pop('error')
            try:
                message = error.pop('message')
            except KeyError:
                message = ''
            try:
                data = error.pop('data')
            except KeyError:
                data = ''
            try:
                code = error.pop('code')
            except KeyError:
                code = ''
            error_message = '(from server) message: {0}, data: {1}, code: {2}'.format(message,data,code)
            raise IOError(error_message)
        except KeyError:
            pass
        try:
            result  = response_dict.pop('result')
        except KeyError:
            error_message = 'Server response does not contain result member:\n{0}'.format(response)
            raise IOError(error_message)
        return result

    def _send_request_get_result(self,*args):
        '''
        Sends request to server over serial port and
        returns response result
        '''
        request = self._args_to_request(*args)
        self._debug_print('request', request)
        response = self._serial_interface.write_read(request,use_readline=True,check_write_freq=True)
        self._debug_print('response', response)
        if (type(response) != str):
            response = response.decode('utf-8')
        self._debug_print('type(response)', type(response))
        result = self._handle_response(response,args[0])
        return result

    def _get_method_dict(self):
        method_dict = self._send_request_get_result(self._METHOD_ID_GET_METHOD_IDS)
        return method_dict

    def _send_request_by_method_name(self,name,*args):
        method_id = self._method_dict[name]
        method_args = [method_id]
        method_args.extend(args)
        result = self._send_request_get_result(*method_args)
        return result

    def _method_func_base(self,method_name,*args):
        if len(args) == 1 and type(args[0]) is dict:
            args_dict = args[0]
            args_list = self._args_dict_to_list(args_dict)
        else:
            args_list = args
        try:
            result = self._send_request_by_method_name(method_name,*args_list)
        except Exception as e:
            write_data = self._serial_interface._write_data
            read_data = self._serial_interface._read_data
            error_message = 'serial_interface.write_data:{0},serial_interface.read_data:{1}'.format(write_data,read_data)
            raise e from Exception(error_message)
        return result

    def _create_methods(self):
        self._method_func_dict = {}
        for method_id, method_name in sorted(self._method_dict_inv.items()):
            method_func = functools.partial(self._method_func_base, method_name)
            setattr(self,inflection.underscore(method_name),method_func)
            self._method_func_dict[method_name] = method_func

    def _args_dict_to_list(self,args_dict):
        key_set = set(args_dict.keys())
        try:
            order_list = sorted([(num,name) for (name,num) in order_dict.items()])
        except AttributeError:
            order_list = sorted([(num,name) for (name,num) in order_dict.iteritems()])
        args_list = [args_dict[name] for (num, name) in order_list]
        return args_list

    def close(self):
        '''
        Close the device serial port.
        '''
        self._serial_interface.close()

    def get_port(self):
        return self._serial_interface.port

    def get_methods(self):
        '''
        Get a list of modular methods automatically attached as class methods.
        '''
        return [inflection.underscore(key) for key in list(self._method_dict.keys())]

    def call_get_result(self,method_name,*args):
        method_name = inflection.camelize(method_name,False)
        return self._send_request_get_result(method_name,*args)

    def call(self,method_name,*args):
        self.call_get_result(method_name,*args)

    def send_json_request(self,request):
        '''
        Sends json request to device over serial port and returns result
        '''
        request_python = json.loads(request)
        try:
            request_id = request_python["id"]
        except TypeError:
            pass
        except KeyError:
            error_message = 'Request does not contain an id:\n{0}'.format(request)
            raise IOError(error_message)
        try:
            request_python["method"] = inflection.camelize(request_python["method"],False)
        except TypeError:
            pass
        except KeyError:
            error_message = 'Request does not contain a method:\n{0}'.format(request)
            raise IOError(error_message)
        try:
            request_python[0] = inflection.camelize(request_python[0],False)
            request_id = request_python[0]
        except IndexError:
            error_message = 'Request does not contain a method:\n{0}'.format(request)
            raise IOError(error_message)
        request = json.dumps(request_python,separators=(',',':'))
        request += '\n'
        self._debug_print('request', request)
        response = self._serial_interface.write_read(request,use_readline=True,check_write_freq=True)
        self._debug_print('response', response)
        result = self._handle_response(response,request_id)
        return result

    def convert_to_json(self,python_to_convert,response_indent=None):
        '''
        Convert python object to json string.
        '''
        converted_json = json.dumps(python_to_convert,separators=(',',':'),indent=response_indent)
        return converted_json

    def save_device_id(self,output_directory):
        '''
        Save device_id as a json file.
        '''
        if output_directory is None:
            output_directory = os.path.join(os.path.curdir)
        elif len(os.path.splitext(output_directory)[1]) > 0:
            output_directory = os.path.dirname(output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        result = self.call_get_result('getDeviceId')
        output = {}
        output['id'] = 'getDeviceId'
        output['result'] = result
        output_path = os.path.join(output_directory,'device_id.json')
        with open(output_path,'w') as output_file:
            json.dump(output,output_file,separators=(',',':'),indent=2)
        try:
            os.removedirs(output_directory)
        except OSError:
            pass

    def save_device_info(self,output_directory):
        '''
        Save device_info as a json file.
        '''
        if output_directory is None:
            output_directory = os.path.join(os.path.curdir)
        elif len(os.path.splitext(output_directory)[1]) > 0:
            output_directory = os.path.dirname(output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        result = self.call_get_result('getDeviceInfo')
        output = {}
        output['id'] = 'getDeviceInfo'
        output['result'] = result
        output_path = os.path.join(output_directory,'device_info.json')
        with open(output_path,'w') as output_file:
            json.dump(output,output_file,separators=(',',':'),indent=2)
        try:
            os.removedirs(output_directory)
        except OSError:
            pass

    def save_api(self,output_directory,verbosity='DETAILED',firmware='ALL'):
        '''
        Save api as a set of json files.
        '''
        if output_directory is None:
            output_directory = os.path.join(os.path.curdir,'api')
        elif len(os.path.splitext(output_directory)[1]) > 0:
            output_directory = os.path.dirname(output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        device_info = self.call_get_result('getDeviceInfo')
        for firmware_info in device_info['firmware']:
            if (firmware == 'ALL') or (firmware == firmware_info['name']):
                result = self.call_get_result('getApi',verbosity,[firmware_info['name']])
                api = {}
                api['id'] = 'getApi'
                api['result'] = result
                output_path = os.path.join(output_directory,firmware_info['name'] + '.json')
                with open(output_path,'w') as api_file:
                    json.dump(api,api_file,separators=(',',':'),indent=2)
        try:
            os.removedirs(output_directory)
        except OSError:
            pass

class ModularClients(dict):
    '''ModularClients inherits from dict and automatically populates it with
    modular clients on all available serial ports. Access each individual client
    with three keys, the device name, the form_factor, and the serial_number. If
    you want to connect multiple ModularClients with the same name and
    form_factor at the same time, first make sure they have unique
    serial_numbers by connecting each device one by one and using the
    set_serial_number method on each device.

    Example Usage:

    from modular_client import ModularClients
    devs = ModularClients()
    # Will try to automatically find all available devices. This may be slow if it
    # needs to search many serial ports. If they are not found automatically or to
    # speed up, specify ports to use.
    devs = ModularClients(use_ports=['/dev/ttyACM0','/dev/ttyACM1']) # Linux
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]') # Linux string RE alternative
    devs = ModularClients(use_ports=['/dev/tty.usbmodem262471','/dev/tty.usbmodem262472']) # Mac OS X
    devs = ModularClients(use_ports='(/dev/tty\.usbmodem26247)[1-2]') # Mac OS X RE Alternative
    devs = ModularClients(use_ports=['COM3','COM4']) # Windows
    devs = ModularClients(use_ports='(COM)[3-4]') # Windows RE Alternative
    devs.items()
    # dev = devs[name][form_factor][serial_number]
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',keys=[0,1])
    dev = devs[0]
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',keys='(device)[0-1]')
    dev = devs['device0']
    devs = ModularClients(use_ports='(/dev/ttyACM)[0-1]',ports_as_keys=True)
    dev = devs['/dev/ttyACM0']
    '''
    def __init__(self,*args,**kwargs):
        if 'key_port_debug' in kwargs:
            self.key_port_debug = kwargs.pop('key_port_debug')
        else:
            self.key_port_debug = False
        try:
            modular_device_ports = kwargs.pop('use_ports')
            if modular_device_ports is None:
                raise KeyError
            if isinstance(modular_device_ports,str):
                modular_device_ports = list(sre_yield.AllStrings(modular_device_ports))
            if len(modular_device_ports) != len(set(modular_device_ports)):
                raise KeyError
        except KeyError:
            modular_device_ports = find_modular_device_ports(*args,**kwargs)

        try:
            keys = kwargs.pop('keys')
            if keys is None:
                raise KeyError
            if isinstance(keys,str):
                keys = list(sre_yield.AllStrings(keys))
            if len(keys) != len(modular_device_ports):
                raise KeyError
            if len(keys) != len(set(keys)):
                raise KeyError
        except (KeyError,TypeError):
            keys = [None] * len(modular_device_ports)

        try:
            ports_as_keys = kwargs.pop('ports_as_keys')
            if ports_as_keys is None:
                raise KeyError
        except KeyError:
            ports_as_keys = False

        for key,port in zip(keys,modular_device_ports):
            self._add_device(key,port,ports_as_keys,*args,**kwargs)

    def _key_port_debug_print(self,key,port):
        if self.key_port_debug:
            print('key={0}, port={1}'.format(key,port))

    def _add_device(self,key,port,ports_as_keys,*args,**kwargs):
        kwargs.update({'port': port})
        dev = ModularClient(*args,**kwargs)
        if (key is None) and (not ports_as_keys):
            device_id = dev.get_device_id()
            name = device_id['name']
            form_factor = device_id['form_factor']
            serial_number = device_id['serial_number']
            if name not in self:
                self[name] = {}
            if form_factor not in self[name]:
                self[name][form_factor] = {}
            self[name][form_factor][serial_number] = dev
            self._key_port_debug_print('[{0}][{1}][{2}]'.format(name,form_factor,serial_number),port)
        elif key is not None:
            self[key] = dev
            self._key_port_debug_print(key,port)
        else:
            key = dev.get_port()
            self[key] = dev
            self._key_port_debug_print(key,port)

def check_dict_for_key(d,k,dname=''):
    if not k in d:
        if not dname:
            dname = 'dictionary'
        raise IOError('{0} does not contain {1}'.format(dname,k))

def json_string_to_dict(json_string):
    json_dict =  json.loads(json_string,object_hook=json_decode_dict)
    return json_dict

def json_decode_dict(data):
    '''
    Object hook for decoding dictionaries from serialized json data. Ensures that
    all strings are unpacked as str objects rather than unicode.
    '''
    rv = {}
    try:
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = json_decode_list(value)
            elif isinstance(value, dict):
                value = json_decode_dict(value)
            rv[key] = value
    except (AttributeError,NameError):
        for key, value in data.items():
            if isinstance(value, list):
                value = json_decode_list(value)
            elif isinstance(value, dict):
                value = json_decode_dict(value)
            rv[key] = value
    return rv

def json_decode_list(data):
    '''
    Object hook for decoding lists from serialized json data. Ensures that
    all strings are unpacked as str objects rather than unicode.
    '''
    rv = []
    try:
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = json_decode_list(item)
            elif isinstance(item, dict):
                item = json_decode_dict(item)
            rv.append(item)
    except NameError:
        for item in data:
            if isinstance(item, list):
                item = json_decode_list(item)
            elif isinstance(item, dict):
                item = json_decode_dict(item)
            rv.append(item)
    return rv

def find_modular_device_ports(baudrate=None,
                              name=None,
                              form_factor=None,
                              serial_number=None,
                              try_ports=None,
                              debug=DEBUG,
                              *args,
                              **kwargs):
    serial_interface_ports = find_serial_interface_ports(try_ports=try_ports, debug=debug)
    os_type = platform.system()
    if os_type == 'Darwin':
        serial_interface_ports = [x for x in serial_interface_ports if 'tty.usbmodem' in x or 'tty.usbserial' in x]

    if type(name) is str:
        name = [name]
    if type(form_factor) is str:
        form_factor = [form_factor]
    if type(serial_number) is int:
        serial_number = [serial_number]

    modular_device_ports = {}
    for port in serial_interface_ports:
        try:
            dev = ModularClient(port=port,baudrate=baudrate,debug=debug)
            device_id = dev.get_device_id()
            if ((name is None ) and (device_id['name'] is not None)) or (device_id['name'] in name):
                if ((form_factor is None) and (device_id['form_factor'] is not None)) or (device_id['form_factor'] in form_factor):
                    if ((serial_number is None) and (device_id['serial_number'] is not None)) or (device_id['serial_number'] in serial_number):
                        modular_device_ports[port] = {'name': device_id['name'],
                                                      'form_factor': device_id['form_factor'],
                                                      'serial_number': device_id['serial_number']}
            dev.close()
        except (serial.SerialException, IOError):
            pass
    return modular_device_ports

def find_modular_device_port(baudrate=None,
                             name=None,
                             form_factor=None,
                             serial_number=None,
                             try_ports=None,
                             debug=DEBUG):
    modular_device_ports = find_modular_device_ports(baudrate=baudrate,
                                                     name=name,
                                                     form_factor=form_factor,
                                                     serial_number=serial_number,
                                                     try_ports=try_ports,
                                                     debug=debug)
    if len(modular_device_ports) == 1:
        return list(modular_device_ports.keys())[0]
    elif len(modular_device_ports) == 0:
        serial_interface_ports = find_serial_interface_ports(try_ports)
        err_string = 'Could not find any Modular devices. Check connections and permissions.\n'
        err_string += 'Tried ports: ' + str(serial_interface_ports)
        raise RuntimeError(err_string)
    else:
        err_string = 'Found more than one Modular device. Specify port or name and/or form_factor and/or serial_number.\n'
        err_string += 'Matching ports: ' + str(modular_device_ports)
        raise RuntimeError(err_string)


# -----------------------------------------------------------------------------------------
if __name__ == '__main__':

    debug = False
    dev = ModularClient(debug=debug)
