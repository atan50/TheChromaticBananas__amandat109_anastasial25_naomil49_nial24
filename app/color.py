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

def color_distance(c1, c2):
    total = 0
    for i in range(len(c1)):
        diff = c1[i] - c2[i]
        total += diff * diff
    return total ** 0.5

def color_randomizer():
    base_value = [random.randint(20, 235) for _ in range(3)]
    negate = random.choice([-1, 1])
    variation = random.randint(5, 10) * negate

    # outer squares
    outer_left = [random.randint(1, 255) for _ in range(3)]
    outer_right = [random.randint(1, 255) for _ in range(3)]

    # inner squares
    color1 = []
    for c in base_value:
        new_value = c + variation
        if new_value < 1:
            new_value = 1
        elif new_value > 255:
            new_value = 255
        color1.append(new_value)

    same = random.choice([True, False])

    if same:
        color2 = color1
    else:
        #  change
        diff = 10
        while True:
            color2 = []
            for c in base_value:
                neg = random.choice([-1, 1])
                var = random.randint(5, 10) * neg
                new_value = c + var
                if new_value < 1:
                    new_value = 1
                elif new_value > 255:
                    new_value = 255
                color2.append(new_value)

            dist = color_distance(color1, color2)
            if dist >= diff:
                break

    return {
        "inner_left": rgb(color1),
        "inner_right": rgb(color2),
        "outer_left": rgb(outer_left),
        "outer_right": rgb(outer_right),
        "same": same
    }