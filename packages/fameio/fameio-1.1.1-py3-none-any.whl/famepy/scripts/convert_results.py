# !/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re
import logging as log
from pathlib import Path

import pandas as pd

from famepy.source.tools import set_logfile
from famepy.protobuf_definitions import Services_pb2 as Service


def run(file_path, agents_to_extract=None):
    """Executes the main workflow for the reading of a FAME result file in protobuf format"""
    set_logfile("convertFameResults.log")
    source_file_name = file_path.split('\\')[-1]
    proto_buffer = read_proto_file(file_path)
    log.info('==> Create data frames and csv-files from results')

    for agent_type in proto_buffer.agentType:
        class_name = agent_type.className

        if agents_to_extract is not None:
            if class_name.upper() not in agents_to_extract:
                log.info('Output for agent {} ignored.'.format(class_name))
                continue
            else:
                agents_to_extract = agents_to_extract.replace(class_name.upper(), "")

        field_names_by_id = extract_agent_fields(agent_type)
        data_frames = create_data_frames(class_name, proto_buffer, field_names_by_id)

        output_folder_name = source_file_name.split(".")[1]
        if not os.path.exists(output_folder_name):
            os.mkdir(output_folder_name)

        out_file_name = output_folder_name + '/' + class_name + '.csv'
        if data_frames:
            write_to_file(out_file_name, data_frames)
        else:
            log.info('No output data for agent {}'.format(class_name))

    if agents_to_extract is not None:
        unknown_agents = re.sub("[,; \s]", " ", agents_to_extract)
        unknown_agents = re.sub("\s+", " ", unknown_agents)

        if len(unknown_agents) > 0:
            log.info('==> Unknown agents specified: {}'.format(unknown_agents))


def read_proto_file(proto_file_name):
    """Reads protobuf file with given `proto_file_name`"""
    log.info('==> Read data from file {}'.format(proto_file_name))
    proto_buffer = Service.Output()
    file = open(Path(proto_file_name).as_posix(), 'rb')
    proto_buffer.ParseFromString(file.read())
    file.close()
    return proto_buffer


def extract_agent_fields(agent_type):
    """Returns dictionary of column_names by column_id of given `agent_type`"""
    field_names_by_id = {}
    for field in agent_type.field:
        field_names_by_id[field.fieldId] = field.fieldName
    log.info('Added fields {} for agent {}'.format(field_names_by_id, agent_type.className))
    return field_names_by_id


def create_data_frames(class_name, proto_buffer, agent_fields):
    """Returns list of DataFrames each containing output (timestep, value) of one agent (by id) and column (by name)"""
    data_frames = []
    for series in proto_buffer.series:
        if class_name == series.className:
            column_data = extract_series(series, agent_fields)
            column_data_frames = build_frames_from_column_data(column_data)
            data_frames.extend(column_data_frames)
    return data_frames


def extract_series(series, agent_fields):
    """
    Returns a dictionary with the following shape:

    'times': dictionary mapping each output column (by name) to list of timesteps where an output occured
    'agentId': id of agent that created this output
    'values': dictionary mapping each output column (by name) to list of values for each timesteps with an output
    """
    values_dict = {}
    time_index_dict = {}

    for fieldId in agent_fields.keys():
        values_dict[fieldId] = []
        time_index_dict[fieldId] = []

    for line in series.line:
        current_time_step = line.timeStep
        for column in line.column:
            values_dict[column.fieldId].append(column.value)
            time_index_dict[column.fieldId].append(current_time_step)

    # rename fields from column_id to match column names
    values_dict = {agent_fields[k]: v for k, v in values_dict.items()}
    time_index_dict = {agent_fields[k]: v for k, v in time_index_dict.items()}

    return {'times': time_index_dict,
            'agentId': series.agentId,
            'values': values_dict}


def build_frames_from_column_data(column_data):
    """Returns list of DataFrames each entry resembling an output column with 'TimeStep' and 'AgentId' index"""
    column_data_frames = []
    values = column_data['values']
    times = column_data['times']
    for col_name, value_list in values.items():
        data_frame = pd.DataFrame({'TimeStep': times[col_name],
                                   'AgentId': column_data['agentId'],
                                   col_name: value_list})
        data_frame.set_index(['TimeStep', 'AgentId'], inplace=True)
        column_data_frames.append(data_frame)
    return column_data_frames


def write_to_file(out_file_name, data_frames):
    """Joins all DataFrames grouping by 'TimeStep' and 'AgentId' and exports result to disk"""
    joined_data_frame = pd.concat(data_frames, sort=False)
    grouped_joined_frame = joined_data_frame.groupby(['TimeStep', 'AgentId']).sum()
    grouped_joined_frame.sort_index(inplace=True)
    grouped_joined_frame.to_csv(out_file_name, sep=';', header=True, index=True)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        run(sys.argv[1], sys.argv[2].upper())
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print("Usage: {} <path/to/result/file.pb> ['list', 'of', 'agents']".format(sys.argv[0]))
