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
from PIL import Image

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

def coastline_plot(adm, exponent, minLat, maxLat, minLon, maxLon, invert_colors=False):
    """
    Draws the coastline from shapefile data onto a blank image at a given scale.
    """
    scale = 2**exponent
    height = abs(maxLat - minLat) * scale
    width = abs(maxLon - minLon) * scale
    if invert_colors:
        picture = np.ones((height, width, 3), np.uint8) * 255  # White background
        line_color = (0, 0, 0)  # Black lines
    else:
        picture = np.zeros((height, width, 3), np.uint8)  # Black background
        line_color = (255, 255, 255)  # White lines

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
                        cv2.line(picture, coords[i], coords[i - 1], line_color, 1)
                    i = i + 1
                # Close the polygon by connecting last to first
                cv2.line(picture, coords[i - 1], coords[0], line_color, 1)
    return picture

def mandelbrot_set(exponent, invert_colors=False, max_iter=50):
    """
    Draws the Mandelbrot set on a blank image.
    """
    scale = 2 ** (exponent + 5)  # Increase resolution for detail
    width, height = scale, scale
    if invert_colors:
        image = np.ones((height, width, 3), np.uint8) * 255
        color = (0, 0, 0)
    else:
        image = np.zeros((height, width, 3), np.uint8)
        color = (255, 255, 255)
    # Mandelbrot set bounds
    re_start, re_end = -2.0, 1.0
    im_start, im_end = -1.5, 1.5
    for x in range(width):
        for y in range(height):
            c = complex(re_start + (x / width) * (re_end - re_start),
                        im_start + (y / height) * (im_end - im_start))
            z = 0
            iter_count = 0
            while abs(z) <= 2 and iter_count < max_iter:
                z = z * z + c
                iter_count += 1
            if iter_count == max_iter:
                image[y, x] = color
    return image

def sierpinski_triangle(exponent, invert_colors=False):
    """
    Draws a Sierpinski triangle on a blank image.
    """
    scale = 2 ** exponent
    size = 2 ** (exponent + 4)  # Ensures enough resolution for detail
    if invert_colors:
        image = np.ones((size, size, 3), np.uint8) * 255
        color = (0, 0, 0)
    else:
        image = np.zeros((size, size, 3), np.uint8)
        color = (255, 255, 255)

    def draw_triangle(img, top, left, right, depth):
        if depth == 0:
            pts = np.array([top, left, right], np.int32)
            cv2.fillPoly(img, [pts], color)
        else:
            mid_left = ((top[0]+left[0])//2, (top[1]+left[1])//2)
            mid_right = ((top[0]+right[0])//2, (top[1]+right[1])//2)
            mid_base = ((left[0]+right[0])//2, (left[1]+right[1])//2)
            draw_triangle(img, top, mid_left, mid_right, depth-1)
            draw_triangle(img, mid_left, left, mid_base, depth-1)
            draw_triangle(img, mid_right, mid_base, right, depth-1)

    # Triangle vertices
    top = (size//2, 0)
    left = (0, size-1)
    right = (size-1, size-1)
    max_depth = exponent + 2  # Controls recursion depth/detail
    draw_triangle(image, top, left, right, max_depth)
    return image

def circle(radius, exponent, invert_colors=False):
    """
    Draws a circle (outline only) on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    center_coordinates = (5 * scale, 5 * scale)
    if invert_colors:
        picture = np.ones((height, width, 3), np.uint8) * 255
        color = (0, 0, 0)
    else:
        picture = np.zeros((height, width, 3), np.uint8)
        color = (255, 255, 255)
    thickness = 1
    cv2.circle(picture, center_coordinates, radius * scale, color, thickness)
    return picture

def disk(radius, exponent, invert_colors=False):
    """
    Draws a filled disk (circle) on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    center_coordinates = (5 * scale, 5 * scale)
    if invert_colors:
        picture = np.ones((height, width, 3), np.uint8) * 255
        color = (0, 0, 0)
    else:
        picture = np.zeros((height, width, 3), np.uint8)
        color = (255, 255, 255)
    thickness = -1  # Filled circle
    cv2.circle(picture, center_coordinates, radius * scale, color, thickness)
    return picture

def line(exponent, invert_colors=False):
    """
    Draws a diagonal line on a blank image.
    """
    scale = 2**exponent
    height = 10 * scale
    width = 10 * scale
    start_coordinates = (2 * scale, 2 * scale)
    end_coordinates = (8 * scale, 8 * scale)
    if invert_colors:
        picture = np.ones((height, width, 3), np.uint8) * 255
        color = (0, 0, 0)
    else:
        picture = np.zeros((height, width, 3), np.uint8)
        color = (255, 255, 255)
    thickness = 1
    cv2.line(picture, start_coordinates, end_coordinates, color, thickness)
    return picture

# Main loop: Try different scales (exponents) to estimate fractal dimension
invert_colors = True  # Set to True for black-on-white, False for white-on-black
frames = []
for exponent in range(0, 12):
    exponents.append(exponent)
    # Uncomment one of the following to choose the shape to analyze
    # image = coastline_plot(adm, exponent, 49, 62, -9, 2, invert_colors)  # Great Britain
    # image = coastline_plot(adm, exponent, 15, 60, 70, 137, invert_colors)  # China
    # image = circle(3, exponent, invert_colors)  # Circle (outline)
    # image = disk(3, exponent, invert_colors)    # Filled disk
    # image = line(exponent, invert_colors)       # Diagonal line
    image = sierpinski_triangle(exponent, invert_colors)  # Sierpinski triangle
    # image = mandelbrot_set(exponent, invert_colors)  # Mandelbrot set

    if invert_colors:
        boxes_counted.append(np.sum(np.all(image == [0, 0, 0], axis=2)))
    else:
        boxes_counted.append(np.sum(np.all(image == [255, 255, 255], axis=2)))

    frames.append((image.copy(), exponent, boxes_counted[-1]))

    # im = Image.fromarray(image)
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
if len(frames) > 1:
    import matplotlib.animation as animation
    fig, ax = plt.subplots(figsize=(6, 6))
    def update(frame):
        ax.clear()
        img, exponent, count = frame
        ax.imshow(img)
        ax.set_title(f"Box Scale: 2^{exponent}\n Total boxes counted: {count}")
        ax.axis('off')
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=600, blit=False, repeat=True)
    ani.save("fractal_series.gif", writer='pillow', fps=2)
    plt.close(fig)
    print("Saved GIF as fractal_series.gif")
print("\nNote: To switch between black-on-white and white-on-black images, set invert_colors = True or False at the top of the main loop.")