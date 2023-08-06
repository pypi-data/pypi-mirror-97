import logging
import struct
import numpy as np


class ImageEncoder(object):
    @staticmethod
    def layout(frame, amp, dist, conf, x, y, z, timestamp):
        logger = logging.getLogger(__file__)
        timestamp = np.uint(timestamp * 1e6)

        def encode(image, chunkType, pixelFormat):
            height, width = image.shape
            data = image.tobytes()
            assert len(data) % 4 == 0
            headerVersion = 1
            headerSize = 9 * 4
            chunkSize = len(data) + headerSize
            header = struct.pack("9I", chunkType, chunkSize, headerSize, headerVersion, width, height, pixelFormat, timestamp, frame)
            logger.debug(
                'header: { chunkType=%s, chunkSize=%s, headerSize=%s, headerVersion=%s, width=%s, height=%s, pixelFormat=%s, timestamp=%s, frame=%s }',
                chunkType, chunkSize, headerSize, headerVersion, width, height, pixelFormat, timestamp, frame
            )
            return header + data

        dist = np.clip(dist * 1000., 0, 65535).astype(np.uint16)
        amp = np.clip(amp * 65535. / 100., 0, 65535).astype(np.uint16)
        conf = np.clip(conf, 0, 255).astype(np.uint8)
        x = np.clip(x * 1000., -32767, 32767).astype(np.int16)
        y = np.clip(y * 1000., -32767, 32767).astype(np.int16)
        z = np.clip(z * 1000., -32767, 32767).astype(np.int16)

        chunks = [
            'star'.encode('ascii'),
            encode(dist, chunkType=100, pixelFormat=2),
            encode(amp, chunkType=101, pixelFormat=2),
            encode(conf, chunkType=300, pixelFormat=0),
            encode(x, chunkType=200, pixelFormat=3),
            encode(y, chunkType=201, pixelFormat=3),
            encode(z, chunkType=202, pixelFormat=3),
            'stop'.encode('ascii'),
        ]
        return b''.join(chunks)
