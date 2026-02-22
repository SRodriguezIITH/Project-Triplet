import ezc3d
import json
import numpy as np
import os


def c3d_to_json(input_path, output_path):

    # Load C3D file
    c3d = ezc3d.c3d(input_path)

    # Extract marker labels
    marker_labels = c3d['parameters']['POINT']['LABELS']['value']

    # Extract frame rate
    frame_rate = c3d['parameters']['POINT']['RATE']['value'][0]

    # Extract marker data
    # Shape: (4, num_markers, num_frames)
    # First 3 rows = X, Y, Z
    points = c3d['data']['points']

    # Keep only XYZ
    xyz = points[:3, :, :]   # shape: (3, markers, frames)

    # Rearrange to (frames, markers, 3)
    xyz = np.transpose(xyz, (2, 1, 0))

    # Replace NaNs with zeros
    xyz = np.nan_to_num(xyz)

    data_dict = {
        "frame_rate": frame_rate,
        "num_frames": xyz.shape[0],
        "num_markers": xyz.shape[1],
        "markers": marker_labels,
        "frames": xyz.tolist()
    }

    with open(output_path, 'w') as outfile:
        json.dump(data_dict, outfile)

    print("Conversion complete.")
    print(f"Frames: {xyz.shape[0]}")
    print(f"Markers: {xyz.shape[1]}")
    print(f"Frame Rate: {frame_rate}")


if __name__ == "__main__":

    input_c3d = os.path.join(os.getcwd(), 'main', 'data', '01_01.c3d')
    output_json = os.path.join(os.getcwd(), 'main', 'data', 'mocap.json')

    c3d_to_json(input_c3d, output_json)