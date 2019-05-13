"""
Helpful functions that do not belong to a data structure or other set.
"""


def event_wrapper(function):
    """
    Useful to wrap callbacks for calling in a different context.
    """
    def f(event):
        function()
    return f
