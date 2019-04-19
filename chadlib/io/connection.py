from logging    import getLogger
from queue      import Queue
from selectors  import DefaultSelector, EVENT_READ
from socket     import socket, SO_REUSEADDR, SOL_SOCKET
from struct     import calcsize, pack, unpack
from threading  import Lock, Thread
from time       import sleep


class Connection:
    """
    Provides an interface to a multi-threaded socket that handles network I/O 
    without blocking the execution of the main program.
    """

    HEADER_VERSION = 1
    HEADER_PACK_STR = "II"      # version, length
    HEADER_SIZE = calcsize(HEADER_PACK_STR)

    CONNECT_ATTEMPTS = 3
    SELECT_TIMEOUT_INTERVAL = 0.3

    def __init__(self):
        """
        Put the connection in an uninitialized, inactive, state.
        TODO CJR:  pass in the queues so they are owned by the application state
        """
        self.socket = None
        self.socket_lock = None
        self.send_queue = None
        self.receive_queue = None

    @property
    def active(self):
        """
        Boolean property that is true if the socket has an active connection, 
        false otherwise.
        """
        return self.socket is not None

    def startup_accept(self, port):
        """
        Start a listening thread to wait on an incoming connection.
        """
        self._create_and_run_thread(self._wait_for_connection, (port,))
    
    def startup_connect(self, port, ip_address):
        """
        Start a connecting thread to connect to another socket.
        """
        self._create_and_run_thread(self._connect_to_peer, (port, ip_address))

    def _create_and_run_thread(self, thread_target, thread_args):
        """
        Create a thread with the given target and arguments.
        """
        if not self.active:
            t = Thread(target = thread_target, args = thread_args)
            t.start()

    def _wait_for_connection(self, port, *args):
        """
        Open a listening socket to wait for incoming peer connection.

        TODO CJR:  Applications can lock up endlessly here if windows are 
        closed while waiting for a connection.  I should have some mechanism in 
        close to force this to end.
        """
        getLogger(__name__).info("Waiting for connection on port {}..."
                                    .format(port))
        listener = self._create_new_socket()
        listener.bind(("", port))
        listener.listen(1)
        conn, addr = listener.accept()

        self._set_socket(conn)
        getLogger(__name__).info("Connected to peer at {}:{}"
                                    .format(addr[0], addr[1]))

    def _connect_to_peer(self, port, ip_address):
        """
        Create a socket and attempt to connect to a waiting peer.
        """
        getLogger(__name__).info("Attempting to connect to peer {}:{}..."
                                    .format(ip_address, port))
        conn = self._create_new_socket()
        connected = False

        for i in range(self.CONNECT_ATTEMPTS):
            try:
                conn.connect((ip_address, port))
                connected = True
                break
            except (ConnectionRefusedError, OSError):
                getLogger(__name__).info("Attempt {}/{} failed"
                                            .format(i + 1, self.CONNECT_ATTEMPTS))
                if i < self.CONNECT_ATTEMPTS:
                    sleep(i + 1)

        if connected:
            self._set_socket(conn)
            getLogger(__name__).info("Connection established")
        else:
            getLogger(__name__).info(("Connection could not be established."))

    def _set_socket(self, socket):
        """
        Change any options needed to the socket and initialize the other data 
        structures needed for sending and receiving.
        """
        socket.setblocking(False)
        self.socket = socket
        self.socket_lock = Lock()
        self.send_queue = Queue()
        self.receive_queue = Queue()
        # TODO CJR: move this from here, I want separate logic for setting 
        # up a connection and starting to process it.  I already need a place 
        # to call start_data_processing
        self.start()        

    def _create_new_socket(self):
        """
        Return a socket with the re-use option set.
        """
        sock = socket()
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        return sock

    def start(self):
        """
        Begin the sending and receiving threads for normal operation.
        """
        if self.active:
            Thread(target = self._send).start()
            Thread(target = self._receive).start()

    def close(self):
        """
        Release resources held by the connection, putting it back into an 
        uninitialized state.
        """
        if self.active:
            self.socket.close()
            with self.socket_lock:
                self.socket = None
            self.socket_lock = None

            # enqueue messages to close blocking send thread and controller
            # get thread from their blocking get calls
            self.send_queue.put(None)
            self.receive_queue.put(None)

            self.send_queue = None
            self.receive_queue = None

            getLogger(__name__).info("Connection closed.")

    def add_to_send_queue(self, data):
        """
        Add the given data to the queue to be sent.
        """
        result = False
        if self.active:
            self.send_queue.put(data)
            result = True
        return result

    def get_incoming_data(self):
        """
        Blocking get from the receive queue, returns None if the connection is 
        not active.
        """
        result = None
        if self.active:
            result = self.receive_queue.get()
        return result

    def start_data_processing(self, processing_callback):
        """
        Create a thread to service the receive queue with the given callback.
        """
        def f():
            while self.active:
                data = self.get_incoming_data()
                if data is not None:
                    processing_callback(data)
        Thread(target = f).start()

    def _send(self):
        """
        Loop retrieving data from the send queue and sending it on the socket.
        """
        while self.active:
            try:
                data = self._get_data_from_send_queue()
                if self.socket is not None:
                    header = self._create_data_header(data)
                    with self.socket_lock:
                        self.socket.sendall(header + data)
            except Exception as err:
                getLogger(__name__).debug(("Unexpected exception occurred,"
                                " send thread may be in a corrupted state\n"
                                "Error: {}".format(err)))

    def _get_data_from_send_queue(self):
        """
        Retrieve data from the queue.  If there is more than a single item, 
        retrieve multiple pieces of data to improve throughput.

        The queue is not guaranteed to be empty after this method, because of 
        multi-processing new items could be enqueued between the size check 
        and the creation of the data list.
        """
        size = self.send_queue.qsize()
        if size > 1:
            data = b''.join([self.send_queue.get() for _ in range(size)])
        else:
            data = self.send_queue.get()
        return data

    def _receive(self):
        """
        Continuously read data from the socket and put it on the receive queue.
        """
        selector = DefaultSelector()
        selector.register(self.socket, EVENT_READ)

        while self.active:
            try:
                val = selector.select(self.SELECT_TIMEOUT_INTERVAL)
                if val:
                    with self.socket_lock:
                        header = self.socket.recv(self.HEADER_SIZE)
                    if header:
                        data = self._read_data(header)
                        self.receive_queue.put(data)
                    else:           # connection closed from other end
                        self.close()
            except Exception as err:
                getLogger(__name__).debug(("Unexpected exception occurred,"
                            " receive thread may be in a corrupted state\n"
                            "Error: {}".format(err)))

    def _create_data_header(self, data):
        """
        Create a bytes header for variable-sized data messages.
        """
        return pack(self.HEADER_PACK_STR, self.HEADER_VERSION, len(data))

    def _read_data(self, header):
        """
        Use the header to read the body of the message from the socket.
        """
        _, msg_size = unpack(self.HEADER_PACK_STR, header)
        with self.socket_lock:
            data = self.socket.recv(msg_size)
        return data