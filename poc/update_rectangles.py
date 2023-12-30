def update_rectangles(rectangles):
    for rect in rectangles:
        # Update width and x coordinate
        if rect['width'] < 0:
            rect['x'] += rect['width']  # Move x leftward
            rect['width'] = abs(rect['width'])  # Make width positive

        # Update height and y coordinate
        if rect['height'] < 0:
            rect['y'] += rect['height']  # Move y upward
            rect['height'] = abs(rect['height'])  # Make height positive

    return rectangles


if __name__ == "__main__":
    # Test the function with the provided data
    rectangles = [{
        "x": 95,
        "y": 571,
        "width": 17,
        "height": 13,
    }]
    updated_rectangles = update_rectangles(rectangles)
    print(updated_rectangles)
