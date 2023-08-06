# !/usr/bin/env python
# -*- coding:utf-8 -*-

import logging as log
import pathlib as pt

import yaml


def load_yaml(yaml_file_path):
    """Loads the yaml file from given `yaml_file_path` and returns its content"""
    with open(pt.Path(yaml_file_path), "r") as configfile:
        data = yaml.load(configfile,  Loader=yaml.FullLoader)
    return data


def log_and_raise(message):
    """ Raises a critical error and logs with given `error_message` """
    log.critical(message)
    raise Exception(message)


def set_logfile(file_name):
    """Open a log file with the given name"""
    log.basicConfig(filename=file_name,
                    filemode='w',
                    format='%(levelname)s:%(message)s',
                    level=log.DEBUG,
                    )