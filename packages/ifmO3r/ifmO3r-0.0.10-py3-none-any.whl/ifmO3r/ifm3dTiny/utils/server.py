import socket
import threading
import logging
import logging.handlers
import argparse
from queue import Queue, Empty, Full
import select
import time

from ifmO3r.ifm3dTiny.utils.encoding import ImageEncoder
from ifmO3r.ifm3dTiny.utils.pcicV3 import Parser, Formatter


class PCICServer(threading.Thread):
    def __init__(self, address='0.0.0.0', port=50012):
        threading.Thread.__init__(self, name='PCICServer')
        self.address = address
        self.port = port
        self.queue = Queue(maxsize=100)
        self.async_output = False
        self._run = True

    def send(self, frame_count, amp, dist, conf, x, y, z, timestamp=None):
        timestamp = time.process_time() if timestamp is None else timestamp
        if self.async_output and self._run:
            try:
                logging.debug('putting frame %s into queue', frame_count)
                # do not block if queue is full
                self.queue.put((frame_count, amp, dist, conf, x, y, z, timestamp), timeout=0.001)
            except Full:
                # remove 90% of full queue
                self.drain_queue(keep=int(self.queue.qsize()/10))

    def run(self):
        logger = logging.getLogger(__file__)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.address, self.port))
        sock.listen(1)
        while self._run:
            self.set_async_output(False)
            self.drain_queue()
            logger.info('waiting for a connection on %s:%s', self.address, self.port)
            while self._run:
                ready, _, _ = select.select([sock],[],[],1) # timeout set to 1 second
                if ready:
                    break
            if not self._run:
                break
            client, client_address = sock.accept()

            try:
                logger.info('connection from %s', client_address)
                self.set_async_output(True)
                while self._run:
                    if select.select([client], [], [], 0.0001)[0]:
                        ticket, command = Parser.recv(client)
                        response = self.handle(command).encode('ascii')
                        Formatter.send(client, ticket, response)
                    else:
                        try:
                            response = ImageEncoder.layout(*self.queue.get(timeout=0.0001))
                            Formatter.send(client, "0000", response)
                        except Empty:
                            pass

            except Exception as ex:
                logging.exception("server error")

            finally:
                logger.info('closed connection to %s', client_address)
                client.close()

        logger.debug('finishing server')
        self.set_async_output(False)
        self.drain_queue()

    def handle(self, command):
        if command[0] == 'p':
            if len(command) != 2:
                return '?'
            if command[1] == '0':
                self.set_async_output(False)
                return '*'
            # default = turn output on
            self.set_async_output(True)
            return '*'
        # return OK for every other command that we don't handle
        return '*'

    def drain_queue(self, keep=0):
        try:
            while self.queue.qsize() > keep:
                self.queue.get(timeout=0.001)
        except Empty:
            return

    def set_async_output(self, value):
        logger = logging.getLogger(__file__)
        logger.debug('async_output = %s', bool(value))
        self.async_output = bool(value)

    def stop(self):
        logger = logging.getLogger(__file__)
        logger.info('stopping server')
        self._run = False
        self.join()
        logger.debug('server stopped')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def setup_logger(level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(level)

    fileHandler = logging.handlers.WatchedFileHandler('server.log')
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


def main():
    parser = argparse.ArgumentParser(description='ifm PCIC Server')
    parser.add_argument('-ip', type=str, default='0.0.0.0', help='listen address')
    parser.add_argument('-port', type=int, default=50012, help='listen port')
    parser.add_argument('-loglevel', type=str, default='DEBUG', help='log level to use')
    args = parser.parse_args()

    setup_logger(args.loglevel)

    server = PCICServer(args.ip, args.port)
    server.run()


if __name__ == "__main__":
    main()
