import tkinter as tk
from tkinter import *
import tkinter.font as font 
from run import game_controller 
import os, sys

# 图片路径(相对路径:当前文件所在目录, 图片名字)
imgs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tutorial_poses')

# 创建窗口:展示游戏界面
def img1():
    Pic = tk.Toplevel()             # 图片
    Pic.title("Rule 1")             # 图片标题
    Pic.geometry("550x800")         # 图片大小
    canvas1 = Canvas(Pic, width = 400, height = 800)                # 创建画布  
    img1 = PhotoImage(file=os.path.join(imgs_path, 'no_move.gif'))  # 再次创建图片:重命名图片     
    canvas1.create_image(20,20, anchor=NW, image=img1)              # 在画布上添加图片
    canvas1.pack()                                                  # 将画布添加到窗口
    Pic.mainloop()                                                  # 展示图片窗口
    
def img2():                         # 创建图片2
    Pic = tk.Toplevel()             # 图片
    Pic.title("Rule 2")             # 图片标题
    Pic.geometry("550x750")         # 图片大小  
    canvas2 = Canvas(Pic, width = 900, height = 1200)               # 创建画布 
    img2 = PhotoImage(file=os.path.join(imgs_path, 'hook.gif'))     # 再次创建图片:重命名图片
    canvas2.create_image(20,20, anchor=NW, image=img2)              # 在画布上添加图片
    canvas2.pack()                                                  # 将画布添加到窗口
    Pic.mainloop()                                                  # 展示图片窗口

def img3():                        # 创建图片3
    Pic = tk.Toplevel()            # 图片
    Pic.title("Rule 3")            # 图片标题
    Pic.geometry("450x550")        # 图片大小
    canvas3 = Canvas(Pic, width = 900, height = 500)                # 创建画布
    canvas3.pack()                                                  # 将画布添加到窗口
    img3 = PhotoImage(file=os.path.join(imgs_path, 'kick.gif'))     # 再次创建图片:重命名图片  
    canvas3.create_image(20,20, anchor=NW, image=img3)              # 在画布上添加图片
    canvas3.pack()                                                  # 将画布添加到窗口
    Pic.mainloop()                                                  # 展示图片窗口

def img4():                        # 创建图片4
    Pic = tk.Toplevel()            # 图片
    Pic.title("Rule 4")            # 图片标题
    Pic.geometry("550x750")        # 图片大小
    canvas4 = Canvas(Pic, width = 900, height = 800)                # 创建画布
    canvas4.pack()                                                  # 将画布添加到窗口
    img4 = PhotoImage(file=os.path.join(imgs_path, 'crouch.gif'))   # 再次创建图片:重命名图片    
    canvas4.create_image(20,20, anchor=NW, image=img4)              # 在画布上添加图片
    canvas4.pack()
    Pic.mainloop()

def img5():                        # 创建图片5
    Pic = tk.Toplevel()            # 图片
    Pic.title("Rule 5")            # 图片标题
    Pic.geometry("550x750")        # 图片大小
    canvas5 = Canvas(Pic, width = 900, height = 800)                # 创建画布      
    canvas5.pack()                                                  # 将画布添加到窗口
    img5 = PhotoImage(file=os.path.join(imgs_path, 'special.gif'))  # 再次创建图片:重命名图片    
    canvas5.create_image(20,20, anchor=NW, image=img5)              # 在画布上添加图片
    canvas5.pack()                                                  # 将画布添加到窗口
    Pic.mainloop()                                                  # 展示图片窗口

