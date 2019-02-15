from msvcrt import getch
from random import randint 
import os
import time
import msvcrt
from pygame import mixer

ROWSNUMBER = 17
COLUMNSNUMBER = 19
informations = {}
informations["RowsBuff"] = 0
informations["Columnsbuff"] = 1
informations["Alive"] = 1
informations["RowsFood"] = 8
informations["ColumnsFood"] = 14
informations["Points"] = 0
informations["Head"] = '>'
informations["Mute"] = 1
SnakeRows = [8]
SnakeColumns = [9]


def PrintBoard(matriz):
	for i in range(ROWSNUMBER):
		for j in range(COLUMNSNUMBER):
			if j != COLUMNSNUMBER - 1:
				print(matriz[i][j] + ' ', end = '')
			else:
				print(matriz[i][j])
	print(" Score: " + str(informations["Points"]) + " pts")
	if informations["Mute"] == -1:
		print(" MUTED")


def clean():
	os.system('cls' if os.name == 'nt' else 'clear')


def BoardMaker():
	board = []
	for a in range(ROWSNUMBER):
		board = board + [['0']*COLUMNSNUMBER]
	for rows in range(ROWSNUMBER):
		for columns in range(COLUMNSNUMBER):
			if (rows == 0 or columns == 0) or (rows == ROWSNUMBER - 1 or columns == COLUMNSNUMBER - 1):
				board[rows][columns] = '+'
			else:
				board[rows][columns] = ' '
	for n in range(len(SnakeRows)):
		if n == 0:
			board[SnakeRows[0]][SnakeColumns[0]] = informations["Head"]
		else:
			board[SnakeRows[n]][SnakeColumns[n]] = '*'
	board[informations["RowsFood"]][informations["ColumnsFood"]] = 'O'
	return board


def die():
	informations["Alive"] = 0


def food(board):
	informations["RowsFood"] = randint(1, ROWSNUMBER - 2)
	informations["ColumnsFood"] = randint(1, COLUMNSNUMBER - 2)
	FoodPosition = board[informations["RowsFood"]][informations["ColumnsFood"]]
	while (FoodPosition == '+' or FoodPosition == informations["Head"]) or (FoodPosition == '*' or FoodPosition == 'O'):
		informations["RowsFood"] = randint(1, ROWSNUMBER - 2)
		informations["ColumnsFood"] = randint(1, COLUMNSNUMBER - 2)
		FoodPosition = board[informations["RowsFood"]][informations["ColumnsFood"]]

def IncreaseSize():
	informations["Points"] += 1
	global SnakeRows
	global SnakeColumns
	SnakeRows = [SnakeRows[0] + informations["RowsBuff"]] + SnakeRows 
	SnakeColumns = [SnakeColumns[0] + informations["Columnsbuff"]] + SnakeColumns

def walk():
	global SnakeRows
	global SnakeColumns
	SnakeRows = [SnakeRows[0] + informations["RowsBuff"]] + SnakeRows[:-1]
	SnakeColumns = [SnakeColumns[0] + informations["Columnsbuff"]] + SnakeColumns[:-1]

def song():
	mixer.init()
	mixer.music.load("kagamine.ogg")
	mixer.music.play(-1)
	mixer.music.set_volume(0.1)

def Mute(a):
	if a == 1:
		mixer.music.set_volume(0.1)
	else:
		mixer.music.set_volume(0.0)

def decision(board):
	NextPosition = board[SnakeRows[0] + informations["RowsBuff"]][SnakeColumns[0] + informations["Columnsbuff"]]
	if NextPosition == 'O':
		IncreaseSize()
		food(BoardMaker())
	elif (NextPosition == '+' or NextPosition == informations["Head"]) or NextPosition == '*':
		die()
	else:
		walk()

def ShowCommands():
	print(" Valid commands:")
	print("  W - Up")
	print("  S - Down")
	print("  A - Left")
	print("  D - Right")
	print("  M - Mute/Desmute")
	getch()

def play():
	song()
	while informations["Alive"] == 1:
		if msvcrt.kbhit():
			key = getch().lower().decode('utf-8')
			if key == 'w' and informations["RowsBuff"] != 1:
				informations["RowsBuff"] = -1
				informations["Columnsbuff"] = 0 
				informations["Head"] = '^'
			elif key == 's' and informations["RowsBuff"] != -1:
				informations["RowsBuff"] = 1 
				informations["Columnsbuff"] = 0
				informations["Head"] = 'v'
			elif key == 'a' and informations["Columnsbuff"] != 1:
				informations["Columnsbuff"] = -1 
				informations["RowsBuff"] = 0
				informations["Head"] = '<'
			elif key == 'd' and informations["Columnsbuff"] != -1:
				informations["Columnsbuff"] = 1
				informations["RowsBuff"] = 0
				informations["Head"] = '>'
			elif key == 'm':
				informations["Mute"] = informations["Mute"] * -1
				Mute(informations["Mute"])
			else:
				ShowCommands()
		decision(BoardMaker())
		clean()
		PrintBoard(BoardMaker())
		time.sleep(0.27)

play()