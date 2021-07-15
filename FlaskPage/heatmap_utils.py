"""
This file constructs a heatmap using Folium to be displayed on the Flask site. The weather data is shown as a heatmap, with hardcoded color values.
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import branca
from scipy.ndimage import gaussian_filter
import geojsoncontour
import numpy as np
import folium
import matplotlib as mpl
from matplotlib.figure import Figure

# Geospatial coordinate declarations
# Longitude
xcords = (-125, -60)
HORZ_DIMS = 175
# Latitude
ycords = (25, 50)
VERT_DIMS = 100
# generate lists of sample points
lat_vals = np.arange(ycords[0], ycords[1], (ycords[1] - ycords[0]) / VERT_DIMS)
long_vals = np.arange(xcords[0], xcords[1],
                      (xcords[1] - xcords[0]) / HORZ_DIMS)

# load pickled mask arrays
filter_data_mask = np.empty(shape=(VERT_DIMS, HORZ_DIMS))
with open('static/no_stations_mask.npy', 'rb') as filename:
    filter_data_mask = np.load(filename)


# function to generate three 1D lists of weather data: lat, long, and temps
def display_format(data_line):
    # three empty 1D lists
    long = np.empty(shape=(HORZ_DIMS * VERT_DIMS))
    lat = np.empty(shape=(HORZ_DIMS * VERT_DIMS))
    temps = np.empty(shape=(HORZ_DIMS * VERT_DIMS))
    # assign values to list (lat, long, and temp)
    count = 0
    for lats in lat_vals:
        for lons in long_vals:
            long[count] = lons
            lat[count] = lats
            temps[count] = (data_line[count])
            count += 1
    # return collected values
    return long, lat, temps


# function to generate folium map with heatmap layer, takes in 1D lists of: long, lat, temps
def gen_folium_map(longitude, latitude, data_line, zoomstart=4, startcords=(39.8, -98.6), mapheight='100%'):
    # Setup colormap
    colors = ['#26195e', '#024c7a', '#185110',
              '#abdda4', '#F2F29E', '#eac5a1', '#cc7475']
    vmin = -20
    vmax = 120
    levels = [-20 + 20 * x for x in range(len(colors))]
    color_map = branca.colormap.LinearColormap(
        colors, vmin=vmin, vmax=vmax).to_step(len(colors))
    color_map.caption = 'Temperature (°F)'
    # make meshes of longitude and latitude values (100,175)
    longmesh, latmesh = np.meshgrid(long_vals, lat_vals)
    # make initial folium map
    folium_map = folium.Map(
        location=startcords,
        zoom_start=zoomstart,
        height=mapheight,
        tiles='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png',
        scrollWheelZoom=False,
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )
    # var Esri_WorldTopoMap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    # attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
    # });
    # generate temperature mesh to match latitude and longitude meshes
    temp_mesh = np.reshape(data_line, newshape=(VERT_DIMS, HORZ_DIMS))
    # gaussian filter to smooth out data
    temp_mesh = gaussian_filter(temp_mesh * filter_data_mask, sigma=2)
    temp_mesh /= gaussian_filter(filter_data_mask, sigma=2)
    temp_mesh[np.logical_not(filter_data_mask)] = np.nan
    # generate matplotlib contour plot from lat, long, and temp meshes
    fig = Figure()
    ax = fig.add_subplot(111)
    temp_contour = ax.contourf(
        longmesh,
        latmesh,
        temp_mesh,
        levels=levels,
        alpha=0.7,
        linestyles='None',
        vmin=vmin, vmax=vmax,
        colors=colors
    )
    # generate geojson data from contour plot
    temp_geojson = geojsoncontour.contourf_to_geojson(
        contourf=temp_contour,
        min_angle_deg=3.0,
        ndigits=5,
        stroke_width=1,
        fill_opacity=0.5
    )
    # generate folium chloropleth and add to previously created map
    folium.GeoJson(
        temp_geojson,
        style_function=lambda x: {
            'color':        x['properties']['stroke'],
            'weight':       x['properties']['stroke-width'],
            'fillColor':    x['properties']['fill'],
            'opacity':      0.6
        }).add_to(folium_map)
    # Combine folium and color map
    folium_map.add_child(color_map)
    # return map
    return folium_map
