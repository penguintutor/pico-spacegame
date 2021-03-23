import utime
from constants import *

class Shot:
    
    def __init__ (self, display, start_position, color=(255, 255, 255)):
        self.display = display
        self.x = start_position[0]
        self.y = start_position[1]
        self.color = color
        
    def update(self):
        self.y -= 2
    
    def draw(self, display_buffer):
        if self.y <= 0:
            return
        self.display.set_pen(*self.color)
        self.display.pixel(int(self.x), int(self.y))
        self.display.pixel(int(self.x+1), int(self.y))
        self.display.pixel(int(self.x), int(self.y+1))
        self.display.pixel(int(self.x+1), int(self.y+1))