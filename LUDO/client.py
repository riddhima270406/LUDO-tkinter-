#------------- Boilerplate Code Start------
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None

canvas1 = None
canvas2 = None

playerName = None
nameEntry = None
nameWindow = None
gamewindow = None

dice = None
finish_box = None
player_type = None
r_button = None
turn = None

left_boxes = []
right_boxes = []

player1Name = "joining"
player2Name = "joining"
player1Label = None
player2Label = None
player1Score = 0
player2Score = 0

winning_func_call = 0
winning_msg = None

reset_button = None


def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()
    SERVER.send(playerName.encode())

    gameWindow()

def gameWindow():
    global gamewindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global r_button
    global turn

    gamewindow = Tk()
    gamewindow.title('LUDOOO')

    screen_width = gamewindow.winfo_screenwidth()
    screen_height = gamewindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gamewindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)
    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo game", font=("Chalkboard SE",100), fill="white")

    leftBoard()
    rightBoard()
    finishBox()

    r_button = Button(gamewindow, text='ROLL DICE', font=("Chalkboard SE", 15), width=20, height=5, bg='grey', command=rollDice())
    
    if player_type == 'player1' and turn:
        r_button.place(x=screen_width/2-80, y = screen_height/2+250)
    else:
        r_button.pack_forget()

    if player_type == 'player2' and turn:
        r_button.place(x=screen_width/2-80, y = screen_height/2+250)
    else:
        r_button.pack_forget()

    dice = canvas2.create_text(screen_width/2+10, screen_height/2+100, text='', font=('Arial', 100))
    gamewindow.mainloop()
    

def rollDice():
    global SERVER
    global player_type
    global r_button
    global turn

    diceChoices = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
    value = random.choice(diceChoices)

    r_button.destroy()
    turn = False

    if player_type == 'player1':
        SERVER.send(f'{value}player2turn'.encode())
        
    if player_type == 'player2':
        SERVER.send(f'{value}player1turn'.encode())

def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget("bg")
        if(boxColor == color):
            return boxes.index(box)
    return False


def movePlayer1(steps):
    global left_boxes
    global finish_box
    global SERVER
    global playerName
    
    boxPos = checkColorPosition(left_boxes[1:], "red")
    if boxPos:
        diceValue = steps
        coloredBoxIndex = boxPos
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if steps == remainingSteps:
            for box in left_boxes[1:]:
                box.configure(bg = 'white')
            finish_box.configure(bg='red')
            greet = f'red wins the game!'
            SERVER.send(greet.encode())

        elif steps < remainingSteps:
            for box in left_boxes[1:]:
                box.configure(bg = 'white')
            nextStep = coloredBoxIndex+1+diceValue
            left_boxes[nextStep].configure(bg='red')
        
        else:
            print("MOVE FALSE")

    else:
        left_boxes[steps].configure(bg='red')


def movePlayer2(steps):
    global right_boxes
    global finish_box
    global SERVER
    global playerName
    
    boxPos = checkColorPosition(right_boxes[-2::-1], "yellow")
    if boxPos:
        diceValue = steps
        coloredBoxIndex = boxPos
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if steps == remainingSteps:
            for box in right_boxes[-2::-1]:
                box.configure(bg = 'white')
            finish_box.configure(bg='yellow')
            greet = f'red wins the game!'
            SERVER.send(greet.encode())

        elif steps < remainingSteps:
            for box in right_boxes[-2::-1]:
                box.configure(bg = 'white')
            nextStep = coloredBoxIndex+1+diceValue
            right_boxes[nextStep].configure(bg='yellow')
        
        else:
            print("MOVE FALSE")

    else:
        right_boxes[steps].configure(bg='yellow')


    
def finishBox():
    global gamewindow
    global finish_box
    global screen_height
    global screen_width

    finish_box = Label(gamewindow, text='HOME', font=('Arial Bold', 40), width=7, height=4, bg='green', fg='blue')
    finish_box.place(x=screen_width/2-113, y= screen_height/2-160)



def leftBoard():
    global gamewindow
    global left_boxes
    global screen_height
    global screen_width

    xpos= 50
    for box in range(0,11):
        if box == 0:
            boxLabel = Label(gamewindow, font=('Arial', 30), width = 2, height=1, bg="red")
            boxLabel.place(x = xpos, y = screen_height/2-88)

            left_boxes.append(boxLabel)

            xpos += 55
        else:
            boxLabel = Label(gamewindow, font=('Arial', 30), width = 2, height=1, bg="white")
            boxLabel.place(x = xpos, y = screen_height/2-88)

            left_boxes.append(boxLabel)

            xpos += 55

        
