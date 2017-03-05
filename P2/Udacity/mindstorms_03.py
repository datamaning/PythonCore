import turtle

def draw_square(brad):
    for i in range(1,4):
        brad.forward(100)
        brad.right(150)

def draw_art():
    window=turtle.Screen()
    window.bgcolor('red')

    brad=turtle.Turtle()
    brad.shape('turtle')
    brad.color('yellow')
    brad.speed(20)
    for i in range(1,37):
        draw_square(brad)
        brad.right(10)
    window.exitonclick()

draw_art()

