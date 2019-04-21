"""
Helpful functions that do not belong to a particular data structure.
"""


def event_wrapper(function):
    """
    Useful to wrap callbacks for calling in a different context.
    """
    def f(event):
        function()
    return f
