"""
Author: ifm CSR

This is a helper script: it contains the grabber class which can be imported in other scripts.

To use this class:
:FrameGrabber   :   Connects to the camera head for receiving a frame
:ImageBuffer    :   Is used to save the image data from the Framegrabber-Object and make
                    images retrievable

Simple use cas:
    fg = FrameGrabber()
    im = ImageBuffer()

    fg.wait_for_frame(im,1)
    print(im.amplitude_image())
    print(im.distance_image())
    print(im.xyz_image())
"""
# %%
import pickle
import os
import threading
import numpy as np
from ifmO3r.pcic import ImageClient
from ifmO3r.ifm3dTiny.utils import GetCallableMethods
from ifmO3r import o3ralgo

# %%
DEFAULT_IMAGE_STACK_DEPTH = 10  # Arbitrary number
DEFAULT_TIMEOUT = 5  # Timeout in sec.
DEFAULT_TIMEOUT_LIVE = 30

# %%
class FrameGrabber:
    """
    Use the framegrabber to retrieve a frame from a head
    """

    def __init__(self, device):
        """
        :device         :   Device class, uses IP,PORT
        """
        if device is None:
            self.device = self._Connection(IP, PORT)
        else:
            self.device = self._Connection(device.ip, device.port)

        self.run = False

    def __str__(self):
        """
        Provide a list of *public* functions to be used by the user.

        :return:str_method_list     :   String representing a list of functions
        """
        str_method_list = GetCallableMethods().get_methods(self)
        return str_method_list

    def __timeout(self):
        raise TimeoutError("Timeout occurred - check power, connection, port, ip, timout in sec.")
        # raise ifm3dTinyExceptions.Timeout()
        # raise Exception("""Timeout during reception of frame.
        #     Did you check connection and trigger mode?""")

    def wait_for_frame(self, image_buffer, timeout):
        """
        Uses the device object within a context manager for establishing a connection.
        Provides only one single frame. Do not use this for streaming data.

        The module threading is used to create a timer thread and call the
        __timeout after 'n' amount of seconds. Raising an exception if the timer
        is not canceld before. See following description:
        https://realpython.com/intro-to-python-threading/

        :imageBuffer        :   ImageBuffer-Object (Class) responsible for saving/accessing the
                                image data within the frame
        :timeout (sec.)     :   Timeout for the receiving of a frame
        """

        if timeout is None:
            timeout = DEFAULT_TIMEOUT

        thread_timeout = threading.Timer(timeout, self.__timeout)
        thread_timeout.start()  # Start the timeout

        with self.device as port:
            frame = port.device.readNextFrame()
            image_buffer.frame = frame
            # If data was received, timeout thread will be stopped before raising an exception
            thread_timeout.cancel()
            return True

    def stream_on(self, image_buffer, timeout):
        """
        This function starts _stream_frame as a thread and if called again, cancels
        this thread too.

        :imageBuffer        :   ImageBuffer-Object (Class) responsible for saving/accessing
                                the image data within the frame
        :timeout (sec.)     :   Timeout for the receiving of a frame
        """

        if timeout is None:
            timeout = DEFAULT_TIMEOUT_LIVE

        if self.run is False:
            self.run = True
            self.thread_stream = threading.Thread(
                target=self._stream_frame, args=(image_buffer, timeout), daemon=True
            )

            self.thread_stream.start()
        else:
            self.run = False  # Deactivate the while True within _stream_frame
            self.thread_stream.join()  # Block the program until the thread is closed

    def _stream_frame(self, image_buffer, timeout):
        """
        This function opens a connection via FrameGrabber() and receives always the
        next frame. Instead of overwriting the frame within ImageBuffer() it is using
        an image stack within ImageBuffer().

        :imageBuffer        :   ImageBuffer-Object (Class) responsible for saving/accessing the image data within the frame
        :timeout (sec.)     :   Timeout for the receiving of a frame
        """
        if timeout is None:
            timeout = DEFAULT_TIMEOUT_LIVE

        # TODO: Implement working timeout calls
        with self.device as port:
            while self.run is True:  # run is toggled via stream_on
                frame = port.device.readNextFrame()
                image_buffer._push(frame)

    class _Connection:
        """
        This object is taking care of the connection to the head (ImagerClient)
        """

        def __init__(self, ip="192.168.0.69", port=50012):
            """
            :ip             :   IP Address of the head -  default:192.168.0.69
            :port           :   Port of the head - default: 50010
            """
            self.ip = ip
            self.port = port

        def __enter__(self):
            """
            Used for the context manager
            Opens a TCP/IP connection via ImageClient to the defined ip/port
            """
            self.device = ImageClient(self.ip, self.port, True)
            return self

        def __exit__(self, exc_t, exc_v, trace):
            """
            Used for the context manager
            Closes the TCP/IP connection
            """
            self.device.close()


