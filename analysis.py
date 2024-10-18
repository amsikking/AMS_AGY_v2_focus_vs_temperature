# Third party imports, installable via pip:
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude as ggm
from scipy.optimize import curve_fit
from tifffile import imread, imwrite

# Decide if using full or cropped data set:
data_cropped = True

# Copy steps from 'acquisition.py' and get metadata:
z_steps_um = np.arange(0, 100, 0.25)
t_steps_C = np.arange(22, 42, 1)
with open('data\\metadata.txt', 'r') as file:
    metadata_lines = file.read().splitlines()

# Calculate the gradient magnitude for each image and sum the pixels:
# -> the image with the sharpest features should have the highest sum
t_actual_C = np.zeros(len(t_steps_C))
t_actual_O2_C = np.zeros(len(t_steps_C))
grad_mag_sum = np.zeros((len(t_steps_C), len(z_steps_um)))
focal_plane_index = []
focal_plane_z_um = np.zeros(len(t_steps_C))     # focal plane in data
O2_focal_plane_z_um = np.zeros(len(t_steps_C))  # calculated drift from O2
O3_focal_plane_z_um = np.zeros(len(t_steps_C))  # focal plane without O2 drift
for i, t in enumerate(t_steps_C):
    # Get data:
    date, filename, t1_C, t2_C, t1_O2_C, t2_O2_C = metadata_lines[i].split(',')
    t_actual_C[i] = (float(t1_C) + float(t2_C)) / 2
    t_actual_O2_C[i] = (float(t1_O2_C) + float(t2_O2_C)) / 2
    if data_cropped: # Overwrite filename to cropped data
        filename = 'data_cropped\\z_stack_%iC.tif'%t
    z_stack = imread(filename)
    for j in range(len(z_steps_um)):
        # Get image and normalize:
        image = z_stack[j,:,:]
        image = image / np.max(image)
        grad_mag = ggm(image, 2, mode='reflect')
        grad_mag_sum[i, j] = np.sum(grad_mag)
    # Normalize gradient magnitude to max:
    grad_mag_sum[i, :] = grad_mag_sum[i, :] / np.max(grad_mag_sum[i, :])
    # Find the index for max gradient magnitude sum:
    focal_plane_index.append(grad_mag_sum[i, :].argmax(axis=0))
    focal_plane_z_um[i] = z_steps_um[focal_plane_index[i]]
    # Remove focal plane drift from O2:
    # 1.58 -> github.com/amsikking/Nikon_40x0.95air_focus_vs_temperture
    O2_focal_plane_z_um[i] = 1.58 * (t_actual_O2_C[i] - t_actual_O2_C[0])
    # now add O2 drift for correct transformation:
    O3_focal_plane_z_um[i] = focal_plane_z_um[i] + O2_focal_plane_z_um[i]    
    print('temp=%0.2fC, focal plane index = %i (%0.2fum, O2=%0.2fum)'%(
        t_actual_C[i], focal_plane_index[i],
        focal_plane_z_um[i], O2_focal_plane_z_um[i]))

# Calculate focal plane shift from objective expansion and fit straight line:
focal_plane_shift_um = np.max(focal_plane_z_um) - focal_plane_z_um
O2_focal_plane_shift_um = O2_focal_plane_z_um
O3_focal_plane_shift_um = np.max(O3_focal_plane_z_um) - O3_focal_plane_z_um

def straight_line(x, m, c):
    return m*x + c
popt, pcov = curve_fit(straight_line, t_actual_C, O3_focal_plane_shift_um)

O3_fitted_focal_plane_shift_um = popt[0] * t_actual_C + popt[1]
O3_focal_plane_shift_umpC = popt[0]
O3_objective_length_mm = 108.15 # github.com/amsikking/AMS_AGY_v2_specifications
O3_CLTE_pK = O3_focal_plane_shift_umpC / (1e3 * O3_objective_length_mm)
print('O3_focal_plane_shift_umpC = %0.2f'%O3_focal_plane_shift_umpC)
print('O3_CLTE_pK = %0.3e'%O3_CLTE_pK)

# Plot:
import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2)
title = 'AMS-AGY_v2_focus_vs_temperature_data.png'
if data_cropped:
    title = 'AMS-AGY_v2_focus_vs_temperature_data_cropped.png'
fig.suptitle(title, fontsize=16)
# Top plot:
ax1.set_title('O2-O3 image sharpness vs image index \n (vs temperature)')
ax1.set_xlabel('image index')
ax1.set_ylabel('normalised gradient magnitude sum (a.u)')
for i, t in enumerate(t_actual_C):
    ax1.plot(range(len(z_steps_um)), grad_mag_sum[i, :], label='%0.1fC'%t)
ax1.legend(loc="upper left", ncol=2)
# Bottom plot:
ax2.set_title('O3 expansion = %0.2fum per C \n (O3_CLTE_pK=%0.3e)'%(
    popt[0], O3_CLTE_pK))
ax2.set_xlabel('temperature (C)')
ax2.set_ylabel('focal plane shift (um)')
ax2.plot(t_actual_C, focal_plane_shift_um, label='data (O2 + O3)')
ax2.plot(t_actual_C, O2_focal_plane_shift_um, label='O2 drift')
ax2.plot(t_actual_C, O3_focal_plane_shift_um, label='O3 expansion')
ax2.plot(t_actual_C, O3_fitted_focal_plane_shift_um, label='O3 linear fit')
ax2.legend(loc="upper left")
# Format, save and show:
fig.set_size_inches(8.5, 11)
plt.subplots_adjust(
    left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.3)
fig.savefig(title, dpi=150)
plt.show()
plt.close(fig)
