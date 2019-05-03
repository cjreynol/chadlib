from abc                import abstractmethod
from logging            import getLogger
from threading          import Thread

from chadlib.io         import Connection

from .controller_base   import ControllerBase
from .text_entry_dialog import TextEntryDialog


class ConnController(ControllerBase):
    
    def __init__(self, default_port, send_queue, receive_queue, *args):
        super().__init__(*args)

        self.default_port = default_port
        self.receive_queue = receive_queue

        self.connection = Connection(self, send_queue, self.receive_queue)

    def startup_listening(self):
        self.connection.startup_accept(self.default_port)

    def startup_connect(self, ip_address):
        self.connection.startup_connect(self.default_port, ip_address)

    def disconnect(self):
        self.connection.close()

    # disconnected from method?

    def get_ip(self):
        """
        Requests the IP address to connect to, and passes it to that method.
        """
        TextEntryDialog("Enter IP address of host", self.startup_connect, None)

    def start_processing_receive_queue(self):
        """
        Start up the thread to decode drawings and put them on the drawing 
        queue.
        """
        self.application_state.active = True
        def f():
            getLogger(__name__).debug("Process thread starting.")
            while self.application_state.active:
                data = self.receive_queue.get()
                if data is not None:
                    self.process_received_data(data)
            getLogger(__name__).debug("Process thread done.")
        Thread(target = f).start()

    @abstractmethod
    def process_received_data(self, data):
        """
        Overridden by subclasses to handle data from the receive queue.
        """
        pass

    def stop(self):
        super().stop()
        self.connection.close()

    def get_menu_data(self):
        """
        Get the default menu setup data, add network control commands.
        """
        menu_setup = super().get_menu_data()
        menu_setup.add_submenu_items("Network", 
                                [("Host", self.startup_listening, "Alt-h"),
                                ("Connect", self.get_ip, "Alt-c"),
                                ("Disconnect", self.disconnect, "Alt-d")])
        return menu_setup
