import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Set global font size
plt.rcParams['font.family'] = 'Helvetica'
plt.rcParams.update({'font.size': 17})

# File name
file_name = '../NGC7538_CII_merged_PCA.fits'

try:
    # Open the FITS file
    with fits.open(file_name) as hdul:
        data = hdul[0].data
        header = hdul[0].header

        # Get the World Coordinate System (WCS) information
        wcs = WCS(header)

        # Print some basic information about the cube
        print(f"Data shape: {data.shape}")
        print(f"Dimensions: {wcs.naxis}")
        print(f"Coordinate types: {wcs.axis_type_names}")

        # Assume the cube shape is (velocity, declination, right ascension)
        v, y, x = data.shape

        # Calculate the moment 0 map by integrating along the velocity axis
        moment0_map = np.sum(data, axis=0)

        # Create PV diagrams for each vertical cut
        for i in range(x):
            # Extract the slice
            pv_slice = data[:, :, i]
            
            # Create the plot
            fig = plt.figure(figsize=(20.5, 8))
            gs = gridspec.GridSpec(1, 2)

            # Plot the moment 0 map
            ax0 = plt.subplot(gs[0], projection=wcs.celestial)
            im0 = ax0.imshow(moment0_map, origin='lower', cmap='viridis', vmin=0, vmax=1000)
            ax0.axvline(x=i, color='red', linestyle='--', linewidth=2)
            ax0.set_xlabel('Right Ascension')
            ax0.set_ylabel('Declination')
            ax0.set_title('NGC 7538 Moment 0 Map - Red Crosscut')
            plt.colorbar(im0, ax=ax0, pad=0.0)

            # Plot the PV diagram
            ax1 = plt.subplot(gs[1])
            im1 = ax1.imshow(pv_slice, aspect='auto', origin='lower', cmap='viridis', vmin=0, vmax=10)
            plt.colorbar(im1, ax=ax1, label='Intensity', pad=0)
            ax1.set_xlabel('Declination')
            ax1.set_ylabel('Velocity')
            ax1.set_title(f'CII - PV Diagram - Vertical Cut {i}')
            
            # Save the combined figure
            plt.savefig(f'NGC7538_CII_pv_diagram_with_moment0_{i:03d}.png', dpi=300, bbox_inches='tight')
            plt.close()

        print(f"Created {x} PV diagrams with moment 0 maps.")

except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")



import cv2
import os
from natsort import natsorted

# Path to the directory containing the PNG images
image_directory = '.'

# Get list of all files in the directory
file_list = os.listdir(image_directory)

# Sort files naturally to ensure they are in the correct order
file_list = natsorted(file_list)

# Filter out only PNG files
image_files = [f for f in file_list if f.endswith('.png')]

# Check if there are any images in the directory
if not image_files:
    raise ValueError("No PNG images found in the specified directory.")

# Read the first image to get the size
first_image_path = os.path.join(image_directory, image_files[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape

# Define the codec and create VideoWriter object
video_name = 'NGC7538_VerticalPVDiagram.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 10, (width, height))

# Loop through all images and write them to the video
for image_file in image_files:
    image_path = os.path.join(image_directory, image_file)
    frame = cv2.imread(image_path)
    video.write(frame)

# Release the video writer
video.release()

print("Video created successfully.")
