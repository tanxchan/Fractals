# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 08:59:08 2023

@author: 1304t
"""

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from gadm import GADMDownloader
import fiona
from PIL import *

# downloader = GADMDownloader(version = "4.0")
# Example code for downloading GADM data

# country_name = "Vietnam"
# ad_level = 0
# gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)
# assert isinstance(gdf, gpd.GeoDataFrame)
# gdf.plot()

import os  # For finding relative path

script_dir = os.path.dirname(os.path.abspath(__file__))

# Example for Great Britain shapefile (commented out)
# shapefile_path = os.path.join(script_dir, "shp files", "gadm36_GBR_0.shp")
# adm = fiona.open(shapefile_path)

# Path to China shapefile
shapefile_path = os.path.join(script_dir, "shp files", "gadm36_CHN_0.shp")
adm = fiona.open(shapefile_path)

exponents = []        # List to store exponents (scaling factors)
boxes_counted = []    # List to store number of boxes counted at each scale

def coastline_plot(adm, exponent, minLat, maxLat, minLon, maxLon):
    """
    Draws the coastline from shapefile data onto a blank image at a given scale.
    """
    scale = 2**exponent
    height = abs(maxLat - minLat) * scale
    width = abs(maxLon - minLon) * scale
    picture = np.zeros((height, width, 3), np.uint8)  # Create blank image

    for feature in adm:
        geom = feature["geometry"]
        # geom["type"] should be MultiPolygon
        for polygon in geom["coordinates"]:
            for ring in polygon:
                coords = []
                i = 0
                for coordinate in ring:
                    # Convert lat/lon to pixel coordinates
                    coords.append([int(coordinate[0] * scale) - minLon * scale, -int(coordinate[1] * scale) + maxLat * scale])
                    if i > 0:
                        # Draw line between consecutive points
                        cv2.line(picture, coords[i], coords[i - 1], (255, 255, 255), 1)
                    i = i + 1
                # Close the polygon by connecting last to first
                cv2.line(picture, coords[i - 1], coords[0], (255, 255, 255), 1)
    return picture

def circle(radius, exponent):
    """
    Draws a circle (outline only) on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    center_coordinates = (5 * scale, 5 * scale)
    color = (255, 255, 255)
    thickness = 1
    picture = np.zeros((height, width, 3), np.uint8)
    cv2.circle(picture, center_coordinates, radius * scale, color, thickness)
    return picture

def disk(radius, exponent):
    """
    Draws a filled disk (circle) on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    center_coordinates = (5 * scale, 5 * scale)
    color = (255, 255, 255)
    thickness = -1  # Filled circle
    picture = np.zeros((height, width, 3), np.uint8)
    cv2.circle(picture, center_coordinates, radius * scale, color, thickness)
    return picture

def line(exponent):
    """
    Draws a diagonal line on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    start_coordinates = (2 * scale, 2 * scale)
    end_coordinates = (8 * scale, 8 * scale)
    color = (255, 255, 255)
    thickness = 1
    picture = np.zeros((height, width, 3), np.uint8)
    cv2.line(picture, start_coordinates, end_coordinates, color, thickness)
    return picture

# Main loop: Try different scales (exponents) to estimate fractal dimension
for exponent in range(0, 9):  # Increases image size/decreases pixel size by 2x each time
    exponents.append(exponent)
    
    #uncomment one of the following to choose the shape to analyze
    #selection should match the shapefile loaded above

    # image = coastline_plot(adm, exponent, 49, 62, -9, 2)  # Great Britain
    image = coastline_plot(adm, exponent, 15, 60, 70, 137)  # China
    # image = circle(3, exponent)  # Circle (outline)
    # image = disk(3, exponent)    # Filled disk
    # image = line(exponent)       # Diagonal line

    values, counts = np.unique(image, return_counts=True)
    # Count the number of white pixels (255 values)
    boxes_counted.append(int(counts[1] / 3))  # Each white pixel has 3 channels (RGB), so divide by 3

    plt.imshow(image)
    plt.title("Exponent: " + str(exponent) + "\n Total boxes counted: " + str(int(counts[1] / 2)))
    plt.axis('off')
    plt.show()
    # im = Image.fromarray(picture)
    # im.show()

# Fit a line to log2(boxes_counted) vs exponent to estimate fractal dimension
t = np.arange(0., 10., 0.01)

slope, intercept = np.polyfit(exponents, np.log2(boxes_counted), 1)

plt.plot(
    t,
    2 ** (t * slope + intercept),
    c="red",
    label="Boxes counted(predicted) Equation: "
    + "\n"
    + str(round(2 ** intercept, 3))
    + "*2^("
    + str(round(slope, 3))
    + "t)",
)  # Predicted

plt.scatter(exponents, boxes_counted, c="blue", label="Boxes counted(actual)")
plt.title("Total boxes counted vs. Exponent")
plt.xlabel("Exponent")
plt.ylabel("Boxes counted")
plt.legend()
plt.show()

plt.scatter(
    exponents,
    np.log2(boxes_counted),
    c="blue",
    label="Log2 of Boxes counted(actual)"
    + "\n"
    + str(round(slope, 3))
    + "t + "
    + str(round(intercept, 3)),
)
plt.title("Log graph of total boxes counted vs Exponent")
plt.xlabel("Exponent")  # Base 2 so slope matches dimension
plt.ylabel("Log2 of boxes counted")
plt.plot(
    t, t * slope + intercept, c="red", label="Log2 of boxes counted(predicted)"
)  # Predicted
plt.legend()
plt.show()

print("Dimensionality found: " + str(slope))  # Estimated fractal dimension