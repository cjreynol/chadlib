from unittest                   import TestCase

from chadlib.utility.hex_math   import *


class TestHexMath(TestCase):
    
    def setUp(self):
        self.position0 = (0, 0, 0)
        self.position1 = (3, 2, -5)
        self.cubic_positions = [self.position0, self.position1]
        self.axial_positions = [cubic_to_axial(*pos) 
                                for pos in self.cubic_positions]

    def tearDown(self):
        pass

    def test_cubic_to_axial_to_cubic(self):
        for pos in self.cubic_positions:
            axial = cubic_to_axial(*self.position0)
            cubic = axial_to_cubic(*axial)
            self.assertTupleEqual(self.position0, cubic)

    def test_cubic_inverse_movements(self):
        for pos in self.cubic_positions:
            self.assertTupleEqual(pos, cubic_north(*cubic_south(*pos)))
            self.assertTupleEqual(pos, cubic_south(*cubic_north(*pos)))

            self.assertTupleEqual(pos, cubic_northeast(*cubic_southwest(*pos)))
            self.assertTupleEqual(pos, cubic_southwest(*cubic_northeast(*pos)))

            self.assertTupleEqual(pos, cubic_northwest(*cubic_southeast(*pos)))
            self.assertTupleEqual(pos, cubic_southeast(*cubic_northwest(*pos)))

            self.assertTupleEqual(pos, cubic_east(*cubic_west(*pos)))
            self.assertTupleEqual(pos, cubic_west(*cubic_east(*pos)))

    def test_axial_inverse_movements(self):
        for pos in self.axial_positions:
            self.assertTupleEqual(pos, axial_north(*axial_south(*pos)))
            self.assertTupleEqual(pos, axial_south(*axial_north(*pos)))

            self.assertTupleEqual(pos, axial_northeast(*axial_southwest(*pos)))
            self.assertTupleEqual(pos, axial_southwest(*axial_northeast(*pos)))

            self.assertTupleEqual(pos, axial_northwest(*axial_southeast(*pos)))
            self.assertTupleEqual(pos, axial_southeast(*axial_northwest(*pos)))

            self.assertTupleEqual(pos, axial_east(*axial_west(*pos)))
            self.assertTupleEqual(pos, axial_west(*axial_east(*pos)))

    def test_cubic_n_inverse_movement(self):
        n = 10
        for pos in self.cubic_positions:
            self.assertTupleEqual(pos, cubic_n_moves(cubic_north, n, 
                                    *cubic_n_moves(cubic_south, n, *pos)))
    
    def test_axial_n_inverse_movement(self):
        n = 10
        for pos in self.axial_positions:
            self.assertTupleEqual(pos, axial_n_moves(axial_north, n, 
                                    *axial_n_moves(axial_south, n, *pos)))

    def test_cubic_validation(self):
        for pos in self.cubic_positions:
            self.assertTrue(is_valid_cubic_coord(*pos))
