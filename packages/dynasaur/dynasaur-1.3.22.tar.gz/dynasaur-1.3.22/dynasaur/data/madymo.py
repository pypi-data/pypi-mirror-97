import h5py
import numpy as np

from ..utils.constants import LOGConstants, UnitsConstants, MadymoConstants, DataChannelTypesNodout, \
    DataChannelTypesSecforc, DataChannelTypesContact, DataChannelTypesSbtout
from ..utils.logger import ConsoleLogger
from ..data.dynasaur_definitions import DynasaurDefinitions
import re


class MadymoData:
    """ """

    def _extratct_data(self, node, data_type, channel_type, idx_madymo_data):
        """

        Args:
          node: param data_type:
          idx_madymo_data: return:
          data_type: 
          channel_type: 

        Returns:

        """
        ids_name = "ids" if data_type != "sbtout" else "belt_ids"
        for idx, id_ in enumerate(self._d[data_type][ids_name]):
            keys = [i for i in node.keys() if i.startswith("SIGNAL")]
            for key in keys:
                if data_type == "rcforc" or data_type == "sbtout":
                    id_string= ''.join([chr(i) for i in list(node[key].attrs.items())[0][1] if i != 0])
                    id_to_compare = self._get_simplified_double_id(id_string)
                else:
                    id_to_compare = ''.join([chr(i) for i in list(node[key].attrs.items())[0][1] if i != 0]).split(" ")[0]

                if id_to_compare == id_:
                    self._d[data_type][channel_type][:, idx] = node[key]["Y_VALUES"][idx_madymo_data, :]
                    # self._d[data_type][channel_type][:, idx] = node[key]["Y_VALUES"][:, idx_madymo_data]

    def _extract_data_energy(self, node, data_type, ids,  enegry_type):
        """

        Args:
          node: param enegry_type:
          idx_madymo_data: return:
          data_type: 
          ids: 
          enegry_type: 

        Returns:

        """
        keys = [i for i in node.keys() if i.startswith("SIGNAL")]
        for key in keys:
            id_string = ''.join([chr(i) for i in list(node[key].attrs.items())[0][1] if i != 0]).strip()
            id_ = [i for i in id_string.split() if i.startswith("/")][0]

            if id_ not in ids:
                continue
            insert_idx = ids.index(id_)
            if id_string.startswith("total energy") and enegry_type == "total_energy":
                self._d[data_type]["total_energy"][:, insert_idx] = node[key]["Y_VALUES"][0, :]

            elif id_string.startswith("kinetic energy") and enegry_type == "kinetic_energy":
                self._d[data_type]["kinetic_energy"][:, insert_idx] = node[key]["Y_VALUES"][0, :]

            elif id_string.startswith("total hourglass energy") and enegry_type == "hourglass_energy":
                self._d[data_type]["hourglass_energy"][:, insert_idx] = node[key]["Y_VALUES"][0, :]

            elif id_string.startswith("work done by external loading") and enegry_type == "external_work":
                self._d[data_type]["external_work"][:, insert_idx] = node[key]["Y_VALUES"][0, :]

            elif id_string.startswith("work done by contact forces") and enegry_type == "sliding_interface_energy":
                self._d[data_type]["sliding_interface_energy"][:, insert_idx] = node[key]["Y_VALUES"][0, :]

    def _add_energy_ids(self, node, data_type):
        """

        Args:
          node: param data_type:
          data_type: 

        Returns:

        """
        signals = [signal for signal in node.keys() if signal.startswith("SIGNAL")]
        for signal in signals:
            id_string = ''.join([chr(i) for i in list(node[signal].attrs.items())[0][1] if i != 0]).strip()

            # Assumption "/" indicates the ID ... not the best approach, but data does not provide more content
            ids_ = [(idx, i) for idx, i in enumerate(id_string.split()) if i.startswith("/")]
            assert(len(ids_) == 1)
            id_ = ids_[0][1]

            # check if global or system energy
            # assumption: output identifier uses the wording system
            #     i.e. system -->  total hourglass energy of system : /10 ( Vehicle_sys )

            data_type = "matsum" if id_string.split()[ids_[0][0]-2] == "system" else "glstat"
            if id_ not in self._d[data_type]["ids"]:
                self._d[data_type]["ids"].append(id_)

            if id_string.startswith("total energy"):
                self._d[data_type]["total_energy"] = None

            if id_string.startswith("total hourglass energy"):
                self._d[data_type]["hourglass_energy"] = None

            if id_string.startswith("kinetic energy"):
                self._d[data_type]["kinetic_energy"] = None

            if id_string.startswith("work done by external loading"):
                self._d[data_type]["external_work"] = None

            if id_string.startswith("work done by contact forces"):
                self._d[data_type]["sliding_interface_energy"] = None

    def _get_simplified_double_id(self, id_string):
        """

        Args:
          id_string: return:

        Returns:

        """

        id_string_ = id_string.split(" ")
        xy = [re.search("(\/[0-9]+)+", i).group(0) for i in id_string_ if re.search("(\/[0-9]+)+", i) is not None]
        if id_string.split(":")[-1].isnumeric():
            # case
            # /1000/101 ( /SystemInteractions_sys/Seat-Occupant_cntfrc ) contact.mb_fe /1000/54 ( /SystemInteractions_sys/ASM-Occupant_cnt ) :1
            simiplified_id = "-".join(xy) + ":" + str(id_string.split(":")[-1])
        elif id_string.split(":")[-1] == id_string:
            # case
            # /1000/999 ( /SystemInteractions_sys/Airbag-Occupant_cntfrc ) contact.fe_fe /1000/91 ( /SystemInteractions_sys/Occupant-Airbag_cnt ) CFC600
            simiplified_id = "-".join(xy)
        else:
            # case
            # /1000/1002 ( /SystemInteractions_sys/Airbag-Interior_cntfrc ) contact.mb_fe /1000/112 ( /SystemInteractions_sys/Seat-Airbag_cnt ) :1 CFC600
            chn_nr = id_string.split(":")[-1].split("CFC")[0]
            simiplified_id = "-".join(xy) + ":" + chn_nr

        return simiplified_id

    def _add_ids(self, node, data_type):
        """add signal ids

        Args:
          node: param data_type:
          data_type: 

        Returns:

        """
        signals = [signal for signal in node.keys() if signal.startswith("SIGNAL")]
        for signal in signals:
            id_string = ''.join([chr(i) for i in list(node[signal].attrs.items())[0][1] if i != 0]).strip()
            if data_type == "rcforc" or data_type == "sbtout":
                simiplified_id = self._get_simplified_double_id(id_string)
            else:
                simiplified_id = id_string.split(" ")[0]

            ids_name = "ids" if data_type != "sbtout" else "belt_ids"
            # assert (simiplified_id not in self._d[data_type][ids_name])
            # if assert: ID is already in id list
            if simiplified_id  in self._d[data_type][ids_name]:
                continue

            self._d[data_type][ids_name].append(simiplified_id)
            self._d[data_type]["legend_ids"].append(id_string)

    def _add_time(self, node, data_type):
        """add time

        Args:
          node: param data_type:
          data_type: 

        Returns:

        """
        time_ = [signal for signal in node.keys() if signal == "X_VALUES"]
        assert len(time_) == 1
        if self._d[data_type]["time"] is None:
            self._d[data_type]["time"] = node["X_VALUES"][:]
        else:
            # sanity checks:
            #
            # Issue with different time lengths or different values
            assert self._d[data_type]["time"].shape == node["X_VALUES"][:].shape
            assert all([self._d[data_type]["time"][i] == node["X_VALUES"][i] for i in
                        np.arange(self._d[data_type]["time"].shape[0])])

    def __init__(self, madymo_file_path):
        """
        extracts data of the hdf5 files and wraps it into
        a readable file format

        :param madymo_file_path: full path to hdf5 file path
        """
        self._madymo_file_path = madymo_file_path
        self._d = dict()

        with h5py.File(self._madymo_file_path, 'r') as f:

            # 1. extracts available data categories : i.e. glstat, matsum, nodout, elout ... etc
            #       for each category the sub categories are assigned i.e. glstat --> internal_energy  etc.,
            #       mapping is done according to the identifiers in the output files i.e.
            f['MODEL_0'].visititems(self._get_available_data_types_dict)

            if "rcforc" in self._d:
                dimension = (self._d['rcforc']['time'].shape[0], len(self._d['rcforc']['ids']))
                data_types_to_be_filled = [i for i in self._d['rcforc'].keys() if i != "ids" and i != "time" and i != "legend_ids"]
                for data_type in data_types_to_be_filled:
                    self._d['rcforc'][data_type] = np.empty(dimension)
                    self._d['rcforc'][data_type][:] = np.nan

                    if data_type == DataChannelTypesContact.X_FORCE or \
                            data_type == DataChannelTypesContact.Y_FORCE or \
                            data_type == DataChannelTypesContact.Z_FORCE:
                        idx_madymo_data = 1 if data_type == DataChannelTypesContact.X_FORCE else (
                            2 if data_type == DataChannelTypesContact.Y_FORCE else 3)

                        self._extratct_data(f["MODEL_0/contact loads"], "rcforc", data_type,
                                            idx_madymo_data=idx_madymo_data)
                    elif data_type == DataChannelTypesContact.TIE_AREA:
                        idx_madymo_data = 1
                        self._extratct_data(f["MODEL_0/Contact Penetration|Area"], "rcforc", data_type,
                                            idx_madymo_data=idx_madymo_data)

            # extend the data dictionary
            if "nodout" in self._d:
                dimension = (self._d['nodout']['time'].shape[0], len(self._d['nodout']['ids']))
                data_types_to_be_filled = [i for i in self._d['nodout'].keys() if i != "ids" and i != "time" and i != "legend_ids"]
                for data_type in data_types_to_be_filled:
                    self._d['nodout'][data_type] = np.empty(dimension)
                    self._d['nodout'][data_type][:] = np.nan

                    if data_type == DataChannelTypesNodout.RX_DISPLACEMENT or \
                            data_type == DataChannelTypesNodout.RY_DISPLACEMENT or \
                            data_type == DataChannelTypesNodout.RZ_DISPLACEMENT:
                        #TODO: Check with LS-Dyna outputs the index for madymo data, maybe should be incrested by 1
                        idx_madymo_data = 0 if data_type == DataChannelTypesNodout.RX_DISPLACEMENT else (
                            1 if data_type == DataChannelTypesNodout.RY_DISPLACEMENT else 2)
                        self._extratct_data(f["MODEL_0/Angular displacements"], "nodout", data_type,
                                            idx_madymo_data=idx_madymo_data)
                        self._extratct_data(f["/MODEL_0/Relative displacements"], "nodout", data_type,
                                            idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.RX_VELOCITY or \
                            data_type == DataChannelTypesNodout.RY_VELOCITY or \
                            data_type == DataChannelTypesNodout.RZ_VELOCITY:
                        idx_madymo_data = 0 if data_type == DataChannelTypesNodout.RX_VELOCITY else (
                            1 if data_type == DataChannelTypesNodout.RY_VELOCITY else 2)
                        self._extratct_data(f["MODEL_0/Angular velocities"], "nodout",
                                            data_type, idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.RX_ACCELERATION or \
                            data_type == DataChannelTypesNodout.RY_ACCELERATION or \
                            data_type == DataChannelTypesNodout.RZ_ACCELERATION:
                        idx_madymo_data = 0 if data_type == DataChannelTypesNodout.RX_ACCELERATION else (
                            1 if data_type == DataChannelTypesNodout.RY_ACCELERATION else 2)
                        self._extratct_data(f["MODEL_0/Angular accelerations"], "nodout", data_type,
                                            idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.X_ACCELERATION or \
                            data_type == DataChannelTypesNodout.Y_ACCELERATION or \
                            data_type == DataChannelTypesNodout.Z_ACCELERATION:
                        idx_madymo_data = 1 if data_type == DataChannelTypesNodout.X_ACCELERATION else (
                            2 if data_type == DataChannelTypesNodout.Y_ACCELERATION else 3)
                        self._extratct_data(f["MODEL_0/Linear accelerations"],"nodout",
                                            data_type, idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.X_VELOCITY or \
                            data_type == DataChannelTypesNodout.Y_VELOCITY or \
                            data_type == DataChannelTypesNodout.Z_VELOCITY:
                        idx_madymo_data = 1 if data_type == DataChannelTypesNodout.X_VELOCITY else (
                            2 if data_type == DataChannelTypesNodout.Y_VELOCITY else 3)
                        self._extratct_data(f["MODEL_0/Linear velocities"], "nodout",
                                            data_type, idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.X_COORDINATE or \
                            data_type == DataChannelTypesNodout.Y_COORDINATE or \
                            data_type == DataChannelTypesNodout.Z_COORDINATE:
                        idx_madymo_data = 1 if data_type == DataChannelTypesNodout.X_COORDINATE else \
                            (2 if data_type == DataChannelTypesNodout.Y_COORDINATE else 3)
                        self._extratct_data(f["MODEL_0/Linear positions"], "nodout", data_type,
                                            idx_madymo_data=idx_madymo_data)

                    elif data_type == DataChannelTypesNodout.X_DISPLACEMENT or \
                            data_type == DataChannelTypesNodout.Y_DISPLACEMENT or \
                            data_type == DataChannelTypesNodout.Z_DISPLACEMENT:
                        idx_madymo_data = 1 if data_type == DataChannelTypesNodout.X_DISPLACEMENT else (
                            2 if data_type == DataChannelTypesNodout.Y_DISPLACEMENT else 3)
                        self._extratct_data(f["MODEL_0/Linear displacements"], "nodout", data_type,
                                            idx_madymo_data=idx_madymo_data)

            if "matsum" in self._d:
                dimension = (self._d['matsum']['time'].shape[0], len(self._d['matsum']['ids']))
                energy_to_be_filled = [i for i in self._d['matsum'].keys() if i != "ids" and i != "time" and i != "legend_ids"]
                for energy_type in energy_to_be_filled:
                    self._d['matsum'][energy_type] = np.empty(dimension)
                    self._d['matsum'][energy_type][:] = np.nan
                    self._extract_data_energy(f["MODEL_0/Energy output"], 'matsum', self._d["matsum"]["ids"], energy_type)

            if "glstat" in self._d:
                dimension = (self._d['glstat']['time'].shape[0],len(self._d['glstat']['ids']))
                energy_to_be_filled = [i for i in self._d['glstat'].keys() if i != "ids" and i != "time" and i != "legend_ids"]
                for energy_type in energy_to_be_filled:
                    self._d['glstat'][energy_type] = np.empty(dimension)
                    self._d['glstat'][energy_type][:] = np.nan
                    self._extract_data_energy(f["MODEL_0/Energy output"], 'glstat', self._d["glstat"]["ids"], energy_type)
                    self._d["glstat"][energy_type] = self._d["glstat"][energy_type].flatten()

            if "sbtout" in self._d:
                dimension = (self._d['sbtout']['time'].shape[0], len(self._d['sbtout']['belt_ids']))
                data_types_to_be_filled = [i for i in self._d['sbtout'].keys() if
                                           i != "belt_ids" and i != "time" and i != "legend_ids"]
                for data_type in data_types_to_be_filled:
                    self._d['sbtout'][data_type] = np.empty(dimension)
                    self._d['sbtout'][data_type][:] = np.nan
                    if data_type == DataChannelTypesSbtout.BELT_FORCE:
                        self._extratct_data(f["MODEL_0/Belt and restraint forces"], "sbtout", data_type,
                                    idx_madymo_data=0)
                    elif data_type == DataChannelTypesSbtout.BELT_LENGTH:
                        self._extratct_data(f["/MODEL_0/Retractor | pretensioner | load limiter | tying"],
                                            "sbtout", data_type, idx_madymo_data=0)
        logger = ConsoleLogger()
        self.dynasaur_definitions = DynasaurDefinitions(logger)

    def _get_available_data_types_dict(self, name, node):
        """callable for the visititems function
        
        function traverses the file tree recursively
        and initializes the data dictionary self._d
        
        self._d = {"nodout" : { "ids": np.array([]),
                                "time": np.array([]),
                                "rx_displacement" : None,
                                "rz_displacement" : None,
                                "ry_displacement" : None}
        
                   "glstat" : {
                                "time": np.array([])},
                                }
                    ...
                    TODO:
                    extension for further code types required!
        
                }
        
        actual values are appended afterwards.
        Done due to data padding:
        
        i.e.
        ids = [1,2,3,4,5,6]
        rx_acceleration only present for node 2/1, 2/2, 2/3
        rx_velocity only present for node 4,5,6
        
        read("nodout", "rx_acceleration") :
        [[Value, Value, Value, None, None, None],
             ...
         [Value, Value, Value, None, None, None],
         [Value, Value, Value, None, None, None]]
        
        
        
        read("nodout", "rx_velocity") :
        [[None, None, None, Value, Value, Value],
             ...
         [None, None, None, Value, Value, Value],
         [None, None, None, Value, Value, Value]]

        Args:
          node: param data_type:
          name: 

        Returns:

        """
        if type(node) is h5py.Dataset:
            # component names
            if "COMP" in node.name.split("/"):
                if 'nodout' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Angular ") or \
                            node.parent.name.split("/")[-1].startswith("Linear ") or \
                            node.parent.name.split("/")[-1].startswith("Relative displacements"):
                        self._d['nodout'] = {"ids": [], "legend_ids": [], "time": None}

                if 'glstat' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Energy output"):
                        self._d['glstat'] = {"ids": [], "legend_ids":[], "time": None}

                if 'matsum' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Energy output"):
                        self._d['matsum'] = {"ids": [], "legend_ids":[], "time": None}

                if 'rcforc' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("contact loads")  or \
                            node.parent.name.split("/")[-1].startswith("Contact Penetration|Area"):
                        self._d['rcforc'] = {"ids": [], "legend_ids":[], "time": None}

                if 'sbtout' not in self._d.keys():
                    if node.parent.name.split("/")[-1].startswith("Belt ") or \
                            node.parent.name.split("/")[-1].startswith("Retractor"):
                        self._d['sbtout'] = {"belt_ids": [], "legend_ids":[], "time": None}

                print(node.parent.name)
                if node.parent.name.split("/")[-1].startswith("Energy output"):
                    # TODO
                    # self._d['glstat'][DataChannelTypesNodout.RX_ACCELERATION] = None
                    # self._d['glstat'][DataChannelTypesNodout.RY_ACCELERATION] = None
                    # self._d['glstat'][DataChannelTypesNodout.RZ_ACCELERATION] = None

                    self._add_energy_ids(node.parent, data_type="glstat")
                    self._add_time(node.parent, data_type="glstat")
                    self._add_time(node.parent, data_type="matsum")

                if node.parent.name.split("/")[-1].startswith("Angular accelerations"):
                    self._d['nodout'][DataChannelTypesNodout.RX_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_ACCELERATION] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Angular velocity"):
                    self._d['nodout'][DataChannelTypesNodout.RX_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_VELOCITY] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Angular displacements"):
                    self._d['nodout'][DataChannelTypesNodout.RX_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_DISPLACEMENT] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Relative displacements"):
                    self._d['nodout'][DataChannelTypesNodout.RX_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RY_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.RZ_DISPLACEMENT] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear accelerations"):
                    self._d['nodout'][DataChannelTypesNodout.X_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_ACCELERATION] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_ACCELERATION] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear displacements"):
                    self._d['nodout'][DataChannelTypesNodout.X_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_DISPLACEMENT] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_DISPLACEMENT] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear positions"):
                    self._d['nodout'][DataChannelTypesNodout.X_COORDINATE] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_COORDINATE] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_COORDINATE] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")

                elif node.parent.name.split("/")[-1].startswith("Linear velocities"):
                    self._d['nodout'][DataChannelTypesNodout.X_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.Y_VELOCITY] = None
                    self._d['nodout'][DataChannelTypesNodout.Z_VELOCITY] = None
                    self._add_ids(node.parent, data_type="nodout")
                    self._add_time(node.parent, data_type="nodout")



                elif node.parent.name.split("/")[-1].startswith("contact loads"):
                    self._d['rcforc'][DataChannelTypesContact.X_FORCE] = None
                    self._d['rcforc'][DataChannelTypesContact.Y_FORCE] = None
                    self._d['rcforc'][DataChannelTypesContact.Z_FORCE] = None
                    self._add_ids(node.parent, data_type="rcforc")
                    self._add_time(node.parent, data_type="rcforc")

                elif node.parent.name.split("/")[-1].startswith("Contact Penetration|Area"):
                    self._d['rcforc'][DataChannelTypesContact.TIE_AREA] = None
                    self._add_ids(node.parent, data_type="rcforc")
                    self._add_time(node.parent, data_type="rcforc")

                elif node.parent.name.split("/")[-1].startswith("Belt "):
                    self._d['sbtout'][DataChannelTypesSbtout.BELT_FORCE] = None
                    self._add_ids(node.parent, data_type="sbtout")
                    self._add_time(node.parent, data_type="sbtout")

                elif node.parent.name.split("/")[-1].startswith("Retractor "):
                    self._d["sbtout"][DataChannelTypesSbtout.BELT_LENGTH] = None
                    self._add_ids(node.parent, data_type="sbtout")
                    #self._add_time(node.parent, data_type="sbtout")

    def read(self, *argv):
        """read function to access Madymo data in a similar way as reading binout files in:
        https://lasso-gmbh.github.io/lasso-python/build/html/dyna/Binout.html
        
        depends on the amount of keywords passed to the function

        Args:
          argv: return: list of keys or values
          *argv: 

        Returns:
          list of keys or values

        """
        read_argv = []

        for i in argv:
            read_argv.append(i)

        assert 0 <= len(read_argv) <= 4
        if len(read_argv) == 0:
            return list(self._d.keys())
        if len(read_argv) == 1:
            if read_argv[0] in self._d.keys():
                return list(self._d[read_argv[0]].keys())
            else:
                return []
        if len(read_argv) == 2:
            if read_argv[0] in self._d.keys():
                if read_argv[1] in self._d[read_argv[0]]:
                    return self._d[read_argv[0]][read_argv[1]]
                else:
                    return []
            else:
                return []
