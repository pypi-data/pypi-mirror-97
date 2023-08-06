import turtle

t = turtle.Turtle()


def start():
    t.left(90)


def speed(speed):
    t.speed(speed)


def end():
    turtle.done()


def penUp():
    t.penup()


def penDown():
    t.pendown()


def penColor(color):
    t.pencolor(color)


def penRGB(red, green, blue):
    hex_code = "#%02x%02x%02x" % (red, green, blue)
    t.pencolor(hex_code)


def penWidth(width):
    t.width(width)


def moveForward(pixcels=20):
    t.forward(pixcels)


def turnRight(angle=90):
    t.right(angle)


def turnLeft(angle=90):
    t.left(angle)


def dot(size):
    t.dot(size)


def arcRight(angle, length):
    t.circle(length, -angle)


def arcLeft(angle, length):
    t.circle(length, angle)


def moveTo(x, y):
    t.setpos(x, y)
