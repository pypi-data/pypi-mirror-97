import logging
import select


def send(sock, data):
    logger = logging.getLogger(__file__)
    logger.debug('sending data: %s', data[:min(len(data), 20)])
    return sock.sendall(data)


def recv(sock, buflen=4096, timeout=None):
    logger = logging.getLogger(__file__)
    if timeout is None:
        data = sock.recv(buflen)
        logger.debug('received data: %s', data[:min(len(data), 20)])
        return data
    else:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            return recv(sock, buflen=buflen, timeout=None)
        else:
            return None


def recvall(sock, size):
    logger = logging.getLogger(__file__)
    data = bytearray()
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data.extend(packet)
    logger.debug('received data: %s', data[:min(len(data), 20)])
    return data

