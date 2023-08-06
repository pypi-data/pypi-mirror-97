#!/usr/bin/env python
"""Communications support for test mocking.

This module provides support for dgram and streaming socket comminucations. It
is designed to be used within code controlled by the
`CleverSheep.Test.PollManager`.

"""
from __future__ import print_function

import six

import errno
import os
import socket
import ssl
import struct

from CleverSheep.Test import PollManager
from CleverSheep.Test.Tester import log

CallbackRef = PollManager.CallbackRef

readBlockSize = 4096 * 8
writeBlockSize = 4096 * 8


class Dgram(object):
    """A class to use datagrams communications.

    This basically wraps a ``socket.socket`` instance that is configured for
    datagrams (typically UDP) communications, to provide better support for
    mock objects.

    """

    def __init__(self, pollManager, peerName, bindAddr=None, peerAddr=None, onReceive=None):
        """Constructor:

        :Parameters:
          pollManager
            This is typically a `CleverSheep.Test.PollManager` instance, but
            could be something that provides the same interface.
          peerName
            The name of the peer entity that is expected to send or receive
            datagrams.
          bindAddr
            The address to bind to before starting to listen. This is a tuple
            of ``(ip-address, port)``. The ip-address may be an empty string,
            meaning 'localhost'.
          peerAddr
            The address of the peer entity that is expected to send or receive
            datagrams.
          onReceive
            An optional function to be invoked when input is received. The
            function is invoked as ``onReceive(self)``.
        """
        self.pollManager = pollManager
        self.peerName = peerName
        self.bindAddr = bindAddr
        self.peerAddr = peerAddr
        self.onReceiveCB = CallbackRef(onReceive)

        # TODO: Add error handling
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.bindAddr is not None:
            self.s.bind(bindAddr)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.setblocking(0)
            self.pollManager.addInputCallback(self.s, self.onReceive)
        self._fileno = self.s.fileno()

    def onReceive(self, fd, ev):
        """Invoked when a socket has received bytes.

        This simple invokes the ``onReceiveCB`` callback function, as
        ``onReceiveCB(self)``.

        """
        self.onReceiveCB(self)

    def read(self):
        """Read s single datagram."""
        try:
            p, self.lastAddr = self.s.recvfrom(65536)
        except socket.error as exc:
            if exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                p = None

        return p

    def send(self, bytes, count=None):
        """Send data to the peer.

        This simply sends the the string `bytes` to the peer.

        :Param bytes:
            The byte string containing the bytes to send.
        :Param count:
            If supplied and non-zero then only the first `count` bytes will be
            sent.
        """
        if self.s is None:
            return
        count = count or len(bytes)
        self.s.sendto(bytes[:count], self.peerAddr)

    def shutDown(self):
        # Remove the callback and close the listening socket.
        self.pollManager.removeInputCallback(self._fileno)
        self.s.close()


class Listener(object):
    """A class to listen for connections on a socket

    This basically wraps a ``socket.socket`` instance to provide better support
    for mock objects.

    Currently only AF_INET address family sockets are supported.
    """

    def __init__(self, pollManager, peerName, bindAddr, onConnect=None):
        """Constructor:

        :Param pollManager:
            This is typically a `PollManager` instance, but could be something
            that provides the same interface.
        :Param peerName:
            A name for the peer that is expected to connect this socket.
        :Param bindAddr:
            The address to bind to before starting to listen. This is a tuple
            if (ip-address, port). The ip-address may be an empty string, meaning
            'localhost'.
        :Param onConnect:
            A function to be invoked when a new connection is established.
        """
        self.pollManager = pollManager
        self.peerName = peerName
        self.bindAddr = bindAddr
        self.onConnectCB = CallbackRef(onConnect)

        # TODO: Add error handling
        self.s = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(bindAddr)
        except socket.error:
            raise
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.pollManager.addInputCallback(s, self.onConnect)
        self._sslParams = None
        self._fileno = self.s.fileno()

    def isSslConnection(self):
        return bool(self._sslParams)

    def useSSL(self, *args, **kwargs):
        kwargs['do_handshake_on_connect'] = False
        self._sslParams = (args, kwargs)

    def shutDown(self):
        # Remove the callback and close the listening socket.
        self.pollManager.removeInputCallback(self._fileno)
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def onConnect(self, fd, ev):
        """Handle a client trying to connect.

        This is invoked by the `PollManager` when a client tries to connect.
        """
        # TODO: Add error handling
        s, addr = self.s.accept()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self._sslParams is not None:
            args, kwargs = self._sslParams
            kwargs['do_handshake_on_connect'] = False
            kwargs['server_side'] = True
            s = ssl.wrap_socket(s, *args, **kwargs)

            # Do the handshaking while the socket is in blocking mode. In
            # theory you can do it in non-blocking mode, but I think there
            # is a nasty timing bug in Python's wrapper or some versions of
            # the SSL library itself.
            s.do_handshake()

        active, ret = self.onConnectCB(s, self.peerName, addr, self)
        if not active:
            # There is nothing to handle the new connection so we immediately
            # shut it down and close it.
            # TODO: Add error handling
            s.shutdown(socket.SHUT_RDWR)
            s.close()


