# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2020 ifm electronic gmbh
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

"""
This module exports functions for interpreting the data returned from O3R's PCIC interface.
To save bandwidth, data is transferred in a 16 bit fix-point format and redundant data (e.g., 
Cartesian coordinates which can be derived from the distance image, the camera intrinsic model
and the extrinsic calibration) is skipped.
"""
import numpy as np

def xyzd_from_distance(distance_u16, distResolution, 
                     extrinsicOpticToUserTrans, extrinsicOpticToUserRot, intrinsicModelID, intrinsicModelParameters,
                     width, height,
                     X=None, Y=None, Z=None, D=None):
    """
    Converts compressed output information from O3R distance image algorithm into original values. 
    
    :param distance_u16             : The distance information, encoded in uint16 format
    :param distResolution           : The resolution of the distance image information
    :param extrinsicOpticToUserTrans: The translational part of the extrinsic optic to user calibration as a 3D vector 
                                      in [m]: [transX, transY, transZ]
    :param extrinsicOpticToUserRot  : The rotational part of the extrinsic optic to user calibration as a 3D vector 
                                      in [rad]: [rotX, rotY, rotZ]
    :param intrinsicModelID         : The model ID of the intrinsic calibration
    :param intrinsicModelParameters : The 32 element parameter array of the intrinsic calibration
    :param width                    : the width of the images
    :param height                   : the height of the images
    :param X                        : optional pre-allocated height x width float32 image for storing the cartesian X
    :param Y                        : optional pre-allocated height x width float32 image for storing the cartesian Y
    :param Z                        : optional pre-allocated height x width float32 image for storing the cartesian Z
    :param D                        : optional pre-allocated height x width float32 image for storing the distance matrix D
    :return: X, Y, Z, D where (X,Y,Z) are the cartesian coordinates in [m] and D is the radial distance image in [m]
    """
    # evaluate intrinsic calibration if cache is not up to date
    if not hasattr(xyzd_from_distance, "intrCache") or xyzd_from_distance.intrCache[0] != (intrinsicModelID, tuple(intrinsicModelParameters), width, height):
        vx, vy, vz = eval_intrinsic(intrinsicModelID, intrinsicModelParameters, width, height)
        xyzd_from_distance.intrCache = ((intrinsicModelID, tuple(intrinsicModelParameters), width, height), vx, vy, vz)
        # invalidate extrinsic cache
        xyzd_from_distance.extrCache = (None,)
    vx, vy, vz = xyzd_from_distance.intrCache[1:]
    # evaluate extrinsic calibration if cache is not up to date
    if xyzd_from_distance.extrCache[0] != (tuple(extrinsicOpticToUserTrans), tuple(extrinsicOpticToUserRot)):
        R, t = eval_extrinsic(extrinsicOpticToUserTrans, extrinsicOpticToUserRot)
        # apply rotation matrix to unit vectors
        uvx = R[0,0]*vx + R[0,1]*vy + R[0,2]*vz
        uvy = R[1,0]*vx + R[1,1]*vy + R[1,2]*vz
        uvz = R[2,0]*vx + R[2,1]*vy + R[2,2]*vz
        xyzd_from_distance.extrCache = ((tuple(extrinsicOpticToUserTrans), tuple(extrinsicOpticToUserRot)), uvx, uvy, uvz, t)
    uvx, uvy, uvz, t = xyzd_from_distance.extrCache[1:]
    # see https://polarionsy.intra.ifm/polarion/redirect/project/O3Rx_01/workitem?id=O3R-2146 for the conversion rules
    n = width * height
    if D is None:
        D = np.zeros((height, width), np.float32)
    if X is None:
        X = np.zeros((height, width), np.float32)
    if Y is None:
        Y = np.zeros((height, width), np.float32)
    if Z is None:
        Z = np.zeros((height, width), np.float32)
    D[...] = np.reshape(distance_u16[:n].astype(np.float32), (height, width))
    D *= distResolution
    X[...] = uvx
    X *= D
    X += t[0]
    Y[...] = uvy
    Y *= D
    Y += t[1]
    Z[...] = uvz
    Z *= D
    Z += t[2]
    # set invalid pixels to (0,0,0)
    X[D == 0] = 0
    Y[D == 0] = 0
    Z[D == 0] = 0
    return X, Y, Z, D

