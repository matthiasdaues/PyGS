import yaml
import os


def read_configuration(config):
    """
    Gets database configuration parameters from the given
    "config.yml" file and creates a configuration dictionary
    to be used in other functions.
    """

    # read the configuration
    with open(config) as file:
        configuration = yaml.safe_load(file)

    # create paths for the local folder structure
    paths = {}
    paths['secret_path'] = os.path.join(configuration['base_path'], 'secrets')


    # append paths to configuration dictionary
    configuration['paths'] = paths

    # create path to secrets.txt
    configuration['stored_secrets'] = os.path.join(configuration['paths']['secret_path'], 'secrets.txt') 

    return configuration