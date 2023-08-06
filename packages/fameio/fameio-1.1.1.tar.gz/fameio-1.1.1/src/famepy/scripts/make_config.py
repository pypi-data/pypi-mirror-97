# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import pathlib as pt
from fnmatch import fnmatch
import os

import yaml

from famepy.source.FieldValidator import FieldValidator, FieldType
from famepy.source.TimeSeriesManager import TimeSeriesManager
from famepy.source.tools import load_yaml, log_and_raise, set_logfile
from famepy.source.FameTime import FameTime
from famepy.protobuf_definitions import InputFile_pb2

DISABLING_YAML_FILE_PREFIX = "DISABLED_"


def add_contracts_from_folder(contracts, path):
    """
    Reads YAML files under the given path and adds their `Contracts` to the given list of contracts.
    Ignores files starting with a disabling prefix
    """
    for contract_file in get_contract_file_list(path):
        with open(pt.Path(path, contract_file), "r") as config_file:
            yaml_data = yaml.load(config_file, Loader=yaml.FullLoader)
            for contract in yaml_data['Contracts']:
                contracts.append(contract)


def get_contract_file_list(path):
    """Returns list of files with ending ".yaml" or ".yml" in given folder not having the disabling prefix"""
    ignore_filter = DISABLING_YAML_FILE_PREFIX + "*"
    file_list = []
    for file_name in os.listdir(path):
        if (fnmatch(file_name, "*.yaml") or fnmatch(file_name, "*.yml")) and not fnmatch(file_name, ignore_filter):
            file_list.append(file_name)
    return file_list


def set_general_properties(properties, proto):
    """Set the general simulation properties in the given proto_buffer"""
    for property_name, property_value in properties.items():
        if not hasattr(property_value, "keys"):
            setattr(proto, property_name, property_value)
        else:
            parent = getattr(proto, property_name)
            for child_property_name, child_property_value in property_value.items():
                if child_property_name == "startTime" or child_property_name == "stopTime":
                    child_property_value = int(FameTime.convert_time_string_to_fame_time_step(child_property_value))
                setattr(parent, child_property_name, child_property_value)


def update_field_values(pb_agent, fields, time_series_manager, field_validator):
    """Adds all fields in the given list to the given agent proto buffer"""
    if fields is not None:
        agent_type = pb_agent.className
        for field_name, field_value in fields.items():
            pb_field = pb_agent.field.add()
            pb_field.fieldName = field_name
            field_type = field_validator.get_field_type(agent_type, field_name)
            if field_validator.is_valid(agent_type, field_name, field_value):
                if field_type is FieldType.INTEGER:
                    pb_field.intValue = field_value
                elif field_type is FieldType.DOUBLE:
                    pb_field.doubleValue.extend([field_value])
                elif field_type is FieldType.ENUM:
                    pb_field.stringValue = field_value
                elif field_type is FieldType.TIME_SERIES:
                    if isinstance(field_value, str):
                        file_name = pt.Path(field_value).as_posix()
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(file_name)
                    else:
                        pb_field.seriesId = time_series_manager.save_get_time_series_id(field_value)
                elif field_type is FieldType.DOUBLE_LIST:
                    for element in field_value:
                        pb_field.doubleValue.extend([element])
                else:
                    log_and_raise("FieldType '{}' not implemented.".format(field_type))
            else:
                log_and_raise("'{}' not allowed in field '{}' of agent {}".format(field_value, field_name, pb_agent.id))


def get_or_error(agent, param):
    """Gets given `param` from dictionary or raises error if field is missing"""
    try:
        return agent[param]
    except KeyError:
        log_and_raise("Cannot find '{}' in `agent` {}".format(param, agent))


def set_agents_and_time_series(agent_list, proto_buffer, field_validator):
    """
    Iterates through all agents, adds them and all of their fields to the given proto buffer and also
    adds all referenced files as time series to the proto_buffer. Ensures proper field parameterization and format.
    """
    time_series_manager = TimeSeriesManager()
    for agent in agent_list:
        agent = convert_keys_to_lower(agent)
        pb_agent = proto_buffer.agent.add()
        pb_agent.className = get_or_error(agent, "type")
        pb_agent.id = get_or_error(agent, "id")
        if "fields" in agent:
            fields = agent.get("fields")
            update_field_values(pb_agent, fields, time_series_manager, field_validator)
    time_series_manager.add_time_series_to_proto_buffer(proto_buffer)


def convert_keys_to_lower(agent):
    """Returns given dictionary with `keys` in lower case"""
    return {keys.lower(): value for keys, value in agent.items()}


def set_contracts(contracts, proto_buffer):
    """Adds all contracts in the given list to the given proto buffer"""
    for contract in contracts:
        pb_contract = proto_buffer.contract.add()
        for key, value in contract.items():
            setattr(pb_contract, key, value)


def run(yaml_file):
    """Executes the main workflow for the building of a FAME configuration file"""
    config_data = load_yaml(yaml_file)
    run_config = config_data["RunConfig"]
    set_logfile(run_config["LogFile"])
    validator = FieldValidator(run_config["Schema"])
    proto_input_data = InputFile_pb2.InputData()
    set_general_properties(config_data["GeneralProperties"], proto_input_data)
    set_agents_and_time_series(config_data["Agents"], proto_input_data, validator)

    contract_list = [] if config_data.get("Contracts") is None else config_data.get("Contracts")
    if "ContractsPath" in run_config:
        contract_folder_path = run_config["ContractsPath"]
        add_contracts_from_folder(contract_list, contract_folder_path)
    set_contracts(contract_list, proto_input_data)

    f = open(run_config["OutputFile"], "wb")
    f.write(proto_input_data.SerializeToString())
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <path/to/configuration/file.yaml>".format(sys.argv[0]))
    else:
        run(sys.argv[1])
