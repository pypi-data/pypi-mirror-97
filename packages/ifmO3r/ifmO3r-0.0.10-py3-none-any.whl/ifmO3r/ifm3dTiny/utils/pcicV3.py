import logging
from ifmO3r.ifm3dTiny.utils import sockets


class Formatter(object):
    @staticmethod
    def format(ticket, content):
        assert len(ticket) == 4, "<ticket> must be 4 digits 0-9"
        length = len(ticket) + len(content) + 2
        return "{}L{:09d}\r\n{}".format(ticket, length, ticket).encode('ascii')+content+"\r\n".encode('ascii')

    @staticmethod
    def send(sock, ticket, content):
        logger = logging.getLogger(__file__)
        if len(content) < 20:
            logger.debug('sending pcic: ticket="%s" content="%s"', ticket, content)
        else:
            logger.debug('sending pcic: ticket="%s" content="%s..."', ticket, content[:20])
        return sockets.send(sock, Formatter.format(ticket, content))


class Parser(object):
    @staticmethod
    def header(buffer):
        buffer = buffer.decode('ascii')
        assert buffer[4] == 'L' and buffer[14:16] == '\r\n', "expected <ticket>L[0-9]9<CR><LF>, but got %s" % buffer
        ticket, length = buffer[:4], int(buffer[5:14])
        return ticket, length

    @staticmethod
    def content(buffer, ticket):
        buffer = buffer.decode('ascii')
        assert buffer[:4] == ticket, "wrong ticket. expected %s, got %s" % (ticket, buffer[:4])
        assert buffer[-2:] == '\r\n', "data must end with <CR><LF>"
        content = buffer[4:-2]
        return content

    @staticmethod
    def parse(buffer):
        ticket, length = Parser.header(buffer[:16])
        content = Parser.content(buffer[16:], ticket)
        return ticket, content

    @staticmethod
    def recv(sock):
        buffer = sockets.recvall(sock, 16)
        ticket, length = Parser.header(buffer)
        buffer = sockets.recvall(sock, length)
        content = Parser.content(buffer, ticket)
        logger = logging.getLogger(__file__)
        if len(content) < 20:
            logger.debug('received pcic: ticket="%s" content="%s"', ticket, content)
        else:
            logger.debug('received pcic: ticket="%s" content="%s..."', ticket, content[:20])
        return ticket, content
