import unittest
from py_blms_ctrl.superlum import Superlum


class TestControl(unittest.TestCase):

    def setUp(self):
        self.blms_ctrl = Superlum('COM4')
        self.blms_ctrl.connect()

    def test_0_current_status(self):

        try:
            s = self.blms_ctrl.get_current_status()
        except RuntimeError:
            self.fail('Cannot check current status. There is a connection error or instrument error.')
    
    def test_1_HI_on(self):
    
        self.blms_ctrl.set_hi_mode()
        self.blms_ctrl.set_power_on()
        (_, status, _) = self.blms_ctrl.get_current_status()
        self.assertTrue(status[1])
        self.assertTrue(status[4])
        
    def test_2_LO_off(self):
    
        # turn the SLD off as the last step
    
        self.blms_ctrl.set_hi_mode()
        self.blms_ctrl.set_power_on()
        self.blms_ctrl.switch_power()
        self.blms_ctrl.switch_hi_mode()
        (_, status, _) = self.blms_ctrl.get_current_status()
        self.assertFalse(status[1])
        self.assertFalse(status[4])
    
    def tearDown(self):
        self.blms_ctrl.close()
        
if __name__ == '__main__':
    unittest.main()