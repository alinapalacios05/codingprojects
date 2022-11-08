# -*- coding: utf-8 -*-
"""clear
@author: drane
"""
from osgeo import gdal
import numpy as np
import math
import cupy as cp
import matplotlib.pyplot as plt
import imageio

#prints min/max elevation from dataset, will add geotagging stuff here
def geoDat(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    band = dataset.GetRasterBand(1)
    print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
    
    min = band.GetMinimum()
    max = band.GetMaximum()
    if not min or not max:
        (min,max) = band.ComputeRasterMinMax(True)
    print("Min={:.3f}, Max={:.3f}".format(min,max))
    
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                    dataset.RasterYSize,
                                    dataset.RasterCount))
    #print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    return geotransform

def latMinSec(lat, latmin, latsec, long, longmin, longsec):
    lat += latmin / 60
    lat += latsec / 3600
    
    long += longmin / 60
    long += longsec / 3600
    
    return lat, long


def coordToPix(latitude, longitude, mapWidth, mapHeight):
    FE = 180 #false easting
    radius = mapWidth / (2 * math.pi)


    latRad = math.radians(latitude)
    lonRad = math.radians(longitude + FE)
    
    x = lonRad * radius

    yFromEquator = radius * math.log(math.tan(math.pi / 4 + latRad / 2))
    y = mapHeight / 2 - yFromEquator

    return (x, y)
    


#reads in data into raster/pixel format
def genElvmap(filename):
    dataset = gdal.Open(filename, gdal.GA_ReadOnly)
    rasterArr = dataset.ReadAsArray()

    for i in range(len(rasterArr)):
        for j in range(len(rasterArr[i])):
            if rasterArr[i][j] <0:
                rasterArr[i][j] = None
    
    return rasterArr 

    
Grid_space = 100    

filename = "delco100.tif"

#flDir:
#1: down
#2: right
#3: up
#4: left
#5: pool

#basic flow direction method, will likely need improvement
#picks cardinal direction that gradient points closest towards as flow direction
#iterates over each cell in array
def flowDir(elvImg):
    gradV, gradH = np.gradient(elvImg, Grid_space)
    flDir = np.empty([len(elvImg), len(elvImg[0])], dtype=np.ubyte)
    for i in range(1,len(elvImg)-1):
        for j in range(1,len(elvImg[0])-1):
            #if elvImg[i][j] != None:
            if not math.isnan(elvImg[i][j]):
                upCell = elvImg[i-1][j] > elvImg[i][j]
                rightCell = elvImg[i][j+1] > elvImg[i][j]
                downCell = elvImg[i+1][j] > elvImg[i][j]
                leftCell = elvImg[i][j-1] > elvImg[i][j]
                
                if upCell and rightCell and downCell and leftCell:
                    flDir[i][j] = 5
                elif abs(gradV[i][j]) > abs(gradH[i][j]):
                    if gradV[i][j] < 0:
                        flDir[i][j] = 1
                    else:
                        flDir[i][j] = 3
                else:
                    if gradH[i][j] < 0:
                        flDir[i][j] = 2
                    else:
                        flDir[i][j] = 4
            else:
                flDir[i][j] = -1
    return flDir

"""
def flowDirng(elvImg):
    
    flDir = np.empty([len(elvImg), len(elvImg[0])], dtype=np.ubyte)
    for i in range(1,len(elvImg)-1):
        for j in range(1,len(elvImg[0])-1):
            #if elvImg[i][j] != None:
            if not math.isnan(elvImg[i][j]):
                upCell = elvImg[i-1][j] > elvImg[i][j]
                rightCell = elvImg[i][j+1] > elvImg[i][j]
                downCell = elvImg[i+1][j] > elvImg[i][j]
                leftCell = elvImg[i][j-1] > elvImg[i][j]
                
                if upCell and rightCell and downCell and leftCell:
                    flDir[i][j] = 5
                else:
                    if 
            else:
                flDir[i][j] = 0
    return flDir
"""


