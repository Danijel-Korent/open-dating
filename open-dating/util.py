import random

def random_hex_color(excluded_colors = []):
    while True:
        # Generate random hex color
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
        # Check if it's in the excluded list
        if color not in excluded_colors:
            return color
        else:
            return random_hex_color(excluded_colors)


