import time
import json
from lasso.dyna.Binout import Binout


from ..utils.constants import LOGConstants, DefFileConstants, UnitsConstants, DefinitionConstants, \
    ObjectConstantsForData, JsonConstants, LoggerERROR, LoggerWARNING, PluginsParamDictDef, DataTypeMapping
from ..utils.constants import LoggerReadDynasaurDefinitionFile as LD
from ..data.def_file_validator import TestDefinitionJSON


class Helpers(object):
    """ """

    @staticmethod
    def create_default_object_definitions(data_source, code_type):
        """TODO
        documentation

        Args:
          data_source: param code_type:
          code_type: 

        Returns:

        """
        d = {"OBJECTS":[]}
        if code_type == "LS-DYNA":
            binout = Binout(data_source)
            for data_type in binout.read():
                if "ids" in binout.read(data_type):
                    legend_ids = [binout.read(data_type, "legend")[i:i + 80].strip(" ") for i in
                                  range(0, len(binout.read(data_type, "legend")), 80)]
                    if len(binout.read(data_type, "ids").shape) > 1:
                        ids = binout.read(data_type, "ids")[0]
                    else:
                        ids = binout.read(data_type, "ids")
                    for nr, id in enumerate(ids):
                        dynasaur_identifier = DataTypeMapping.binary_identifier_2_dynasaur_identifier(data_type)
                        if dynasaur_identifier is None:
                            print(data_type)
                            break
                        if len(legend_ids) == len(binout.read(data_type, "ids")):
                            d["OBJECTS"].append({"type": dynasaur_identifier, "name": legend_ids[nr], "id": [int(id)]})
                        else:
                            d["OBJECTS"].append({"type": dynasaur_identifier, "name": data_type + str(nr), "id": [int(id)]})

        return d



class Units(object):
    """ """
    def __init__(self):
        self._time = 1.0  # in seconds
        self._length = 1.0  # in meters
        self._weight = 1.0  # in kilogram
        self.grav_const = 9.81

    def set_time(self, _time):
        """

        Args:
          _time: 

        Returns:

        """
        self._time = _time

    def set_length(self, length):
        """

        Args:
          length: 

        Returns:

        """
        self._length = length

    def set_weight(self, weight):
        """

        Args:
          weight: 

        Returns:

        """
        self._weight = weight

    def second(self):
        """ """
        return self._time

    def meter(self):
        """ """
        return self._length

    def kilogram(self):
        """ """
        return self._weight


class DefintionObject(object):
    def __init__(self, oid):
        """Init function / constructor

        Args:
            oid: return:

        Returns:

        """
        self._oid = oid
        self._parts = {}
        self._elements = {}

    def set_parts(self, part):
        """

        Args:
          part: 

        Returns:

        """
        self._parts = part

    def add_part(self, pid):
        """

        Args:
          pid: 

        Returns:

        """
        self._parts[pid] = pid

    def add_element(self, eid):
        """

        Args:
          eid: 

        Returns:

        """
        self._elements[eid] = eid

    def get_parts(self):
        """ """
        return sorted(self._parts)

    def get_element(self):
        """ """
        return sorted(self._elements)


