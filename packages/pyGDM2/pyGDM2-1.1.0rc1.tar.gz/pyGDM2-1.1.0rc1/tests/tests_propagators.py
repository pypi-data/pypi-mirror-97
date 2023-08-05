from __future__ import print_function
from __future__ import absolute_import

import unittest

import numpy as np

from pyGDM2 import propagators




class TestDyads(unittest.TestCase):

    def setUp(self):
    
        self.dyads = propagators.DyadsBaseClass()

        


    def test_2_efield(self):
        print(" ----- Start fields.efield test -----")
        self.assertEqual(self.dyads.G_EE, (50,50),
                         'incorrect default size')
# self.assertAlmostEqual(np.sum(np.abs(K.flatten())), self.K_abs_sum[i_sim], delta=.5)
        print("\nFinished `efield` test\n\n")
        
        
    


# =============================================================================
# run tests
# =============================================================================
if __name__ == '__main__':
    
    # ut_classes = TestClasses()
    # ut_classes.test_0_simulation()
    # ut_classes.test_1_struct()
    # ut_classes.test_2_efield()
    
    # ut_core = TestDyads()
    
    # ut_core.test_0_get_sbs()
    # ut_core.test_1_get_K()
    # ut_core.test_2_scatter()
    # # ut_core.test_GPU_0_get_sbs()
    # ut_core.test_GPU_1_get_K()
    # ut_core.test_GPU_2_scatter()
    
    dyads = propagators.DyadsQuasistatic123()
    dyads.G_EE



    # ## all tests
    # unittest.main()
    
    
    
    
    
    
    