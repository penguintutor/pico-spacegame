class Player:
    def __init__ (self, display):
        self.display = display
        self.lives = 3
        self.score = 0

    def reset (self):
        self.lives = 3
        self.score = 0
        
    def get_score_string (self):
        if (self.lives == 3):
            return "III"
        elif (self.lives == 2):
            return " II"
        elif (self.lives == 1):
            return "  I"
        return ""