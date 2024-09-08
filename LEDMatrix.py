from neopixel import Neopixel

class LEDMatrix:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = Neopixel(30, 0, 15, "GRB")
        
    # Function to light up an individual LED given its coordinates
    def light(self, x, y):
        element = ((y - 1) * self.width) + (x - 1)
        
        print("Element #:", element)
        self.pixels[element] = (255, 0, 0)
        self.pixels.show()
    
    # Function to turn off all LEDs in the matrix
    def all_off(self):
        self.pixels.clear()
