import tkinter as tk
from tkinter import *
import tkinter.font as font
from run import game_controller
import os, sys

imgs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tutorial_poses')

def img1():
    Pic = tk.Toplevel()
    Pic.title("Rule 1")
    Pic.geometry("550x800")
    canvas1 = Canvas(Pic, width = 400, height = 800)      
    img1 = PhotoImage(file=os.path.join(imgs_path, 'no_move.gif'))      
    canvas1.create_image(20,20, anchor=NW, image=img1)
    canvas1.pack()
    Pic.mainloop()
    
def img2():
    Pic = tk.Toplevel()
    Pic.title("Rule 2")
    Pic.geometry("550x750")
    canvas2 = Canvas(Pic, width = 900, height = 1200)      
    img2 = PhotoImage(file=os.path.join(imgs_path, 'hook.gif'))      
    canvas2.create_image(20,20, anchor=NW, image=img2)
    canvas2.pack()
    Pic.mainloop()

def img3():
    Pic = tk.Toplevel()
    Pic.title("Rule 3")
    Pic.geometry("450x550")
    canvas3 = Canvas(Pic, width = 900, height = 500)      
    canvas3.pack()
    img3 = PhotoImage(file=os.path.join(imgs_path, 'kick.gif'))      
    canvas3.create_image(20,20, anchor=NW, image=img3)
    canvas3.pack()
    Pic.mainloop()

def img4():
    Pic = tk.Toplevel()
    Pic.title("Rule 4")
    Pic.geometry("550x750")
    canvas4 = Canvas(Pic, width = 900, height = 800)      
    canvas4.pack()
    img4 = PhotoImage(file=os.path.join(imgs_path, 'crouch.gif'))      
    canvas4.create_image(20,20, anchor=NW, image=img4)
    canvas4.pack()
    Pic.mainloop()

def img5():
    Pic = tk.Toplevel()
    Pic.title("Rule 5")
    Pic.geometry("550x750")
    canvas5 = Canvas(Pic, width = 900, height = 800)      
    canvas5.pack()
    img5 = PhotoImage(file=os.path.join(imgs_path, 'special.gif'))      
    canvas5.create_image(20,20, anchor=NW, image=img5)
    canvas5.pack()
    Pic.mainloop()


def create_rules():
    rules = tk.Toplevel()
    rules.geometry("750x750")
    rules.title("How to Play")
    sb = Scrollbar(rules, orient = 'vertical')  
    sb.pack(side = RIGHT, fill = Y)

    r1 = Button(rules,text = "Rule 1",command = img1, fg='red',bg='blue',pady=1,padx=1)
    r1.place(x=100,y=200)
    r1['font']= font.Font(size=10, weight="bold")

    r2 = Button(rules,text = "Rule 2",command = img2, fg='red',bg='blue',pady=1,padx=1)
    r2.place(x=200,y=200)
    r2['font']= font.Font(size=10, weight="bold")

    r3 = Button(rules,text = "Rule 3",command = img3, fg='red',bg='blue',pady=1,padx=1)
    r3.place(x=300,y=200)
    r3['font']= font.Font(size=10, weight="bold")

    r4 = Button(rules,text = "Rule 4",command = img4, fg='red',bg='blue',pady=1,padx=1)
    r4.place(x=400,y=200)
    r4['font']= font.Font(size=10, weight="bold")

    r5 = Button(rules,text = "Rule 5",command = img5, fg='red',bg='blue',pady=1,padx=1)
    r5.place(x=500,y=200)
    r5['font']= font.Font(size=10, weight="bold")

    L1 = Label(rules, text = "How 2 Play")
    L1.config(font =("Times New Roman", 20))
    L1.config(anchor=CENTER)
    L1.pack()
    
    Tip1 = Label(rules, text = "1. Step side to side to move your character")
    Tip1.config(font =("Times New Roman", 12))
    Tip1.config(anchor=CENTER)
    Tip1.pack()

    Tip2 = Label(rules, text = "2. Raise your left arm to perform the punch move")
    Tip2.config(font =("Times New Roman", 12))
    Tip2.config(anchor=CENTER)
    Tip2.pack()


    Tip3 = Label(rules, text = "3. Kick with your leg to perform the kick move")
    Tip3.config(font =("Times New Roman", 12))
    Tip3.config(anchor=CENTER)
    Tip3.pack()

    Tip4 = Label(rules, text = "4. Sqaut to make your character duck down")
    Tip4.config(font =("Times New Roman", 12))
    Tip4.config(anchor=CENTER)
    Tip4.pack()

    Tip5 = Label(rules, text = "5. Place your two hands together, palms extended, \n and stick your arms out to perform a special attack!")
    Tip5.config(font =("Times New Roman", 12))
    Tip5.config(anchor=CENTER)
    Tip5.pack()

    rules.mainloop()

main = Tk()  
main.geometry("500x500")
main.title("Pose2Play")

LTitle = Label(main, text = "Pose2Play")
LTitle.config(font =("Times New Roman", 30))
LTitle.config(anchor=CENTER)
LTitle.pack()

def exit_game():
    sys.exit(0)

OpenGame = Button(main,text = "New \n Game",command = game_controller,fg='black',bg='blue',pady=10,padx=20)
OpenGame.place(x=115,y=200)
OpenGame['font']= font.Font(size=15, weight="bold")

CloseGame = Button(main,text = "Close \n Game",command = exit_game,fg='black',bg='blue',pady=10,padx=20)
CloseGame.place(x=265,y=200)
CloseGame['font']= font.Font(size=15, weight="bold")

GameRules = Button(main,text = "How Do You Play?",command = create_rules,fg='black',bg='blue',pady=7.5,padx=20)
GameRules.place(x=175,y=350)
GameRules['font']= font.Font(size=9, weight="bold")

main.mainloop()
