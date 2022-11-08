#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 13:33:20 2021

@author: alfimuhamad
"""
from osgeo import gdal, osr
#import affine
import numpy as np
import math




def latMinSec(lat, latmin, latsec, long, longmin, longsec):
    lat += latmin / 60
    lat += latsec / 3600
    
    long += longmin / 60
    long += longsec / 3600
    
    return lat, long

"""
def coordToPix(geo_coord, data_source):
    
    x, y = geo_coord[0], geo_coord[1]
    forward_transform =  \
        affine.Affine.from_gdal(*data_source.GetGeoTransform())
    reverse_transform = ~forward_transform
    px, py = reverse_transform * (x, y)
    px, py = int(px + 0.5), int(py + 0.5)
    pixel_coord = px, py
    data_array = np.array(data_source.GetRasterBand(1).ReadAsArray())
    return data_array[pixel_coord[0]][pixel_coord[1]]
"""


dataset= gdal.Open("delco100.tif")
gt = dataset.GetGeoTransform()
proj= dataset.GetProjection()



print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
                            dataset.GetDriver().LongName))
print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                    dataset.RasterYSize,
                                    dataset.RasterCount))
print("Projection is {}".format(dataset.GetProjection()))
geotransform = dataset.GetGeoTransform()
if geotransform:
    print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
    print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    

old_cs = osr.SpatialReference()
old_cs.ImportFromWkt(dataset.GetProjectionRef())    

wgs84_wkt = """
GEOGCS["WGS 84",
    DATUM["WGS_1984",
        SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0,
        AUTHORITY["EPSG","8901"]],
    UNIT["degree",0.01745329251994328,
        AUTHORITY["EPSG","9122"]],
    AUTHORITY["EPSG","4326"]]"""
new_cs = osr.SpatialReference()
new_cs.ImportFromWkt(wgs84_wkt)


transform = osr.CoordinateTransformation(old_cs,new_cs)

width = dataset.RasterXSize
height = dataset.RasterYSize

minx = geotransform[0]
miny = geotransform[3] + width*geotransform[4] + height * geotransform[5]

latlong = transform.TransformPoint(minx,miny)


inverter = osr.CoordinateTransformation(new_cs, old_cs)

def ll2xy(inverter, geotransform, lat, long):
    remap = inverter.TransformPoint(lat, long)
    xPix = (remap[0] - geotransform[0]) / geotransform[1]
    yPix = (remap[1] - geotransform[3]) / geotransform[5]
    return xPix,yPix












