# -*- coding: utf-8 -*-
# ***********************************************************
# aitk.utils: Python utils for AI
#
# Copyright (c) 2021 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.utils
#
# ***********************************************************

import math

try:
    from ipycanvas import Canvas, hold_canvas
except ImportError:
    pass

class Joystick():
    def __init__(self, width=250, height=250, function=print):
        self.state = "up"
        self.width = width
        self.height = height
        self.function = function
        self.canvas = Canvas(width=self.width, height=self.height)
        self.canvas.on_mouse_move(self.handle_mouse_move)
        self.canvas.on_mouse_down(self.handle_mouse_down)
        self.canvas.on_mouse_up(self.handle_mouse_up)
        # Draw blank joystick:
        self.reset()

    def clear(self):
        self.canvas.fill_style = "#B0C4DE"
        self.canvas.fill_rect(0, 0, self.width, self.height)
        self.canvas.stroke_style = "black"
        self.canvas.stroke_rect(0, 0, self.width, self.height)

    def rotate_around(self, x, y, length, angle):
        return (x + length * math.cos(-angle),
                y - length * math.sin(-angle))

    def handle_mouse_move(self, x, y):
        if self.state == "down":
            self.function((self.width/2 - x) / (self.width/2),
                          (self.height/2 - y) / (self.height/2))
            with hold_canvas(self.canvas):
                self.clear()
                self.canvas.stroke_style = "black"
                angle = math.atan2(self.width/2 - x, self.height/2 - y)
                x1, y1 = self.rotate_around(self.width/2, self.height/2, 10, -angle)
                x2, y2 = self.rotate_around(self.width/2, self.height/2, -10, -angle)
                points = [
                    (self.width/2, self.height/2),
                    (x1, y1),
                    (x, y),
                    (x2, y2),
                ]
                self.canvas.fill_style = "gray"
                self.canvas.fill_polygon(points)
                self.canvas.fill_circle(self.width/2, self.height/2, 10)
                self.canvas.fill_style = "black"
                self.canvas.fill_circle(x, y, self.width/10)

    def handle_mouse_down(self, x, y):
        self.state = "down"
        self.handle_mouse_move(x, y)

    def handle_mouse_up(self, x, y):
        self.state = "up"
        self.reset()

    def reset(self):
        self.function(0, 0)
        self.clear()
        self.canvas.fill_style = "black"
        self.canvas.fill_circle(self.width/2, self.height/2, self.width/10)