def convert_distance_noise(distanceNoise_u16, distResolution, width, height, N=None):
    """
    Converts the distance noise information to floating point, unit [m]
    
    :param distanceNoise_u16: The distance noise information, encoded in uint16 format
    :param distResolution   : The resolution of the distance image information
    :param width            : the width of the images
    :param height           : the height of the images
    :param N                : optional pre-allocated height x width float32 image for storing the distance noise N
    :return: N, the distance noise image in [m]
    """
    if N is None:
        N = np.zeros((height, width), np.float32)
    n = width * height        
    N[...] = np.reshape(distanceNoise_u16[:n].astype(np.float32), (height, width))
    N *= distResolution
    return N
    
def convert_amplitude(amplitude_u16, amplitudeResolution, width, height, A=None):
    """
    Converts the amplitude as delivered from O3R to floating point.
    
    :param amplitude_u16        : The amplitude information, encoded in uint16 fromat as delivered from O3R
    :param amplitudeResolution  : The resolution of the amplitude information as delivered from O3R
    :param width                : the width of the images as delivered from O3R
    :param height               : the height of the images as delivered from O3R
    :param A                    : optional pre-allocated height x width float32 image for storing the amplitude A
    :return: A, the amplitude image (negative values are possible here, resulting pixels out of the 
             coded modulation range)
    """
    if A is None:
        A = np.zeros((height, width), np.float32)
    n = width * height        
    A[...] = np.reshape(amplitude_u16[:n].astype(np.float32), (height, width))
    A -= 1
    mask = (A >= 0)
    A[mask] **= 2
    A[mask] *= amplitudeResolution
    return A
    
def eval_intrinsic(intrinsicModelID, intrinsicModelParameters, width, height):
    """
    Returns unit vectors for images with the given size calculated from the given unprojection model. 
    This function is automatically called from xyzdFromDistance.
    
    :param intrinsicModelID         : modelID of intrinsic calibration
    :param intrinsicModelParameters : parameters of intrinsicModel (32 element float32 array)
    :param width                    : width of the images
    :param height                   : height of the images
    :return: vx, vy, vz the x, y and z components of the normalized unit vectors
    """
    if intrinsicModelID == 0:
        # see https://polarionsy.intra.ifm/polarion/redirect/project/O3Rx_01/workitem?id=O3R-3131
        fx, fy, mx, my, alpha, k1, k2, k3, k4, k5 = intrinsicModelParameters[:10]
        iy, ix = np.indices((height, width))
        cx = (ix + 0.5 - mx)/fx
        cy = (iy + 0.5 - my)/fy
        cx -= alpha*cy
        r2 = cx**2 + cy**2
        fradial = 1 + r2*(k1 + r2*(k2 + r2*k5))
        h = 2*cx*cy
        tx = k3*h + k4*(r2 + 2*cx**2)
        ty = k3*(r2 + 2*cy**2) + k4*h
        dx = fradial * cx + tx
        dy = fradial * cy + ty
        fnorm = 1/np.sqrt(dx**2 + dy**2 + 1)
        vx = fnorm*dx
        vy = fnorm*dy
        vz = fnorm
        return vx, vy, vz
    else:
        raise RuntimeError("Unknown model %d" % intrinsicCalib.modelID)
        
def eval_extrinsic(translation, rotation):
    """
    Converts the extrinsic calibration into a rotation matrix and a translation vector.
    This function is automatically called from xyzdFromDistance.
    
    :param translation  : translational part of the extrinsic calibration [transX, transY, transZ]
    :param rotation     : translational part of the extrinsic calibration [rotX, rotY, rotZ]
    :return: R, t (R is the rotation matrix and t is the translation vector
    """
    t = np.array(translation, np.float32)
    rotX, rotY, rotZ = rotation
    # see https://polarionsy.intra.ifm/polarion/redirect/project/O3Rx_01/workitem?id=O3R-3140
    cx = np.cos(rotX)
    cy = np.cos(rotY)
    cz = np.cos(rotZ)
    sx = np.sin(rotX)
    sy = np.sin(rotY)
    sz = np.sin(rotZ)
    R = np.array([
        [cy*cz, -cy*sz, sy],
        [cx*sz + cz*sx*sy, cx*cz - sx*sy*sz, -cy*sx],
        [sx*sz - cx*cz*sy, cz*sx + cx*sy*sz, cx*cy]
    ], np.float32)
    return R, t

