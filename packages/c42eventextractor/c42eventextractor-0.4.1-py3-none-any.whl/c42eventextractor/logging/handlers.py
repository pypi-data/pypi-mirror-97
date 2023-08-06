import socket
from logging.handlers import SysLogHandler


class NoPrioritySysLogHandler(SysLogHandler):
    """
    Overrides the default implementation of SysLogHandler to not send a <PRI> at the
    beginning of the message. Most CEF consumers seem to not expect the <PRI> to be
    present in CEF messages. Attach to a logger via `.addHandler` to use.

    Args:
        hostname: The hostname of the syslog server to send log messages to.
        port: The port of the syslog server to send log messages to.
        protocol: The protocol over which to submit syslog messages. Accepts TCP or UDP.
    """

    def __init__(self, hostname, port=514, protocol="UDP"):
        socket_type = _get_socket_type_from_protocol(protocol.lower().strip())
        super(NoPrioritySysLogHandler, self).__init__(
            address=(hostname, port), socktype=socket_type
        )

    def emit(self, record):
        try:
            msg = self.format(record) + "\n"
            msg = msg.encode("utf-8")
            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except (socket.error, OSError):
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except:
            self.handleError(record)


class NoPrioritySysLogHandlerWrapper(object):
    """
    Uses NoPrioritySysLogHandler but does not make the connection in the constructor. Instead,
    it connects the first time you access the handler property. This makes testing against
    a syslog handler easier.

    Args:
        hostname: The hostname of the syslog server to send log messages to.
        port: The port of the syslog server to send log messages to.
        protocol: The protocol over which to submit syslog messages. Accepts TCP or UDP.
    """

    def __init__(self, hostname, port=514, protocol="UDP"):
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        self._handler = None

    @property
    def handler(self):
        if not self._handler:
            self._handler = NoPrioritySysLogHandler(self.hostname, self.port, self.protocol)
        return self._handler


def _get_socket_type_from_protocol(protocol):
    socket_type = None
    if protocol == "tcp":
        socket_type = socket.SOCK_STREAM
    elif protocol == "udp":
        socket_type = socket.SOCK_DGRAM

    if socket_type is None:
        msg = "Could not determine socket type. Expected TCP or UDP, got {0}".format(protocol)
        raise ValueError(msg)

    return socket_type
