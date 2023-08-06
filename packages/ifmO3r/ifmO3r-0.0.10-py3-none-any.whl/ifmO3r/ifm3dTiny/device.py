"""
Author: ifm CSR

This is a helper script: it contains methods to handle the parameters using the xml-rpc methods.


Architecture doc:
https://polarionsy.intra.ifm/polarion/redirect/project/O3Rx_01/wiki/System%20Requirements/SYAD_O3R?selection=O3R-2927

!!Warning: if you are using the _functions() alone,
you need to set the system in a CONF state.
Otherwise you won't be able to access the mode object.
"""
# %%
import json
from ifmO3r.rpc import Imager
from ifmO3r.ifm3dTiny.logger import StatusLogger
from ifmO3r.ifm3dTiny.utils import GetCallableMethods


# %%
class Device():
    """This class manages the configuration of the device."""
    def __init__(self, ip, port):
        self.id = port - 50010
        self.ip = ip
        self.port = port
        self.imager = Imager(ip, self.id)        
        self.logger = StatusLogger('parameter_handling')

    def __str__(self):
        """
        Provide a list of *public* functions to be used by the user.

        :return:str_method_list     :   String representing a list of functions
        """
        str_method_list = GetCallableMethods().get_methods(self)
        return str_method_list


    def _set_run_state(self):
        """This function sets the system in the run state. Necessary for receiving frames"""
        self.imager.setState("RUN")

    def _set_conf_state(self):
        """This function sets the system in the CONFIG state.
        Necessary for changing the system's configuration"""
        self.imager.setState("CONF")

    def _set_mode(self, mode):
        """
        :mode: name of the expected mode (string)
        """
        if self._is_different(mode, "mode"):
            if self._is_available_mode(mode):
                self.imager.setMode(mode)
            else:
                mode_error = "The expected mode is not available. Please refer to the json schema."
                self.logger.critical(mode_error)
                print(mode_error)

    def _get_mode(self):
        """Returns the current mode"""
        mode = self.imager.getMode()
        return mode

    def _get_available_modes(self):
        """Returns a list of the available modes:
        {'mode': {'values': [...]}}
        """
        modes_list = self.imager.availableModes()
        return modes_list

    def _set_mode_param(self, param):
        """This function sets the mode parameters (framerate, offset, exposure times)
        :param: {param_name: param_value}"""
        param_name = list(param.keys())[0]
        if self._is_different(param, 'modeParam'):
            if self._is_in_range(param, 'modeParam'):
                self.imager.mode.setParameter(param_name, param[param_name])
            else:
                range_error = 'The expected value for ' + param_name + ' is outside of the range. Please refer to the json schema for more details.'
                self.logger.critical(range_error)
                print(range_error)

    def _set_di_param(self, param):
        """This function sets the distance image parameters (filters, etc)
        :param: {param_name: param_value}"""
        param_name = list(param.keys())[0]
        if self._is_different(param, 'diParam'):
            if self._is_in_range(param, 'diParam'):
                self.imager.algo.setParameter(param_name, param[param_name])
            else:
                range_error = 'The expected value for ' + param_name + ' is outside of the range. Please refer to the json schema for more details.'
                self.logger.critical(range_error)
                print(range_error)

    def _get_all_params(self):
        """Returns a list of all the Port parameters
        :params : 	{"mode":
                        {"value": "mode_value",
                        "modeParam": {...}},
                    "diParam": {...}}
        """
        params = {"mode": {}}
        params["mode"]["value"] = self.imager.params.getAllParameters()["mode"]
        params["mode"]["modeParam"] = self.imager.mode.getAllParameters()
        params["diParam"] = self.imager.algo.getAllParameters()
        return params

    def _get_all_params_limits(self):
        """Returns a list of the current value of all Port parameters:
        :params_limits : 	{"mode":
                                {"value": "mode_value",
                                "modeParam": {...}},
                            "diParam": {...}}
        """
        mode_list = self._get_available_modes()
        mode_params_limits = self.imager.mode.getAllParameterLimits()
        algo_limits = self.imager.algo.getAllParameterLimits()
        param_limits = {"mode": {}}
        param_limits['mode']['values'] = mode_list
        param_limits['mode']['modeParam'] = mode_params_limits
        param_limits['diParam'] = algo_limits
        return param_limits

    def _is_available_mode(self, mode):
        """
        Returns True is the expected mode is available
        :mode 	: "mode_value" (for example, "experimental_high_72")
        """
        return bool(mode in self._get_available_modes())

    def _is_different(self, param, param_type):
        """
        Returns True is the expected value of the parameter is different from the current one
        :param 	: "mode_value" or {"param_name": "param_value"}
        :param_type	: "mode", 'modeParam' or "diParam"
        """
        param_current = self._get_all_params()
        if param_type == 'mode':
            return bool(param_current['mode']['value'] != param)

        elif param_type == 'modeParam':
            param_name = str(list(param.keys())[0])
            param_value = param[param_name]
            try:
                return bool(param_current['mode']['modeParam'][param_name] != param_value)

            except KeyError:
                print("ERROR: The parameter "+param_name+"  is not available in this mode.")

        elif param_type == 'diParam':
            param_name = str(list(param.keys())[0])
            param_value = param[param_name]
            return bool(param_current['diParam'][param_name] != param_value)

        else: 
            print("ERROR: The parameter param_type should be mode, modeParam or diParam")

    def _is_number(self, param_name, param_type):
        """ Returns True is param is an int or float
        ToDo: Eventually change this to get data from JSON schema"""
        param_limits = self._get_all_params_limits()
        if param_type == 'diParam':
            return bool('min' and 'max' in param_limits['diParam'][param_name])

        if param_type == 'modeParam':
            return bool('min' and 'max' in param_limits['mode']['modeParam'][param_name])


    def _is_bool(self, param_name, param_type):
        """Returns True is param is bool
        ToDo: Eventually change this to get data from JSON schema
        """
        param_limits = self._get_all_params_limits()
        print(param_name)
        if param_type == 'diParam':
            param_default = param_limits['diParam'][param_name]['default']
            return bool(param_default in [True, False])
        else:
            return False

    def _is_in_range(self, param, param_type):
        """Returns True if expected param value is within defined range
        ToDo ADD exception if using this for a modeParam not available in set mode"""
        param_limits = self._get_all_params_limits()
        param_name = list(param.keys())[0]
        if self._is_number(param_name, param_type):
            param_value = int(param[param_name])
            if param_type == 'diParam':
                param_max = int(param_limits['diParam'][param_name]['max'])
                param_min = int(param_limits['diParam'][param_name]['min'])
                return bool(param_min <= param_value <= param_max)
            if param_type == 'modeParam':
                param_max = int(param_limits['mode']['modeParam'][param_name]['max'])
                param_min = int(param_limits['mode']['modeParam'][param_name]['min'])
                return bool(param_min <= param_value <= param_max)
        if self._is_bool(param_name, param_type):
            param_value = param[param_name]
            return bool(param_value in [True, False])

    def _config_port(self, config):
        """Inputs the expected port configuration:
        :port_config 	:
                    {"PortID":
                        "mode":
                            {"mode":"mode_value",
                            "modeParam": {...}
                        {diParam:
                            {diParam_name: 	diParam_value}}}
        """
        #Check that input structure is as expected
        #TODO check against json schema
        struct_error = "Wrong structure of the json configuration. Please refer to the result of the dump() function."
        port_id = 'Port' + str(self.id)
        if str(list(config.keys())) != str('[\''+port_id+'\']'):
            print("Port number error")
            self.logger.critical("Port number error")
            return
        else:
            port_config = config[port_id]

        if 'mode' in port_config:
            if 'value' in port_config['mode']:
                mode = port_config['mode']['value']
                self._set_mode(mode)
            if 'modeParam' in port_config['mode']:
                for param_name in port_config['mode']['modeParam'].keys():
                    param = {param_name: port_config['mode']['modeParam'][param_name]}
                    self._set_mode_param(param)


        if 'diParam' in port_config:
            for param_name in port_config['diParam'].keys():
                if "version" not in param_name:
                    param = {param_name: port_config['diParam'][param_name]}
                    self._set_di_param(param)

        if 'mode' not in port_config and 'diParam' not in port_config:
            self.logger.critical(struct_error)
            print(struct_error)

    def config_from_json_str(self, str_param):
        """This function configures a parameter from a str (json format)
        :str_param	: should be of the form
                    {"PortID":
                        "mode":
                            {"mode":"mode_value",
                            "modeParam": {...}
                        {diParam:
                            {diParam_name: 	diParam_value}}}

        """
        self._set_conf_state()
        config = json.loads(str_param)
        self._config_port(config)
        self._set_run_state()


    def config_from_json_file(self, file = 'config.json'):
        """Change the parameters values through xmlrpc methods to the value specified in config.json
        if within permitted range"""

        self._set_conf_state()
        with open(file) as f:
            config = json.load(f)
        self._config_port(config)
        self._set_run_state()

    def config_to_default(self):
        """Set all the parameters to default"""
        self._set_conf_state()
        param_limits = self._get_all_params_limits()
        for p in param_limits['diParam'].keys():
            if 'default' in param_limits['diParam'][p].keys():
                self._set_di_param({p: param_limits['diParam'][p]['default']})
        for p in param_limits['mode']['modeParam'].keys():
            if 'default' in param_limits['mode']['modeParam'].keys():
                self._set_mode_param({param_limits['mode']['modeParam'][p]: param_limits['mode']['modeParam'][p]['default']})
        self._set_run_state()

    def dump(self, save=True, file = 'dump.json'):
        """
        Returns a formatted dictionary containing the current parameters values.
        If save is True, writes the current configuration in a json file.
        If no file is specified, writes in dump.json in current directory.
        !!Warning: The dump requires to be in CONF mode, otherwise the mode parameters are not readable.
        This will interrupt the streaming of data for the duration of the dump.
        """
        self._set_conf_state()
        #Reads the current parameters
        mode_params = self._get_all_params()
        port_id = 'Port' + str(self.id)
        params = {}
        params[port_id] = mode_params
        if save:
            #Writes it to a json file if save = True
            with open(file, 'w+') as f:
                json.dump(params, f, sort_keys = True, indent = 4)
        self._set_run_state()
        return params


def main():
    """Example usage"""
    device = Device('192.168.0.69', 50012)
    # #Display list of available functions
    # print(device)
    # #json_dump is a dict
    # json_dump = device.dump(save = False)
    # #Change value in dictionary
    # json_dump['Port2']['mode']['modeParam']['expLong'] = '5000'
    # #Convert to string and input to config function
    # device.config_from_json_str(json.dumps(json_dump))
    device._set_conf_state()
    print(device._get_all_params_limits())


# %%
if __name__ == '__main__':
    main()
