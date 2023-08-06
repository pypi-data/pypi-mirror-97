# Mouse wheel handler for Mac, Windows and Linux
# Windows, Mac: Binding to <MouseWheel> is being used
# Linux: Binding to <Button-4> and <Button-5> is being used

def MouseWheelHandler(event):
    global count

    def delta(event):
        if event.num == 5 or event.delta < 0:
            return -1
        return 1

    count += delta(event)
    print(count)

import tkinter
root = tkinter.Tk()
count = 0
root.bind("<MouseWheel>", MouseWheelHandler)
root.bind("<Button-4>", MouseWheelHandler)
root.bind("<Button-5>", MouseWheelHandler)
root.mainloop()
