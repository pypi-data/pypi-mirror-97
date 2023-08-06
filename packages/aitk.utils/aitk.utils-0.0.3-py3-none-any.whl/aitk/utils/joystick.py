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

from ipywidgets import (
    Button,
    Layout,
    GridBox,
    ButtonStyle,
    FloatSlider,
    HBox,
    VBox,
    GridspecLayout,
    TwoByTwoLayout,
)

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

    def watch(self):
        return self.canvas


class NoJoystick():
    def __init__(self, width=250, height=250, function=print):
        self.function = function
        self.arrows = [
            "⬉ ⬆ ⬈",
            " ╲｜╱ ",
            "⬅－⊙－➡",
            " ╱｜╲ ",
            "⬋ ⬇ ⬊",
        ]

        # Note: rotate is reversed to make it match up with the slider
        # direction
        self.movement = [
            [(1.0, -1.), (1.0, -.5), (1.0, 0.0), (1.0, 0.5), (1.0, 1.0)],
            [(0.5, -1.), (0.5, -.5), (0.5, 0.0), (0.5, 0.5), (0.5, 1.0)],
            [(0.0, -1.), (0.0, -.5), (0.0, 0.0), (0.0, 0.5), (0.0, 1.0)],
            [(-.5, -1.), (-.5, -.5), (-.5, 0.0), (-.5, 0.5), (-.5, 1.0)],
            [(-1., -1.), (-1., -.5), (-1., 0.0), (-1., 0.5), (-1., 1.0)],
        ]

        # Make the widgets:
        layout = Layout(height="35px", width="35px")
        self.buttons = []
        for row in range(5):
            for col in range(5):
                button = Button(description=self.arrows[row][col], layout=layout)
                button.on_click(self.create_move(row, col))
                self.buttons.append(button)

        self.rotate_slider = FloatSlider(
            min=-1, max=1, step=0.1,
            continuous_update=True,
            readout=False,
            layout=Layout(width="200px", height="30px"))

        self.translate_slider = FloatSlider(
            min=-1, max=1, step=0.1,
            orientation="vertical",
            continuous_update=True,
            readout=False,
            layout=Layout(width="30px"))

        self.array = GridBox(
            children=self.buttons,
            layout=Layout(
                grid_template_rows='40px 40px 40px 40px 40px',
                grid_template_columns='40px 40px 40px 40px 40px',
                grid_gap='0px 0px',
                overflow="inherit",
            )
        )

        self.controls = TwoByTwoLayout(
            top_left=self.translate_slider,
            top_right=self.array,
            bottom_right=self.rotate_slider,
            justify_items='center',
            align_items='top',
            width="min-content",
            height="240px",
        )

    def create_move(self, row, col):
        def on_click(button):
            translate, rotate = self.movement[row][col]
            self.translate_slider.value = translate
            self.rotate_slider.value = rotate
        return on_click

    def watch(self):
        return self.controls