#   创建规则(应该是属性和内置方法)
def create_rules(): 
    rules = tk.Toplevel()           # 图片
    rules.geometry("750x750")       # 图片大小
    rules.title("How to Play")      # 图片标题:规则 How to Play
    sb = Scrollbar(rules, orient = 'vertical')  # 创建滚动条
    sb.pack(side = RIGHT, fill = Y) # 将滚动条添加到窗口

    # 按钮1
    r1 = Button(rules,text = "Rule 1",command = img1, fg='red',bg='blue',pady=1,padx=1) 
    r1.place(x=100,y=200)                           # 将按钮添加到窗口的位置
    r1['font']= font.Font(size=10, weight="bold")   # 设置字体大小和粗体

    # 按钮2
    r2 = Button(rules,text = "Rule 2",command = img2, fg='red',bg='blue',pady=1,padx=1)
    r2.place(x=200,y=200)                           # 将按钮添加到窗口的位置
    r2['font']= font.Font(size=10, weight="bold")   # 设置字体大小和粗体

    # 按钮3
    r3 = Button(rules,text = "Rule 3",command = img3, fg='red',bg='blue',pady=1,padx=1)
    r3.place(x=300,y=200)                           # 将按钮添加到窗口的位置
    r3['font']= font.Font(size=10, weight="bold")   # 设置字体大小和粗体

    r4 = Button(rules,text = "Rule 4",command = img4, fg='red',bg='blue',pady=1,padx=1)
    r4.place(x=400,y=200)                           # 将按钮添加到窗口的位置
    r4['font']= font.Font(size=10, weight="bold")   # 设置字体大小和粗体

    r5 = Button(rules,text = "Rule 5",command = img5, fg='red',bg='blue',pady=1,padx=1)
    r5.place(x=500,y=200)                           # 将按钮添加到窗口的位置
    r5['font']= font.Font(size=10, weight="bold")   # 设置字体大小和粗体

    L1 = Label(rules, text = "How 2 Play")          # 创建标签
    L1.config(font =("Times New Roman", 20))        # 设置字体大小和粗体
    L1.config(anchor=CENTER)                        # 设置标签的位置
    L1.pack()                                       # 将标签添加到窗口
    
    Tip1 = Label(rules, text = "1. 并排移动角色")    # 创建标签
    Tip1.config(font =("Times New Roman", 12))      # 设置字体大小和粗体
    Tip1.config(anchor=CENTER)                      # 设置标签的位置
    Tip1.pack()                                     # 将标签添加到窗口

    Tip2 = Label(rules, text = "2.抬起左臂执行冲床移动")
    Tip2.config(font =("Times New Roman", 12))      # 设置字体大小和粗体
    Tip2.config(anchor=CENTER)                      # 设置标签的位置
    Tip2.pack()


    Tip3 = Label(rules, text = "3.用腿踢腿，完成踢腿动作")
    Tip3.config(font =("Times New Roman", 12))
    Tip3.config(anchor=CENTER)
    Tip3.pack()

    Tip4 = Label(rules, text = "4.Sqaut让你的角色俯冲下来 ")
    Tip4.config(font =("Times New Roman", 12))
    Tip4.config(anchor=CENTER)
    Tip4.pack()

    Tip5 = Label(rules, text = "5.双手并拢，手掌伸开，伸出双臂进行特殊攻击")
    Tip5.config(font =("Times New Roman", 12))
    Tip5.config(anchor=CENTER)
    Tip5.pack()

    rules.mainloop()                            # 主循环

main = Tk()                                     # 创建主窗口
main.geometry("500x500")                        # 设置窗口大小
main.title("Pose2Play")                         # 设置窗口标题

LTitle = Label(main, text = "Pose2Play")        # 创建标签
LTitle.config(font =("Times New Roman", 30))    # 设置字体大小和粗体
LTitle.config(anchor=CENTER)                    # 设置标签的位置
LTitle.pack()                                   # 将标签添加到窗口

def exit_game():                                # 定义退出函数
    sys.exit(0)                                 # 退出程序

# 打开游戏
OpenGame = Button(main,text = "New \n Game",command = game_controller,fg='black',bg='blue',pady=10,padx=20)
OpenGame.place(x=115,y=200)
OpenGame['font']= font.Font(size=15, weight="bold")

# 关闭游戏
CloseGame = Button(main,text = "Close \n Game",command = exit_game,fg='black',bg='blue',pady=10,padx=20)
CloseGame.place(x=265,y=200)
CloseGame['font']= font.Font(size=15, weight="bold")

# 游戏规则
GameRules = Button(main,text = "How Do You Play?",command = create_rules,fg='black',bg='blue',pady=7.5,padx=20)
GameRules.place(x=175,y=350)
GameRules['font']= font.Font(size=9, weight="bold")

# 主循环
main.mainloop()
