import math
from Tkinter import *

window = Tk()

window.title('Turingmachine')

window.geometry('800x600')

v1 = StringVar()
v2 = StringVar()
e1 = Entry(window, width=10, textvariable=v1)
e1.pack(padx=10, pady=10)
e2 = Entry(window, width=10, textvariable=v2, state='readonly')
e2.pack()

box = Listbox(window, height=15, width=50)
box.pack()


transition2 = {
    ('start', '1') : ('start', '1', 1),
    ('start', 'B') : ('creatediv', '2', 1),
    ('creatediv', 'B') : ('stopcreate', '2', 1),
    ('stopcreate', 'B' ) : ('compare', 'B', -1),
    ('moveleft', '2') : ('moveleft', '2', -1),
    ('moveleft', '4') : ('moveleft', '4', -1),
    ('moveleft', '3') : ('moveleft', '3', -1),
    ('moveleft', '1') : ('moveright', '3', 1), #change direction, mark
    ('moveright', '3') : ('moveright', '3', 1),
    ('moveright', '4') : ('moveright', '4', 1),
    ('moveright', '2') : ('moveleft', '4', -1), #change direction, mark
    ('moveright', 'B') : ('touchbound', 'B', -1),
    ('touchbound', '4') : ('rewash', '2', -1),
    ('rewash', '4') : ('rewash', '2', -1),
    ('rewash', '3') : ('addback', '3', 1),
    ('addback', '2') : ('moveleft', '4', -1),
    ('moveleft', 'B') : ('check', 'B', 1),# check if halt
    ('check', '3') : ('check', '1', 1),
    ('check', '4') : ('check', '2', 1),
    ('check', '2') : ('restart', '2', -1),
    ('check', 'B') : ('halt', 'B', 0),
    ('restart', '2') : ('restart', '2', 1),
    ('restart', 'B') : ('div++', '2', 1),
    ('div++', 'B') : ('compare', 'B', -1),
    ('compare', '2') : ('compare', '2', -1),
    ('compare', '3') : ('compare', '3', -1),
    ('backhead2', '1') : ('backhead2', '1', -1),
    ('backhead2', 'B') : ('restart2', 'B', 1),
    ('restart2', '1') : ('restart2', '1', 1),
    ('restart2', '2') : ('restart2', '2', 1),
    ('restart2', 'B') : ('moveleft', 'B', -1),
    ('compare', 'B') : ('accept', 'B', 0),
    ('compare', '4') : ('compare', '4', -1),
    ('compare', '1') : ('compare2', '3', 1),
    ('compare2', '3') : ('compare2', '3', 1),
    ('compare2', '4') : ('compare2', '4', 1),
    ('compare2', '2') : ('compare', '4', -1),
    ('compare2', 'B') : ('backhead2', 'B', -1),
    ('backhead2', '4') : ('backhead2', '2', -1),
    ('backhead2', '3') : ('backhead2', '1', -1),
}

def simulation(transition2, input):
    head = 0
    tape = input
    state = 'start'
    steps = 0
    while state !='accept' and state != 'halt':
        state, tape[head], move = transition2[(state, tape[head])]
        head += move
        if head < 0:
            tape.insert(0, 'B')
            head += 1
        if head >= len(tape):
            tape.append('B')
        steps += 1
        box.insert(steps - 1, ''.join(tape[:head]) + '*' + ''.join(tape[head:]))
        v2.set(str(state))
        
def error():
    v2.set('error')
    

def call():
    x = int(v1.get())
    if x > 1:
        y = x
        simulation(transition2, ['1'] *  y)
    else:
        error()


   
button = Button(window, text="calculate", command=call)
button.pack()

window.mainloop()