# %%
class ImageBuffer:
    """
    Use the ImageBuffer as an object for saving the frame/images received by the FrameGrabber.
    """

    def __init__(self):

        image_stack_length = DEFAULT_IMAGE_STACK_DEPTH

        from collections import deque

        self.image_stack = deque(maxlen=image_stack_length)

        self.frame = None

    def __next__(self):
        """
        This function is used to pop the last taken image from the image stack and
        assign it to self.frame.
        This enables the user to use next(im) - assuming im = ImageBuffer() and get the
        newest frame.
        """
        if not self.image_stack:
            return False

        self.frame = self._pop()
        return True

    def __str__(self):
        """
        Provide a list of *public* functions to be used by the user.

        :return:str_method_list     :   String representing a list of functions
        """
        str_method_list = GetCallableMethods().get_methods(self)
        return str_method_list

    def __getattr__(self, item):
        if(item == "width"):
            return self.frame["image_width"]
        if(item == "height"):
            return self.frame["image_height"]
        return getattr(self, item)

    def __calculate_distance_xyz(self):
        """
        This function uses the ifmO3r.o3ralgo functionality to calculate the

        :return:x           :   x-image
        :return:y           :   y-image
        :return:z           :   z-image
        :return:distance    :   distance image (not radial distance)
        """
        distResolution = self.frame["distance_image_info"].DistanceResolution
        extrinsicOpticToUserTrans = [
            self.frame["distance_image_info"].ExtrinsicOpticToUser.transX,
            self.frame["distance_image_info"].ExtrinsicOpticToUser.transY,
            self.frame["distance_image_info"].ExtrinsicOpticToUser.transZ,
        ]

        extrinsicOpticToUserRot = [
            self.frame["distance_image_info"].ExtrinsicOpticToUser.rotX,
            self.frame["distance_image_info"].ExtrinsicOpticToUser.rotY,
            self.frame["distance_image_info"].ExtrinsicOpticToUser.rotZ,
        ]

        intrinsicModelID = self.frame[
            "distance_image_info"
        ].IntrinsicCalibration.modelID
        intrinsicModelParameters = list(
            self.frame["distance_image_info"].IntrinsicCalibration.modelParameters
        )

        x, y, z, distance = o3ralgo.xyzd_from_distance(
            np.frombuffer(self.frame["distance"], dtype="uint16"),
            distResolution,
            extrinsicOpticToUserTrans,
            extrinsicOpticToUserRot,
            intrinsicModelID,
            intrinsicModelParameters,
            self.frame["image_width"],
            self.frame["image_height"],
        )

        return x, y, z, distance

    def __convert_distance_noise(self):
        dist_resolution = self.frame["distance_image_info"].DistanceResolution
        distance_noise = o3ralgo.convert_distance_noise(
            np.frombuffer(self.frame["distance_noise"], dtype="uint16"),
            dist_resolution,
            self.frame["image_width"],
            self.frame["image_height"]
        )

        return distance_noise

    def _push(self, frame):
        """
        Adds a frame to the stack (LiFo stack)

        :frame      :   Frame received from FrameGrabber()
        """
        self.image_stack.append(frame)

    def _pop(self):
        """
        Returns/Pops the last item (frame) from the image stack. Raises
        exception if stack is empty.

        :return:frame   :   Returns frame from stack (FrameGrabber)
        """
        return self.image_stack.pop()

    def _save_buffer(self):
        """
        This function might be used to save a frame etc. via the pickle module
        """
        cws = os.path.dirname(os.path.realpath(__file__))
        cws = os.path.join(cws, "file.p")
        pickled_buffer = pickle.dump(self, open(cws, "wb"))

    def _load_buffer(self, path=None):
        """
        You can unpickle a imagebuffer and therefore have access to the frame,
        etc. from the state when the ImageBuffer was pickled.

        :path                       :   The path were the pickled file is based
        :return:ImageBuffer()       :   Pickle loads the ImageBuffer and returns that
        """

        if path == None:
            path = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(path, "file.p")
        return pickle.load(open(path, "rb"))

    def amplitude_image(self):
        """
        :return:amplitudeImg    :   Returns the amplitude image
        """
        if self.frame is None:
            return None

        amplitudeResolution = self.frame["distance_image_info"].AmplitudeResolution
        amplitudeImg = np.frombuffer(self.frame["amplitude"], dtype="uint16")

        amplitudeImg = o3ralgo.convert_amplitude(
            amplitudeImg, amplitudeResolution, self.frame["image_height"], self.frame["image_width"]
        )

        return amplitudeImg

    def distance_image(self):
        """
        :return:distance    :   Returns the distance image (not radial distance)
        """
        x, y, z, distance = self.__calculate_distance_xyz()
        return np.array(distance)

    def confidence_image(self):
        """
        :return:confidence  :   Returns the confidence matrix/image
        """
        confidence = np.reshape(np.frombuffer(self.frame["confidence"], dtype="uint8"), (self.frame["image_height"], self.frame["image_width"]))
        # # It appears, that one part for the calculation is missing

        # confidence = np.full(
        #     (self.image_width, self.image_height), 32
        # )  # Magic number -> confidence not yet working
        return confidence

    def xyz_image(self):
        """
        :return:[x,y,z]     :   Returns x,y,z as a numpy array [[x],[y],[z]]
        """
        x, y, z, _ = self.__calculate_distance_xyz()
        return np.array([x, y, z])

    def distance_noise_image(self):

        return self.__convert_distance_noise()

    def all_images(self):
        """
        :return:[x,y,z,distance,amplitude]  :   Return x,y,z,distance and amplitude image as numpy array [x,y,z,distance,amplitude]
        """
        x, y, z, distance = self.__calculate_distance_xyz()
        amplitude = self.amplitude_image()

        return np.array([x, y, z, distance, amplitude])

    def _set_frame(self, frame):
        """
        Simple setter method for frame. Could be used to provide a frame and
        use image buffer methods (extracting image data)

        :frame: Frame (most likely provided by FrameGrabber
        """
        self.frame = frame

    def _get_frame(self):
        """
        This function is normally not intended to be used by the user.
        Still, if you want to receive the complete frame, instead of single images,
        you can use this function. Because x,y,z images are not yet within the frame, we
        add them to the frame before forwarding it.

        :return:frame           :   Frame from ImageClient()
        """
        x, y, z = self.xyz_image()

        self.frame["x"] = x
        self.frame["y"] = y
        self.frame["z"] = z

        return self.frame

    def _get_image_stack(self):
        """
        Return the complete image stack (up to 10 frames).

        :return:imageStack  :   Image stack containing frames
        """
        return self.image_stack


#%%
if __name__ == "__main__":

    IP = "192.168.0.69"
    PORT = 50012

    DEFAULT_TIMEOUT = 1000

    from ifmO3r.ifm3dTiny.device import Device
    import time

    cam = Device(IP, PORT)

    fg = FrameGrabber(cam)
    im = ImageBuffer()
    fg.stream_on(im, 30)
    time.sleep(1)

    while True:
        if(next(im)):
            print(im.height)
            print(im.width)
            amp = im.amplitude_image()
            conf = im.confidence_image()
            xyz = im.xyz_image()
            print("-------------------------")
            print(amp[0:10])

    # fg.stream_on(im, TIMEOUT_LIVE)

    # for _ in range(6):
    #     time.sleep(0.5)
    #     next(im)
    #     print(im.amplitude_image())
# %%
