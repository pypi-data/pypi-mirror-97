import os,sys
from dotenv.main import dotenv_values


def load_config(path):
    try:
        return dotenv_values(dotenv_path=path)
    except FileNotFoundError:
        print('Invalid path: {}'.format(path))
        sys.exit(1)


def get_variables(config):
    return {**get_environment_variables(config), **get_secret_variables(config)}
    
def get_environment_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('ENV_'), config.keys()))
    variables = {}
    for key in env_keys:
        variables[key.replace('ENV_','')] = config[key]
    return variables


def get_secret_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('SECRET_'), config.keys()))
    variables = {}
    for key in env_keys:
        variables[key.replace('SECRET_','')] = "${"+config[key]+"}"
    return variables