class DynasaurDefinitions:
    """ """
    # create the object container
    def __init__(self, logger):
        """
        constructor

        :param logger:
        :return:
        """
        self._title = ''
        self._objects = {}
        self._logger = logger
        self._info = []

        # set all class members
        self._dynasaur_data_type_container = {ObjectConstantsForData.__dict__[i]: {}
                                              for i in ObjectConstantsForData.__dict__ if not i.startswith("__")}

        self._criteria = {}
        self._data_vis = {}
        self._units = Units()

    def binout_type_data_type_container(self, binout_name):
        """

        Args:
          binout_name: return:

        Returns:

        """
        return DataTypeMapping.binary_identifier_2_dynasaur_identifier(binout_name) in self._dynasaur_data_type_container

    def get_param_dict_from_command(self, command):
        """

        Args:
          command: return dictionary on the command

        Returns:

        """
        if 'visualization' in command:
            d = command
            d[PluginsParamDictDef.DYNASAUR_JSON] = self.get_data_vis(command['visualization'])
            return d

        elif 'criteria' in command:
            d = command
            d[PluginsParamDictDef.DYNASAUR_JSON] = self.get_criteria(command['criteria'])
            return d
        else:
            print("[ERROR] Command not in command list")
            return

    def get_units(self):
        """get units"""
        return self._units

    def get_criteria_ids(self):
        """ """
        return [key for key in self._criteria.keys()]

    def get_criteria(self, key):
        """get criteria

        Args:
          key: return criteria:

        Returns:

        """
        if key not in self._criteria.keys() or len(self._criteria) == 0:
            self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[6] + "\"" + key + "\"")
            exit("Exiting, check your def file")
            return
        return self._criteria[key]

    def get_data_vis_calc_commands(self):
        """:return:"""

        ls = [key for key in self._data_vis.keys()]
        ret = []
        for key in ls:
            d = {"visualization": key}
            if "label" in self._data_vis[key]["x"]:
                x_label = self._data_vis[key]["x"]["label"]
                d["x_label"] = x_label
            if "label" in self._data_vis[key]["y"]:
                y_label = self._data_vis[key]["y"]["label"]
                d["y_label"] = y_label

            ret.append(d)
        return ret

    def get_criteria_calc_commands(self):
        """ """
        ls = [key for key in self._criteria.keys()]
        ret = []
        for nr, key in enumerate(ls):
            ret.append({"criteria": key})

        return ret

    def get_data_vis(self, key):
        """get code

        Args:
          key: 

        Returns:

        """
        if key not in self._data_vis.keys() or len(self._data_vis) == 0:
            self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[7] + "\"" + key + "\"")
            exit("Exiting, check your def file")
        return self._data_vis[key]

    def get_ids_from_name(self, name, data_container, plugin_name):
        """get ids from given name

        Args:
          name: param data_container:
          plugin_name: return dict(name):
          data_container: 

        Returns:

        """
        dynasaur_data_type = DataTypeMapping.binary_identifier_2_dynasaur_identifier(data_container)
        d = self._dynasaur_data_type_container[dynasaur_data_type]

        if name not in d.keys() or len(d) == 0:
            self._logger.emit(LOGConstants.ERROR[0],
                              "In " + plugin_name + LoggerERROR.print_statements[5] + "\"" + name + "\"")
            time.sleep(.5)
            exit("Exiting, check your def file")

            return

        return d[name]

    def get_defined_objects_containing_parts(self, part_ids):
        """get defined object containing parts

        Args:
          part_ids: return list_defined_objects:

        Returns:

        """
        list_defined_objects = []
        for tmp_object_name in sorted(self._objects):
            tmp_part_ids = list(self._objects[tmp_object_name].get_parts())
            intersection = [val for val in tmp_part_ids if val in part_ids]
            if len(intersection) != 0:
                list_defined_objects.append(tmp_object_name)

        if len(list_defined_objects) == 0:
            list_defined_objects.append("")

        return list_defined_objects

    def get_defined_objects_containing_all_parts(self, part_ids):
        """get defined object

        Args:
          part_ids: return list_defined_objects:

        Returns:

        """
        list_defined_objects = []
        for tmp_object_name in sorted(self._objects):
            tmp_part_ids = list(self._objects[tmp_object_name].get_parts())
            intersection = [val for val in tmp_part_ids if val in part_ids]
            if len(tmp_part_ids) == len(intersection):
                list_defined_objects.append(tmp_object_name)

        if len(list_defined_objects) == 0:
            list_defined_objects.append("")

        return list_defined_objects

    def define_dynasaur_everything(self, part_ids):
        """define dynasaur everything

        Args:
          part_ids: list of part_ids

        Returns:

        """

        # create an Everything object
        name = "Dynasaur Everything"
        self._objects[name] = DefintionObject(name)

        # only store ids not the entire dict would cause side effects
        self._objects[name].set_parts(part_ids)

    def get_all_data_types_from_json(self, d, ls):
        """get all data types

        Args:
          d: param ls:
        :return d[TYPE]:
          ls: 

        Returns:

        """

        for key in d.keys():
            if key is None:
                continue
            if isinstance(d[key], dict):
                data_type = self.get_all_data_types_from_json(d[key], ls)
                if data_type is not None and data_type not in ls:
                    if isinstance(data_type, list):
                        for type_ in data_type:
                            ls.append(type_)
                    else:
                        ls.append(data_type)
            elif JsonConstants.TYPE in d.keys():
                return d[JsonConstants.TYPE]

    def get_required_datatypes(self, plugin_name):
        """get required datatype

        Args:
          plugin_name: return ls:

        Returns:

        """
        ls = []
        if DefinitionConstants.CRITERIA == plugin_name:
            self.get_all_data_types_from_json(self._criteria, ls)
        elif DefinitionConstants.DATA_VIS == plugin_name:
            self.get_all_data_types_from_json(self._data_vis, ls)
        else:
            assert False
        return ls

    def get_parts_by_object_containing_part_ids(self, tmp_object, part_ids):
        """get parts by object containing part ids

        Args:
          tmp_object: param part_ids:
        :return parts by object:
          part_ids: 

        Returns:

        """
        return [val for val in part_ids if val in self._objects[tmp_object].get_parts()]

    def get_parts_of_defined_object(self, tmp_object):
        """

        Args:
          tmp_object: type  str:

        Returns:
          array:: the parts as defined in ids.def:

        """

        return self._objects[tmp_object].get_parts()

    def get_info(self):
        """get info"""
        return self._info

    def _set_contact(self, json_object):
        """set contact object type

        Args:
          json_object: return:

        Returns:

        """
        name = json_object[JsonConstants.NAME]

        if JsonConstants.ID in json_object:
            self._dynasaur_data_type_container["CONTACT"][name] = json_object[JsonConstants.ID]

        if JsonConstants.ID_RANGE in json_object:
            self._dynasaur_data_type_container["CONTACT"][name] = [str(i) + json_object[JsonConstants.ID_RANGE][0][-1]
                                   for i in range(int(json_object[JsonConstants.ID_RANGE][0][:-1]),
                                                  int(json_object[JsonConstants.ID_RANGE][-1][:-1]) + 1)]

    def _set_datacontainer_defintion(self, json_object, def_container):
        """

        Args:
          json_object: param def_container:
          def_container: 

        Returns:

        """
        name = json_object[JsonConstants.NAME]

        if JsonConstants.ID in json_object:
            def_container[name] = json_object[JsonConstants.ID]

        if JsonConstants.ID_RANGE in json_object:
            def_container[name] = [i for i in range(json_object[JsonConstants.ID_RANGE][0],
                                                    json_object[JsonConstants.ID_RANGE][-1] + 1)]

        if JsonConstants.PART_ID in json_object:
            def_container[name] = json_object[JsonConstants.PART_ID]

    def __set_object(self, json_object):
        """
        set object

        :param json_object:
        :return:
        """
        name = json_object[JsonConstants.NAME]
        self._objects[name] = DefintionObject(name)
        if JsonConstants.ID in json_object:
            for part in json_object[JsonConstants.ID]:
                self._objects[name].add_part(part)

        if JsonConstants.ID_RANGE in json_object:
            for i in range(json_object[JsonConstants.ID_RANGE][0], json_object[JsonConstants.ID_RANGE][-1]):
                self._objects[name].add_part(i)

        # TODO: Check if we need elem?
        elif "elem" in json_object:
            for elem in json_object["elem"]:
                self._objects[name].add_element(elem)

        elif "elem_range" in json_object:
            for i in range(json_object["elem_range"][0], json_object["elem_range"][1]):
                self._objects[name].add_element(i)

    def _parse_objects(self, json_objects):
        """parse json objects and call setter

        Args:
          json_object: return:
          json_objects: 

        Returns:

        """
        for json_object in json_objects[DefinitionConstants.OBJECTS]:

            if json_object[JsonConstants.TYPE] not in self._dynasaur_data_type_container.keys():
                self._logger.emit(LOGConstants.WARNING[0],
                                  json_object[JsonConstants.TYPE] + LoggerWARNING.print_statements[1] +
                                  str(", ".join(list(self._dynasaur_data_type_container.keys()))))
                continue

            if json_object[JsonConstants.TYPE] == ObjectConstantsForData.ELEMENTOBJECT:
                self.__set_object(json_object)
            elif json_object[JsonConstants.TYPE] == ObjectConstantsForData.CONTACT:
                self._set_contact(json_object)
            else:
                data_type_container = self._dynasaur_data_type_container[json_object[JsonConstants.TYPE]]
                self._set_datacontainer_defintion(json_object, data_type_container)

    def _set_unit(self, json_object):
        """set unit object

        Args:
          json_object: return:

        Returns:

        """
        for key_name in json_object[DefinitionConstants.UNIT]:
            if key_name == UnitsConstants.TIME:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.SECOND:
                    self._units.set_time(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.MILLISECOND:
                    self._units.set_time(UnitsConstants.THOUSAND)
            elif key_name == UnitsConstants.LENGTH:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.METER:
                    self._units.set_length(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.MILLIMETER:
                    self._units.set_length(UnitsConstants.THOUSAND)
            elif key_name == UnitsConstants.WEIGHT:
                if json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.KILOGRAM:
                    self._units.set_weight(UnitsConstants.ONE)
                elif json_object[DefinitionConstants.UNIT][key_name] == UnitsConstants.TON:
                    self._units.set_weight(UnitsConstants.WEIGHT_DEFAULT)

    def _set_criteria(self, json_object):
        """set criteria object

        Args:
          json_object: return:

        Returns:

        """
        for criteria in json_object[DefinitionConstants.CRITERIA]:
            body_part = criteria[JsonConstants.PART_OF]
            self._criteria[body_part + "_" + criteria[JsonConstants.NAME]] = criteria

    def _set_diagram_visualisation(self, json_object):
        """set data visualisation object

        Args:
          json_object: return:

        Returns:

        """
        for definition in json_object[DefinitionConstants.DATA_VIS]:
            body_part = definition[JsonConstants.PART_OF]
            if not body_part + "_" + definition[JsonConstants.NAME] in self._data_vis:
                self._data_vis[body_part + "_" + definition[JsonConstants.NAME]] = definition
            else:
                self._logger.emit(LOGConstants.WARNING[0], "Double declaration of " + body_part + "_" + definition[JsonConstants.NAME])

    def _set_info(self):
        """set info in data visualisation"""
        info = []
        for key in self._data_vis.keys():
            if JsonConstants.INFO in self._data_vis[key].keys():
                if len(self._data_vis[key][JsonConstants.INFO].split(":")) == 3:
                    info.append(self._data_vis[key][JsonConstants.INFO])
                elif len(self._data_vis[key][JsonConstants.INFO].split(":")) == 2:
                    self._data_vis[key][JsonConstants.INFO].append(":")
                    info.append(self._data_vis[key][JsonConstants.INFO])
                elif len(self._data_vis[key][JsonConstants.INFO].split(":")) > 3:
                    self._data_vis[key][JsonConstants.INFO] = "::"
                    info.append(self._data_vis[key][JsonConstants.INFO])
                else:
                    self._data_vis[key][JsonConstants.INFO].append(":")
                    info.append(self._data_vis[key][JsonConstants.INFO])
            else:
                info.append(None)
        self._info = info

    def read_def(self, fn):
        """read definition file(s)

        Args:
          fn: return:

        Returns:

        """
        if fn is None:
            exit("No definition file")

        if isinstance(fn, str):
            fn = [fn]

        if isinstance(fn, list):

            if len(fn) < 1:
                exit("No definition file(s) in list")
            is_entity_set = {i: False for i in DefinitionConstants.__dict__ if i[:1] != "_"}

            for single_def_file in fn:
                self._logger.emit(LOGConstants.READ_DYNASAUR_DEF[0], LD.READ % single_def_file)
                try:
                    with open(single_def_file) as fd:
                        try:
                            json_objects = json.load(fd)
                            for j_object in json_objects:
                                if DefinitionConstants.TITLE in j_object:
                                    if not is_entity_set[DefinitionConstants.TITLE]:
                                        self._title = j_object[DefinitionConstants.TITLE]
                                        is_entity_set[DefinitionConstants.TITLE] = True
                                    else:
                                        self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[8] + DefinitionConstants.TITLE)
                                        exit("Entity Title already set " + self._title)

                                elif DefinitionConstants.UNIT in j_object:
                                    if not is_entity_set[DefinitionConstants.UNIT]:
                                        self._set_unit(j_object)
                                        is_entity_set[DefinitionConstants.UNIT] = True
                                    else:
                                        self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[8] + DefinitionConstants.UNIT)
                                        exit("Entity Units already set " + self._units)

                                elif DefinitionConstants.CRITERIA in j_object:
                                    self._set_criteria(j_object)

                                elif DefinitionConstants.DATA_VIS in j_object:
                                    self._set_diagram_visualisation(j_object)
                                    self._set_info()

                                elif DefinitionConstants.OBJECTS in j_object:
                                    self._parse_objects(json_objects)

                                else:
                                    self._logger.emit(LOGConstants.ERROR[0],
                                                      "json object not understood:" + str(j_object))
                                    return

                        except ValueError as e:
                            self._logger.emit(LOGConstants.ERROR[0], LoggerERROR.print_statements[4] % e)
                            exit("Exiting - Invalid JSON file")  # Because Mutant, if GUI "exit()" comment
                            return
                except FileNotFoundError as e:
                    self._logger.emit(LOGConstants.ERROR[0],  e.strerror + " " + e.filename)
                    exit(e.strerror + " " + e.filename)

        else:
            exit("No definition file")

        self._logger.emit(LOGConstants.READ_DYNASAUR_DEF[0], LD.DONE)

