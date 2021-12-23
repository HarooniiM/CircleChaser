from tkinter import *
from time import *
from math import *
from random import *
import pygame,sys
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()
base_font = pygame.font.Font(None,32)

root = Tk()
screen = Canvas( root, width=800, height=800, background = "white" )

def setInitialValues():
    global sx, sy, sr, sxspeed, syspeed
    global cx,cy,cr,circle,num, cxspeed,cyspeed
    global mode, userQuit, gameOver, colors, startTime, gameClock, left, true, end, score

    colors = ["brown","orange","red","green","blue","cyan","pink","gold3","blue4","dark slate gray"]
    
    sx = 400
    sy = 600
    sr = 70
    sxspeed = 0
    syspeed = 0

    num = 0
    cx = []
    cy = []
    cr = []
    circle = []
    cxspeed = []
    cyspeed = []

    ox = []
    oy = []

    true = 0

    if roundnum <= 1:
        num = 1
        gameClock = 15
    elif roundnum <= 3:
        num = randint(3,5)
        gameClock = 20
    elif roundnum <= 8:
        num = randint(5,7)
        gameClock = 30
    elif roundnum <= 12:
        num = randint(6,9)
        gameClock = 35
    else:
        num = randint(8,10)
        gameClock = 60

    for i in range (num):
        circle.append(3476)
        cx.append(randint(50,750))
        cy.append(randint(50,200))
        cxspeed.append(randint(-10,10))
        cyspeed.append(randint(-10,10))
        ox.append(randint(50,750))
        oy.append(randint(50,200))

        if roundnum <= 3:
            cr.append(randint(20,35))
        elif roundnum <= 8:
            cr.append(randint(35,50))
        elif roundnum <= 12:
            cr.append(randint(40,60))
        else:
            cr.append(randint(50,65))

    startTime = time()
    
    left = num
    
    userQuit = False
    gameOver = False

def setData():
    global highscore, score,d
    
    try:
        with open("data.txt", "r") as d:
            highscore = int(d.read())

    except:
        highscore = 0

def setLeaderboard():
    global pos,l,sortTitle
    with open("leaderboard.txt", "r") as l:
        pos = l.readlines()
        sortTitle = sorted(pos,reverse=True)
        
def setup():
    global best, title, qquit
    Play.destroy()
    instruct.destroy()
    Exit.destroy()
    screen.delete(title, best, runner, maker, losedata)
    qquit = screen.create_text(740,10,text='press "Esc" to quit',font="Times 10", fill="black")

    
def keyDownHandler(event):
    global userQuit, sxspeed, syspeed, left, num, circle, score, cr

    if event.keysym == "w" or event.keysym == "Up":
        sxspeed = 0
        syspeed = -10

    elif event.keysym == "s" or event.keysym == "Down" :
        syspeed = 10
        sxspeed = 0

    elif event.keysym == "a" or event.keysym == "Left":
        sxspeed = -10
        syspeed = 0

    elif event.keysym == "d" or event.keysym == "Right" :
        sxspeed = 10
        syspeed = 0

    elif event.keysym == "Escape":
        userQuit = True

            
    elif event.keysym == "Delete":
        if true == 1:
            with open("data.txt", "w") as d:
                d.write("%d" % 0)
            with open("leaderboard.txt", "w") as l:
                l.write("")
            setup()
            screen.delete(qquit)
            initialSetup()
        

    elif event.keysym == "space":
        for i in range(num):
            if cx[i] >= sx and cy[i] >= sy and cy[i] + cr[i] <= sy + sr and cx[i] +cr[i] <= sx + sr:
                screen.delete(circle[i])
                cx[i] = 10000 #the circle caught moves off screen
                cy[i] = 10000
                left = left - 1
                score = score + cr[i]
                if left >= 1:
                    mixer.music.load("ding.mp3")
                    mixer.music.play()
                
def keyUpHandler (event):
    global sxspeed, syspeed

    if true == 0:
        sxspeed = sxspeed
        syspeed = syspeed

def updatecircle():
    global cx, cy, cxspeed, cyspeed
    for i in range(num):
            cx[i] = cx[i] + cxspeed[i]
            cy[i] = cy[i] + cyspeed[i]

            if cx[i] <= 0:
                cxspeed[i] = randint(5,10)
            if cx[i] >= 800 - cr[i]:
                cxspeed[i] = randint(-10,-5)
            if cy[i] <= 0:
                cyspeed[i] = randint(5,10)
            if cy[i] >= 800 - cr[i]:
                cyspeed[i] = randint(-10,-5)

