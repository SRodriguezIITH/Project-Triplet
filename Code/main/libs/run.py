import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import logging
import os
import sys
import yaml
from main.libs.process import MotionPipeline


def load_config(config_file=os.path.join(os.getcwd(), 'util', 'params', 'config.yaml')):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['folders']


logging.basicConfig(level=logging.INFO)

    # Load folder paths from YAML config file
config = load_config()

folder_path = os.path.join(os.getcwd(), config['mocap_txt'])
json_folder_path = os.path.join(os.getcwd(), config['mocap_json'])
bvh_folder_path = os.path.join(os.getcwd(), config['mocap_bvh'])

    # Initialize the MotionPipeline with paths
pipeline = MotionPipeline(folder_path, json_folder_path, bvh_folder_path)

    # Run the pipeline
pipeline.convert_txt_to_json()
pipeline.convert_json_to_bvh()