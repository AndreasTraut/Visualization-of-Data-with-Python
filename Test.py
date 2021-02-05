# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 08:52:38 2020
File for testing the "convert" function
@author: andre
"""

import unittest
import numpy as np
from Example_Marathon_extended import convert

class SampleTest(unittest.TestCase):
    
    def test_convert_function(self):
        return convert("01:05:38") / np.timedelta64(1, 's')
        self.assertEquals(3938.0, result)
        
if __name__ == '__main__':
    unittest.main()