#CUDA kernel for calculating immediate flow accumulation at each nearby tile
#called with one thread/pixel
flow_kernel = cp.RawKernel(r'''
extern "C" __global__                          
void flow_kernel(int* flowDir, int* acc, int xDim, int yDim,
                 int* dAcc, int* uAcc, int* rAcc, int* lAcc){
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    
    int realInd = y * xDim + x;
    
    if(x > 0 && x < xDim -1 && y >0 && y < yDim -1){
        if(flowDir[realInd] ==3){
            int adjInd = (y+1) * yDim + x;
            uAcc[adjInd] = acc[realInd];
        }else if(flowDir[realInd] == 4){
            int adjInd = y * yDim + (x+1);
            lAcc[adjInd] = acc[realInd];
        }else if(flowDir[realInd] ==1){
            int adjInd = (y-1) * yDim + x;
            dAcc[adjInd] = acc[realInd];    
        }else if(flowDir[realInd]==2){
            int adjInd = y * yDim + x-1;
            rAcc[adjInd] = acc[realInd];    
        }
    }
}                           
''', 'flow_kernel')

#CUDA kernel for summing accumulation at a tile from nearby neighbors
#called with one thread/pixel
flow_copy = cp.RawKernel(r'''
extern "C" __global__                          
void flow_copy(int* acc, int xDim, int yDim,
                 int* dAcc, int* uAcc, int* rAcc, int* lAcc){
    int x = blockDim.x * blockIdx.x + threadIdx.x;
    int y = blockDim.y * blockIdx.y + threadIdx.y;
    
    int realInd = y * xDim + x;
    if(x > 0 && x < xDim -1 && y >0 && y < yDim -1){
            acc[realInd] = dAcc[realInd] + uAcc[realInd] + lAcc[realInd] + rAcc[realInd] + 1;
    }
}                           
''', 'flow_copy')


#reconverts flattened arr into logged 2d arr
def imgen(flatIm, sDimlen):
    deflat = unflatten(flatIm, sDimlen)
    validIm =np.nan_to_num(np.log(deflat))
    return validIm

#converts final image array into [0,255] bounded uint8 values for gif color
#saves output as gif
def imFin(filename, imarr):
    
    imMin = 1000.0
    imMax = 0.0
    for im in imarr:
        print(type(im))
        i_min = im.min()
        i_max = im.max()
        if i_min < imMin:
            imMin = i_min
        if i_max > imMax:
            imMax = i_max
    print("max: ", imMax)
    print("min: ", imMin)
    for i in range(len(imarr)):
        imarr[i] = np.interp(imarr[i], (imMin, imMax), (255,0))
    imageio.mimsave(filename, imarr)
    
#reconverts 1D arr into original 2d array, reversing flattening command
def unflatten(arr, sDimlen):
    fDimlen = int(len(arr) / sDimlen)
    
    arrUF = np.zeros([fDimlen, sDimlen])
    
    startInd = 0
    
    for block in range(fDimlen):
        endInd = startInd + sDimlen
        arrUF[block] = arr[startInd:endInd]
        startInd += sDimlen
    return arrUF

"""
Conservative Flow accumulation solver running in parallel on CUDA
allows for gif output if given filename *WIP*

"""
def flowAccConsCuda(flDir, iters, elvImg, blockDim, filename = None, itRange = 1, gif=False):
    dAcc = cp.zeros([len(flDir) * len(flDir[0])], dtype=cp.int32)
    uAcc = cp.zeros([len(flDir) * len(flDir[0])], dtype=cp.int32)
    rAcc = cp.zeros([len(flDir) * len(flDir[0])], dtype=cp.int32)
    lAcc = cp.zeros([len(flDir) * len(flDir[0])], dtype=cp.int32)
    
    acc_d = cp.ones([len(flDir) * len(flDir[0])], dtype=cp.int32)
    fldir_d = cp.asarray(fldir.flatten(), dtype=cp.int32)
    
    xBlockNum = int(math.ceil(len(flDir[0])))
    yBlockNum = int(math.ceil(len(flDir)))    
    
    images = []
    if gif:
        images.append(np.full([len(flDir), len(flDir[0])], 0, dtype = np.uint8))
        print("wah: ", type(images[0]))
    for it in range(iters):
        print("iteration: ", it)
        flow_kernel((xBlockNum, yBlockNum),(blockDim, blockDim),
                    (fldir_d, acc_d, len(flDir[0]), len(flDir), dAcc, uAcc, rAcc, lAcc))
        
        flow_copy((xBlockNum, yBlockNum),(blockDim, blockDim),
                  (acc_d, len(flDir[0]), len(flDir), dAcc, uAcc, rAcc, lAcc))
        
        if gif and it % itRange == 0:
            images.append(imgen(cp.asnumpy(acc_d), len(flDir[0])))
    
    acc_flat = cp.asnumpy(acc_d)
    
    acc = unflatten(acc_flat, len(fldir[0]))
    
    if gif:
        imFin(filename, images)
    
    
    for i in range(len(flDir)):
        for j in range(len(flDir[0])):
            if math.isnan(elvImg[i][j]):
                acc[i][j] = np.nan
    
    return acc

