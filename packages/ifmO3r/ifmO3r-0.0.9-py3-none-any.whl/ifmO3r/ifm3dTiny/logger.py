"""
Author: ifm CSR
This script provides logging features for logging status messages and data to file

This is sample code. Use at your own risk.
"""

import logging
import os
import pickle
import struct
from pathlib import Path
import h5py
import matplotlib.pyplot as plt
import numpy as np

from ifmO3r.ifm3dTiny.utils import hdf5dict
from ifmO3r.ifm3dTiny.grabber import FrameGrabber, ImageBuffer

class ImageLogger:
    """
    This image logger class provides helper functions for writing image data to file
    """
    def __init__(self, frameGrabber=None, imageBuffer=None, path=None):
        """

        :param path: std output path for all data written to file
        :param frameGrabber: frame grabber object of the grabber class
        :param imageBuffer: image buffer object of the grabber class
        """
        # check for provided data output path
        if path is None:
            cwd = os.getcwd()
            self.path = os.path.join(cwd, 'data')
            if not os.path.exists(self.path):
                try:
                    os.makedirs(self.path)
                except IOError as err:
                    print('A data output folder can not be created at the current working directory: ', err)
        else:
            self.path = path
            if not os.path.exists(self.path):
                try:
                    os.makedirs(self.path)
                except IOError as err:
                    print('The output folder can not created', err)

        # check args for a provided FrameGrabber and ImageBuffer
        if frameGrabber is None:
            self.frameGrabber = FrameGrabber
        else:
            self.frameGrabber = frameGrabber

        if imageBuffer is None:
            self.imageBuffer = ImageBuffer
        else:
            self.imageBuffer = imageBuffer

        # get the first frame and set it inside the ImageBuffer
        self.frameGrabber.wait_for_frame(self.imageBuffer, 5)

    def set_frame(self, frame):
        """
        setter method for setting to a specific frame from the outside
        :param frame: frame object of the frameGrabber class
        :return:
        """
        self.imageBuffer.frame = frame
        # ToDo: the grabber class so far does not have a setter method for frames

    def _get_frame(self):
        """
        returns the frame currently stored inside the ImageBuffer object
        :return: frame
        """
        return self.imageBuffer._get_frame()

    def get_current_frame(self, timeout=5):
        """
        this method sets to frame inside the ImageBuffer to the current frame
        :return:
        """
        self.frameGrabber.wait_for_frame(self.imageBuffer, timeout)

    def write_png(self, dictToSave):
        """
        write a the data of a frame png file: provide a list of the names of the data fields
        :param dictToSave: dict of key - value pairs: of data fields and file names to be written
            (e.g. {"distance": "distance_frame1", "amplitude": "amplitude_frame1", "confidence": "confidence_frame1"})
        :return:
        :raises: IOError, Exception
        """

        try:
            for key in list(dictToSave.keys()):
                if 'distance' in key.lower():
                    distance_img = self.imageBuffer.distance_image()
                    self.__write_png(distance_img, str(dictToSave[key]))
                elif 'amplitude' in key.lower():
                    amplitude_img = self.imageBuffer.amplitude_image()
                    self.__write_png(amplitude_img, str(dictToSave[key]))
                elif 'confidence' in key.lower():
                    confidence_img = self.imageBuffer.confidence_image()
                    self.__write_png(confidence_img, str(dictToSave[key]))
                else:
                    raise NameError('The data field of the supplied key can not be written to a h5 file currently.')
        except OSError('Writing data to file failed') as e:
            pass

    def write_binary(self, dictToSave):
        """
        write a the data of a frame to binary file: provide a list of the names of the data fields
        :param dictToSave: dict of key - value pairs: of data fields and file names to be written
            (e.g. {"x": "x_frame1", "y": "y_frame1", "z": "z_frame1",
            "distance": "distance_frame1", "amplitude": "amplitude_frame1", "confidence": "confidence_frame1"})

        :return:
        :raises: IOError, Exception
        """
        x, y, z = self.imageBuffer.xyz_image()

        try:
            for key in list(dictToSave.keys()):
                if 'x' in key.lower():
                    self.__write_binary(x, np.uint16, str(dictToSave[key]))
                elif 'y' in key.lower():
                    self.__write_binary(y, np.uint16, str(dictToSave[key]))
                elif 'z' in key.lower():
                    self.__write_binary(z, np.uint16, str(dictToSave[key]))

                elif 'distance' in key.lower():
                    distance_img = self.imageBuffer.distance_image()
                    self.__write_binary(distance_img, np.float32, str(dictToSave[key]))
                elif 'amplitude' in key.lower():
                    amplitude_img = self.imageBuffer.amplitude_image()
                    self.__write_binary(amplitude_img, np.uint16, str(dictToSave[key]))
                elif 'confidence' in key.lower():
                    confidence_img = self.imageBuffer.confidence_image()  # TODO: replace dummy method in ImageBuffer
                    self.__write_binary(confidence_img, np.uint16, str(dictToSave[key]))
                else:
                    raise NameError('The data field of the supplied key can not be written to a h5 file currently.')
        except OSError('Writing data to file failed') as e:
            pass

    def write_to_h5(self, dictToSave):
        """
        write a the data of a frame to hdf5 file: provide a list of the names of the data fields
        :param (e.g. {"x": "x_frame1", "y": "y_frame1", "z": "z_frame1",
            "distance": "distance_frame1", "amplitude": "amplitude_frame1", "confidence": "confidence_frame1"})
        :return:
        :raises: IOError, Exception
        """
        x, y, z = self.imageBuffer.xyz_image()

        try:
            for key in list(dictToSave.keys()):
                if 'x' in key.lower():
                    self.__write_h5(x, str(dictToSave[key]))
                elif 'y' in key.lower():
                    self.__write_h5(y,str(dictToSave[key]))
                elif 'z' in key.lower():
                    self.__write_h5(z, str(dictToSave[key]))

                elif 'distance' in key.lower():
                    distance_img = self.imageBuffer.distance_image()
                    self.__write_h5(distance_img, str(dictToSave[key]))
                elif 'amplitude' in key.lower():
                    amplitude_img = self.imageBuffer.amplitude_image()
                    self.__write_h5(amplitude_img, str(dictToSave[key]))
                elif 'confidence' in key.lower():
                    confidence_img = self.imageBuffer.confidence_image()
                    self.__write_h5(confidence_img, str(dictToSave[key]))
                    # TODO: implement the binary coded representation
                else:
                    raise NameError('The data field of the supplied key can not be written to a h5 file currently.')
        except OSError('Writing data to file failed') as e:
            pass

    def __write_h5(self, data, name, filename=None):
        """
        this method expects numpy array and writes the data to HDF5

        :param data: data to be written to file (expects: np.array)
        :param name: name of the data field inside the hdf5 object
        :param filename: output filename without file designation
        :return:
        :raise:IOError, OSError

        """
        if filename is None:
            filename = "{}.h5".format(str(name))
            filename_out = os.path.join(self.path, filename)
        else:
            filename_out = os.path.join(self.path, "{}.h5".format(filename))
        try:
            hf = h5py.File(filename_out, 'w')
            hf.create_dataset(name, data=data)
            hf.close()
        except IOError('The data can not be written to file. Did you check the permissions of the file directory?') \
                as e:
            pass
        except OSError('Data can not be written to file') as e:
            pass

    def _write_frame_to_h5(self, filename):
        """
        write a complete frame to hdf5-file
        :param filename: output filename without file designation
        :return:
        """
        # set output path based on filename
        filename_out = os.path.join(self.path, "{}.h5".format(filename))

        # convert arrays in frame to np.arrays
        x, y, z = self.imageBuffer.xyz_image()
        distance = self.imageBuffer.distance_image()
        amplitude = self.imageBuffer.amplitude_image()
        confidence_img = self.imageBuffer.confidence_image()
        distance_noise_tmp = self.imageBuffer.frame['distance_noise']
        distance_noise = np.resize(distance_noise_tmp, (self.imageBuffer.height, self.imageBuffer.width))
        distance_noise = np.frombuffer(distance_noise, dtype=np.float32)

        # get the current frame for the rest of the data
        frame_current = self._get_frame()
        extrinsic = frame_current['distance_image_info'].ExtrinsicOpticToUser
        intrinsic = frame_current['distance_image_info'].IntrinsicCalibration
        inverse_intrinsic = frame_current['distance_image_info'].InverseIntrinsicCalibration
        # TODO: add further data fields to hdf5 export

        # create new dict
        frame = {'distance': distance,
                 'amplitude': amplitude,
                 'confidence': confidence_img,
                 'x': x,
                 'y': y,
                 'z': z,
                 }
        hdf5dict.saveDictToHdf5(frame, filename_out)

    def __write_png(self, data, filename):
        """
        this method expects a numpy array and writes the data to PNG
        :param data: data to be written to file (expects: np.array)
        :param filename: output filename without file designation
        :return:
        """
        try:
            filename_out = os.path.join(self.path, "{}.png".format(filename))
            plt.imsave(filename_out, data)
        except IOError('The data can not be written to file. Did you check the permissions of the file directory?')\
                as e:
            pass
        except OSError('Data can not be written to file') as e:
            pass


    def __write_binary(self, data, d_type, name):
        """
        this method expects a numpy array and writes the data to non-structured binary output file
        :param data: data to be written to file
        :param d_type: data type (e.g. numpy.flat32)
        :param name:  output filename without file designation
        :return:
        """
        filename_out = os.path.join(self.path, str(name))
        data = np.frombuffer(data, dtype=d_type)

        # struct format based on numpy data types
        if d_type == 'float32':
            fmt = 'f' * len(data)
        elif d_type == 'float64':
            fmt = 'd' * len(data)
        elif d_type == 'uint8':
            fmt = 'H' * len(data)
        elif d_type == 'uint16':
            fmt = 'L' * len(data)
        elif d_type == 'uint32':
            fmt = 'Q' * len(data)
        else:
            fmt = 'd' * len(data)

        try:
            # pack the data and write to file
            f = open(filename_out, "wb")
            data_bin = struct.pack(fmt, *data)
            f.write(data_bin)
            f.close()
        except IOError('The data can not be written to file. Did you check the permissions of the file directory?')\
                as e:
            pass
        except OSError('Data can not be written to file') as e:
            pass

    def save_frame_as_pickle(self, name=None):
        """
        saves the complete frame by serializing it and save to pickle file
        :param name: filename of the output
        :return:
        """
        if name is None:
            name = "{}.p".format('frame')
            name = os.path.join(self.path, name)
        else:
            name = os.path.join(self.path, "{}.p".format(name))

        try:
            pickle.dump(self.imageBuffer.frame, open(name, "wb"))
        except IOError('The data can not be written to file. Did you check the permissions of the file directory?')\
                 as e:
            pass
        except OSError('Data can not be written to file') as e:
            pass

    def load_frame_from_pickle(self, name):
        """
        load frame from pickle file
        :param name: filename
        :return:
        """
        try:
            frame_from_pickle = pickle.load(open(name, "rb"))
            self.set_frame(frame_from_pickle)
        except OSError('File not found') as e:
            pass

