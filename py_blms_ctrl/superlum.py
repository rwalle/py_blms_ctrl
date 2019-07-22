"""
Superlum responses to command `S20\n`:

A219 = high, on 19 = 16 + 2 + 1
A217 = high, off 17 = 16 + 1

A203 = low, on 3 = 2 + 1
A201 = low, off 1 = 1"""

import re, serial, io

BAUD_RATE = 57600
TIMEOUT = 1

BITS_DEFINITION = (('bad SLD temperature', 'normal SLD temperature'), 
    ('SLD power is off or failure occurred', 'SLD power is on'),
    ('', 'SLD current limit reached'),
    ('', 'failure occurred'),
    ('LO mode', 'HI mode'))
    
class Superlum:

    """
    A class that controls a Superlum BLMS mini light source connected to computer via USB (RS-232 emulation). Can query current light source status, switch ON/OFF and LO/HI mode, and set to HI mode and turn ON based on current status.
    """

    blms = None
    blms_io = None
    
    def __init__(self, port):
        self.port = port

    def read_response(self):
    
        if self.blms_io == None:
            raise NameError('Use connect() to connect to the device before the query.')
            
        response = self.blms_io.readline()
        return response

    def analyze_response(self, response):
    
        # return a tuple (status_code, status_bool, status_text)
              
        f = re.match(r'^A\d{3}\n$', response)
        
        if f == None:
            if response[:2] == 'AE':
                raise RuntimeError('BLMS mini returned error!')
            else:
                raise RuntimeError('cannot understand response: ' + response)
        else:
            status_code = int(response[2:4])
        
        binary_rep = '{:05b}'.format(status_code)
        
        status_text = []
        status_bool = []
        
        for digit_loc, digit in enumerate(reversed(binary_rep)):
        
            status_bool.append(bool(int(digit)))
            digit_text = BITS_DEFINITION[digit_loc][int(digit)]
            if digit_text:
                status_text.append(digit_text)
        
        status_text = ', '.join(status_text)
            
        return (status_code, status_bool, status_text)
        
    def get_current_status(self):
    
        if self.blms_io == None:
            raise NameError('Use connect() to connect to the device before the query.')
    
        self.blms_io.write('S20\n')
        self.blms_io.flush()
        return self.analyze_response(self.read_response())
        
    def connect(self):
        
        self.blms = serial.Serial(self.port, BAUD_RATE, timeout=TIMEOUT)
        self.blms_io = io.TextIOWrapper(io.BufferedRWPair(self.blms, self.blms))
        
    def switch_power(self):
    
        if self.blms_io == None:
            raise NameError('Use connect() to connect to the device before the query.')
        
        self.blms_io.write('S21\n')
        self.blms_io.flush()
        return self.read_response()
    
    def switch_hi_mode(self):
        
        if self.blms_io == None:
            raise NameError('Use connect() to connect to the device before the query.')
        
        self.blms_io.write('S41\n')
        self.blms_io.flush()
        return self.read_response()
        
    def set_hi_mode(self):
    
        """
        LO & OFF => SWITCH HI
        LO & ON  => SWITCH ON, SWITCH HI
        HI & OFF => NOTHING
        HI & ON  => NOTHING
        """
    
        (_, status, _) = self.get_current_status()
        
        if status[4] == False:

            if status[1]:
                self.switch_power()
                response = self.switch_hi_mode()
            else:
                response = self.switch_hi_mode()
                
            (_, status, status_txt) = self.get_current_status()
            
            if status[4] == False:
                raise RuntimeError('cannot switch to HI mode. current status: ' + status_txt)
                
    def set_power_on(self):
        
        (_, status, _) = self.get_current_status()
        
        if status[1] == False:
            response = self.switch_power()
            
            (_, status, status_txt) = self.get_current_status()
            
            if status[1] == False:
                raise RuntimeError('cannot switch on. current status: ' + status_txt)

    def close(self):
    
        if self.blms_io == None:
            raise NameError('The device is not open yet.')
    
        self.blms.close()
        
    
        
        
    
        
    
    