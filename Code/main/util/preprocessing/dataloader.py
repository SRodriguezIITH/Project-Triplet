import os
import json
import pandas as pd
import numpy as np

class DataLoader:
    def __init__(self, folder_path, skip_header_rows=5, downsample_factor=1):
        """
        folder_path: directory containing .txt or .trc mocap files
        skip_header_rows: used for generic .txt files
        downsample_factor: e.g., 10 reduces 1000 Hz -> 100 Hz
        """
        self.folder_path = folder_path
        self.skip_header_rows = skip_header_rows
        self.downsample_factor = downsample_factor
        self.datasets = {}

    def _load_trc_file(self, file_path):
        """Parses standard TRC (Track Row Column) files."""
        try:
            # TRC files are typically tab-separated. 
            # Row 3 contains Marker Names, Row 4 contains X, Y, Z labels.
            # Data usually starts at Row 6.
            with open(file_path, 'r') as f:
                header = [f.readline() for _ in range(5)]
            
            # Extract basic info from header
            # Row 3: Name1, , , Name2, , , 
            marker_names_raw = header[3].split('\t')
            # Filter out empty strings and generic labels like 'Frame', 'Time'
            marker_names = [m.strip() for m in marker_names_raw if m.strip() and m.strip() not in ['Frame#', 'Time']]
            
            # Load the data
            df = pd.read_csv(file_path, sep='\t', skiprows=5)
            
            # TRC columns: Frame, Time, X1, Y1, Z1, X2, Y2, Z2...
            # We skip the first two columns (Frame and Time)
            raw_data = df.iloc[:, 2:].values
            
            # Reshape to (Frames, Markers, 3)
            num_frames = raw_data.shape[0]
            num_markers = len(marker_names)
            
            # Ensure the data matches expected marker count (truncate if extra cols exist)
            data = raw_data[:, :num_markers * 3].reshape(num_frames, num_markers, 3)

            return {
                "file_name": os.path.basename(file_path),
                "num_frames": num_frames,
                "num_markers": num_markers,
                "marker_names": marker_names,
                "data": data.astype(np.float32)
            }
        except Exception as e:
            print(f"Error parsing TRC {file_path}: {e}")
            return None

    def _load_txt_file(self, file_path):
        """Original logic for custom tab-separated TXT files."""
        try:
            df = pd.read_csv(
                file_path,
                sep="\t",
                skiprows=self.skip_header_rows
            )
            df = df.loc[:, ~df.columns.duplicated()]

            xyz_columns = [col for col in df.columns if col.endswith(('_X', '_Y', '_Z'))]
            marker_dict = {}
            for col in xyz_columns:
                base, axis = col.rsplit('_', 1)
                if base not in marker_dict: marker_dict[base] = {}
                marker_dict[base][axis] = col

            valid_markers = {n: a for n, a in marker_dict.items() if all(x in a for x in ['X', 'Y', 'Z'])}
            marker_names = sorted(valid_markers.keys())

            if not marker_names:
                return None

            frames = len(df)
            num_markers = len(marker_names)
            data = np.zeros((frames, num_markers, 3), dtype=np.float32)

            for i, name in enumerate(marker_names):
                data[:, i, 0] = df[valid_markers[name]['X']].values
                data[:, i, 1] = df[valid_markers[name]['Y']].values
                data[:, i, 2] = df[valid_markers[name]['Z']].values

            return {
                "file_name": os.path.basename(file_path),
                "num_frames": frames,
                "num_markers": num_markers,
                "marker_names": marker_names,
                "data": data
            }
        except Exception as e:
            print(f"Error parsing TXT {file_path}: {e}")
            return None

    def load_all_files(self):
        for file in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, file)
            result = None

            if file.lower().endswith(".txt"):
                result = self._load_txt_file(full_path)
            elif file.lower().endswith(".trc"):
                result = self._load_trc_file(full_path)

            if result:
                # Apply downsampling if needed
                if self.downsample_factor > 1:
                    result["data"] = result["data"][::self.downsample_factor]
                    result["num_frames"] = result["data"].shape[0]
                
                self.datasets[file] = result
                print(f"Loaded {file} → {result['num_frames']} frames, {result['num_markers']} markers")

        return self.datasets

    def export_all_to_json(self, output_folder, frame_rate=120):
        os.makedirs(output_folder, exist_ok=True)

        for name, dataset in self.datasets.items():
            json_data = {
                "file_source": name,
                "frame_rate": frame_rate / self.downsample_factor,
                "num_frames": dataset["num_frames"],
                "num_markers": dataset["num_markers"],
                "markers": dataset["marker_names"],
                "frames": dataset["data"].tolist() # Convert numpy to list for JSON
            }

            # Clean name for folder structure
            clean_name = name.replace(".txt", "").replace(".trc", "").replace(".", "_")
            output_path = os.path.join(output_folder, clean_name, "mocap.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w") as f:
                json.dump(json_data, f)

            print(f"Exported {output_path}")


