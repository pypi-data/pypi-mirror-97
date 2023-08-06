"""
Author: ifm CSR

This is a helper script: it contains useful functions (TBD)


:hostPCICserver         :   This function creates a PCICv3 server anf forwards the provided data to a viewer.
"""
# %%
import sys, getopt, os
import numpy as np
# %%
class GetCallableMethods:
    def get_methods(self, obj):
        """
        Provides a list of all callable functions within an object.
        Callable non callable is defined by _ and __
        :obj:   Object to get functions from
        :return:str_method_list:    List of callable functions
        """
        method_list = [
            func
            for func in dir(obj)
            if callable(getattr(obj, func))
            and not func.startswith("__")
            and not func.startswith("_")
        ]

        str_method_list = "\r\n".join(method_list)
        return str_method_list

# %%
def getCmdArgs():
    """
    Get the command line arguments, if none are passed,, set to default:
        ip: the IP address of the VPU (default 192.168.0.69)
        port: the port of the used head (default 50010)
    """
    address = None
    port = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ip=", "port="])
    except getopt.GetoptError:
        print("script.py [--ip <IP ADRESS> --port <PORT NUMBER>]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "--ip":
            address = arg
        if opt == "--port":
            port = arg
    if address == None:
        address = "192.168.0.69"
    if port == None:
        port = 50010
    return address, port


def _send_data(im, server, i):
    xyz = im.xyz_image()
    amp = im.amplitude_image()
    dist = im.distance_image()
    conf = im.confidence_image()

    server.send(i, amp, dist, conf, xyz[0], xyz[1], xyz[2])

def _send_data_2heads(im1, im2, server, i):
    """
    stream data of two heads
    :param im1: image buffer 1
    :param im2: image buffer 2
    :param server: PCIC server
    :param i: image counter
    :return:
    """
    xyz1 = im1.xyz_image()
    amp1 = im1.amplitude_image()
    dist1 = im1.distance_image()
    conf1 = im1.confidence_image()

    xyz2 = np.flip(im2.xyz_image(), (1,2))
    amp2 = np.flip(im2.amplitude_image(), (0,1))
    dist2 = np.flip(im2.distance_image(),(0,1))
    conf2 = np.flip(im2.confidence_image(), (0,1))

    #one line rot matrix
    beta = -84*(np.pi/180)
    R_beta = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])

    gamma = 180*(np.pi/180)
    R_gamme = np.array([[np.cos(gamma), np.sin(gamma), 0], [np.sin(gamma), np.cos(gamma), 0], [0, 0, 1]])

    # one line trans
    # one line of multiplication + addition

    xyz2_rot = np.matmul(np.matmul(R_gamme, R_beta), np.reshape(xyz2, (3, 172*224)))
    xyz2_rot = np.reshape(xyz2_rot, (3,172,224))

    amp = np.concatenate((amp1[:, :215], amp2[:, 9:]), 1)
    dist = np.concatenate((dist1[:, :215], dist2[:, 9:]), 1)
    conf = np.concatenate((conf1[:, :215], conf2[:, 9:]), 1)
    x = np.concatenate((xyz1[0,:, :215],  xyz2_rot[0,:,9:]), 1)
    y = np.concatenate((xyz1[1,:, :215],  xyz2_rot[1,:,9:]+0.1), 1)
    z = np.concatenate((xyz1[2,:, :215],  xyz2_rot[2,:,9:]-0.08), 1)

    server.send(i, amp, dist, conf, x, y, z)


# %%
def hostPCICserver(ip='192.168.0.69',port=50012):
    """
    This function creates a server and forwards frame data (amplitude, distance, etc.)
    with the needed chunk header, etc. to any connected client. Typically, the B-sample
    viewer is the client.

    :ip     :   IP address of the VPU
    :port   :   Port number (e.g. 50012) of the head
    """
    from ifmO3r.ifm3dTiny import FrameGrabber, ImageBuffer, Device, StatusLogger
    from ifmO3r.ifm3dTiny.utils.server import PCICServer

    log = StatusLogger('hostPCICserver')
    device = Device(ip, port)
    fg = FrameGrabber(device)
    im = ImageBuffer()

    timeout = 25 # Fairly high due to VM delays
    fg.stream_on(im, timeout)
    import time
    time.sleep(1) # give the framegrabber time to get some frames

    with PCICServer(port=port) as server:
        i = 0
        while True:
            if next(im):
                _send_data(im, server, i)
                log.info(f"Frame count: {i}")
                i += 1

def hostPCICserver_2Heads(ip='192.168.0.69',port1=50012, port2=50013):
    """
    This function creates a server and forwards frame data (amplitude, distance, etc.)
    with the needed chunk header, etc. to any connected client. Typically, the B-sample
    viewer is the client.

    :ip:   IP address of the VPU
    :port1: Port number head 1 (e.g. 50012)
    :port2: Port number head 2

    """
    from ifmO3r.ifm3dTiny import FrameGrabber, ImageBuffer, Device, StatusLogger
    from ifmO3r.ifm3dTiny.utils.server import PCICServer

    log = StatusLogger('hostPCICserver_2Heads.log')
    device1 = Device(ip, port1)
    device2 = Device(ip, port2)

    # 2 frame grabber and image buffers
    fg1 = FrameGrabber(device1)
    im1 = ImageBuffer()
    fg2 = FrameGrabber(device2)
    im2 = ImageBuffer()

    timeout = 25 # Fairly high due to VM delays

    with PCICServer(port=port1) as server:
        i = 0
        while True:
            fg1.wait_for_frame(im1, timeout)
            fg2.wait_for_frame(im2, timeout)
            _send_data_2heads(im1, im2, server, i)
            log.info(f"Frame count: {i}")
            i += 1

# %%
if __name__ == "__main__":
    hostPCICserver_2Heads()
    # import ifmO3rViewer.startViewer as v
    # v.start()

# >>> from ifmO3r.ifm3dTiny import ImageBuffer, FrameGrabber
# >>> from ifmO3r.ifm3dTiny import ImageBuffer, FrameGrabber, ParamHandler
# >>> device = ParamHandler('192.168.0.69',50012)
# >>> fg = FrameGrabber(device)
# >>> im = ImageBuffer()
# >>> from ifmO3r.ifm3dTiny.utils import utils
# >>> utils.background_viewer()

# %%
