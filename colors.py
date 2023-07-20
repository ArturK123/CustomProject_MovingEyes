def interpolate(color_a, color_b, t):
    # 'color_a' and 'color_b' are RGB tuples
    # 't' is a value between 0.0 and 1.0
    # this is a naive interpolation
    return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

    

def changeBrightness(color_a, color_b, invert):
    color = interpolate(color_a, (color_b, color_b, color_b), invert/255)
    return color


if __name__ == "__main__":
    import sys
    sys.exit(main())