class Connecter(object):
    """A class to establish a connections on a socket

    Currently only AF_INET address family sockets are supported.
    """

    def __init__(self, pollManager, peerName, peerAddr, connectTimes, onConnect=None, bindAddress=None,
                 maxErrorRetries=5, onError=None):
        """Constructor:

        :param pollManager:
            This is typically a `PollManager` instance, but could be something
            that provides the same interface.
        :param peerName:
            The name of the peer we are connecting to
        :param peerAddr:
            The address to bind to before starting to listen. This is a tuple
            if (ip-address, port). The ip-address may be an empty string,
            meaning 'localhost'.
        :param connectTimes:
            A tuple of ``(firstDelay, retryDelay)``, each is floating point
            value representing seconds. The first connection attempt will
            be made after ``firstDelay`` seconds. If that fails then
            connection attempts will be made every ``retryDelay`` seconds.
        :param onConnect:
            A callback function called when a connection has been established
        :param bindAddress:
            The address to bind to
        :param maxErrorRetries:
            The maximum number of times we will try to connect to a socket when
            errors occur - this includes attempts to ssl handshake
        :Param onError:
            Callback function to call on error
        """
        self.pollManager = pollManager
        self.peerName = peerName
        self.peerAddr = peerAddr
        self.onConnectCB = CallbackRef(onConnect)
        self._sslHandshaker = None
        self._useSSL = False

        self.error_callback = CallbackRef(onError)

        delay, self.retryPeriod = connectTimes
        self.maxErrorRetries = maxErrorRetries
        self.errorsOnConnection = 0
        self.sslHandshakeErrorsOnConnection = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setblocking(0)
        if bindAddress:
            self.s.bind(bindAddress)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _ = self.pollManager.addTimeout(delay, self.onTryconnect)
        self.tid = self.pollManager.addRepeatingTimeout(
                self.retryPeriod, self.onTryconnect)
        self._fileno = self.s.fileno()
        self._connected = False
        self._handshakeComplete = False

    def isSslConnection(self):
        return bool(self._sslHandshaker is not None)

    def useSSL(self, *args, **kwargs):
        kwargs['do_handshake_on_connect'] = False
        self.s = ssl.wrap_socket(self.s, *args, **kwargs)
        self._useSSL = True

    def _connectionFailed(self):
        error_count = self.sslHandshakeErrorsOnConnection + self.errorsOnConnection

        log.error(
            "%d errors have occurred when trying to connect,"
            " abandoning connection attempts",
            error_count
        )
        if self.error_callback is not None:
            self.error_callback()

        self.shutDown()

    def _setupConnection(self):
        try:
            self.s.connect(self.peerAddr)
            self._connected = True
        except socket.error as exc:
            code = exc.args[0]
            # EINPROGRESS is expected and does not count towards the errors
            if code != errno.EINPROGRESS:
                self.errorsOnConnection += 1
                log.warning(
                    "An exception occurred when trying to connect to %s:%s\nException was %s",
                    self.peerName,
                    self.peerAddr,
                    str(exc)
                )
                log.warning(
                    "Errors on conn %d, max errors %d",
                    self.errorsOnConnection,
                    self.maxErrorRetries
                )

    def _setupSSLHandshake(self):
        # Do the handshaking while the socket is in blocking mode. In
        # theory you can do it in non-blocking mode, but I think there
        # is a nasty timing bug in Python's wrapper or some versions of
        # the SSL library itself.
        try:
            self.s.setblocking(1)
            self.s.do_handshake()
            self.s.setblocking(0)
            self._handshakeComplete = True
        except ssl.SSLError as exc:
            self.sslHandshakeErrorsOnConnection += 1
            log.warning("SSL exception performing SSL handshake.\nException was %s", str(exc))
            log.warning(
                "Errors on conn %d, SSL handshake errors %d max errors %d",
                self.errorsOnConnection,
                self.sslHandshakeErrorsOnConnection,
                self.maxErrorRetries
            )

    def onTryconnect(self):
        """Invoked by the `PollManager` until a connection has been established
        or self.maxErrorRetries has been reached at which point we abandon
        trying to connect.

        If SSL is in use this function will continue to be invoked after we are connected until the
        SSL handshake completes or self.maxErrorRetries has been reached.

        :return None
        """
        if not self._connected:
            self._setupConnection()

            if not self._connected:
                # If we're still not connected check if we should give up and return
                if self.errorsOnConnection > self.maxErrorRetries:
                    # This will also remove the pollmanger timer so this function is no longer
                    # called
                    self._connectionFailed()

                return

        # We have a connection - do we need to do the ssl handshake
        if self._useSSL and not self._handshakeComplete:
            self._setupSSLHandshake()

            if not self._handshakeComplete:
                # Check if we should give up and return
                error_count = self.errorsOnConnection + self.sslHandshakeErrorsOnConnection
                if error_count > self.maxErrorRetries:
                    # This will also remove the pollmanger timer so this function is no longer
                    # called
                    self._connectionFailed()

                return

        # If we reach this point we're connected and have performed the handshake if required so
        # remove the timer
        self.pollManager.removeTimeout(self.tid)
        self.tid = None

        active, ret = self.onConnectCB(self.peerName, self)
        if not active:
            self.shutDown()

    def shutDown(self):
        """Remove the connection callback and close the socket.

        :return None
        """
        if self.tid is not None:
            self.pollManager.removeTimeout(self.tid)
            self.tid = None
        self.s.close()


