
from pynput import keyboard
from random import randint
import random
import os
import sys 

print("Monster = ~")
print("rock= # ")
print("player = ♂")
print("treasure = $")
print("heals =  ♥ ")


height = 10
width = 15
player = chr(11)
treasure = '$'
monster = '~'
rock = "#"

no_of_monsters = 5
no_of_rocks = 5
no_of_health = 3
score = 0
health_level = 100
health = chr(3)
message = ''
map = [[" "]*width for i in range(height)]

compliment = ["You're amazing!", "Well done!", "Great job!", "Excellent!", "Fantastic!", "That's the way!", "Now you have it!", "Good for you!"]

# generate monsters, notice that the new generated one might overwrite an existing one, so check first
def generate_monsters():
	global no_of_monsters
	while no_of_monsters > 0:
		m_row = randint(0, height-1)
		m_col = randint(0, width-1)
		if map[m_row][m_col] == ' ':
			map[m_row][m_col] = monster
			no_of_monsters -= 1

def generate_rock():
	global no_of_rocks
	while no_of_rocks > 0:
		r_row = randint(0, height-1)
		r_col = randint(0, width-1)
		if map[r_row][r_col] == ' ':
			map[r_row][r_col] = rock
			no_of_rocks -= 1

def generate_health():
	global no_of_health
	while no_of_health > 0:
		h_row = randint(0, height-1)
		h_col = randint(0, width-1)
		if map[h_row][h_col] == ' ':
			map[h_row][h_col] = health
			no_of_health -= 1

def generate_player():
	global row, col
	while True:
		row = randint(0, height-1)
		col = randint(0, width-1)
		if map[row][col] == ' ':
			map[row][col] = player
			break
 
def generate_treasure():
	global row, col
	while True:
		t_row = randint(0, height-1)
		t_col = randint(0, width-1)
		if map[t_row][t_col] == ' ':
			map[t_row][t_col] = treasure
			break

def print_map():
	print(" Use Arror keys for moving [Left, Right, Up, Down], [Space] to Quit")
	print(" ---------------------------------")
	for r in map:
		print(" | ", end='')
		for c in r:
			print(c, end=' ')
		print("|")
	print(" ---------------------------------")
	print(f" You are at {(row, col)} | Score = {score} | Health = {health_level}")
	
def collide_check():	
	global score, health_level, message

	# treasure found
	if map[row][col] == treasure:
		score += 1
		message = random.choice(compliment)

		# when a treasure is found, generate a new one, but check to make sure that the coordinates are not occupied
		while True:			
			t_row = randint(0, height-1)
			t_col = randint(0, width-1)
			if map[t_row][t_col] == ' ':
				map[t_row][t_col] = treasure
				break

	# get more health
	if map[row][col] == health:
		message = " Have a rest and get something to eat."
		health_level += randint(15, 25)
		if health_level > 100:
			health_level = 100

	# hit the monster
	if map[row][col] == monster:
		message = " Oh no! Try to kill th snake or it will kill you."
		health_level -= randint(20, 30)

		# generate another snake
		while True:			
			m_row = randint(0, height-1)
			m_col = randint(0, width-1)
			if map[m_row][m_col] == ' ':
				map[m_row][m_col] = monster
				break

		if health_level <= 0:
			print(" You died!")
			sys.exit()		 

def play(key):
	global row, col, message
	message = ''
	
	map[row][col] = ' '
	match key:	
		case keyboard.Key.left:
			if col==0:
				message = " You hit the left border!"
			elif map[row][col-1]==rock:
				message = " You hit the rock! Be careful, you might be hurt."
			else:				
				col -= 1					
		case keyboard.Key.right:
			if col==width-1:
				message = " You hit the right border!"
			elif map[row][col+1]==rock:
				message = " You hit the rock! Be careful, you might be hurt."
			else:
				col += 1					
		case keyboard.Key.up:
			if row==0:
				message = " You hit the top border!"
			elif map[row-1][col]==rock:
				message = " You hit the rock! Be careful, you might be hurt."
			else:
				row -= 1					
		case keyboard.Key.down:
			if row==height-1:
				message = " You hit the bottom border!"
			elif map[row+1][col]==rock:
				message = " You hit the rock! Be careful, you might be hurt."
			else:
				row += 1					
		case keyboard.Key.space:			
			return False
	collide_check()		
	map[row][col] = player
	os.system('cls')
	print_map()
	if message:
		print(message)

if __name__ == '__main__':
	with keyboard.Listener(on_press=play) as lis:
		generate_monsters()
		generate_rock()
		generate_health()
		generate_player()
		generate_treasure()
		print_map()
		lis.join()	
