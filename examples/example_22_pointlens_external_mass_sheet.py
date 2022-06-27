"""
Example use of MulensModel to model a PSPL with an
external mass sheet, Chang-refsdal.
PSPL with external mass sheet assumes a point source.
"""
import numpy as np
import matplotlib.pyplot as plt

import MulensModel as mm


# Define lens model and source parameters
alpha = 180
K = 0.1
G = complex(0.1, -0.05)
t_0 = 300
t_E = 500
u_0 = 0.1

time = np.arange(t_0-775., t_0+775., 0.4, dtype=float)

lens = mm.model.Model({
    't_0': t_0, 'u_0': u_0, 't_E': t_E,
    'convergence_K': K, 'shear_G': G, 'alpha': alpha})
no_shear = mm.model.Model({'t_0': t_0, 'u_0': u_0, 't_E': t_E})

lens.set_magnification_methods(
    [min(time), 'point_source_with_shear', max(time)])
no_shear.set_magnification_methods([min(time), 'point_source', max(time)])

# Plot magnification curve and caustics
(_, (ax1, ax2)) = plt.subplots(figsize=(10, 5), ncols=2)

ax1.plot(time, lens.get_magnification(time), color='r')
ax1.plot(time, no_shear.get_magnification(time), alpha=0.4)

ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_xlabel("x", fontweight="bold")
ax2.set_ylabel("y", fontweight="bold")
lens.plot_trajectory(t_range=[t_0 - 475, t_0], caustics=True, color='green')
lens.plot_trajectory(t_range=[t_0, t_0 + 475], color='blue')

plt.show()
