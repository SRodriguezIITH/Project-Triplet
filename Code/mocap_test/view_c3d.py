
import ezc3d
import numpy as np
import os

file_path = os.path.join(os.getcwd(), 'main', 'data', '01_01.c3d')

c3d_data = ezc3d.c3d(file_path)

# Marker data
points = c3d_data['data']['points']  # shape: (4, n_markers, n_frames)

# Extract xyz only
xyz = points[:3, :, :]  # remove residual row

# Rearrange to (frames, markers, 3)
xyz = np.transpose(xyz, (2, 1, 0))

print("Shape:", xyz.shape)
print("Marker labels:", c3d_data['parameters']['POINT']['LABELS']['value'])