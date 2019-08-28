# UI using tkinter and ttk (tkintre widgets)
from tkinter import *
from ttk import Button,Combobox
import random

class Matrix():
    def __init__(self,row,col,fill=0):
        self.row = row
        self.col = col
        self.fill = fill
        self.matrix = []
        for i in range(row):
            r =[]
            for j in range(col):
                r.append(fill)
            self.matrix.append(r)

    def __getitem__(self, index):
        return self.matrix[index]

    def transpose(self):
        self.matrix = list(zip(*self.matrix))
        row = self.row
        self.row = self.col
        self.col = row
        for i in range(self.row):
            self.matrix[i] = list(self.matrix[i])

    def merge(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] == self.matrix[i][j-1] and self.matrix[i][j] != self.fill:
                    self.matrix[i][j] = 2 * self.matrix[i][j]
                    self.matrix[i][j-1] = self.fill

    def move(self,d):
        for i in range(self.row):
            if d ==1 :
                for j in range(self.col-1,0,-1):
                    if self.matrix[i][j] ==  self.fill:
                        for k in range(j,-1,1):
                            if self.matrix[i][k]!= self.fill:
                                self.matrix[i][j] = self.matrix[i][k]
                                self.matrix[i][k] = self.fill
                                break
            elif d == -1:
                for j in range(self.col):
                    if self.matrix[i][j] ==  self.fill:
                        for k in range(j,self.col):
                            if self.matrix[i][k]!= self.fill:
                                self.matrix[i][j] = self.matrix[i][k]
                                self.matrix[i][k] = self.fill
                                break

    def random(self,nums = [2,4]):
        pos = []
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] == self.fill:
                    pos.append([i,j])
            if pos:
                i,j = random.choice(pos)
                num = random.choice(nums)
                self.matrix[i][j] = num
    def copy(self):
        matrix = []
        for r in self.matrix:
            nr = []
            for c in r :
                nr.append(c)
            matrix.append(nr)
        return  matrix

    def get(self):
        return self.matrix

    def isWin(self,num= 2048):
        for r in self.matrix:
            if num in r:
                return True
        return False

    def _isOver(self):
        over = True
        for i in range(self.row):
            for j in range(self.col-1):
                if self.matrix[i][j] == self.fill or self.matrix[i][j] ==self.matrix[i][j+1]:
                    return False
        return True

    def isOver(self):
        if self._isOver():
            self.transpose()
            over = self._isOver()
            self.transpose()
            return over
        else:
            return False



colors = {
    '':'#f1c40f',
    2:'#1abc9c',
    4:'#2ecc71',
    8:'#8e44ad',
    16:'#f1c40f',
    32:'#f39c12',
    64:'#34495e',
    128: '#16a085',
    256: '#bdc3c7',
    512: '#95a5a6',
    1024: '#e74c3c'
}
class Board(Frame):
    def __init__(self,parent,row,col ,winOrOver,*args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)

        self.parent = parent
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.moves = 0
        self.winOrOver = winOrOver

        self.parent.bind('<key>',self.moves)
        self.parent.bind('<ButtonPress-1>',self.startMove)
        self.parent.bind('<ButtonRelease-1>',self.move)

        self.moveLabel = Label(self,text = '0',font=(",30"),fg='#f1c40f')
        self.moveLabel.pack(pady=10)
        self.gridFrame = Frame(self)
        self.gridFrame.pack()


        self.matrix = Matrix(row,col,fill= '')
        self.matrix.random()

    def show(self):
        for child in self.winfo_children():
            child.grid_forget()

        for i in range(self.row):
            for j in range(self.col):
                Label(self.gridFrame,text = self.matrix[i][j],font=(",30"),fg ='white',
                      bg = colors[self.matrix[i][j]],width=6,height = 3).grid(row=i,column=j,padx =2,pady=2)

    def startMove(self,event):
        self.x = event.x
        self.y = event.y

    def move(self,event):
        key = event.keysym
        x1 = self.x
        x2 = event.x
        y1 = self.y
        y2 = event.y

        oldmatrix = self.matrix.copy()
        if (x2 -x1 >80 and -50 <y2-y2<50) or key == 'Right':
            self.matrix.merge()
            self.matrix.move(1)
        elif (x1 -x2 >80 and -50 <y2-y2<50) or key == 'Left':
            self.matrix.merge()
            self.matrix.move(-1)
        elif (y2 -y1 >80 and -50 <x2-x2<50) or key == 'Down':
            self.matrix.transpose()
            self.matrix.merge()
            self.matrix.move(1)
            self.matrix.transpose()
        elif (y1-y2 >80 and -50 <x2-x2<50) or key == 'UP':
            self.matrix.transpose()
            self.matrix.merge()
            self.matrix.move(-1)
            self.matrix.transpose()

        if oldmatrix != self.matrix.get():
            self.matrix.random()
            self.show()
            self.moves +=1
            self.moveLabel['text'] = self.moves
        self.winOrOver(self.matrix.isWin(),self.matrix.isOver())

    def stop(self):
        self.parent.unbind('<key>')
        self.parent.unbind('<ButtonPress-1>')
        self.parent.unbind('<ButtonRelease-1>')

