#
# Copyright ifm electronic, gmbh
# SPDX-License-Identifier: MIT
#
from __future__ import absolute_import, division, print_function
from builtins import *
import struct
import array

from ifmO3r.pcic.client import PCICV3Client
from ifmO3r.pcic.cwrappers import (
    IntrinsicCalibration,
    ExtrinsicCalibration,
    DistanceImageInfo,
)


class ImageClient(PCICV3Client):
    def __init__(self, address, port, isO3R=False):
        super(ImageClient, self).__init__(address, port)
        if not isO3R:
            # disable all result output
            self.sendCommand("p0")
            # format string for all images
            pcicConfig = '{ "layouter": "flexible", "format": { "dataencoding": "ascii" }, "elements": [ { "type": "string", "value": "star", "id": "start_string" }, { "type": "blob", "id": "normalized_amplitude_image" }, { "type": "blob", "id": "distance_image" }, { "type": "blob", "id": "x_image" }, { "type": "blob", "id": "y_image" }, { "type": "blob", "id": "z_image" }, { "type": "blob", "id": "confidence_image" }, { "type": "blob", "id": "diagnostic_data" }, { "type": "blob", "id": "extrinsic_calibration" }, { "type": "blob", "id": "intrinsic_calibration" },{ "type": "blob", "id": "inverse_intrinsic_calibration" },{ "type": "string", "value": "stop", "id": "end_string" } ] }'
            answer = self.sendCommand("c%09d%s" % (len(pcicConfig), pcicConfig))
            if str(answer, "utf-8") != "*":
                raise
            # enable result output again
            self.sendCommand("p1")

    def readNextFrame(self):
        result = {}

        # look for asynchronous output
        ticket, answer = self.readNextAnswer()
        if ticket == b"0000":
            answerIndex = 0

            # read start sequence
            data = answer[answerIndex : answerIndex + 4]
            answerIndex += 4
            if self.debugFull == True:
                print('Read 4 Bytes start sequence: "%s"' % data)

            if data != b"star":
                print(data)
                raise RuntimeError("Start of PCIC Frame missing (star)")

            chunkCounter = 1

            while True:
                # read next 4 bytes
                data = answer[answerIndex : answerIndex + 4]
                answerIndex += 4
                MetaData = None
                # stop if frame finished
                if data == b"stop":
                    break

                # else read rest of image header
                data += answer[answerIndex : answerIndex + 12]
                answerIndex += 12
                if self.debugFull == True:
                    print('Read %d Bytes image header: "%r"' % (len(data), data))

                # extract information about chunk
                chunkType, chunkSize, headerSize, headerVersion = struct.unpack(
                    "IIII", bytes(data)
                )

                # read rest of chunk header
                data += answer[answerIndex : answerIndex + headerSize - 16]
                answerIndex += headerSize - 16

                if headerVersion == 1:
                    (
                        chunkType,
                        chunkSize,
                        headerSize,
                        headerVersion,
                        imageWidth,
                        imageHeight,
                        pixelFormat,
                        timeStamp,
                        frameCount,
                    ) = struct.unpack("IIIIIIIII", bytes(data))
                elif headerVersion == 2:
                    (
                        chunkType,
                        chunkSize,
                        headerSize,
                        headerVersion,
                        imageWidth,
                        imageHeight,
                        pixelFormat,
                        timeStamp,
                        frameCount,
                        statusCode,
                        timeStampSec,
                        timeStampNsec,
                    ) = struct.unpack("IIIIIIIIIIII", bytes(data))
                elif headerVersion == 3:
                    (
                        chunkType,
                        chunkSize,
                        headerSize,
                        headerVersion,
                        imageWidth,
                        imageHeight,
                        pixelFormat,
                        timeStamp,
                        frameCount,
                        statusCode,
                        timeStampSec,
                        timeStampNsec,
                    ) = struct.unpack("IIIIIIIIIIII", bytes(data[0:48]))
                    MetaData = data[48:]
                else:
                    # raise RuntimeError("Unknown chunk header version %d!" % headerVersion)
                    print("Unknown chunk header version %d!" % headerVersion)

                if self.debug == True:
                    print(
                        """Data chunk %d:
	Chunk type: %d
	Chunk size: %d
	Header size: %d
	Header version: %d
	Image width: %d
	Image height: %d
	Pixel format: %d
	Time stamp: %d
	Frame counter: %d"""
                        % (
                            chunkCounter,
                            chunkType,
                            chunkSize,
                            headerSize,
                            headerVersion,
                            imageWidth,
                            imageHeight,
                            pixelFormat,
                            timeStamp,
                            frameCount,
                        )
                    )

                # read chunk data
                data = answer[answerIndex : answerIndex + chunkSize - headerSize]
                answerIndex += chunkSize - headerSize

                # distinguish pixel type
                if pixelFormat == 0:
                    image = array.array("B", bytes(data))
                elif pixelFormat == 1:
                    image = array.array("b", bytes(data))
                elif pixelFormat == 2:
                    image = array.array("H", bytes(data))
                elif pixelFormat == 3:
                    image = array.array("h", bytes(data))
                elif pixelFormat == 4:
                    image = array.array("I", bytes(data))
                elif pixelFormat == 5:
                    image = array.array("i", bytes(data))
                elif pixelFormat == 6:
                    image = array.array("f", bytes(data))
                elif pixelFormat == 8:
                    image = array.array("d", bytes(data))
                else:
                    image = None

                # distance image
                if chunkType == 100:
                    result["distance"] = image
                    result["distance_meta"] = MetaData

                # amplitude image
                elif chunkType == 101:
                    result["amplitude"] = image
                    result["amplitude_meta"] = MetaData

                # intensity image
                elif chunkType == 102:
                    result["intensity"] = image

                # raw amplitude image
                elif chunkType == 103:
                    result["rawAmplitude"] = image

                # raw amplitude image
                elif chunkType == 105:
                    result["distance_noise"] = image
                    result["distance_noise_meta"] = MetaData

                # X image
                elif chunkType == 200:
                    result["x"] = image

                # Y image
                elif chunkType == 201:
                    result["y"] = image

                # Z image
                elif chunkType == 202:
                    result["z"] = image

                # confidence image
                elif chunkType == 300:
                    result["confidence"] = image

                # raw image
                elif chunkType == 301:
                    if "raw" not in result:
                        result["raw"] = []
                    result["raw"].append(image)

                # diagnostic data
                elif chunkType == 302:
                    diagnosticData = {}
                    payloadSize = chunkSize - headerSize
                    # the diagnostic data blob contains at least four temperatures plus the evaluation time
                    if payloadSize >= 20:
                        (
                            illuTemp,
                            frontendTemp1,
                            frontendTemp2,
                            imx6Temp,
                            evalTime,
                        ) = struct.unpack("=iiiiI", bytes(data[0:20]))
                        diagnosticData = dict(
                            [
                                ("illuTemp", illuTemp / 10.0),
                                ("frontendTemp1", frontendTemp1 / 10.0),
                                ("frontendTemp2", frontendTemp2 / 10.0),
                                ("imx6Temp", imx6Temp / 10.0),
                                ("evalTime", evalTime),
                            ]
                        )
                    # check whether framerate is also provided
                    if payloadSize == 24:
                        diagnosticData["frameRate"] = struct.unpack(
                            "=I", bytes(data[20:24])
                        )[0]
                    result["diagnostic"] = diagnosticData

                elif chunkType == 402 or chunkType == 420:
                    result["distance_image_info"] = DistanceImageInfo.from_buffer(data)

                chunkCounter = chunkCounter + 1

        # return amplitudeImage, intensityImage, distanceImage, xImage, yImage, zImage, confidenceImage, diagnosticData, rawImage, rawAmplitudeImage
        result["image_width"] = imageWidth
        result["image_height"] = imageHeight
        return result
