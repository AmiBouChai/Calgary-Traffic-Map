import time
import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


# 16 x 2 LCD I2C Sample Code
# Library from https://github.com/T-622/RPI-PICO-I2C-LCD

# See library GitHub repository for full list of functions and their use

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

print("Running sample code...")

sda = machine.Pin(26)
scl = machine.Pin(27) # NOTE: It is important you change this to match the SDA and SCL pins you are using.
i2c_controller = 1    # Also change this to match the controller you are using (Listed on the Raspberry Pi Pico W Pinout as "I2C0" or "I2C1")
                      # You will need to wire the LCD to your Pi Pico, ensuring that each pin goes to the correct header. The pinout should be written on the LCDs PCB.
                      # You can use either 5V power via VBUS or 3.3V power via either VSYS or 3V(OUT).

i2c = I2C(i2c_controller, sda=sda, scl=scl, freq=400000) 
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    
testString = "This is a really long string to test scrolling. This text will scroll across the screen!"
    
while True:
    for i in range(len(testString) - 15):
        lcd.putstr(testString[i:i+16])
        time.sleep(0.6)
        lcd.move_to(0,0)




