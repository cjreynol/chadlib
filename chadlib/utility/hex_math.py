"""
Collection of functions for adjusting hex coordinates.

All directions are in reference to flat-topped hexes, as opposed to pointy.

For quick reference:
dir_changes = {"north" : (0, 1, -1), "south" : (0, -1, 1), 
                "n_east" : (1, 0, -1), "s_east" : (1, -1, 0),
                "n_west" : (-1, 1, 0), "s_west" : (-1, 0, 1),
                "east" : (2, -1, -1), "west" : (-2, 1, 1)}
"""


def axial_to_cubic(col, slant):
    """
    Convert axial coordinate to its cubic equivalent.
    """
    x = col
    z = slant
    y = -x - z
    return x, y, z

def cubic_to_axial(x, y, z):
    """
    Convert cubic coordinate to its axial equivalent.
    """
    return x, z

def is_valid_cubic_coord(x, y, z):
    """
    Tests if the cubic coordinates sum to 0, a property of this hex 
    coordinate system.
    """
    return (x + y + z) == 0

def _tuple_add(t1, t2):
    return tuple([a + b for a, b in zip(t1, t2)])

def cubic_n_moves(f, n, x, y, z):
    """
    Return coordinate moved n hexes by the action defined in f.

    f is expected to be a cubic move function.
    """
    for _ in range(n):
        x, y, z = f(x, y, z)
    return x, y, z

def cubic_north(x, y, z):
    return _tuple_add((x, y, z), (0, 1, -1))

def cubic_south(x, y, z):
    return _tuple_add((x, y, z), (0, -1, 1))

def cubic_northeast(x, y, z):
    return _tuple_add((x, y, z), (1, 0, -1))

def cubic_southeast(x, y, z):
    return _tuple_add((x, y, z), (1, -1, 0))

def cubic_northwest(x, y, z):
    return _tuple_add((x, y, z), (-1, 1, 0))

def cubic_southwest(x, y, z):
    return _tuple_add((x, y, z), (-1, 0, 1))

def cubic_east(x, y, z):
    return _tuple_add((x, y, z), (2, -1, -1))

def cubic_west(x, y, z):
    return _tuple_add((x, y, z), (-2, 1, 1))

def axial_n_moves(f, n, col, slant):
    """
    Return coordinate moved n hexes by the action defined in f.

    f is expected to be an axial move function.
    """
    for _ in range(n):
        col, slant = f(col, slant)
    return col, slant

def axial_north(col, slant):
    return _tuple_add((col, slant), (0, -1))

def axial_south(col, slant):
    return _tuple_add((col, slant), (0, 1))

def axial_northeast(col, slant):
    return _tuple_add((col, slant), (1, -1))

def axial_southeast(col, slant):
    return _tuple_add((col, slant), (1, 0))

def axial_northwest(col, slant):
    return _tuple_add((col, slant), (-1, 0))

def axial_southwest(col, slant):
    return _tuple_add((col, slant), (-1, 1))

def axial_east(col, slant):
    return _tuple_add((col, slant), (2, -1))

def axial_west(col, slant):
    return _tuple_add((col, slant), (-2, 1))
