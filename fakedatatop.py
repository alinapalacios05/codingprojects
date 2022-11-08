//import numpy as np

//def genFake()
from osgeo import gdal
import numpy as np
 coordinate-points
#long, lat to pixels
#use data set (has built in)
def genFake()
=======
#import cupy as cp
import matplotlib.pyplot as plt
#def coordToPix(rasterArr, latCoord, longCoord):
def geoDat(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
    
    min =band.GetMinimum()
    max = band.GetMaximum()
    if not min or not max:
        (min,max) = band.ComputeRasterMinMax(True)
    print("Min={:.3f}, Max={:.3f}".format(min,max))
    
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                    dataset.RasterYSize,
                                    dataset.RasterCount))
    print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    return geotransform

def coordToPix(rasterArr, dataset):
    longCoord = 39.907
    latCoord = 75.3879
    

    xP = (longCoord * dataset.RasterXSize)/360
    yP = (latCoord * dataset.RasterYSize)/180
    #return xP, yP
    print(xP)
    print(yP)

def main():
    coordToPix(rasterArr)
