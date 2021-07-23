# implementation of card game - Memory

import simplegui
import random

l = range(8)
mem = []
exposed = []
moves = 0
state = 0
for i in range(16):
    exposed.append(False)
# helper function to initialize globals
def init():
    global mem, state, moves
    moves = 0
    label.set_text("Moves = 0")
    state = 0
    mem = l + l
    random.shuffle(mem)
    for i in range(16):
        exposed[i] = False
    
     
# define event handlers
def mouseclick(pos):
    global moves, label, state, first, second
    i = pos[0] // 50
    if exposed[i] == True:
        return
    exposed[i] = True
    if state == 0:
        first = i
        moves += 1
        label.set_text("Moves = " + str(moves))
        state = 1
    elif state == 1:
        state = 2
        second = i
    else:
        state = 1
        if mem[first] != mem[second]:
            exposed[first] = False
            exposed[second] = False
        first = i
        moves += 1
        label.set_text("Moves = " + str(moves))
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i] == False:
            canvas.draw_polygon([(i * 50, 0),((i+1)*50, 0),((i+1)*50, 100),(i * 50, 100)], 2, "Red", "Green")
        else:
            canvas.draw_polygon([(i * 50, 0),((i+1)*50, 0),((i+1)*50, 100),(i * 50, 100)], 2, "Black", "Black")
            canvas.draw_text(str(mem[i]), (10 + i * 50, 70), 60, "White")
    



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric
