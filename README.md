
# FITS File Processing and PV Diagrams Generation

This project processes a FITS file containing spectral data, generates moment 0 maps and Position-Velocity (PV) diagrams, and combines these diagrams into a video.

## Steps

### 1. Import Required Libraries
```python
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cv2
import os
from natsort import natsorted
```
Import necessary libraries for data handling, visualization, and video creation.

### 2. Set Global Plot Settings
```python
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams.update({'font.size': 17})
```
Configure global settings for plots, such as font family and size.

### 3. Define the File Name
```python
file_name = '../NGC7538_CII_merged_PCA.fits'
```
Specify the path to the FITS file to be processed.

### 4. Open the FITS File
```python
with fits.open(file_name) as hdul:
    data = hdul[0].data
    header = hdul[0].header

    # Get the World Coordinate System (WCS) information
    wcs = WCS(header)

    # Print some basic information about the cube
    print(f"Data shape: {data.shape}")
    print(f"Dimensions: {wcs.naxis}")
    print(f"Coordinate types: {wcs.axis_type_names}")
```
Open the FITS file, read its data and header, and extract WCS information. Print basic details about the data.

### 5. Calculate the Moment 0 Map
```python
v, y, x = data.shape
moment0_map = np.sum(data, axis=0)
```
Assuming the cube shape is (velocity, declination, right ascension), calculate the moment 0 map by integrating along the velocity axis.

### 6. Create PV Diagrams
```python
for i in range(x):
    pv_slice = data[:, :, i]
    
    fig = plt.figure(figsize=(20.5, 8))
    gs = gridspec.GridSpec(1, 2)

    ax0 = plt.subplot(gs[0], projection=wcs.celestial)
    im0 = ax0.imshow(moment0_map, origin='lower', cmap='viridis', vmin=0, vmax=1000)
    ax0.axvline(x=i, color='red', linestyle='--', linewidth=2)
    ax0.set_xlabel('Right Ascension')
    ax0.set_ylabel('Declination')
    ax0.set_title('NGC 7538 Moment 0 Map - Red Crosscut')
    plt.colorbar(im0, ax=ax0, pad=0.0)

    ax1 = plt.subplot(gs[1])
    im1 = ax1.imshow(pv_slice, aspect='auto', origin='lower', cmap='viridis', vmin=0, vmax=10)
    plt.colorbar(im1, ax=ax1, label='Intensity', pad=0)
    ax1.set_xlabel('Declination')
    ax1.set_ylabel('Velocity')
    ax1.set_title(f'CII - PV Diagram - Vertical Cut {i}')
    
    plt.savefig(f'NGC7538_CII_pv_diagram_with_moment0_{i:03d}.png', dpi=300, bbox_inches='tight')
    plt.close()

print(f"Created {x} PV diagrams with moment 0 maps.")
```
For each vertical slice in the data cube, create a PV diagram and overlay it on the moment 0 map. Save each combined figure as a PNG file.

One of the PV diagrams:

![NGC7538_CII_pv_diagram_with_moment0_140](https://github.com/umitkavak/PvDiagramMovieFromaDataCube/assets/26542534/826d5854-8f7c-450c-b2c7-16133333cd27)



### 7. Handle Errors
```python
except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```
Catch and handle potential errors, such as file not found or other exceptions.

### 8. Create a Video from PNG Images
```python
image_directory = '.'
file_list = os.listdir(image_directory)
file_list = natsorted(file_list)
image_files = [f for f in file_list if f.endswith('.png')]

if not image_files:
    raise ValueError("No PNG images found in the specified directory.")

first_image_path = os.path.join(image_directory, image_files[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape

video_name = 'NGC7538_VerticalPVDiagram.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 10, (width, height))

for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    frame = cv2.imread(image_path)
    video.write(frame)

video.release()
print("Video created successfully.")
```
Read all generated PNG images, sort them, and combine them into an MP4 video using OpenCV.