def updatesquare():
    global sx, sy, sxspeed, syspeed, sr

    sx = sx + sxspeed
    sy = sy + syspeed

    if sx <= 0:
        sx = 0
    if sx >= 800 - sr:
        sx = 800 - sr
    if sy <= 0:
        sy = 0 
    if sy >= 800 - sr:
        sy = 800 - sr
    

def updateTimer(): 
    global startTime, gameClock

    timeSinceLastTick = time() - startTime

    if timeSinceLastTick >= 1:
        gameClock = gameClock - 1
        startTime = time()
   

def drawcircle():
    global circle, num, points, resolution
    for i in range(num):
        resolution = 100000
        points = [cx[i], cy[i],
              cx[i]+cr[i], cy[i],
              cx[i]+cr[i], cy[i]+cr[i],
              cx[i], cy[i]+cr[i],
              cx[i], cy[i]]
        circle[i] = screen.create_polygon(points, fill=colors[i], smooth=True, splinesteps=resolution)


def drawsquare():
    global cube
    cube=screen.create_rectangle(sx,sy,sx+sr,sy+sr,outline="purple",width=5)

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return screen.create_polygon(points, **kwargs, smooth=True)

def drawStats():
    global clockDrawing, leftDraw, rank, high, border1, border2
    border1 = round_rectangle(5, 10, 150, 100, radius=20, fill="black", outline="grey",width = 3)
    border2 = round_rectangle(718, 698, 798, 798, radius=20, fill="black",outline="grey",width = 3)
    clockDrawing = screen.create_text(750, 730, text=str(gameClock), font = "Times 20", anchor = CENTER, fill="white")
    leftDraw = screen.create_text(770, 770, text = str(left), font = "Times 35", anchor=CENTER, fill="white")
    rank = screen.create_text(75,70, text = "score: "+str(score), font = "times 20",fill = "white")
    high = screen.create_text(65,40,text = "HighScore: "+str(highscore),font="Arial 10", fill = "white")
    

def deleteImages():
    num, circle
    screen.delete(clockDrawing, leftDraw, cube, rank, high, border1, border2)#DELETES THE TIMER AND CUBE
    for i in range(num):
        screen.delete(circle[i])

def updatescore():
    global score, highscore, d
    
    if highscore < score:
        with open("data.txt", "w") as d:
            d.write("%d" % score)

    setData()

def updateLeaderboard():
    global l, thescore, score

    thescore = str(score)
     
    if score < 10:
        thescore = "0"+thescore
    if score < 100:
        thescore = "0"+thescore
    if score < 1000:
        thescore = "0"+thescore

        
    try:
        with open("leaderboard.txt","a") as l:
            l.write(thescore+" | "+name+"\n")

    except:
        ban=""

    setLeaderboard()
    
def userquit():
    if userQuit == True:
        return True
    else:
        return False

def deletion():
    screen.delete(cube, clockDrawing, leftDraw,context,title, border1, border2,rank,high)

    for i in range(num):
        screen.delete(circle[i])
        
######### INTRO #########
def initialSetup():
    setData()
    setLeaderboard()
    rungame()
    
def rungame():
    global losedata, runner, true, clean, title, Exit, instruct,Play, roundnum, score, highscore, best, maker, end
    
    true = 1
    score = 0

    #title cover
    clean = PhotoImage(file = "titlescreen.png")
    runner = screen.create_image(400,450,image = clean,anchor=CENTER)
    title = screen.create_text(400,85,text="Circle Chaser",font="Arial 60", fill="black")
    maker = screen.create_text(400,135, text = "By: Haroon Moammer", font = "Arial 15", fill="black")
    best = screen.create_text(400,180,text = "HighScore: "+str(highscore),font="Arial 20", fill = "black")
    losedata = screen.create_text(400,790, text = "press 'delete' to erase all data", font="Times 10", fill = "black")                             
    #quit 
    Exit = Button(root,text="Leaderboard", font="Arial 30", command = Leaderboard, anchor = CENTER, bg="grey90")
    Exit.pack()
    Exit.place(x = 450, y = 675, width = 250 , height = 100)

    #play    
    Play = Button(root,text = "Play", font = "Times 30", command = playButtonNormalPressed, anchor = CENTER, bg="grey90")  #button for normal mode
    Play.pack()
    Play.place(x = 285, y = 550, width = 220 , height = 100 )
    
    #see instructions
    instruct = Button(root,text="Instructions", font="Arial 30", command = instruction, anchor = CENTER, bg="grey90")
    instruct.pack()
    instruct.place(x = 150, y = 675, width = 220 , height = 100)

