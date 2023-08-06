import time
from six import string_types

from ..utils.constants import LOGConstants, JsonConstants, DefinitionConstants, UnitsConstants, ObjectConstantsForData
from ..utils.constants import LoggerDefinitionFileValidator as LD


class TestDefinitionJSON:
    """ """
    @staticmethod
    def _assert_objects(object, logger):
        """

        Args:
          object: param logger:
          logger: 

        Returns:

        """
        if (JsonConstants.ID in object and JsonConstants.ID_RANGE in object):
            assert False, logger.emit(LOGConstants.ERROR[0], LD.ID_MUST_BE_DEFINITED)
        if JsonConstants.ID in object:
            assert isinstance(object[JsonConstants.ID], list), logger.emit(LOGConstants.ERROR[0], LD.ID_IS_INTEGER_LIST)
        elif JsonConstants.ID_RANGE in object:
            assert isinstance(object[JsonConstants.ID_RANGE], list), logger.emit(LOGConstants.ERROR[0], LD.ID_IS_INTEGER_LIST)
        elif JsonConstants.PART_ID in object:
            assert isinstance(object[JsonConstants.PART_ID], list), logger.emit(LOGConstants.ERROR[0], LD.ID_IS_INTEGER_LIST)
        else:
            assert(False)

        if object[JsonConstants.TYPE] != ObjectConstantsForData.CONTACT:
            if JsonConstants.ID in object:
                assert all(isinstance(x, int) for x in object[JsonConstants.ID]), \
                logger.emit(LOGConstants.ERROR[0], "ID must be list of integers")
            elif JsonConstants.ID_RANGE in object:
                assert all(isinstance(x, int) for x in object[JsonConstants.ID_RANGE]), \
                    logger.emit(LOGConstants.ERROR[0], "ID must be list of integers")

    @staticmethod
    def test_def_json(json_objects, logger):
        """

        Args:
          json_objects: param logger:
          logger: 

        Returns:

        """
        #code_type = CodeType.BINOUT
        if DefinitionConstants.OBJECTS in json_objects:
                assert isinstance(json_objects[DefinitionConstants.OBJECTS], list), \
                    logger.emit(LOGConstants.ERROR[0], LD.LIST_TYPE)
                for obj in json_objects[DefinitionConstants.OBJECTS]:
                    assert JsonConstants.TYPE in obj, \
                        logger.emit(LOGConstants.ERROR[0], LD.TYPE_MISSING)
                    assert isinstance(obj[JsonConstants.TYPE], string_types)
                    assert JsonConstants.NAME in obj, \
                        logger.emit(LOGConstants.ERROR[0], LD.NAME_MISSING)
                    assert isinstance(obj[JsonConstants.NAME], string_types)
                    if obj[JsonConstants.TYPE] == ObjectConstantsForData.NODE:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.CONTACT:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.ELEMENT:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.DISCRETE:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.SEAT_BELT:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.ENERGY_PART:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.ENERGY_GLOBAL:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.CROSS_SECTION:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.DISBOUT:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.DISBOUT_PART:
                        TestDefinitionJSON._assert_objects(obj, logger)
                    elif obj[JsonConstants.TYPE] == ObjectConstantsForData.ELEMENTOBJECT:
                        if JsonConstants.ID not in obj and "id_range" not in obj:
                            raise IOError("Not defined")
                        if "id_range" in obj:
                            assert len(obj["id_range"]) > 1
                            # assert obj["id_range"][0] < obj["id_range"][1]
                    else:
                        logger.emit(LOGConstants.ERROR[0], "Not valid type: >>> " + obj[JsonConstants.TYPE] + " <<<")
                        time.sleep(0.5)
                        exit("Exiting")
        else:
            for j_obj in json_objects:
                if DefinitionConstants.TITLE in j_obj:
                    assert isinstance(j_obj[DefinitionConstants.TITLE], string_types), \
                        logger.emit(LOGConstants.ERROR[0], LD.STRING_TYPE)

                elif DefinitionConstants.UNIT in j_obj:
                    assert UnitsConstants.TIME in j_obj[DefinitionConstants.UNIT], \
                        logger.emit(LOGConstants.ERROR[0], LD.TIME_MISSING)
                    assert isinstance(j_obj[DefinitionConstants.UNIT][UnitsConstants.TIME], string_types), \
                        logger.emit(LOGConstants.ERROR[0], LD.STRING_TYPE)
                    assert UnitsConstants.LENGTH in j_obj[DefinitionConstants.UNIT], \
                        logger.emit(LOGConstants.ERROR[0], LD.LENGTH_MISSING)
                    assert isinstance(j_obj[DefinitionConstants.UNIT][UnitsConstants.LENGTH], string_types), \
                        logger.emit(LOGConstants.ERROR[0], LD.STRING_TYPE)
                    assert UnitsConstants.WEIGHT in j_obj[DefinitionConstants.UNIT], \
                        logger.emit(LOGConstants.ERROR[0], LD.WEIGHT_MISSING)
                    assert isinstance(j_obj[DefinitionConstants.UNIT][UnitsConstants.WEIGHT], string_types), \
                        logger.emit(LOGConstants.ERROR[0], LD.STRING_TYPE)


                elif DefinitionConstants.DATA_VIS in j_obj:
                    assert isinstance(j_obj[DefinitionConstants.DATA_VIS], list)
                    for def_vis in j_obj[DefinitionConstants.DATA_VIS]:
                        assert JsonConstants.NAME in def_vis, logger.emit(LOGConstants.ERROR[0], LD.NAME_MISSING)
                        assert isinstance(def_vis[JsonConstants.NAME], string_types), \
                            logger.emit(LOGConstants.ERROR[0], LD.STRING_TYPE)
                        assert JsonConstants.PART_OF in def_vis, \
                            logger.emit(LOGConstants.ERROR[0],
                                        LD.PART_OF_MISSING + def_vis[JsonConstants.NAME])

                elif DefinitionConstants.CRITERIA in j_obj:
                    assert isinstance(j_obj[DefinitionConstants.CRITERIA], list), \
                        logger.emit(LOGConstants.ERROR[0], DefinitionConstants.CRITERIA + LD.LIST_TYPE)
                    for criteria in j_obj[DefinitionConstants.CRITERIA]:
                        assert JsonConstants.NAME in criteria, \
                            logger.emit(LOGConstants.ERROR[0], LD.NAME_MISSING)
                        assert JsonConstants.TYPE_OF_CRTITERIA in criteria, \
                            logger.emit(LOGConstants.ERROR[0], LD.CRITERIA_TYPE_OF_MISSING + criteria[JsonConstants.NAME])
                        assert JsonConstants.PART_OF in criteria, \
                            logger.emit(LOGConstants.ERROR[0], LD.PART_OF_MISSING + criteria[JsonConstants.NAME])
                        assert JsonConstants.FUNCTION in criteria, \
                            logger.emit(LOGConstants.ERROR[0], LD.CRITERIA_FUNCTION_MISSING + criteria[JsonConstants.NAME])
                        value_of_crit = criteria[JsonConstants.TYPE_OF_CRTITERIA]
                        if value_of_crit != JsonConstants.CRITERIA_KINEMATIC and value_of_crit != JsonConstants.CRITERIA_LOAD \
                                and value_of_crit != JsonConstants.CRITERIA_INJURY and value_of_crit != JsonConstants.CRITERIA_ENERGY \
                                and value_of_crit != JsonConstants.CRITERIA_METADATA and value_of_crit != JsonConstants.CRITERIA_RISK \
                                and value_of_crit != JsonConstants.CRITERIA_TIME:
                            assert False, \
                                logger.emit(LOGConstants.ERROR[0], LD.CRITERIA_TYPE_INCORRECT + value_of_crit)

                # elif DefinitionConstants.CODE in j_obj:
                #     assert "MADYMO" == j_obj[DefinitionConstants.CODE] or "BINOUT" == j_obj[DefinitionConstants.CODE]
                else:
                    assert False, logger.emit(LOGConstants.ERROR[0],
                                              LD.NOT_VALID_DEFINITION + str(j_obj) + LD.GITLAB_REFERENCE)
