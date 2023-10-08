#Matplotlib has a whole system of colormaps for doing this, but I didn't want to use it right now.
def numToColor(num):
    # Here I map numbers from 0 to 1 (inclusive) to colors from red to yellow to green to cyan to blue to purple.
    # This is for Matplotlib, so R,G, and B values are each represented as floating point numbers between 0 and 1,
    # rather than as integers (or bytes) from 0 to 255, as I'm more used to.
    if num < 0 or num > 1:
        print("numToColor only works with numbers between 0 and 1 (inclusive).")
        # I should probably make this an error.
    elif num < .2:
        return (1, 5*num, 0)
    elif num < .4:
        return (1-5*(num-.2), 1, 0)
    elif num < .6:
        return (0, 1, 5*(num-.4))
    elif num < .8:
        return (0, 1-5*(num-.6), 1)
    else:
        return (5*(num-.8), 0, 1)