# import os
# import json
# import pandas as pd
# import numpy as np


# class DataLoader:
#     def __init__(self, folder_path, skip_header_rows=5, downsample_factor=1):
#         """
#         folder_path: directory containing .txt mocap files
#         skip_header_rows: number of metadata rows before table header
#         downsample_factor: e.g., 10 reduces 1000 Hz -> 100 Hz
#         """
#         self.folder_path = folder_path
#         self.skip_header_rows = skip_header_rows
#         self.downsample_factor = downsample_factor
#         self.datasets = {}

#     def _load_single_file(self, file_path):
#         try:
#             # Read tab-separated file
#             df = pd.read_csv(
#                 file_path,
#                 sep="\t",
#                 skiprows=self.skip_header_rows
#             )

#             # Remove duplicate columns
#             df = df.loc[:, ~df.columns.duplicated()]

#             # Identify XYZ columns only
#             xyz_columns = [
#                 col for col in df.columns
#                 if col.endswith(('_X', '_Y', '_Z'))
#             ]

#             # Group by marker base name
#             marker_dict = {}
#             for col in xyz_columns:
#                 base = col.rsplit('_', 1)[0]
#                 axis = col.rsplit('_', 1)[1]

#                 if base not in marker_dict:
#                     marker_dict[base] = {}

#                 marker_dict[base][axis] = col

#             # Keep only markers with complete XYZ
#             valid_markers = {
#                 name: axes for name, axes in marker_dict.items()
#                 if all(a in axes for a in ['X', 'Y', 'Z'])
#             }

#             marker_names = sorted(valid_markers.keys())

#             if len(marker_names) == 0:
#                 print(f"No valid markers in {file_path}")
#                 return None

#             frames = len(df)
#             num_markers = len(marker_names)

#             # Allocate structured array
#             data = np.zeros((frames, num_markers, 3), dtype=np.float32)

#             for i, name in enumerate(marker_names):
#                 data[:, i, 0] = df[valid_markers[name]['X']].values
#                 data[:, i, 1] = df[valid_markers[name]['Y']].values
#                 data[:, i, 2] = df[valid_markers[name]['Z']].values

#             # Downsample if requested
#             if self.downsample_factor > 1:
#                 data = data[::self.downsample_factor]
#                 frames = data.shape[0]

#             print(f"Loaded {os.path.basename(file_path)} → "
#                   f"{frames} frames, {num_markers} markers")

#             return {
#                 "file_name": os.path.basename(file_path),
#                 "num_frames": frames,
#                 "num_markers": num_markers,
#                 "marker_names": marker_names,
#                 "data": data
#             }

#         except Exception as e:
#             print(f"Error processing {file_path}: {e}")
#             return None

#     def load_all_files(self):
#         for file in os.listdir(self.folder_path):
#             if file.endswith(".txt"):
#                 full_path = os.path.join(self.folder_path, file)
#                 result = self._load_single_file(full_path)

#                 if result:
#                     self.datasets[file] = result

#         return self.datasets

#     def export_all_to_json(self, output_folder, frame_rate=120):
#         os.makedirs(output_folder, exist_ok=True)

#         for name, dataset in self.datasets.items():
#             json_data = {
#                 "frame_rate": frame_rate,
#                 "num_frames": dataset["num_frames"],
#                 "num_markers": dataset["num_markers"],
#                 "markers": dataset["marker_names"],
#                 "frames": dataset["data"].tolist()
#             }

#             output_path = os.path.join(
#                 output_folder,
#                 name.replace(".txt", ""),
#                 "mocap.json"
#             )
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)

#             with open(output_path, "w") as f:
#                 json.dump(json_data, f)

#             print(f"Exported {output_path}")