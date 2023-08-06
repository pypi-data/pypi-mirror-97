import gmsh


class Disk:
    """
    Creates a disk.

    Parameters
    ----------
    x0 : array-like[3]
        The 3 coordinates of the center of the disk face.
    radius0 : float
        Radius value of the disk.
    radius1 : float
        Radius along Y, leading to an ellipse.
    """

    dim = 2

    def __init__(self, x0, radius0, radius1=None):
        if len(x0) == 2:
            x0 = [x0[0], x0[1], 0.0]
        assert len(x0) == 3

        if radius1 is None:
            radius1 = radius0
        assert radius0 >= radius1

        self.x0 = x0
        self.radius0 = radius0
        self.radius1 = radius1

        self._ID = gmsh.model.occ.addDisk(*x0, radius0, radius1)
        self.dim_tags = [(self.dim, self._ID)]

    def __repr__(self):
        return f"<pygmsh Disk object, ID {self._ID}>"
