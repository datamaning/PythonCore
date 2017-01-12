import turtle

def draw_square(brad):
    for i in range(1,4):
        brad.forward(100)
        brad.right(150)
def draw_triangle(brad,size,flag):
    if flag==0:
        for i in range(1,4):
            brad.forward(size)
            brad.right(60)
    else:
        for i in range(1,4):
            brad.forward(size)
            brad.left(120)
            
def draw_art():
    window=turtle.Screen()
    window.bgcolor('green')

    brad=turtle.Turtle()
    brad.shape('turtle')
    brad.color('yellow')
    brad.speed(1)
    init_size=12.5
    pay=2
    for i in range(1,9):
        if i%2==1:
            brad.forward(12.5)
        else:
            if init_size==50:
                pay=0.5
            brad.left(60)
            draw_triangle(brad,init_size,1)
            brad.right(60)
            init_size*=pay
    window.exitonclick()

draw_art()

