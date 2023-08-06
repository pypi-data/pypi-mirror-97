import numpy as np
import segyio

filename = "testing.segy"
with segyio.open(filename, ignore_geometry=True) as f:
    nz, nx = len(f.samples), len(f.trace)
    vp = np.zeros(shape=(nz, nx))
    for index, trace in enumerate(f.trace):
        vp[:, index] = trace


spec = segyio.spec()
spec.tracecount = nx
spec.samples = list(range(nz))
spec.format = 1
output_file = "testing2.segy"
with segyio.create(output_file, spec) as src:
    for index in range(nx):
        src.trace[index] = vp[:, index]
