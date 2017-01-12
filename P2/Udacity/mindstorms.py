import turtle

def draw_square():

    window=turtle.Screen()
    window.bgcolor('red')

    brad=turtle.Turtle()
    brad.forward(100)
    brad.right(90)
    brad.forward(100)
    brad.right(90)
    brad.forward(100)
    brad.right(90)
    brad.forward(100)


    angie=turtle.Turtle()
    angie.shape('arrow')
    angie.color('blue')
    angie.circle(100)
    
    tri=turtle.Turtle()
    tri.shape('arrow')
    tri.forward(100)
    tri.left(120)
    tri.forward(100)
    tri.left(120)
    tri.forward(100)

    window.exitonclick()

draw_square()
