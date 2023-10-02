import unittest

class TestProject(unittest.TestCase):
    def setUp(self):
        print("setup")

    def test_one(self):
        print("testone")

    def test_two(self):
        print("testtwo")

    def test_three(self):
        print("testthree")

    def tearDown(self):
        print("teardown")
