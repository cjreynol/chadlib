from logging            import getLogger
from threading          import Thread

from chadlib.io         import Connection

from .conn_controller   import ConnController
from .text_entry_dialog import TextEntryDialog


class ConnComponent:
    
    def __init__(self, controller, default_port, send_queue, receive_queue):
        self.controller = controller
        if not isinstance(self.controller, ConnController):
            raise RuntimeError("Controller does not implement the required "
                                "ConnController interface.")

        self.default_port = default_port
        self.receive_queue = receive_queue

        self.connection = Connection(self, send_queue, self.receive_queue)

    def startup_listening(self):
        self.connection.startup_accept(self.default_port)

    def startup_connect(self, ip_address):
        self.connection.startup_connect(self.default_port, ip_address)

    def disconnect(self):
        self.controller.disconnect()
        self.connection.close()

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
        self.controller.connection_start()
        def f():
            getLogger(__name__).debug("Process thread starting.")
            while self.connection.active:
                data = self.receive_queue.get()
                if data is not None:
                    self.controller.process_received_data(data)
            getLogger(__name__).debug("Process thread done.")
        Thread(target = f).start()

    def get_menu_data(self, menu_setup):
        """
        Get the default menu setup data, add network control commands.
        """
        menu_setup.add_submenu_items("Network", 
                                [("Host", self.startup_listening, "Alt-h"),
                                ("Connect", self.get_ip, "Alt-c"),
                                ("Disconnect", self.disconnect, "Alt-d")])
        return menu_setup

    def stop(self):
        self.connection.close()
