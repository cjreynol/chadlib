

class Stack:
    """
    A standard stack data structure that supports push, pull, pop operations.

    List based version.
    """
    
    def __init__(self, *args):
        self.data = list(args)

    @property
    def is_empty(self):
        return not bool(self.data)

    def pop(self):
        return self.data.pop()

    def push(self, value):
        self.data.append(value)

    def peek(self):
        return self.data[-1]

    def clear(self):
        self.data = list()
