# AMS_AGY_v2_focus_vs_temperature
Data showing how the focal plane of an AMS-AGY v2 objective moves axially with temperature.

## Result:
The focal plane of an AMS-AGY v2 objective (54-18-9) moves axially with temperature at a linear rate of **~2.04um/degC**. The parfocal length (flange to image plane) is ~108.15mm, which gives a coefficient of linear thermal expansion (CLTE) of
**~18.9e-6/K**. For reference, typical values of CLTE are ~10-17 for stainless steel, ~18-19 for brass and 21-24 for aluminium (e-6/K).

![social_preview](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/blob/main/social_preview.png)

## Test setup:
See the numbered photos in the [photos](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/tree/main/photos) folder or click on the links below:

0) [**Overview:**](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/blob/main/photos/0_overview.jpg)
    - A minimal microscope was built on a full size optical table (305mm thick, Newport M-RS4000-46-12).
    - The microscope consisted of an objective 'O2' (Nikon MRD00405) mounted on a 100um range piezo (PI P-726.1CD), a tube lens (Thorlabs TTL200-A) and a camera (Thorlabs CS165MU1).
    - The optics were carefully aligned onto the same optical axis using an alignment laser, and the camera focus was set using a collimated beam into the tube lens (see 'alignment_laser.tif' for focus). The axial separation of the objective and tube lens was set with a ruler to ~170mm (within spec).
    - The O2 objective is coverslip corrected, so a small ~170um optical window was bonded to the front, and the correction collar was adjusted to 170um. This is an unusual thing to do to but is required for another setup, see [here](https://andrewgyork.github.io/high_na_single_objective_lightsheet/appendix.html#Parts_em_optical) for details on the optical window.
    - The AMS-AGY v2 objective 'O3' was aligned into the focal plane of the O2 microscope, so that the O2-O3 pair preserved beam direction and collimation. O3 was then slightly decentered so that the O2 microscope could image the ground glass edge of O3 to give a definitive focal plane.
    - O3 was mounted firmly: firstly into a thread adaptor (Thorlabs SM2A22), then into a short 2in lens tube (Thorlabs SM2L10) housed in a 2in flexure mount (Thorlabs SM2RC/M). The flexure mount was attached to a thermally isolating 25mm diameter fiberglass post (Thorlabs RS50G/M) and secured onto the optical table with a non bridging flexure clamp (Thorlabs POLARIS-CA25/M).
1) [**O3 heater and insulation:**](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/blob/main/photos/1_O3_heater_and_insulation.jpg) Heat tape with a built in thermister (Thorlabs TLK-H) was taped onto the body of the O3 and driven with a PID controller (Thorlabs TC200).
2) [**Insulated setup:**](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/blob/main/photos/2_insulated_setup.jpg) An insulated jacket fashioned out of thick foam (Uline S-13715) was secured to the O3 with lab tape. This helped reduce heat transfer to the air, which reduced equilibration time and thermal gradients.
3) [**Piezo_O2-O3 light:**](https://github.com/amsikking/AMS_AGY_v2_focus_vs_temperature/blob/main/photos/3_piezo_O2_O3_light.jpg) O2 was mounted into the 100um piezo, and the axial position of O3 was adjusted to be roughly in the focus of O2 with the piezo at 90um. This ensured that as O3 was heated (and expanded) that the piezo could retract towards 0um to find the new position of the focal plane. The 'TH1' temperature sensor was taped to O2 to track it's temperature and corresponding thermal expansion.

## Acquisition:
The data was collected programmatically (see '**acquisition.py**') in the following way:
- The temperature was set from 22C (just above room temp) to 42C in steps of 1C.
- A 30min settle time was given after each temperature set point to allow for thermal equilibration. This was proven adequate since an experimental run with a 3min settle time gave almost the same results.
- After waiting the settle time, a z stack of 400 images were acquired over the 100um piezo range with an axial separation of 0.25um (about 2x Nyquist sampling based on a depth of field of ~1um).
- The temperature from the thermistor on O3 (TLK-H) and the temperature of O2 (TH1) were recorded before and after each z stack.

## Data:
Both the full 'data' and 'data_cropped' were analyzed. Both gave the same results, but only the cropped data was included in the repository to save on storage and computation time. Cropping was performed according to 'data_cropped.py'.

**Note:** When inspecting the data manually, in addition to the obvious temperature induced focal plane drift, there is also a significant left right drift in the image. The left right axis on the camera corresponds to the vertical axis on the optical table, so this image motion is likely from the expansion of the fiberglass post and other mechanical elements holding the objective on the table.

## Analysis:
The data was analyzed programmatically (see '**analysis.py**') in the following way:
- At each temperature set point, the sum of the gradient magnitude of each normalized image in the z stack was calculated. The image with the highest gradient magnitude sum (i.e. the 'sharpest features') was then selected as the focal plane.
- The temperature used for analysis was the average of the measured before and after z stack temperatures (which measured to within 0.1C in all cases). The measured range was 21.7-39.4C for O3 and 20.7-21.8C for O2 (see data\metadata.txt).
- The focal plane position (um) was then plotted against the measured temperatures (C) to give the '**data (O2 + O3)**' plot.
- The temperature of the lab was not stable during the testing, introducing a unwanted focal plane drift (um) from O2. This was plotted against the measured temperatures (C) to give the '**O2 drift**' plot.
- The O2 drift was then removed from the data to give a linear trend for the '**O3 expansion**'.
- The linear trend was then fitted with a straight line '**O3 linear fit**' to give an accurate estimate of the axial shift of the focal plane with temperature and the associated coefficient of linear thermal expansion (CLTE).
- See the included figure '**AMS-AGY_v2_focus_vs_temperature_data.png**' for the end result.

To reproduce the analysis of the cropped data download the repository and run 'analysis.py'.

## Acknowledgments:
Inspired by, and with contributions from: [jlazzaridean](https://github.com/jlazzaridean) and [AndrewGYork](https://github.com/AndrewGYork).