class SocketConn(object):
    """A class to manage a socket connection.

    This basically wraps a ``socket.socket`` instance to provide better support
    for mock objects.

    Currently only AF_INET address family sockets are supported.
    """

    def __init__(self, s, peerName, pollManager, onReceive=None, onClose=None,
                 onError=None, native=False, addr=None, isSSL=False):
        """Constructor:

        :Parameters:
          s
            The active socket, as obtained from a call to the standard
            ``socket.socket``.
          peerName
            This should be a plain text string used to represent the peer
            entity at the other end of the socket. This name tends to get
            used in logging.
          pollManager
            The instance of `CleverSheep.Test.PollManager` to use provide
            events.
          onReceive
            An optional function to be invoked when input is received. The
            function is invoked as ``onReceive(self)``.
          onClose
            An optional function to be invoked when the socket is
            closed. The function is invoked as ``onClose(self)``.
          addr
            The peer's address if any.
          onError
            An optional function to be invoked when an exception occurs during
            a socket read. The function is invoked as ``onError(self, exc)``.
            Where ``exc`` is the exception that was handled.

            Note that EAGAIN and ECONNRESET do not cause this function to be
            invoked.
          native
            If set `True` then it assumed that the connection transmits in
            native (rather than network) byte order.

        """
        self.pollManager = pollManager
        self.s = s
        self._fileno = self.s.fileno()
        self.s.setblocking(0)
        self.peerName = peerName
        self.addr = addr
        self.onReceiveCB = CallbackRef(onReceive)
        self.onCloseCB = CallbackRef(onClose)
        self.onErrorCB = CallbackRef(onError)
        self.inBuf = six.b("")
        self.outBuf = six.b("")
        self.pollManager.addInputCallback(s, self._onInputActivity,)
        self._eofSeen = False
        self._native = native
        if isSSL:
            self._doRead = self.s.read
        else:
            self._doRead = self.s.recv

        # It seems that if some data has been sucked into the TCP stack quickly
        # enough then we get no file activity reported on the socket. This
        # initial read seems to sort things out.
        #
        # This seems wrong for a standard socket.
        self.pollManager.addCallback(self._doInitialRead, self.s.fileno())

    def _handleEOF(self):
        """Handle attempt to read from socket when EOF has occurred.

        This is invoked by the `._read` method when EOF has been seen and
        there is no buffered input data. It always invokes the onCloseCB and
        the first time it is called will remove callbacks and cleanly shutdown
        the socket.
        """
        self.onCloseCB(self)
        if self.s is not None:
            self.pollManager.removeOutputCallback(self._fileno)
            self.pollManager.removeInputCallback(self._fileno)
            try:
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
            except socket.error:
                pass  # We are really beyond caring!
            self.s = None

    def _read(self):
        """Read some or all available data."""
        # Read in a loop until no more input is available. We must do this or
        # an SSLSocket can stop causing select events.
        data = []
        if self.s is None:
            if not self.inBuf:
                self._handleEOF()
            return

        while True:
            got_eof = error = False
            try:
                s = self._doRead(readBlockSize)
                if not s:
                    got_eof = True
                    self._eofSeen = True
                    break
                data.append(s)
            except ssl.SSLError as exc:
                if exc.args[0] == ssl.SSLWantReadError:
                    break
                # Need to break on any ssl error, otherwise we end up in a busy loop.
                log.warning("SSL exception on read: %s", str(exc))

                break
            except socket.error as exc:
                if exc.args[0] == errno.ECONNRESET:
                    got_eof = True
                elif exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                    pass
                break

        if data:
            # We read some data, so update the input buffer. If we also got EOF
            # then that will be handled when this gets called next time around.
            self.inBuf += six.b("").join(data)

        elif got_eof:
            # The socket has been closed and we have no buffered data.
            if error:
                self.onErrorCB(self, error)
            self._handleEOF()

    def _onInputActivity(self, fd, ev):
        """Invoked when the socket has input activity.

        Basically this either means that there is data to read or the
        connection is shutting down. The latter case is indicated by a read
        attempt returning zero bytes.

        TODO: We can also get EAGAIN, but that is not yet handled.
        """
        self._read()
        if self.inBuf:
            active, ret = self.onReceiveCB(self)
            if not active:
                self.inBuf = six.b("")

    def _doInitialRead(self, fd):
        self._read()
        if self.inBuf:
            active, ret = self.onReceiveCB(self)
            if not active:
                self.inBuf = six.b("")

    def read(self):
        """Read all the data in the input buffer.

        The buffer is cleared.
        """
        s, self.inBuf = self.inBuf, six.b("")
        return s

    def peek(self):
        """Peek at the data in the input buffer."""
        return self.inBuf

    def readMsg(self):
        """Read a complete message from the input buffer.

        The read bytes are removed from the input buffer.

        Note this can ONLY be used if the messages have headers, if they do not
        use the read function.

        +---+---+---+---+---+--- ... ---+---+
        |    Length     |      Payload      |
        +---+---+---+---+---+--- ... ---+---+

        |<-------------- Length ----------->|
        """
        if len(self.inBuf) < 4:
            return None

        buf = self.inBuf
        if self._native:
            (msgLen,) = struct.unpack("=L", buf[:4])
        else:
            (msgLen,) = struct.unpack("!L", buf[:4])
        if len(buf) < msgLen:
            return None

        msg, self.inBuf = buf[:msgLen], buf[msgLen:]
        return msg

    def send(self, bytes, count=None):
        """Send data to the peer.

        This simply sends (and logs) the the string `bytes` to the peer.

        Currently this only supports TCP. In the future it should support UDP
        as well; there is no plan to add a ``sendto`` method.

        :Param bytes:
            The string containing the bytes to send.
        :Param count:
            If supplied and non-zero then only the first `count` bytes will be
            sent.
        """
        if self.s is None:
            return
        count = count or len(bytes)
        already_sending = bool(self.outBuf)
        self.outBuf += bytes[:count]
        if not already_sending:
            ret = self.pollManager.addOutputCallback(self.s, self._onTryToSend)
            if ret == -1:
                # The socket has become unusable - the peer probably shut it
                # down.
                try:
                    self.pollManager.addTimeout(0,0, self.onCloseCB, self)
                    self.s.shutdown(socket.SHUT_RDWR)
                    self.s.close()
                except socket.error:
                    pass # We are really beyond caring!
                self.s = None
                return

        # Try poking things. so we detect socket shutdown earlier rather than
        # later.
        self._onTryToSend(None, None)

    def _doSend(self):
        must_close = error = False
        sent = 0
        try:
            sent = self.s.send(self.outBuf[:writeBlockSize])
        except socket.error as exc:
            if exc.args[0] == errno.ECONNRESET:
                # A clean close.
                must_close = True
            elif exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                pass
            else:
                # A non-clean close.
                must_close = True
                error = exc
                log.warning("Failed to send %s", exc)

        if sent:
            self.outBuf = self.outBuf[sent:]
        return sent, must_close, error

    def _onTryToSend(self, fd, ev):
        while True and self.outBuf:
            sent, mustClose, error = self._doSend()

            if mustClose:
                # If the connection has closed, ...
                if error:
                    self.pollManager.addTimeout(0.0, self.onErrorCB, self,
                            error)
                self.pollManager.addTimeout(0.0, self.onCloseCB, self)
                self.pollManager.removeOutputCallback(self._fileno)
                self.pollManager.removeInputCallback(self._fileno)
                self.outBuf = six.b("")
                try:
                    self.s.shutdown(socket.SHUT_RDWR)
                    self.s.close()
                except socket.error:
                    pass # We are really beyond caring!
                self.s = None

            if sent == 0:
                break

        if not self.outBuf:
            self.pollManager.removeOutputCallback(self._fileno)

    # TODO: Should deregister as well.
    def shutDown(self, v=socket.SHUT_RDWR):
        self.pollManager.removeInputCallback(self._fileno)
        if self.s is None:
            return
        try:
            return self.s.shutdown(v)
        except socket.error:
            pass
        self.s.close()
    shutdown = shutDown

    def close(self):
        try:
            return self.s.close()
        except IOError:
            pass


