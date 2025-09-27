# Fractals

Repository for dimensionality calculations using box-counting methods.

## Overview

This project estimates the fractal dimension of various shapes (such as country coastlines, circles, disks, and lines) by drawing them at different scales and counting the number of boxes (pixels) needed to cover the shape. The main script uses shapefiles for real-world boundaries and OpenCV for drawing.

## Features

- Calculate fractal dimension for:
  - Country coastlines (using shapefiles)
  - Circles (outline and filled)
  - Diagonal lines
- Visualize the scaling and box-counting process
- Plot results and estimated fractal dimension

## Requirements

- Python 3.x
- numpy
- matplotlib
- opencv-python
- geopandas
- fiona
- gadm (for downloading GADM shapefiles)
- Pillow

Install dependencies with:
```sh
pip install numpy matplotlib opencv-python geopandas fiona gadm Pillow
```

## Usage

1. Place your shapefiles in the `shp files` directory.
2. Open `Dimensionality_calc.py` in your editor.
3. To select which shape to analyze, **uncomment** the relevant line in the main loop section:
    - For a coastline (e.g., China or Great Britain), uncomment the line starting with `image = coastline_plot(...)`.
    - For a circle outline, uncomment `image = circle(...)`.
    - For a filled disk, uncomment `image = disk(...)`.
    - For a diagonal line, uncomment `image = line(...)`.
4. Make sure only one shape line is uncommented at a time.
5. Run the script:
   ```sh
   python Dimensionality_calc.py
   ```
6. View the plots and the estimated fractal dimension in the output.

## Example

To analyze the coastline of China, ensure the China shapefile is present and uncomment this line in the script:
```python
image = coastline_plot(adm, exponent, 15, 60, 70, 137)  # China
```
To analyze a circle outline, uncomment:
```python
image = circle(3, exponent)
```
**Only one of these lines should be active at a time.**

## Notes

- The script expects shapefiles to be in the `shp files` folder.
- You can use the `gadm` downloader (see commented code) to fetch new country boundaries.
- For best results, ensure all required shapefile components (`.shp`, `.shx`, `.dbf`, `.prj`) are present.
- You must determine the latitude and longitude boundaries for your shape and enter them in the function call.

## License

MIT License

