class Actor:
    
    def __init__ (self, display, filename, position=(0,0)):
        
        self.display = display
        
        self.x = position[0]
        self.y = position[1]
        
        self._angle = 0
        
        # If enable then black is converted into transparency
        self.enable_transparency = True
        
        # private member - when changed reload image
        self._image = filename
        self.load_image()

    # Image property can be used to change the image
    # if use <instance>.image = newfile then it will load that file instead
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_value):
        self._image = new_value
        self.load_image()
        
    # rotation angle can be set in degrees
    # Only actual rotate in 90 deg intervals
    @property
    def angle(self):
        return self._angle
    
    # angle should be between -359 and +359
    # if this has been changed slightly then correct 
    # If outside that range then add / subtract 360 - attempt to fix
    @angle.setter
    def angle(self, new_value):
        if (new_value >= 360):
            new_value -= 360
        if (new_value <= -360):
            new_value += 360
        self._angle = new_value
        
    def load_image(self):
        filename = self._image
        with open (filename, "rb") as file:
        
            # First byte is width
            self.width = ord(file.read(1))
            self.height = ord(file.read(1))
            
            self.image_data = bytearray(self.width * self.height * 2)
            
            position = 0
            while position < (self.width * self.height * 2):
                current_byte = file.read(1)
                # if eof
                if len(current_byte) == 0:
                    break
                # copy to buffer
                self.image_data[position] = ord(current_byte)
                position += 1
        file.close()

    
    def draw(self, display_buffer):
        # position to start creating image is offset (x,y is center of image)
        # this gives top left hand corner of image
        topleft_x = self.x - int(self.get_rotate_width()/2)
        topleft_y = self.y - int(self.get_rotate_height()/2)
        for y in range (0, self.get_rotate_height()):
            # Check y is in range
            if (topleft_y +y < 0 or topleft_y + y >= self.display.get_height()):
                continue
            # buffer pos of display
            display_start_row = self.display_buffer_pos (topleft_x, topleft_y+y)
            # buffer pos of actor
            actor_start_row = self.sprite_buffer_pos (0, y)
            for x in range (0, self.get_rotate_width()):
                # Check x is in range
                if (topleft_x +x < 0 or topleft_x + x >= self.display.get_width()):
                    continue
                color_bytes = self.get_sprite_data(x,y)
                # If transparent then don't copy
                if (self.enable_transparency and color_bytes[0] == 0 and color_bytes[1] == 0):
                    continue
                display_buffer[display_start_row + (x*2)] = color_bytes[0]
                display_buffer[display_start_row + (x*2) + 1] = color_bytes[1]


    def get_sprite_data (self, x, y):
        color_bytes = bytearray(2)
        
        # First use 0 - saves performing multiple checks
        if (self._angle == 0):
            rot_x = x
            rot_y = y
        # If translated then rot_x / rot_y is used
        # 90 degs
        elif ((self._angle > 45 and self._angle <= 135) or (self._angle < -225 and self._angle >= -315)):
            rot_x = y
            rot_y = self.height - 1 - x
        # -90 degs
        elif ((self._angle < -45 and self._angle >= -135) or (self._angle > 225 and self._angle <= 315)):
            rot_x = self.width - 1 - y
            rot_y = x
        # 180
        elif ((self._angle > 135 and self._angle <= 225) or (self._angle < -135 and self.angle >= -225)):
            rot_x = self.width - 1 - x
            rot_y = self.height - 1 -y
        # if no rotation (default)
        else:
            rot_x = x
            rot_y = y
            
        color_bytes[0] = self.image_data[(rot_y*self.width*2) + (rot_x*2)]
        color_bytes[1] = self.image_data[(rot_y*self.width*2) + (rot_x*2) + 1]
        return color_bytes

    # give height reflecting any rotation
    def get_rotate_height(self):
        # if rotated 90 deg left or right
        if ((self._angle > 45 and self._angle <= 135) or (self._angle < -225 and self._angle >= -315) or (self._angle > 225 and self._angle <= 315) or (self._angle < -45 and self._angle >= -135)):
            return self.width
        else:
            return self.height

    def get_rotate_width(self):
        # if rotated 90 deg left or right
        if ((self._angle > 45 and self._angle <= 135) or (self._angle < -225 and self._angle >= -315) or (self._angle > 225 and self._angle <= 315) or (self._angle < -45 and self._angle >= -135)):
            return self.height
        else:
            return self.width

    # return buffer pos of a x,y coord
    def sprite_buffer_pos (self, x, y):
        buffer_pos = (x*2) + (y*self.width*2)
        return buffer_pos

    # return buffer pos of a x,y coord
    def display_buffer_pos (self, x, y):
        buffer_pos = (x*2) + (y*self.display.get_width()*2)
        return buffer_pos