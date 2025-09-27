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

#downloader = GADMDownloader(version = "4.0")

#country_name = "Vietnam"
#ad_level = 0
#gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)

#assert isinstance(gdf, gpd.GeoDataFrame)
#gdf.plot()
#

import os#code to find relative path

script_dir = os.path.dirname(os.path.abspath(__file__))

# shapefile_path = os.path.join(script_dir, "shp files", "gadm36_GBR_0.shp")
# adm = fiona.open(shapefile_path)

shapefile_path = os.path.join(script_dir, "shp files", "gadm36_CHN_0.shp")
adm = fiona.open(shapefile_path)



exponents = []
boxes_counted = []

def coastline_plot(adm, exponent, minLat, maxLat, minLon, maxLon):
    scale = 2**exponent
    height = abs(maxLat-minLat)*scale
    width = abs(maxLon-minLon)*scale
    picture = np.zeros((height,width,3), np.uint8)
    for feature in adm:
        geom = feature["geometry"] 
        #geom["type"] should be MultiPolygon
        for polygon in geom["coordinates"]:
            for ring in polygon:
                #x = []
                #y = []
                coords = []
                i = 0
                for coordinate in ring:
                    #print(coordinate[0], coordinate[1])
                    #x.append(coordinate[0])
                    #y.append(coordinate[1])
                    coords.append([int(coordinate[0]*scale)-minLon*scale, -int(coordinate[1]*scale)+maxLat*scale])
                    #print(coords)
                    if i>0:
                        cv2.line(picture, coords[i], coords[i-1], (255, 255, 255), 1)
                    i = i + 1
                cv2.line(picture, coords[i-1],coords[0],(255,255,255),1)
    return picture

def circle(radius, exponent):
    scale = 2**exponent
    height = 10*scale
    width = 10*scale
    
    center_coordinates = (5*scale,5*scale)
    color = (255,255,255)
    thickness = 1
    
    picture = np.zeros((height,width,3), np.uint8)
    cv2.circle(picture, center_coordinates, radius*scale, color, thickness)
    return picture

def disk(radius, exponent):
    scale = 2**exponent
    height = 10*scale
    width = 10*scale
    
    center_coordinates = (5*scale,5*scale)
    color = (255,255,255)
    thickness = -1 
    
    picture = np.zeros((height,width,3), np.uint8)
    cv2.circle(picture, center_coordinates, radius*scale, color, thickness)
    return picture

def line(exponent):
    scale = 2**exponent
    height = 10*scale
    width = 10*scale
    
    start_coordinates = (2*scale,2*scale)
    end_coordinates = (8*scale,8*scale)
    color = (255,255,255)
    thickness = 1
    
    picture = np.zeros((height,width,3), np.uint8)
    cv2.line(picture, start_coordinates, end_coordinates, color, thickness)
    return picture

for exponent in range(0,7):#increases the size of the image and/or decreases the size of the pixels by 2x
    exponents.append(exponent)#too lazy to do smth else
    #image = coastline_plot(adm,exponent,49,62,-9,2)#great britain graph
    #image = coastline_plot(adm,exponent,15,60,70,137)#china graph 
    image = circle(3,exponent)#circle with radius 3, does not include interior
    #image = disk(3,exponent)#disk with radius 3, including interior
    #image = line(exponent)
    
    
    values, counts = np.unique(image, return_counts = True)
    #print(counts)
    #counting the numebr of white pixels = 1/3 of the 255 values
    boxes_counted.append(int(counts[1]/3))
    
    plt.imshow(image)
    plt.title("Exponent: " + str(exponent) + "\n Total boxes counted: " + str(int(counts[1]/2)))
    plt.axis('off')
    plt.show()
    #im = Image.fromarray(picture)
    #im.show()
    
#p.zeros()
#img = Image.fromarray(x,y)
#img.show()
t = np.arange(0., 10., 0.01)

slope, intercept = np.polyfit(exponents, np.log2(boxes_counted),1)

plt.plot(t,2**(t*slope+intercept), c = "red", label = "Boxes counted(predicted) Equation: " + "\n" + str(round(2**intercept, 3)) + "*2^(" + str(round(slope,3)) + "t)")#predicted vs actual, off by a constant

plt.scatter(exponents, boxes_counted, c = "blue", label = "Boxes counted(actual)")
plt.title("Total boxes counted vs. Exponent")
plt.xlabel("Exponent")
plt.ylabel("Boxes counted")
plt.legend()
plt.show()

plt.scatter(exponents, np.log2(boxes_counted), c = "blue", label = "Log2 of Boxes counted(actual)" + "\n" + str(round(slope,3)) + "t + " + str(round(intercept,3)))
plt.title("Log graph of total boxes counted vs Exponent")
plt.xlabel("Exponent")#its base two because then the logs match and the slope matches exactly
plt.ylabel("Log2 of boxes counted")
plt.plot(t,t*slope + intercept, c = "red", label = "Log2 of boxes counted(predicted)")#predicted
plt.legend()
plt.show()

print("Dimensionality found: " + str(slope))
#plt.scatter(x,y)
#plt.show

#shapefile = gpd.read_file()