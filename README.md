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
# Fractals

Repository for dimensionality calculations using box-counting methods.

## Overview

This project estimates the fractal dimension of various shapes (such as country coastlines, circles, disks, Sierpinski triangle, Mandelbrot set, and lines) by drawing them at different scales and counting the number of boxes (pixels) needed to cover the shape. The main script uses shapefiles for real-world boundaries and OpenCV for drawing. Animated plots are saved as GIFs using matplotlib.

## Features

- Calculate fractal dimension for:
  - Country coastlines (using shapefiles)
  - Circles (outline and filled)
  - Diagonal lines
  - Sierpinski triangle
  - Mandelbrot set
- Visualize the scaling and box-counting process
- Plot results and estimated fractal dimension
- Save animated plots as GIFs with titles using matplotlib

## Requirements

- Python 3.x
- numpy
- matplotlib
- opencv-python
- geopandas
- fiona
- gadm (for downloading GADM shapefiles)

Install dependencies with:
```sh
pip install numpy matplotlib opencv-python geopandas fiona gadm
```

**You must also determine the latitude and longitude boundaries for your shape of interest.**  
These boundaries are required as input to the script to correctly scale and draw the shape. You can find them by inspecting your shapefile using GIS software or a Python script with GeoPandas.

## Usage

1. Place your shapefiles in the `shp files` directory.
2. Find and set the latitude and longitude boundaries for your shape.
3. Edit `Dimensionality_calc.py` to select the shape you want to analyze (uncomment the relevant line in the main loop).
4. Run the script:
   ```sh
   python Dimensionality_calc.py
   ```
5. View the plots and the estimated fractal dimension in the output.
6. The animated GIF of the plots will be saved as `fractal_series.gif` in your project folder.

## Example

To analyze the coastline of China, ensure the China shapefile is present and uncomment this line in the script:
```python
image = coastline_plot(adm, exponent, 15, 60, 70, 137)  # China
```
Here, `15, 60, 70, 137` are the latitude and longitude boundaries.

To generate a GIF of the Mandelbrot set or Sierpinski triangle, uncomment the corresponding line in the main loop.

## Notes

- The script expects shapefiles to be in the `shp files` folder.
- You can use the `gadm` downloader (see commented code) to fetch new country boundaries.
- For best results, ensure all required shapefile components (`.shp`, `.shx`, `.dbf`, `.prj`) are present.
- You must determine the latitude and longitude boundaries for your shape and enter them in the function call.
- The GIF is created using matplotlib's animation module and includes plot titles for each frame.

## License

MIT License

