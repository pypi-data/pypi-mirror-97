import numpy as np

class Rotation:
    def __init__(self, geometry, angle):
         self.R = np.array(
            [
                [+np.cos(angle), -np.sin(angle)],
                [+np.sin(angle), +np.cos(angle)],
            ]
        )
        self.R_inv = np.array(
            [
                [+np.cos(angle), +np.sin(angle)],
                [-np.sin(angle), +np.cos(angle)],
            ]
        )

        # rotate bounding box
        if geometry.corners is not None:
            rotated_corners = np.dot(self.R, geometry.corners.T)

        geometry.bbox = [
            np.min(rotated_corners[0]),
            np.max(rotated_corners[0]),
            np.min(rotated_corners[1]),
            np.max(rotated_corners[1]),
        ]
        return geometry
