from tkinter import *

def click(event):
    global scvalue
    text=event.widget.cget("text")
    
    if text == "=":
        if scvalue.get().isdigit():
            value=int(scvalue.get())
        else:
            try:
                value=eval(screen.get())
            except Exception as e:
                scvalue.set("error")
                screen.update()    
        scvalue.set(value)
        screen.update()
    elif text=="C":
        scvalue.set("")
        screen.update()
    else:
        scvalue.set(scvalue.get() + text)
        screen.update()
        

root=Tk()
root.geometry("500x300")
root.title("calculator")
root.config(bg="#2c4550")

scvalue=StringVar()
scvalue.set("")

screen=Entry(root,textvar=scvalue,font="lucida 25")
screen.pack(fill=Y,ipady=10,pady=10,padx=85)
#screen.pack(fill=X,ipadx=8,ipady=15,padx=10,pady=10)

button_layout = [
    ["1", "2", "3", "/"],
    ["4", "5", "6", "*"],
    ["7", "8", "9", "-"],
    ["C", "0", "=", "+"]
]


for row in button_layout:
    f = Frame(root, bg="#2c4550") 
    for char in row:
        
        b = Button(f, text=char, font="lucida 15 bold", padx=10, width=4)
        
      
        if char == "=":
            b.config(bg="green", fg="white")  
        elif char == "C":
            b.config(bg="red", fg="white")     
            
        b.pack(side=LEFT, padx=1, pady=1, ipadx=2, ipady=2)
        b.bind("<Button-1>", click)
    f.pack()
root.mainloop()
