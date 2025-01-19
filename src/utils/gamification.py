# Utility for gamification
# src/utils/gamification.py

class Gamification:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def get_points(self):
        return self.points