class StatusLogger:
    """
    This status logger class provides helper functions for writing status messages to file while using the standard
    Python logging class
    """
    def __init__(self, nameLogFile):
        """
        creates a logger object for asynchronous message logging
        :param nameLogFile: log file name
        """

        # create logger and set logging level to info
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create a fileHandler for writing the the logging messages to file
        fh = logging.FileHandler(nameLogFile + '.log')
        fh.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(fh)

    def __enter__(self):
        return self

    def info(self, message):
        """
        logs a info message

        :param message: content of the message
        :return:
        """
        self.logger.info(message)

    def critical(self, message):
        """
        logs a critical message
        :param message: content of the message
        :return:
        """
        self.logger.critical(message)


#%%
if __name__ == "__main__":
    from ifmO3r.ifm3dTiny.device import Device

    cam1 = Device("192.168.0.69", 50012)
    # build a FrameGrabber and ImageBuffer
    fg = FrameGrabber(cam1)
    im = ImageBuffer()

    # specify a data dir
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        Path(os.path.join(dir_path, 'data')).mkdir(parents=True, exist_ok=True)
        data_path = os.path.join(dir_path, 'data')
    except IOError as arg:
        print('The data dir can not be accessed or written to: ' + arg)
        pass

    # get a ImgLogger objet with the specified frame and data dir
    imgLogger = ImageLogger(fg, im, data_path)
    imgLogger.get_current_frame()

    # get an image
    imgLogger.get_current_frame()

    # try some data logging
    save_this = {"distance": "distance_frame1", "amplitude": "amplitude_frame1"}
    imgLogger.write_png(save_this)
    imgLogger.write_binary(save_this)
    imgLogger.write_to_h5(save_this)

    imgLogger.write_to_h5({"X": "x_f1", "Y": "y_f1", "Z": "z_f1"})

    # save whole frame as pickle
    imgLogger.save_frame_as_pickle('frame')

    # load a frame from pickle
    file_path = os.path.join(data_path, 'frame.p')
    imgLogger.load_frame_from_pickle(file_path)

    save_imgs = {"distance": "distance_frame_new", "amplitude": "amplitude_frame_new",
                 "confidence": "confidence_frame_new"}
    imgLogger.write_png(save_imgs)


