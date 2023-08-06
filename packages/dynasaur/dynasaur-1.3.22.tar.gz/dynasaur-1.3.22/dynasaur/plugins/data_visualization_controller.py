import os
import csv
import copy
import numpy as np

from ..io.ISO_MME_Converter import ISOMMEConverter
from ..plugins.plugin import PluginInterface, Plugin
from ..utils.constants import PluginsParamDictDef, DataPluginConstants, DefinitionConstants, LoggerSCRIPT, LOGConstants


class DataVisualizationController(PluginInterface, Plugin):
    """ """

    def __init__(self, calculation_procedure_def_file, object_def_file, data_source, user_function_object=None,
                 code_type="LS-DYNA"):
        """
        Initialization i.e. call Plugin constructor

        :param: root
        :param: calculation_procedure_def_file
        :param: object_def_file
        :param: data_source(binout path)
        :param: logger
        :param: dynasaur definition

        :return:
        """
        Plugin.__init__(self, path_to_def_file=calculation_procedure_def_file, path_def_file_id=object_def_file,
                        data_source=data_source, name=DefinitionConstants.DATA_VIS,
                        user_function_object=user_function_object,
                        code_type=code_type)
        self.init_plugin_data(update=True)
        self._data_dict = {}

    def get_defined_calculation_procedures(self):
        """ """
        return self._dynasaur_definitions.get_data_vis_calc_commands()

    def _convert_to_si(self, data, label, procedure_name):
        """

        Args:
          data: 
          label: 
          procedure_name: 

        Returns:

        """
        if "[" in label and label.find("[") < label.find(']'):
            unit_string = label[label.find("[") + 1:label.find("]")]
            if unit_string == "m": # and self._dynasaur_definitions.get_units().meter() != 1:
                data /= self._dynasaur_definitions.get_units().meter()
            elif unit_string == "s": # and self._dynasaur_definitions.get_units().second() != 1:
                data /= self._dynasaur_definitions.get_units().second()
            else:
                self._logger.emit(LOGConstants.WARNING[0],
                                  "y channel of " + procedure_name + "could not be converted to SI units: "
                                  + unit_string + " could not be interpreted. Please check your label (i.e. Displacement[m], Time[s])")

        else:
            self._logger.emit(LOGConstants.WARNING[0],
                              "y channel of " + procedure_name + "could not be converted to SI units. "
                              "Please check your label (i.e. Displacement[m], Time[s])")

        return data

    def _calculate_and_store_results(self, param_dict, to_si=False):
        """

        Args:
          param_dict: return:
          to_si:  (Default value = False)

        Returns:

        """
        self._logger.emit(LOGConstants.SCRIPT[0], "Calculating Visualization: " + param_dict["visualization"])

        json_object = param_dict[PluginsParamDictDef.DYNASAUR_JSON]

        x_label = "None" if PluginsParamDictDef.X_LABEL not in param_dict else param_dict[PluginsParamDictDef.X_LABEL]
        y_label = "None" if PluginsParamDictDef.Y_LABEL not in param_dict else param_dict[PluginsParamDictDef.Y_LABEL]

        sample_offsets = self._get_sample_offset(param_dict)
        if sample_offsets is None:
            return None

        reduced_sample_offsets_x = self._reduce_sample_offset(json_object[DataPluginConstants.X], sample_offsets)
        reduced_sample_offsets_y = self._reduce_sample_offset(json_object[DataPluginConstants.Y], sample_offsets)

        x_data = self._get_data_from_dynasaur_json(json_object=json_object[DataPluginConstants.X],
                                                   data_offsets=reduced_sample_offsets_x)
        if x_data is None:
            return None

        if to_si:
            x_data = self._convert_to_si(x_data, label=x_label, procedure_name=param_dict["visualization"])

        y_data = self._get_data_from_dynasaur_json(json_object=json_object[DataPluginConstants.Y],
                                                   data_offsets=reduced_sample_offsets_y)
        if y_data is None:
            return None

        if to_si:
            y_data = self._convert_to_si(y_data, label=y_label, procedure_name=param_dict["visualization"])


        self._store_data_to_dict(part_of=param_dict[DataPluginConstants.VISUALIZATION].split("_")[0],
                                 diagram_name="_".join(param_dict[DataPluginConstants.VISUALIZATION].split("_")[1:]),
                                 x_data_name=x_label, y_data_name=y_label,
                                 x_data=x_data.flatten(), y_data=y_data.flatten())

    def _store_data_to_dict(self, part_of, diagram_name, x_data_name, y_data_name, x_data, y_data):
        """

        Args:
          separator: param x_data_name:
          y_data_name: param x_data:
          y_data: return:
          part_of: 
          diagram_name: 
          x_data_name: 
          x_data: 

        Returns:

        """
        if part_of not in self._data_dict.keys():
            self._data_dict.update({part_of: {}})

        if diagram_name not in self._data_dict[part_of].keys():
            self._data_dict[part_of].update({diagram_name: {"X": x_data, "x_name": x_data_name,
                                                            "Y": y_data, "y_name": y_data_name}})
        else:
            self._data_dict[part_of][diagram_name].update({"X": x_data, "x_name": x_data_name,
                                                           "Y": y_data, "y_name": y_data_name})

    def write_ISO_MME(self, path_to_dir=None, test=False):
        """

        Args:
          path_to_dir: param test: (Default value = None)
          test:  (Default value = False)

        Returns:

        """
        converter = ISOMMEConverter()
        converter.write_ISOMME(path_to_dir=path_to_dir, data=self.get_data(),
                               dynasaur_definitions=self._dynasaur_definitions, logger=self._logger, test=test)

    def write_CSV(self, directory, filename=None):
        """writes a csv file to the given directory
        if no filename is passed to the function, a default
        is used (<PLUGIN_NAME>_<timestamp>)

        Args:
          directory: path/to/directory
          filename: return: None (Default value = None)

        Returns:
          None

        """
        if os.path.isdir(directory) is None:
            self._logger.emit(LOGConstants.ERROR[0], self._name + ": csv_file_dir is not a directory")
            return

        if filename is None:
            filename = self._name + "_" + self._timestamp + ".csv"

        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[1] + directory)
        path = os.path.join(directory, filename)

        rows = []
        values = []
        d = self._get_padded_data_dict()

        # header information
        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                rows.append(part_of + ":" + diagram_name + ":" + d[part_of][diagram_name]["x_name"])
                rows.append(part_of + ":" + diagram_name + ":" + d[part_of][diagram_name]["y_name"])

        # actual data
        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                values.append(d[part_of][diagram_name]["X"])
                values.append(d[part_of][diagram_name]["Y"])

        list_lengths = [len(i) for i in values]
        assert(all([a == list_lengths[0] for a in list_lengths]))

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
            writer.writerow(rows)

            t_m = list(zip(*values))
            for key in t_m:
                writer.writerow(key)

        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[6] + path)

    def get_data(self, part_of=None, diagram_name=None):
        """Get data from data dict

        Args:
          part_of:  (Default value = None)
          diagram_name:  (Default value = None)

        Returns:

        """
        if part_of is None and diagram_name is None:
            return self._data_dict

        elif part_of is None and diagram_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], "data dictionary is empty")
                return
            return_dict = {}
            for counter, parts_of in enumerate(self._data_dict.keys()):
                if diagram_name not in self._data_dict[parts_of]:
                    if counter == len(self._data_dict.keys()):
                        self._logger.emit(LOGConstants.ERROR[0], diagram_name + "not in data dictionary")
                        return
                else:
                    return_dict.update(self._data_dict[parts_of][diagram_name])

            return return_dict

        elif part_of is not None and diagram_name is None:
            if len(self._data_dict):
                return self._data_dict[part_of]
            else:
                self._logger.emit(LOGConstants.ERROR[0], " data dictionary is empty")
                return

        elif part_of is not None and diagram_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0],
                                  "No data available.")
                return
            if part_of not in self._data_dict.keys():
                self._logger.emit(LOGConstants.ERROR[0],
                                  "For Region " + part_of + " no calculated results are available.")
                return
            if diagram_name not in self._data_dict[part_of].keys():
                self._logger.emit(LOGConstants.ERROR[0], diagram_name + " has not been calculated")
                return
            else:
                return self._data_dict[part_of][diagram_name]

    def _get_padded_data_dict(self):
        """add padding to data visualization list"""
        d = copy.deepcopy(self._data_dict)
        length = DataVisualizationController._get_maximum_length(d)
        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                if len(d[part_of][diagram_name]["X"]) < length or len(d[part_of][diagram_name]["Y"]) < length:
                    index_x = len(d[part_of][diagram_name]["X"])
                    d[part_of][diagram_name]["X"] = np.concatenate(
                        (d[part_of][diagram_name]["X"], ['-'] * (length - index_x)))

                    index_y = len(d[part_of][diagram_name]["Y"])
                    d[part_of][diagram_name]["Y"] = np.concatenate(
                        (d[part_of][diagram_name]["Y"], ['-'] * (length - index_y)))
        return d

    @staticmethod
    def _get_maximum_length(data_dict):
        """find max length of data visualization list
        :return max length:

        Args:
          data_dict: 

        Returns:

        """
        if len(data_dict.keys()) == 0:
            return 0
        length = np.max([len(data_dict[p][d]["X"]) for p in data_dict.keys() for d in data_dict[p].keys()])
        return length
