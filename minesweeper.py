#!/usr/bin/python3

import random

rows = 20
columns = 10
total_mines = 0
revealed_count = 0

field = list()
row = list()

for i in range(rows):
	row.clear()
	for j in range(columns):
		if (i == 0 and j == 0) or (i == 0 and j == 1) or (i == 1 and j == 0) or (i == 1 and j == 1):
			row.append('E')
			continue
		mine = random.randint(1, 100)
		if mine > 90:
			row.append('M')
			# global total_mines
			total_mines += 1
		else:
			row.append('E')
	field.append(row.copy())


for i in range(rows):
	for j in range(columns):
		if field[i][j] == 'M':
			continue
		k = i-1
		count = 0
		while k <= i+1:
			l = j-1
			while l <= j+1:
				if not (k < 0 or k >= rows or l < 0 or l >= columns):
					if field[k][l] == 'M':
						count += 1
				l += 1
			k += 1
		field[i][j] = count

revealed_field = list()
for i in range(rows):
	row.clear()
	for j in range(columns):
		row.append('F')
	revealed_field.append(row.copy())

print('MINE FIELD')

def display_field():
	print('     ', end='')
	for r in range(len(field[0])):
		print(r, end='   ')
	print()
	for r in range(rows):
		print('    ', end='')
		for slot in range(columns):
			print('---', end=' ')
		print()
		print(f'{r:02}', end = ' ')
		for slot in range(columns):
			print('|', end=' ')
			if revealed_field[r][slot] == 'T':
				if field[r][slot] == 0:
					print(' ', end=' ')
				else:
					print(field[r][slot], end=' ')
			else:
				print('O', end=' ')
		print('|')

	print('   ', end='')
	for r in field[0]:
		print('---', end=' ')
	print()


def reveal(field, revealed_field, x, y):
	if x<0 or y<0 or x>=rows or y>=columns or revealed_field[x][y] == 'T':
		return True
	revealed_field[x][y] = 'T'
	global revealed_count
	revealed_count += 1
	if str(field[x][y]) == 'M':
		print('Stepped on mine. YOU\'RE DEAD!')
		return False
	if field[x][y] == 0:
		reveal(field, revealed_field, x-1, y-1)
		reveal(field, revealed_field, x-1, y)
		reveal(field, revealed_field, x-1, y+1)
		reveal(field, revealed_field, x, y-1)
		reveal(field, revealed_field, x, y+1)
		reveal(field, revealed_field, x+1, y-1)
		reveal(field, revealed_field, x+1, y)
		reveal(field, revealed_field, x+1, y+1)
	return True

print(f'Total mines: {total_mines}')
display_field()

while True:
	x = input('Enter row number: ')
	y = input('Enter column number: ')
	alive = reveal(field, revealed_field, int(x), int(y))
	display_field()
	if revealed_count + total_mines == rows*columns:
		print('YAY! You did it!')
		break
	if not alive:
		break
