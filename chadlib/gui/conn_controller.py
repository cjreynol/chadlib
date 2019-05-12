from abc                import ABC, abstractmethod


class ConnController(ABC):
    """
    Companion class to the connection component, specifies the interface 
    required for that component to function.
    """
    
    @abstractmethod
    def connection_start(self):
        """
        Overridden by subclasses to trigger logic when a network connection is 
        made.
        """
        pass

    @abstractmethod
    def process_received_data(self, data):
        """
        Overridden by subclasses to handle data from the receive queue.
        """
        pass

    def disconnect(self):
        """
        Can be overridden by subclass as a hook to act when the connection 
        disconnects itself or is disconnected from.
        """
        pass
