import os
import csv

from ..plugins.plugin import Plugin, PluginInterface
from ..utils.constants import DefinitionConstants, OutputStringForPlugins, PluginsParamDictDef, JsonConstants, \
    LoggerSCRIPT, LOGConstants


class CriteriaController(Plugin, PluginInterface):
    """ """
    def __init__(self, calculation_procedure_def_file, object_def_file, data_source, user_function_object=None,
                 volume_def_file=None, code_type="LS-DYNA"):
        """
        Initialization i.e. call Plugin constructor
        :param: root
        :param: calculation_procedure_def_file
        :param: object_def_file
        :param: data_source(binout path)
        :param: user_function_object
        :param: volume_def_file
        :param: code_type

        :return:
        """
        Plugin.__init__(self, path_to_def_file=calculation_procedure_def_file, path_def_file_id=object_def_file,
                        data_source=data_source, volume_path=volume_def_file, user_function_object=user_function_object,
                        name=DefinitionConstants.CRITERIA, code_type=code_type)

        # self._data_source = data_source
        self.init_plugin_data(update=True)
        self._data_dict = {}


    def get_defined_calculation_procedures(self):
        """ """
        return self._dynasaur_definitions.get_criteria_calc_commands()

    def _calculate_and_store_results(self, param_dict, to_si=False):
        """

        Args:
          param_dict: return:
          to_si:  (Default value = False)

        Returns:

        """

        if to_si:
            self._logger.emit(LOGConstants.WARNING[0], "Parameter to_si has no effect on criteria calculations!")

        self._logger.emit(LOGConstants.SCRIPT[0], "Calculating Criteria: " + param_dict["criteria"])

        sample_offset = self._get_sample_offset(param_dict)
        if sample_offset is None:
            return

        json_object = param_dict[PluginsParamDictDef.DYNASAUR_JSON]
        reduced_sample_offsets = self._reduce_sample_offset(json_object, sample_offset)

        if not all([off == sample_offset[0][1] for i, off, _ in sample_offset]):
            required_data = [data_type for data_type, _, _ in sample_offset]
            self._logger.emit(LOGConstants.ERROR[0],
                              "Required data " + str(required_data) + " has not the same sampling frequency.")
            return

        ret = self._get_data_from_dynasaur_json(json_object, reduced_sample_offsets)
        ret_tuple = ret if isinstance(ret, tuple) else (ret, '-')
        value = ret_tuple[0]

        limit_string = None
        if JsonConstants.LIMITS in json_object and len(json_object[JsonConstants.LIMITS]) == 3:
            limit_string = str(json_object[JsonConstants.LIMITS])

        self._store_data_to_dict(part_of=json_object[JsonConstants.PART_OF],
                                 type_of_criteria=json_object[JsonConstants.TYPE_OF_CRTITERIA],
                                 criteria_name="_".join(param_dict["criteria"].split("_")[1:]),
                                 limits=limit_string, value=value)

    def _store_data_to_dict(self, part_of, type_of_criteria, criteria_name, limits, value):
        """

        Args:
          part_of: 
          type_of_criteria: 
          criteria_name: 
          limits: 
          value: 

        Returns:

        """

        if part_of not in self._data_dict.keys():
            self._data_dict.update({part_of: {}})

        if type_of_criteria not in self._data_dict[part_of].keys():
            self._data_dict[part_of].update({type_of_criteria: {}})

        if criteria_name not in self._data_dict[part_of][type_of_criteria].keys():

            if limits is None:
                self._data_dict[part_of][type_of_criteria].update({criteria_name:
                                                                       {OutputStringForPlugins.VALUE: value}})
            else:
                self._data_dict[part_of][type_of_criteria].update({criteria_name:
                                                                       {OutputStringForPlugins.VALUE: value,
                                                                        OutputStringForPlugins.LIMITS: limits}})

    def write_CSV(self, directory, filename=None):
        """write csv file on the given path

        Args:
          csv_file_dir: param filename:
          directory: 
          filename:  (Default value = None)

        Returns:

        """
        if os.path.isdir(directory) is None:
            self._logger.emit(LOGConstants.ERROR[0], self._name + ": csv_file_dir is not a directory")
            return
        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[1] + directory)
        if filename is None:
            filename = self._name + "_" + self._timestamp + ".csv"
        path = os.path.join(directory, filename)

        rows = []
        for part_of in self._data_dict.keys():
            for criteria_type in self._data_dict[part_of]:
                for criteria_name in self._data_dict[part_of][criteria_type].keys():
                    if OutputStringForPlugins.LIMITS in self._data_dict[part_of][criteria_type][criteria_name]:
                        rows.append(part_of + ":" + criteria_type + ":" + criteria_name + ":" +
                                    self._data_dict[part_of][criteria_type][criteria_name][
                                        OutputStringForPlugins.LIMITS])
                    else:
                        rows.append(part_of + ":" + criteria_type + ":" + criteria_name)

        values = [self._data_dict[part_of][criteria_type][criteria_name][OutputStringForPlugins.VALUE]
                  for part_of in self._data_dict.keys()
                  for criteria_type in self._data_dict[part_of]
                  for criteria_name in self._data_dict[part_of][criteria_type].keys()]

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
            writer.writerow(rows)
            writer.writerow(values)

        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[6] + path)

    def get_data(self, part_of=None, criteria_type=None, criteria_name=None):
        """Get data from data dict

        Args:
          part_of:  (Default value = None)
          criteria_type:  (Default value = None)
          criteria_name:  (Default value = None)

        Returns:

        """
        if part_of is None and criteria_type is None and criteria_name is None:
            return self._data_dict

        elif part_of is None and criteria_type is None and criteria_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            return_dict = {}
            for counter_one, parts_of in enumerate(self._data_dict.keys()):
                for counter, criteria_t in enumerate(self._data_dict[parts_of].keys()):
                    if criteria_name not in self._data_dict[parts_of][criteria_t]:
                        if counter == len(self._data_dict[parts_of].keys()) - 1 \
                                and counter_one == len(self._data_dict.keys()) - 1 \
                                and len(return_dict) == 0:
                            self._logger.emit(LOGConstants.ERROR[0], criteria_name + " not in data dictionary")
                            return
                    else:
                        return_dict.update(self._data_dict[parts_of][criteria_t][criteria_name])

            return return_dict

        elif part_of is None and criteria_type is not None and criteria_name is None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            return_dict = {}
            for counter, parts_of in enumerate(self._data_dict.keys()):
                if criteria_type not in self._data_dict[parts_of]:
                    if counter == len(self._data_dict.keys()) - 1 and len(return_dict) == 0:
                        self._logger.emit(LOGConstants.ERROR[0], criteria_type + " not in data dictionary")
                        return
                else:
                    return_dict.update(self._data_dict[parts_of][criteria_type])

            return return_dict

        elif part_of is None and criteria_type is not None and criteria_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            return_dict = {}
            for counter, part in enumerate(self._data_dict.keys()):
                if criteria_type not in self._data_dict[part]:
                    if counter == len(self._data_dict.keys()) - 1 and len(return_dict) == 0:
                        self._logger.emit(LOGConstants.ERROR[0], criteria_type + " not in data dictionary")
                        return
                else:
                    if criteria_name in self._data_dict[part][criteria_type].keys():
                        return_dict.update(self._data_dict[part][criteria_type][criteria_name])
            return return_dict

        elif part_of is not None and criteria_type is None and criteria_name is None:
            if len(self._data_dict):
                if part_of not in self._data_dict.keys():
                    self._logger.emit(LOGConstants.ERROR[0], part_of + " not in data dictionary")
                    return
                return self._data_dict[part_of]
            else:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return

        elif part_of is not None and criteria_type is None and criteria_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            return_dict = {}
            if part_of not in self._data_dict.keys():
                self._logger.emit(LOGConstants.ERROR[0], part_of + " not in data dictionary")
                return
            for counter, criteria_t in enumerate(self._data_dict[part_of].keys()):
                if criteria_name not in self._data_dict[part_of][criteria_t].keys():
                    if counter == len(self._data_dict[part_of].keys()) - 1 and len(return_dict) == 0:
                        self._logger.emit(LOGConstants.ERROR[0], criteria_name + " not in data dictionary")
                        return
                else:
                    return_dict.update(self._data_dict[part_of][criteria_t][criteria_name])
            return return_dict

        elif part_of is not None and criteria_type is not None and criteria_name is None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            if part_of not in self._data_dict.keys():
                self._logger.emit(LOGConstants.ERROR[0], part_of + " not in data dictionary")
                return
            if criteria_type not in self._data_dict[part_of].keys():
                self._logger.emit(LOGConstants.ERROR[0], criteria_type + " not in data dictionary")
                return
            return self._data_dict[part_of][criteria_type]

        elif part_of is not None and criteria_type is not None and criteria_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return
            if part_of not in self._data_dict.keys():
                self._logger.emit(LOGConstants.ERROR[0], part_of + " not in data dictionary")
                return
            if criteria_type not in self._data_dict[part_of].keys():
                self._logger.emit(LOGConstants.ERROR[0], criteria_type + " not in data dictionary")
                return
            if criteria_name not in self._data_dict[part_of][criteria_type].keys():
                self._logger.emit(LOGConstants.ERROR[0], criteria_name + " not in data dictionary")
                return
            else:
                return self._data_dict[part_of][criteria_type][criteria_name]