def Leaderboard():
    global backtomenu, bar,ttl
    
    instruct.destroy()
    Exit.destroy()
    Play.destroy()
    screen.delete(best, runner,title,maker, losedata)

    backtomenu = Button(root,text="Back", font="Times 30",command=back2,anchor = CENTER, bg="grey90")
    backtomenu.pack()
    backtomenu.place(x = 300, y = 675, width = 225 , height = 100)

    ttl = screen.create_text(400,50,text="Leaderboard",font="Arial 40 bold", fill="black")
    bar = round_rectangle(150,100,650,650, fill="black")
    for i in range (10):
        try:
            rank = str(i+1)+"."+"\t"+str(sortTitle[i])
        except:
            rank = str(i+1)+"."+"\t"+"------"
        screen.create_text(400,150+i*50,text = rank, font = "Arial 30 bold", fill="white")
    
#WHEN THE NORMAL BUTTON IS PRESSED
def playButtonNormalPressed():
    global roundnum
    roundnum = 0
    play()
    
def instruction():
    global letter,msg,backtomenu
    instruct.destroy()
    Exit.destroy()
    Play.destroy()
    screen.delete(best, runner, losedata)
    letter = PhotoImage(file = "Instruction.png")
    msg = screen.create_image(400,405,image=letter,anchor=CENTER)

    backtomenu = Button(root,text="Back", font="Times 30",command=back,anchor = CENTER, bg="grey90")
    backtomenu.pack()
    backtomenu.place(x = 300, y = 675, width = 225 , height = 100)

def back2():
    backtomenu.destroy()
    screen.delete(bar,ttl)
    rungame()
    
def back():
    backtomenu.destroy()
    screen.delete(msg,title,maker,losedata)
    rungame()

def play():
    global num, sx, sy, sxspeed, syspeed, gameClock, gameOver, userQuit, left, roundnum

    roundnum += 1
    
    setInitialValues()
    setup()

    
    
    while userQuit == False and gameOver == False:
        updatesquare()
        updateTimer()
        updatecircle()

        drawStats()
        drawsquare()
        drawcircle()

        if left == 0:
            gameOver = True
            
        elif gameClock <= 0:
            gameOver = True
            
        screen.update()
        sleep(0.03)
        deleteImages()
        
    
    over()

def over():
    global backdrop, context, highscore, score, latestscore, gamenum, insert, end, box, printttl, printscr, txtfield,ok

    screen.delete(qquit)
    
    if userQuit == True:
        gameOverMessage = ""

        context = screen.create_text( 400, 400, text = gameOverMessage, font = "Times 25 bold",anchor=CENTER, fill = "black" )

        deletion()
        rungame()
        
    elif gameClock <=0:
        gameOver = True
        context = "Insert Name"
        
        mixer.music.load("huh.mp3")
        mixer.music.play()

        updatescore()

        box = round_rectangle(280,280,520,520,fill="black",outline="grey",width=5)
        printttl = screen.create_text(400,325,text = "SCORE:", font = "Times 20", anchor=CENTER, fill="white")
        printscr = screen.create_text(400,355, text=score, font = "Times 25 bold", anchor=CENTER, fill = "white")
        insert = screen.create_text( 400, 405, text = context, font = "Times 20 bold",anchor=CENTER, fill = "white" )
        txtfield = Entry(root,font="Arial 20 bold", justify="center")
        txtfield.pack()
        txtfield.place(x = 325, y = 435, width = 150 , height = 40)

            
        ok = Button(root,state = "normal",text="OK", font="Times 30", command=returnn ,anchor = CENTER, bg="grey90")
        ok.pack()
        ok.place(x=350,y=480,width = 100, height = 35)
            
        screen.update()
        deletion()
            

    elif left == 0:
        gameOver = False
        
        gameOverMessage = "SUCESS!"

        mixer.music.load("win.mp3")
        mixer.music.play()
        context = screen.create_text( 400, 400, text = gameOverMessage, font = "Times 25 bold",anchor=CENTER, fill = "black" )
                
        screen.update()
        
        deletion()
        sleep(1)
        play()
        
def returnn():
    global name
    name = txtfield.get()
    updateLeaderboard()
    screen.focus_set()
    
    screen.delete(box,printttl, printscr, insert)
    ok.destroy()
    
    txtfield.delete(0,"end")
    txtfield.destroy()
    

    screen.update()
    rungame()


  
#starts the game by passing control to the procedure rungame()
root.after(5, initialSetup)

#BINDS THE USER'S KEY-STROKES TO THE PROCEDURE keyDownHandler(forpressingkeys)
screen.bind("<Key>", keyDownHandler)

#BINDS THE USER'S KEY-STROKES TO THE PROCEDURE keyUpHandler(forreleasingkeys)
screen.bind("<KeyRelease>", keyUpHandler)

#creates the screen and sets the event listeners
screen.pack()
screen.focus_set()

#starts the program
root.mainloop()
