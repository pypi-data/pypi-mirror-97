# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

from unittest import mock


class MocketPool:
    SOCK_STREAM = 0

    def __init__(self):
        self.getaddrinfo = mock.Mock()
        self.socket = mock.Mock()


class Mocket:
    def __init__(self, response):
        self.settimeout = mock.Mock()
        self.close = mock.Mock()
        self.connect = mock.Mock()
        self.send = mock.Mock(side_effect=self._send)
        self.readline = mock.Mock(side_effect=self._readline)
        self.recv = mock.Mock(side_effect=self._recv)
        self.recv_into = mock.Mock(side_effect=self._recv_into)
        self._response = response
        self._position = 0
        self.fail_next_send = False

    def _send(self, data):
        if self.fail_next_send:
            self.fail_next_send = False
            return 0
        return len(data)

    def _readline(self):
        i = self._response.find(b"\r\n", self._position)
        r = self._response[self._position : i + 2]
        self._position = i + 2
        return r

    def _recv(self, count):
        end = self._position + count
        r = self._response[self._position : end]
        self._position = end
        return r

    def _recv_into(self, buf, nbytes=0):
        assert isinstance(nbytes, int) and nbytes >= 0
        read = nbytes if nbytes > 0 else len(buf)
        remaining = len(self._response) - self._position
        if read > remaining:
            read = remaining
        end = self._position + read
        buf[:read] = self._response[self._position : end]
        self._position = end
        return read


class SSLContext:
    def __init__(self):
        self.wrap_socket = mock.Mock(side_effect=self._wrap_socket)

    def _wrap_socket(self, sock, server_hostname=None):
        return sock