class PipeConn(object):
    """A class to manage a pipe connection.

    This basically wraps an open pipe instance to provide better support
    for mock objects.
    """

    def __init__(self, isWrite, pipePath, peerName, pollManager, onReceive=None, onClose=None, onError=None,
                 native=False, addMsgLengthOnSend=False):
        """Constructor:

        :Parameters:
          isWrite
            Set to ``True`` if the pipe is to be written to and ``False``
            for a pipe that should be read from.
          pipePath
            The name of the pipe file to be opened.
          peerName
            The name of the peer entity that is expected to send or receive
            data.
          pollManager
            This is typically a `CleverSheep.Test.PollManager` instance, but
            could be something that provides the same interface.
          onReceive
            An optional function to be invoked when input is received. The
            function is invoked as ``onReceive(self)``.
          onClose
            An optional function to be invoked when the socket is closed. The
            function is invoked as ``onClose(self)``.
          onError
            An optional function to be invoked when an exception occurs during
            a socket read. The function is invoked as ``onError(self, exc)``.
            Where ``exc`` is the exception that was handled.

            Note that EAGAIN and ECONNRESET do not cause this function to be
            invoked.
          native
            If set `True` then it assumed that the connection transmits in
            native (rather than network) byte order.
          addMsgLengthOnSend
            Should the length of the message being send be added in front of
            the message itself, only affects send operations.
        """
        self.pollManager = pollManager
        self.pipeF = None
        self.pipePath = pipePath
        self.peerName = peerName
        self.isWrite = isWrite
        self.onReceiveCB = CallbackRef(onReceive)
        self.onCloseCB = CallbackRef(onClose)
        self.onErrorCB = CallbackRef(onError)
        self.inBuf = six.b("")
        self.outBuf = six.b("")
        self._native = native
        self._msgHeader = addMsgLengthOnSend
        self._fileno = None

        # Try to open the pipe
        self.tryOpen()

    def tryOpen(self):
        """Try to open the pipe if it is not open already

        :return: Was the pipe opened?
        """
        if self.pipeF is not None:
            return True

        try:
            if self.isWrite:
                fd = os.open(self.pipePath, os.O_WRONLY | os.O_NDELAY)
                self.pipeF = os.fdopen(fd, "wb")
                self._fileno = self.pipeF.fileno()
                return True
            else:
                fd = os.open(self.pipePath, os.O_RDONLY | os.O_NDELAY)
                self.pipeF = os.fdopen(fd, "rb")
                self._fileno = self.pipeF.fileno()
                self.pollManager.addInputCallback(self.pipeF,
                    self._onInputActivity,)
                return True
        except (OSError, IOError) as exc:
            log.error("Failed to open Pipe %s, error: %s", self.pipePath, exc)

        return False

    def tryRead(self):
        try:
            if self._fileno is None:
                self.tryOpen()
            s = self.pipeF.read(readBlockSize)
        except (OSError, IOError) as exc:
            if exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                raise
            self.pollManager.removeInputCallback(self._fileno)
            s = None
            try:
                self.pipeF.close()
            except (OSError, IOError):
                pass
            self.pipeF = None
        return s

    def _onInputActivity(self, fd, ev):
        """Invoked when the socket has input activity.

        Basically this either means that there is data to read or the
        connection is shutting down. The latter case is indicated by a read
        attempt returning zero bytes.
        """
        must_close = error = False
        try:
            s = self.tryRead()
            if not s:
                must_close = True
        except (IOError, OSError) as exc:
            if exc.args[0] == errno.ECONNRESET:
                must_close = True

            elif exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                # This can happen, even though this method is only called
                # when the socket supposedly has data ready to read.
                return

            else:
                # A non-clean close.
                must_close = True
                error = exc
                log.warning("Failed to read, closing connection: %s", exc)

        if must_close:
            # If the connection has closed, ...
            if error:
                self.onErrorCB(self, error)
            self.onCloseCB(self)
            self.pollManager.removeOutputCallback(self._fileno)
            self.pollManager.removeInputCallback(self._fileno)
            self.outBuf = six.b("")
            try:
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
            except socket.error:
                pass # We are really beyond caring!
            self.s = None
            return

        self.inBuf += s
        active, ret = self.onReceiveCB(self)
        if not active:
            self.inBuf = six.b("")

    def read(self):
        """Read all the data in the input buffer.

        The buffer is cleared.
        """
        s, self.inBuf = self.inBuf, six.b("")
        return s

    def peek(self):
        """Peek at the data in the input buffer."""
        return self.inBuf

    def readMsg(self):
        """Read a complete message from the input buffer.

        The read bytes are removed from the input buffer.

        Note this can ONLY be used if the messages have headers, if they do not
        use the read function

        +---+---+---+---+---+--- ... ---+---+
        |    Length     |      Payload      |
        +---+---+---+---+---+--- ... ---+---+

                        |<---- Length ----->|
        """
        if len(self.inBuf) < 4:
            return None

        buf = self.inBuf
        if self._native:
            (msgLen,) = struct.unpack("=L", buf[:4])
        else:
            (msgLen,) = struct.unpack("!L", buf[:4])

        msgLen += 4
        if len(buf) < msgLen:
            return None

        msg, self.inBuf = buf[:msgLen], buf[msgLen:]
        return msg

    def send(self, bytes, count=None):
        """Send data to the peer.

        This simply sends (and logs) the the string `bytes` to the peer.

        Currently this only supports TCP. In the future it should support UDP
        as well; there is no plan to add a ``sendto`` method.

        :Param bytes:
            The string containing the bytes to send.
        :Param count:
            If supplied and non-zero then only the first `count` bytes will be
            sent.
        """
        count = count or len(bytes)
        if self._msgHeader:
            if self._native:
                hdr = struct.pack("=L", count)
            else:
                hdr = struct.pack("!L", count)
        else:
            hdr = six.b("")

        already_sending = bool(self.outBuf)
        self.outBuf += hdr
        self.outBuf += bytes[:count]
        if not self.tryOpen():
            return

        if not already_sending:
            ret = self.pollManager.addOutputCallback(self.pipeF,
                                                     self._onTryToSend)
            if ret == -1:
                # The pipe has become unusable - the peer probably shut it
                # down.
                log.debug("Failed to send, connection assumed closed by peer")
                try:
                    self.pipeF.close()
                except IOError:
                    pass  # We are really beyond caring!

                return

        # Try poking things. so we detect pipe closure earlier rather than
        # later.
        self._onTryToSend(None, None)

    def _onTryToSend(self, fd, ev):
        must_close = False
        sent = 0
        try:
            sent = os.write(self.pipeF.fileno(), self.outBuf[:1024])
        except (IOError, OSError) as exc:
            if exc.args[0] in (errno.EAGAIN, errno.EWOULDBLOCK):
                return
            else:
                # A non-clean close.
                must_close = True
                log.warning("Failed to send, closing connection: %s", exc)

        if must_close:
            # If the connection has closed, ...
            self.pollManager.removeOutputCallback(self._fileno)
            self.pollManager.removeInputCallback(self._fileno)
            self.outBuf = six.b("")
            try:
                self.pipeF.close()
            except (IOError, OSError):
                pass # We are really beyond caring!
            self.pipeF = None
            return

        self.outBuf = self.outBuf[sent:]
        if not self.outBuf:
            self.pollManager.removeOutputCallback(self.pipeF)

    def shutDown(self):
        if self._fileno is not None:
            self.pollManager.removeInputCallback(self._fileno)
        else:
            log.warning("The pipe %s was never successfully opened", self.pipePath)
    shutdown = shutDown

    def close(self):
        try:
            return self.pipeF.close()
        except IOError:
            pass
