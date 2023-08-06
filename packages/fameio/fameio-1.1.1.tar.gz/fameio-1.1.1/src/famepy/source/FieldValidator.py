# !/usr/bin/env python
# -*- coding:utf-8 -*-

from enum import Enum
import logging as log

from .tools import load_yaml, log_and_raise


class FieldValidator:
    """ Handles validation of agent `Inputs` in scenario YAML files """
    type_schema = dict()

    def __init__(self, path_to_schema):
        data = load_yaml(path_to_schema)
        for agent, agent_details in data['AgentTypes'].items():
            if 'Inputs' in agent_details:
                self.type_schema[agent] = agent_details['Inputs']
            else:
                log.info("Agent '{}' has no specified 'Inputs'.".format(agent))

    def get_field_type(self, agent_type, field_name):
        """ Returns FieldType of given `field_name` of `agent_type` as specified in scenario schema """
        try:
            agent = self.type_schema[agent_type]
        except KeyError:
            log_and_raise("Schema has no agent '{}'.".format(agent_type))

        try:
            field = agent[field_name]
        except KeyError:
            log_and_raise("Schema agent '{}' has no field '{}'.".format(agent_type, field_name))

        try:
            field_type = field['FieldType']
        except KeyError:
            log_and_raise("'FieldType' missing in agent '{}' field '{}'.".format(agent_type, field_name))

        try:
            return FieldType[field_type.upper()]
        except KeyError:
            log_and_raise("FieldType '{}' not implemented.".format(field_type.upper()))

    def is_valid(self, agent_type, field_name, field_value):
        """ Returns true if `field_value` can be matched to given `data_type` """
        data_type = self.get_field_type(agent_type, field_name)
        return FieldValidator.is_compatible(data_type, field_value) and \
               FieldValidator.allowed_value(self.type_schema[agent_type][field_name], field_value)

    @staticmethod
    def is_compatible(data_type, field_value):
        """ Returns true if field type of given `field_value` is compatible to required `field_type`. """
        if data_type is FieldType.INTEGER:
            return isinstance(field_value, int)
        elif data_type is FieldType.DOUBLE:
            return isinstance(field_value, (int, float))
        elif data_type is FieldType.DOUBLE_LIST:
            return all(isinstance(x, (int, float)) for x in field_value)
        elif data_type is FieldType.ENUM:
            return isinstance(field_value, str)
        elif data_type is FieldType.TIME_SERIES:
            return isinstance(field_value, (str, int, float))
        else:
            log_and_raise("Validation not implemented for FieldType '{}'.".format(data_type))

    @staticmethod
    def allowed_value(field_definition, field_value):
        """
        Returns true if `field_value` matches one allowed 'Values' of `field_definition` or true,
        if no 'Values'-restrictions are specified.
        """
        if 'Values' in field_definition:
            return field_value in field_definition['Values']
        return True


class FieldType(Enum):
    INTEGER = 0
    DOUBLE = 1
    ENUM = 2
    TIME_SERIES = 3
    DOUBLE_LIST = 4
