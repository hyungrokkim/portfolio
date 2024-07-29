import Tkinter
import threading
canvas=None
points=set()
event=threading.Event()

def initialize(width, height):
    root=Tkinter.Tk()
    global canvas
    canvas=Tkinter.Canvas(root, width=width, height=height)
    canvas.grid()
    def main():
        def update():
            global event
            event.wait()
            event.clear()
            
            global canvas
            canvas.delete(Tkinter.ALL)
            for x, y in points:
                canvas.create_line(x, y, x+1, y+1)
            canvas.after(0, update)
        
        global event
        event.set()
        update()
        root.mainloop()
    threading.Thread(target=main).start()

def plot(x, y):
    global points
    points.add((x,y))
    global event
    event.set()
def clear():
    global points
    points=set()
    global event
    event.set()