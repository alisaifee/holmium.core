import unittest
from holmium.core import repeat


tr1_counter = 0
tr2_counter = 0

@repeat(1)
def test_repeat_once():
    global tr1_counter
    tr1_counter += 1

@repeat(2)
def test_repeat_twice():
    global tr2_counter
    tr2_counter += 1



def test_all_repetitions():
    assert tr1_counter == 1
    assert tr2_counter == 2


class RepeatedTests(unittest.TestCase):
    def setUp(self):
        self.tr1 = self.tr2 = -1

    @repeat(1)
    def test_repeat_one(self):
        if self.tr1 < 0:self.tr1=0
        self.tr1+=1

    @repeat(2)
    def test_repeat_two(self):
        if self.tr2 < 0:self.tr2=0
        self.tr2+=1


    def tearDown(self):
        if self.tr1 > 0:
            assert self.tr1 == 1
        if self.tr2 > 0:
            assert self.tr2 == 2
