"""
The Chromatic BaNANAs: Amanda Tan, Anastasia Lee, Naomi Lai, and Nia Lam
SoftDev
P05: Color Theory for Dummies
2025-06-06
"""

from flask import Flask, render_template, request, redirect, session, flash
import random

# background color randomized
# inner square color randomized within range
def rgb(c):
        return f"rgb({c[0]}, {c[1]}, {c[2]})"

def color_randomizer():
    base_value = [random.randint(0, 255) for i in range(3)]
    # small chance you get white which is maybe bad? if website bkgd is white
    variation = random.randint(-15, 15)

    # outer squares
    outer_left = [random.randint(0, 255) for i in range(3)]
    outer_right = [random.randint(0, 255) for i in range(3)]

    # inner squares
    color1 = []
    for c in base_value:
        new_value = c + variation

        if new_value < 0:
            new_value = 0
        elif new_value > 255:
            new_value = 255

        color1.append(new_value)
    
    same = random.choice([True, False])

    if same:
        color2 = color1
    else:
        color2 = []
        for c in base_value:
            variation = random.randint(-15, 15)
            new_value = c + variation

            if new_value < 0:
                new_value = 0
            elif new_value > 255:
                new_value = 255

            color2.append(new_value)

    return {
        "inner_left": rgb(color1),
        "inner_right": rgb(color2),
        "outer_left": rgb(outer_left),
        "outer_right": rgb(outer_right),
        "same": same
    }