class Main():
    def __init__(self,parent):
        self.parent = parent
        self.parent.title("2048")
        self.grid = IntVar()
        self.grid.set(3)
        self.moves = StringVar()
        self.createWidgets()
        self.showMainFrame()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame,text ='2048 Game',font = (",30"),fg="#2980b9").pack(padx = 20,pady = 20)
        f1 = Frame(self.mainFrame)
        Label(f1,text ='Grid').pack(side= LEFT,padx = 5)
        Combobox(f1,textvariable = self.grid).pack(side = LEFT,padx = 50)
        Button(f1,text = 'Play',command= self.play).pack(side = LEFT,padx=5)
        f1.pack(pady=10)

        self.winFrame = Frame(self.parent)
        Label(self.winFrame,text = ' you win!',font = ('',30),fg='#e74c3c').pack(padx=20,pady=10)
        Label(self.winFrame,textvariable = self.moves,font = ('',30),fg='#e74c3c').pack()
        f2 = Frame(self.winFrame)
        Button(f2,text = 'play again',command=self.play).pack(side = LEFT,padx=5)
        Button(f2,text = 'Cancel',command=self.showMainFrame).pack(side = LEFT,padx=5)
        f2.pack(pady = 10)


        self.gameOverFrame = Frame(self.parent)
        Label(self.gameOverFrame,text = 'Gameover!',font = ('',30),fg='#e74c3c').pack(padx=20,pady=10)
        f2 = Frame(self.gameOverFrame)
        Button(f2,text = 'play again',command=self.play).pack(side = LEFT,padx=5)
        Button(f2,text = 'Cancel',command=self.showMainFrame).pack(side = LEFT,padx=5)
        f2.pack(pady = 10)
    def play(self):
        grid =self.grid.get()
        if grid:
            self.mainFrame.pack_forget()
            self.winFrame.pack_forget()
            self.gameOverFrame.pack_forget()
            self.board = Board(self.parent,grid,grid,self.winOrOver)
            self.board.pack()
            self.board.show()

    def winOrOver(self,win,over):
        if win:
            self.showWinFrame()
            self.board.stop()
        elif over:
            self.showGameOverFrame()
            self.board.stop()
    def showWinFrame(self):
        self.board.pack_forget()
        self.moves.set('with {0} moves'.format(self.board.moves))
        self.winFrame.pack()

    def showGameOverFrame(self):
        self.board.pack_forget()
        self.gameOverFrame.pack()

    def showMainFrame(self):
        self.winFrame.pack_forget()
        self.gameOverFrame.pack_forget()
        self.mainFrame.pack()

if __name__ == '__main__':
    root = Tk()
    Main(root)
    root.mainloop()