import os
import json
import numpy as np
from scipy.spatial.transform import Rotation as R


class BVHMaker:

    def __init__(self, json_folder, output_folder, scale=1.0):
        self.json_folder = json_folder
        self.output_folder = output_folder
        self.scale = scale

        os.makedirs(self.output_folder, exist_ok=True)

    # ----------------------------
    # Load JSON
    # ----------------------------
    def load_json(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.markers = data["markers"]
        self.frames = data["frames"]
        self.fps = data.get("frame_rate", 50)

        self.marker_map = {name: i for i, name in enumerate(self.markers)}

    # ----------------------------
    # Safe vector fetch
    # ----------------------------
    def vec(self, frame, marker_name):
        if marker_name not in self.marker_map:
            return np.zeros(3)

        idx = self.marker_map[marker_name]
        return np.array(frame[idx]) * self.scale

    def midpoint(self, a, b):
        return (a + b) / 2

    # ----------------------------
    # Safe normalize
    # ----------------------------
    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm < 1e-6:
            return None
        return v / norm

    # ----------------------------
    # Clean values
    # ----------------------------
    def clean(self, arr):
        return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)

    # ----------------------------
    # Joint reconstruction
    # ----------------------------
    def compute_joints(self):
        joint_frames = []

        for frame in self.frames:

            joints = {}

            pelvis = self.midpoint(
                self.vec(frame, "LASIS"),
                self.vec(frame, "RASIS")
            )

            lk = self.midpoint(
                self.vec(frame, "L.KneeLateral"),
                self.vec(frame, "L.KneeMedial")
            )

            rk = self.midpoint(
                self.vec(frame, "R.KneeLateral"),
                self.vec(frame, "R.KneeMedial")
            )

            la = self.midpoint(
                self.vec(frame, "L.AnkleLateral"),
                self.vec(frame, "L.AnkleMedial")
            )

            ra = self.midpoint(
                self.vec(frame, "R.AnkleLateral"),
                self.vec(frame, "R.AnkleMedial")
            )

            head = self.vec(frame, "Head_Top")

            joints["Hips"] = self.clean(pelvis)
            joints["LeftUpLeg"] = self.clean(lk)
            joints["LeftLeg"] = self.clean(la)
            joints["RightUpLeg"] = self.clean(rk)
            joints["RightLeg"] = self.clean(ra)
            joints["Head"] = self.clean(head)

            joint_frames.append(joints)

        return joint_frames

    # ----------------------------
    # Safe rotation
    # ----------------------------
    def compute_rotation(self, parent, child):
        direction = child - parent
        direction = self.normalize(direction)

        if direction is None:
            return np.array([0.0, 0.0, 0.0])

        forward = np.array([0, 0, 1])

        try:
            rot, _ = R.align_vectors([direction], [forward])
            euler = rot.as_euler('zyx', degrees=True)

            if np.isnan(euler).any():
                return np.array([0.0, 0.0, 0.0])

            return euler

        except:
            return np.array([0.0, 0.0, 0.0])

    def compute_frame_rotations(self, joints):
        return {
            "Hips": np.array([0.0, 0.0, 0.0]),
            "LeftUpLeg": self.compute_rotation(joints["Hips"], joints["LeftUpLeg"]),
            "LeftLeg": self.compute_rotation(joints["LeftUpLeg"], joints["LeftLeg"]),
            "RightUpLeg": self.compute_rotation(joints["Hips"], joints["RightUpLeg"]),
            "RightLeg": self.compute_rotation(joints["RightUpLeg"], joints["RightLeg"]),
            "Head": self.compute_rotation(joints["Hips"], joints["Head"]),
        }

    # ----------------------------
    # Offsets
    # ----------------------------
    def compute_offsets(self, first_frame):
        return {
            "Hips": np.array([0, 0, 0]),
            "LeftUpLeg": self.clean(first_frame["LeftUpLeg"] - first_frame["Hips"]),
            "LeftLeg": self.clean(first_frame["LeftLeg"] - first_frame["LeftUpLeg"]),
            "RightUpLeg": self.clean(first_frame["RightUpLeg"] - first_frame["Hips"]),
            "RightLeg": self.clean(first_frame["RightLeg"] - first_frame["RightUpLeg"]),
            "Head": self.clean(first_frame["Head"] - first_frame["Hips"]),
        }

    # ----------------------------
    # Write BVH
    # ----------------------------
    def write_bvh(self, filepath, joint_frames):

        offsets = self.compute_offsets(joint_frames[0])

        with open(filepath, "w") as f:

            f.write("HIERARCHY\n")
            f.write("ROOT Hips\n{\n")
            f.write(f"\tOFFSET {offsets['Hips'][0]} {offsets['Hips'][1]} {offsets['Hips'][2]}\n")
            f.write("\tCHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation\n")

            # LEFT
            f.write("\tJOINT LeftUpLeg\n\t{\n")
            f.write(f"\t\tOFFSET {offsets['LeftUpLeg'][0]} {offsets['LeftUpLeg'][1]} {offsets['LeftUpLeg'][2]}\n")
            f.write("\t\tCHANNELS 3 Zrotation Xrotation Yrotation\n")

            f.write("\t\tJOINT LeftLeg\n\t\t{\n")
            f.write(f"\t\t\tOFFSET {offsets['LeftLeg'][0]} {offsets['LeftLeg'][1]} {offsets['LeftLeg'][2]}\n")
            f.write("\t\t\tCHANNELS 3 Zrotation Xrotation Yrotation\n")
            f.write("\t\t\tEnd Site\n\t\t\t{\n\t\t\t\tOFFSET 0 0 0\n\t\t\t}\n")
            f.write("\t\t}\n\t}\n")

            # RIGHT
            f.write("\tJOINT RightUpLeg\n\t{\n")
            f.write(f"\t\tOFFSET {offsets['RightUpLeg'][0]} {offsets['RightUpLeg'][1]} {offsets['RightUpLeg'][2]}\n")
            f.write("\t\tCHANNELS 3 Zrotation Xrotation Yrotation\n")

            f.write("\t\tJOINT RightLeg\n\t\t{\n")
            f.write(f"\t\t\tOFFSET {offsets['RightLeg'][0]} {offsets['RightLeg'][1]} {offsets['RightLeg'][2]}\n")
            f.write("\t\t\tCHANNELS 3 Zrotation Xrotation Yrotation\n")
            f.write("\t\t\tEnd Site\n\t\t\t{\n\t\t\t\tOFFSET 0 0 0\n\t\t\t}\n")
            f.write("\t\t}\n\t}\n")

            # HEAD
            f.write("\tJOINT Head\n\t{\n")
            f.write(f"\t\tOFFSET {offsets['Head'][0]} {offsets['Head'][1]} {offsets['Head'][2]}\n")
            f.write("\t\tCHANNELS 3 Zrotation Xrotation Yrotation\n")
            f.write("\t\tEnd Site\n\t\t{\n\t\t\tOFFSET 0 0 0\n\t\t}\n")
            f.write("\t}\n")

            f.write("}\n")

            # MOTION
            f.write("MOTION\n")
            f.write(f"Frames: {len(joint_frames)}\n")
            f.write(f"Frame Time: {1.0/self.fps}\n")

            for joints in joint_frames:
                rot = self.compute_frame_rotations(joints)

                hips = self.clean(joints["Hips"])
                rot = {k: self.clean(v) for k, v in rot.items()}

                line = f"{hips[0]} {hips[1]} {hips[2]} "
                line += " ".join(map(str, rot["Hips"])) + " "
                line += " ".join(map(str, rot["LeftUpLeg"])) + " "
                line += " ".join(map(str, rot["LeftLeg"])) + " "
                line += " ".join(map(str, rot["RightUpLeg"])) + " "
                line += " ".join(map(str, rot["RightLeg"])) + " "
                line += " ".join(map(str, rot["Head"]))

                f.write(line + "\n")

    # ----------------------------
    # Pipeline
    # ----------------------------
    def process_file(self, json_path):

        self.load_json(json_path)

        # Downsample safely
        step = max(1, int(self.fps / 50))
        self.frames = self.frames[::step]

        joint_frames = self.compute_joints()

        filename = os.path.basename(json_path).replace(".json", ".bvh")
        output_path = os.path.join(self.output_folder, filename)

        self.write_bvh(output_path, joint_frames)

        print(f"Processed: {filename}")

    def process_all(self):
        for file in os.listdir(self.json_folder):
            if file.endswith(".json"):
                self.process_file(os.path.join(self.json_folder, file))