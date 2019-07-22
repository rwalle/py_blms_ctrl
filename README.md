# BLMS mini light source control
A python package that allows the control of the output mode and power of a Suplerlum BLMS mini light source via USB. Dependent on [pySerial](https://github.com/pyserial/pyserial).

## A simple example

```Python
>>> blms_ctrl = Superlum('COM4')
>>> blms_ctrl.connect()
>>> (status_code, _, _) = blms_ctrl.get_current_status()
>>> print(status_code)
1
>>> blms_ctrl.switch_hi_mode()
>>> blms_ctrl.switch_power()
>>> (status_code, _, status_txt) = blms_ctrl.get_current_status()
>>> print(status_code)
19
>>> print(status_text)
normal SLD temperature, SLD power is on, HI mode
>> blms_ctrl.close()
```

## API reference

### initiate an instance
`blms_ctrl = Superlum(port)`

### connect to the source (must be done before writing commands)
`blms_ctrl.connect()`

### switch LO/HI output mode (if currently in HI mode and turned on, the source will be turned off before switching)
`blms_ctrl.switch_hi_mode()`

### switch power ON/OFF
`blms_ctrl.switch_power()`

### determine current status and automatically set the source to HI output mode
`blms_ctrl.set_hi_mode()`

### determine current status and automatically set the source to ON
`blms_ctrl.set_power_on()`

### close the connection
`blms_ctrl.close()`
