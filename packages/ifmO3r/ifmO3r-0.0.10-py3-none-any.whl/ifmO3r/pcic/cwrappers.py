#
# Copyright ifm electronic, gmbh
# SPDX-License-Identifier: MIT
# 
import ctypes as ct


class ExtrinsicCalibration(ct.Structure):
    _fields_ = [("transX", ct.c_float),
                ("transY", ct.c_float),
                ("transZ", ct.c_float),
                ("rotX", ct.c_float),
                ("rotY", ct.c_float),
                ("rotZ", ct.c_float)]

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__,", "
                .join(["{}: {}".format(field[0],getattr(self,field[0])) for field in self._fields_]))

class IntrinsicCalibration(ct.Structure):
    _fields_ = [("modelID", ct.c_uint32),("modelParameters", ct.c_float * 32)]
    def __str__(self):
        return "{}: {{modelID: {}, modelParameters: {}}}".format(self.__class__.__name__,self.modelID,list(self.modelParameters))

class InverseIntrinsicCalibration(IntrinsicCalibration):
    pass

class DistanceImageInfo(ct.Structure):
    _fields_ = [("Version", ct.c_uint32),
                ("DistanceResolution", ct.c_float),
                ("AmplitudeResolution", ct.c_float),
                ("AmpNormalizationFactors", ct.c_float*3),
                ("ExtrinsicOpticToUser", ExtrinsicCalibration),
                ("IntrinsicCalibration", IntrinsicCalibration),
                ("InverseIntrinsicCalibration", InverseIntrinsicCalibration)]

    def __str__(self):
        return "{}: {{{}}}".format(self.__class__.__name__,", "
                .join(["{}: {}".format(field[0], getattr(self, field[0])) for field in self._fields_]))
