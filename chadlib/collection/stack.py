

class Stack:
    """
    A standard stack data structure that supports peek, pop, push operations.

    List based version where the tail end of the list is the top of the stack.
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

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)
