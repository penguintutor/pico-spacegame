from asteroid import Asteroid
import sys
import utime
from constants import *

configfile = "enemies.dat"

class Enemies:
    
    def __init__ (self, display):
        self.display = display
        self.asteroids = []
        # Time that this level started
        self.level_time = utime.time()
        self.level_end = None
        
        # Load the config file
        try:
            with open(configfile, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    enemy_details = line.split(",")
                    if enemy_details[1] == "end":
                        self.level_end = int(enemy_details[0])
                    elif enemy_details[1] == "asteroid":
                        start_time = int(enemy_details[0])
                        # value 1 is type
                        image_size = enemy_details[2]
                        start_pos = (int(enemy_details[3]), int(enemy_details[4]))
                        velocity = int(enemy_details[5])
                        self.asteroids.append(Asteroid(display, start_time, image_size, start_pos, velocity))
                        #print ("Asteroid {} {} {} {}".format(start_time, image_size, start_pos, velocity))
        except IOError:
            print ("Error reading configuration file "+configfile)
            # Just end as cannot play without config file
            sys.exit()
        except:
            print ("Corrupt configuration file "+configfile)
            sys.exit()

    
    def draw(self, display_buffer):
        for this_asteroid in self.asteroids:
            this_asteroid.draw(display_buffer)
            
    # Updates positions of all enemies
    def update(self):
        # Check for level end reached
        if (self.level_end != None and
            utime.time() > self.level_time + self.level_end):
                self.next_level()

        for this_asteroid in self.asteroids:
            this_asteroid.update(self.level_time)
            
    def check_shot(self, shot_x, shot_y):
        for this_asteroid in self.asteroids:
            if this_asteroid.status != STATUS_VISIBLE:
                continue
            if this_asteroid.collidepoint(shot_x, shot_y):
                this_asteroid.status = STATUS_DESTROYED
                return True
        return False
        
            
    def check_crash(self, spacecraft_position, hit_points):
        for this_asteroid in self.asteroids:
            # skip any that are not visible
            if this_asteroid.status != STATUS_VISIBLE:
                continue
            for this_point in hit_points:
                if this_asteroid.collidepoint(
                    spacecraft_position[0]+this_point[0],
                    spacecraft_position[1]+this_point[1] ):
                        this_asteroid.status = STATUS_DESTROYED
                        return True
        return False

    def next_level (self):
        self.level_time = utime.time()
        for this_asteroid in self.asteroids:
            this_asteroid.reset()
            
            