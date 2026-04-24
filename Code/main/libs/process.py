import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from main.util.preprocessing.dataloader import DataLoader
from main.util.preprocessing.bvhmaker import BVHMaker

                           
class MotionPipeline:
    """
    Class which handles the entire motion processing pipeline, from loading raw mocap data to exporting it in various formats,
    and eventually loading it in unity to simulate the motion and save its video.
    """
    def __init__(self, folder_path, json_folder_path, bvh_folder_path):
        self.folder_path = folder_path
        self.json_folder_path = json_folder_path
        self.bvh_folder_path = bvh_folder_path

    #####################
    #Convert all TXT mocaps to JSON mocaps
    #####################

    def convert_txt_to_json(self):
        try:
            loader = DataLoader(folder_path=self.folder_path, skip_header_rows=5, downsample_factor=1)
            print("Loading files from:", self.folder_path)
            print(loader)

            datasets = loader.load_all_files()

            print("Loaded files:\n", list(datasets.keys()))

            print("Converting all to JSON...")

            loader.export_all_to_json(output_folder=self.json_folder_path, frame_rate=120)

        except Exception as e:
            print(f"Error during TXT to JSON conversion: {e}")


    #####################
    #Convert all JSON mocaps to BVH mocaps
    #####################

    def convert_json_to_bvh(self):
        try:
            maker = BVHMaker(json_folder=self.json_folder_path, output_folder=self.bvh_folder_path)
            print("Processing JSON files from:", self.json_folder_path)
            print(maker)

            maker.process_all()
        except Exception as e:
            print(f"Error during JSON to BVH conversion: {e}")

    
    