def rightBoard():
    global gamewindow
    global right_boxes
    global screen_height
    global screen_width

    xpos= 888
    for box in range(0,11):
        if box == 10:
            boxLabel = Label(gamewindow, font=('Arial', 30), width = 2, height=1, bg="yellow")
            boxLabel.place(x = xpos, y = screen_height/2-88)

            left_boxes.append(boxLabel)

            xpos += 55
        else:
            boxLabel = Label(gamewindow, font=('Arial', 30), width = 2, height=1, bg="white")
            boxLabel.place(x = xpos, y = screen_height/2-88)

            left_boxes.append(boxLabel)

            xpos += 55


def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1
    global screen_width
    global screen_height

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)

    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def recieveMessage():
    global SERVER
    global player_type
    global turn
    global r_button
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gamewindow
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global winning_func_call

    while True:
        message = SERVER.recv(2048).decode()
        if 'player_type' in message:
            player_type = message['player_type']
            turn = message['turn']
        
        elif 'player_names' in message:
            players = message['player_names']
            for p in players:
                if p['type'] == 'player1':
                    player1Name = p['name']

                if p['type'] == 'player2':
                    player2Name = p['name']
        
        elif '⚀' in message:
            canvas2.itemconfigure(dice,text='\u2680')

        elif '⚁' in message:
            canvas2.itemconfigure(dice,text='\u2681')

        elif '⚂' in message:
            canvas2.itemconfigure(dice,text='\u2682')

        elif '⚃' in message:
            canvas2.itemconfigure(dice,text='\u2683')

        elif '⚄' in message:
            canvas2.itemconfigure(dice,text='\u2684')

        elif '⚅' in message:
            canvas2.itemconfigure(dice,text='\u2685')

        elif 'wins the game!' in message and winning_func_call == 0:
            winning_func_call += 1
            handleWin(message)

        elif message == 'reset game':
            handleResetGame()

        if 'player1turn' in message and player_type == 'player1':
            turn = True
            r_button = Button(gamewindow, text='ROLL DICE', font=("Chalkboard SE", 15), width=20, height=5, bg='grey', command=rollDice())
            r_button.place(x=screen_width/2-80, y = screen_height/2+250)

        if 'player2turn' in message and player_type == 'player2':
            turn = True
            r_button = Button(gamewindow, text='ROLL DICE', font=("Chalkboard SE", 15), width=20, height=5, bg='grey', command=rollDice())
            r_button.place(x=screen_width/2-80, y = screen_height/2+250)

        if 'player1turn' in message or 'player2turn' in message:
            diceChoices = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
            diceValue = diceChoices.index(message[0])+1
            if 'player1turn' in message:
                movePlayer2(diceValue)

            if 'player2turn' in message:
                movePlayer1(diceValue)

 
def handleWin(msg):
    global player_type
    global r_button
    global canvas2
    global winning_msg
    global screen_width
    global screen_height
    global reset_button

    if 'red' in msg:
        if player_type == 'player2':
            r_button.destroy()

    if 'yeellow' in msg:
        if player_type == 'player1':
            r_button.destroy()

    canvas2.itemconfigure(winning_msg, text=msg)
    reset_button.place(x = screen_width/2-80, y = screen_height-220)


def handleResetGame():
    global canvas2
    global player_type
    global gamewindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global right_boxes
    global left_boxes
    global finish_box
    global resetButton
    global winning_msg
    global winning_func_call

    canvas2.itemconfigure(dice, text='\u2680')

    # Handling Reset Game
    if(player_type == 'player1'):
        # Creating roll dice button
        rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
        playerTurn = True

    if(player_type == 'player2'):
        playerTurn = False

    for rBox in right_boxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox  in left_boxes[1:]:
        lBox.configure(bg='white')


    finish_box.configure(bg='green')
    canvas2.itemconfigure(winning_msg, text="")
    resetButton.destroy()

    # Again Recreating Reset Button for next game
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=resetGame, width=20, height=5)
    winning_func_call = 0     


def resetGame():
    global SERVER

    SERVER.send("reset game".encode())   


# Boilerplate Code
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 5000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    thread1  = Thread(target=recieveMessage)
    thread1.start()


    # Creating First Window
    askPlayerName()


setup()