"""
Flow accumulation solver that prevents infinite accumulation
Runs on CPU, quite slow for any real number of iterations
"""
def flowAccCons(flDir, iters, elvImg):
    dAcc = np.zeros([len(flDir), len(flDir[0])])
    uAcc = np.zeros([len(flDir), len(flDir[0])])
    rAcc = np.zeros([len(flDir), len(flDir[0])])
    lAcc = np.zeros([len(flDir), len(flDir[0])])
    
    acc = np.ones([len(flDir), len(flDir[0])])
    nx_acc = np.copy(acc)
    for it in range(iters):
        for i in range(1, len(flDir) -1):
            for j in range(1, len(flDir[0]) -1):
                if flDir[i][j] != -1:
                    if flDir[i][j]==1:
                        uAcc[i+1][j] = acc[i][j]
                    elif flDir[i][j] ==2:
                        lAcc[i][j+1] = acc[i][j]
                    elif flDir[i][j] ==3:
                        dAcc[i-1][j] =acc[i][j]
                    elif flDir[i][j] ==4:
                        rAcc[i][j-1] =acc[i][j]
        for i in range(1, len(flDir) -1):
            for j in range(1, len(flDir[0]) -1):
                if flDir[i][j] != -1:
                    nx_acc[i][j] = dAcc[i][j] + uAcc[i][j] + rAcc[i][j] + lAcc[i][j] +1
        
        acc = np.copy(nx_acc)
        #plt.imshow(acc)
    
    for i in range(len(flDir)):
        for j in range(len(flDir[0])):
            if math.isnan(elvImg[i][j]):
                acc[i][j] = np.nan
    
    return acc
        

#basic flow accumulation
def flowAcc(flDir, iters):
    acc = np.ones([len(flDir), len(flDir[0])])
   
                
    for it in range(iters):
        nx_acc = np.copy(acc)
        for i in range(1, len(flDir) -1):
            for j in range(1, len(flDir[0]) -1):
                if not math.isnan(flDir[i][j]):
                    if flDir[i][j]==1:
                        nx_acc[i][j+1] += acc[i][j]
                    elif flDir[i][j] ==2:
                        nx_acc[i+1][j] += acc[i][j]
                    elif flDir[i][j] ==3:
                        nx_acc[i][j-1] +=acc[i][j]
                    elif flDir[i][j] ==4:
                        nx_acc[i-1][j] +=acc[i][j]
        acc = np.copy(nx_acc)
        
    for i in range(len(flDir)):
        for j in range(len(flDir[0])):
            if math.isnan(flDir[i][j]):
                acc[i][j] = -1
    return acc
    


#need to pull out mapping from dataset for conversion to geo coordinates

rasterArr = genElvmap(filename)
geotransform = geoDat(filename)

if geotransform and False:
    print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
    print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    
     
#plt.imshow(rasterArr)
ds = gdal.Open(filename, gdal.GA_ReadOnly)
xoff, a, b, yoff, d, e = ds.GetGeoTransform()

def pixel2coord(x, y):
 """Returns global coordinates from pixel x, y coords"""
 xp = a * x + b * y + xoff
 yp = d * x + e * y + yoff
 return(xp, yp)



def retImg(flacc, tLx, tLy, squareDim, logFlag = False):
    
    x_ix = np.arange(squareDim) + tLx
    y_ix = np.arange(squareDim) + tLy
    
    ixg = np.ix_(x_ix, y_ix)
    if not logFlag:
        return flacc[ixg]
    else:
        return flacc[ixg]

fldir = flowDir(rasterArr)
#flacc = flowAccCons(fldir, 100, rasterArr)
#flacc = flowAccConsCuda(fldir, 15, rasterArr, 16, "test6.gif", 1, True)
#flacc = flowAccConsCuda(fldir, 1000, rasterArr, 32)

#np.save("flacc.npy", flacc)

plt.imshow(rasterArr)
#plt.imshow(np.log(flacc))
#grad1 is vertical/dim0, grad2 is horizontal/dim1
#grad1, grad2 = np.gradient(rasterArr, Grid_space)

#plt.imshow(grad1)
#plt.imshow(grad2)

