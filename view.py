import tkinter as tk
import main

bon = False
numOne, numTwo = 0, 0

def hit_me(title):  #该函数实现按一次按钮显示出字，再按一次消失
    global bon
    if bon == False:
        bon = True
        title.set('Jay Chou')
    else:
        bon = False
        title.set('Sodagreen')

def get_text(enter, content):
    text = enter.get()
    main.main(text)
    show_content(text, content)

def print_selections(lb):
    value = lb.get(lb.curselection())  #获取当前选中的文本
    print("{}".format(value))

def chose_who(choseVar1, choseVar2):
    '''
    选择语料库
    '''
    global numOne
    global numTwo
    numOne = choseVar1.get()
    numTwo = choseVar2.get()

def chose_result():
    '''
    语料库与后台接口
    '''
    print(numOne,numTwo)

def show_content(substr, content):
    content.delete('1.0', 'end')
    content.insert('end', substr)

#设置窗口
def show_it():
    global bon, numOne, numTwo
    window = tk.Tk() #建立一个窗口
    window.title('TheWindow')
    window.geometry('1200x800')
    frame_1 = tk.Frame(window, bg = 'yellow', width = 300, height = 150)
    frame_2 = tk.Frame(window, bg = 'silver', width = 800, height = 600)
    frame_3 = tk.Frame(window, bg = 'pink', width = 300, height = 150)
    frame_1.place(x = 0, y = 0)
    frame_2.place(x = 200, y = 200)
    frame_3.place(x = 1050, y = 0)

    title = tk.StringVar() #文字变量存储器
    title.set('Sodagreen')

    #设置标签
    tk.Label(window, textvariable = title, bg = 'silver', font=('Arial', 12), width = 50, height = 2).pack()
    tk.Button(window, text = 'hit me', width = 20, height = 2, command = lambda:hit_me(title)).pack()
    #输入框
    enter = tk.Entry(window, width = 40, show = None, font = ('Arial', 12))
    enter.place(x = 370, y = 100)
    tk.Button(window, text = '确定输出', width = 10, height = 1, command = lambda:get_text(enter, content)).place(x = 740, y = 100)

    #列表框
    tk.Button(frame_3, text = '确定选择', width = 20, height = 2, command = lambda:print_selections(lb)).pack()
    lb = tk.Listbox(frame_3, width = 10, height = 3)
    items = ['苏打绿','五月天','周杰伦']
    for i in items:
        lb.insert('end',i)
    lb.pack()

    # 选择框
    choseVar1 = tk.IntVar()
    choseVar2 = tk.IntVar()
    chose1 = tk.Checkbutton(frame_1, text = 'python', variable = choseVar1, onvalue = 1, offvalue = 0, command = lambda:chose_who(choseVar1, choseVar2))
    chose2 = tk.Checkbutton(frame_1, text = 'java', variable = choseVar2, onvalue = 1, offvalue = 0, command = lambda:chose_who(choseVar1, choseVar2))
    chose_button = tk.Button(frame_1, text = '确定语言', width = 20, height = 2, command = chose_result)
    chose_button.pack()
    chose1.pack()
    chose2.pack()

    #Content
    content = tk.Text(frame_2, width = 110, height = 5)
    content.pack()

    window.mainloop()
