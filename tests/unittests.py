import unittest
from Controller import Controller

class testDiffDistance(unittest.TestCase):
    def test_cur_bigger_target_distance(self):
        controller = Controller()
        controller.set_desired_distance(5000)
        calc_res = controller.calculate_diff_dist(7000)
        self.assertIsInstance(calc_res, int)
        self.assertEqual(calc_res, 2000)

    def test_cur_smaller_target_distance(self):
        controller = Controller()
        controller.set_desired_distance(5000)
        calc_res = controller.calculate_diff_dist(3000)
        self.assertIsInstance(calc_res, int)
        self.assertEqual(calc_res, -2000)
    
    def test_negative_cur_distance(self):
        controller = Controller()
        controller.set_desired_distance(5000)
        calc_res = controller.calculate_diff_dist(-3000)
        self.assertIsInstance(calc_res, int)
        self.assertEqual(calc_res, -10)

if __name__ == '__main__':
    unittest.main()