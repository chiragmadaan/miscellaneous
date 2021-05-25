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
		if mine > 85:
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
displayed_field = list()
for i in range(rows):
	row.clear()
	for j in range(columns):
		row.append('F')
	revealed_field.append(row.copy())

for i in range(rows):
	row.clear()
	for j in range(columns):
		row.append('O')
	displayed_field.append(row.copy())


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

def show_displayed_field():
	global displayed_field
	print()
	print()
	print('Showing displayed field')
	print('     ', end='')
	for r in range(len(displayed_field[0])):
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
			print(displayed_field[r][slot], end=' ')
		print('|')

	print('    ', end='')
	for r in field[0]:
		print('---', end=' ')
	print()

def reveal(field, revealed_field, x, y, displayed_field):
	if x<0 or y<0 or x>=rows or y>=columns or revealed_field[x][y] == 'T':
		return True
	revealed_field[x][y] = 'T'
	displayed_field[x][y] = field[x][y]
	# print(f'Revealed {displayed_field[x][y]} at ({x},{y})')
	if displayed_field[x][y] == 0:
		displayed_field[x][y] = ' '
	global revealed_count
	revealed_count += 1
	if str(field[x][y]) == 'M':
		print('Stepped on a mine. YOU\'RE DEAD!')
		return False
	if field[x][y] == 0:
		reveal(field, revealed_field, x-1, y-1, displayed_field)
		reveal(field, revealed_field, x-1, y, displayed_field)
		reveal(field, revealed_field, x-1, y+1, displayed_field)
		reveal(field, revealed_field, x, y-1, displayed_field)
		reveal(field, revealed_field, x, y+1, displayed_field)
		reveal(field, revealed_field, x+1, y-1, displayed_field)
		reveal(field, revealed_field, x+1, y, displayed_field)
		reveal(field, revealed_field, x+1, y+1, displayed_field)
	return True

def reveal_cells(field, revealed_field, displayed_field, cells):
	for cell in cells:
		if not reveal(field, revealed_field, cell[0], cell[1], displayed_field):
			return False
	return True

def mark_a_mine(displayed_field, x, y):
	displayed_field[x][y] = 'M'

def unmark_a_mine(displayed_field, x, y):
	displayed_field[x][y] = 'O'

def mark_mines(displayed_field, mines):
	for mine in mines:
		mark_a_mine(displayed_field, mine[0], mine[1])

def are_neighbours(cells):
	if len(cells) != 2 or cells[0] == cells[1]:
		return False
	if abs(cells[0][0]-cells[1][0]) < 2 and abs(cells[0][1]-cells[1][1]) < 2:
		return True
	return False

def are_one_away_neighbours(cells):
	if len(cells) != 2 or cells[0] == cells[1]:
		return False
	if abs(cells[0][0]-cells[1][0]) < 3 and abs(cells[0][1]-cells[1][1]) < 3:
		return True
	return False

def find_common_neighbours(cells):
	x1 = cells[0][0]
	y1 = cells[0][1]
	x2 = cells[1][0]
	y2 = cells[1][1]
	if x1 == x2 and y1 == y2-1:
		return [(x1-1, y1), (x1-1, y2), (x1+1, y1), (x1+1, y2)]
	elif x1 == x2-1 and y1 == y2:
		return [(x1, y1-1), (x1, y1+1), (x2, y1-1), (x2, y1+1)]
	elif abs(x1-x2) == 1 and abs(y1-y2) == 1:
		return [(x1, y2), (x2, y1)]
	elif x1 == x2 and y1 == y2-2:
		return [(x1-1, y1+1), (x1, y1+1), (x1+1, y1+1)]
	elif x1 == x2-2 and y1 == y2:	
		return [(x1+1, y1-1), (x1+1, y1), (x1+1, y1+1)]
	elif abs(x1-x2) == 2 and abs(y1-y2) == 2:
		return [(x1+1, min(y1,y2)+1)]
	elif abs(x1-x2) == 2 and abs(y1-y2) == 1:
		return [(x1+1, min(y1,y2)), (x1+1, max(y1,y2))]
	elif abs(x1-x2) == 1 and abs(y1-y2) == 1:
		return [(x1, min(y1,y2)+1), (x2, min(y1,y2)+1)]
	return None

def second_level_check(cell, unknowns, mine_count, displayed_field):
	if cell[0]<0 or cell[0]>=rows or cell[1]<0 or cell[1]>=columns or displayed_field[cell[0]][cell[1]] == 'O' or displayed_field[cell[0]][cell[1]] == 'M' or displayed_field[cell[0]][cell[1]] == ' ':
		return
	all_unknowns = list()
	local_mines = 0
	i = cell[0]-1
	while i <= cell[0]+1:
		j = cell[1]-1
		while j <= cell[1]+1:
			if i >= 0 and i < rows and j >= 0 and j < columns and displayed_field[i][j] == 'O':
				all_unknowns.append((i,j))
			elif i >= 0 and i < rows and j >= 0 and j < columns and displayed_field[i][j] == 'M':
				local_mines += 1
			j += 1
		i += 1
	remaining_unknowns = all_unknowns
	# print(f'All unknowns of {cell} with value {displayed_field[cell[0]][cell[1]]} are {all_unknowns}, removing either/or cells {unknowns}')
	for unknown in unknowns:
		if unknown in remaining_unknowns:
			remaining_unknowns.remove(unknown)

	if len(remaining_unknowns) == 0:
		return None

	if displayed_field[cell[0]][cell[1]] - 1 - local_mines == 0:
		# print(f'Second level check for {cell} says mines are NOT at {remaining_unknowns}')
		remaining_unknowns.insert(0, 'empty')
		return remaining_unknowns
	elif displayed_field[cell[0]][cell[1]] - 1 - local_mines == len(remaining_unknowns):
		# print(f'Second level check for {cell} says mines are at {remaining_unknowns}')
		remaining_unknowns.insert(0, 'mines')
		return remaining_unknowns
	return None

def find_and_mark_mines(field, revealed_field, displayed_field):
	successful_finds = 0
	for i in range(rows):
		for j in range(columns):
			local_mines = 0
			if displayed_field[i][j] != ' ' and displayed_field[i][j] != 'M' and displayed_field[i][j] != 'O':
				unknowns = list()
				k = i-1
				while k <= i+1:
					l = j-1
					while l <= j+1:
						if k >= 0 and k < rows and l >= 0 and l < columns and displayed_field[k][l] == 'O':
							unknowns.append((k,l))
						elif k >= 0 and k < rows and l >= 0 and l < columns and displayed_field[k][l] == 'M':
							local_mines += 1
						l += 1
					k += 1
				if len(unknowns) > 0 and len(unknowns) == displayed_field[i][j] - local_mines:
					# print(f'Mines are at {unknowns}')
					mark_mines(displayed_field, unknowns)
					unknowns.clear()
					del unknowns
					successful_finds += 1
				elif len(unknowns) > 0 and displayed_field[i][j] == local_mines:
					# print(f'Mines are NOT at {unknowns}')
					alive = reveal_cells(field, revealed_field, displayed_field, unknowns)
					unknowns.clear()
					del unknowns
					if not alive:
						return False
					successful_finds += 1
				# elif are_neighbours(unknowns) and len(unknowns)-1 == displayed_field[i][j] - local_mines:
				# 	print(f'Possiblity of either/or at {unknowns} for ({i},{j})')
				# 	common_neighbours = find_common_neighbours(unknowns)
				# 	# print(f'Common Neighbours: {common_neighbours}')
				# 	# print(f'Removing the original cell: ({i},{j})')
				# 	common_neighbours.remove((i,j))
				# 	# print(f'Common Neighbours for which second level checking needs to be done: {common_neighbours}')
				# 	for cell in common_neighbours:
				# 		result = second_level_check(cell, unknowns, 1, displayed_field)
				# 		# print(f'result for {cell} is {result}')
				# 		if result is None:
				# 			continue
				# 		action = result.pop(0)
				# 		if action == 'empty':
				# 			# print(f'Revealing {result}')
				# 			alive = reveal_cells(field, revealed_field, displayed_field, result)
				# 			if not alive:
				# 				return False
				# 			successful_finds += 1
				# 			show_displayed_field()
				# 		elif action == 'mines':
				# 			# print(f'marking as mines {result}')
				# 			mark_mines(displayed_field, result)
				# 			successful_finds += 1
				# 			show_displayed_field()
				# 	# if len(common_neighbours) > 0:
				# 	# 	show_displayed_field()
				# elif are_one_away_neighbours(unknowns) and len(unknowns)-1 == displayed_field[i][j] - local_mines:
				# 	print(f'Possiblity of either/or at {unknowns}, on away neighbours of ({i},{j})')
				# 	common_neighbours = find_common_neighbours(unknowns)
				# 	# print(f'Common Neighbours: {common_neighbours}')
				# 	# print(f'Removing the original cell: ({i},{j})')
				# 	common_neighbours.remove((i,j))
				# 	# print(f'Common Neighbours for which second level checking needs to be done: {common_neighbours}')
				# 	for cell in common_neighbours:
				# 		result = second_level_check(cell, unknowns, 1, displayed_field)
				# 		# print(f'result for {cell} is {result}')
				# 		if result is None:
				# 			continue
				# 		action = result.pop(0)
				# 		if action == 'empty':
				# 			# print(f'Revealing {result}')
				# 			alive = reveal_cells(field, revealed_field, displayed_field, result)
				# 			if not alive:
				# 				return False
				# 			successful_finds += 1
				# 			show_displayed_field()
				# 		elif action == 'mines':
				# 			# print(f'marking as mines {result}')
				# 			mark_mines(displayed_field, result)
				# 			successful_finds += 1
				# 			show_displayed_field()
					# if len(common_neighbours) > 0:
					# 	show_displayed_field()

	if successful_finds > 0:
		return find_and_mark_mines(field, revealed_field, displayed_field)
	else:
		return find_and_mark_mines_after_second_level_check(field, revealed_field, displayed_field)
	return True

def find_and_mark_mines_after_second_level_check(field, revealed_field, displayed_field):
	successful_finds = 0
	for i in range(rows):
		for j in range(columns):
			local_mines = 0
			if displayed_field[i][j] != ' ' and displayed_field[i][j] != 'M' and displayed_field[i][j] != 'O':
				unknowns = list()
				k = i-1
				while k <= i+1:
					l = j-1
					while l <= j+1:
						if k >= 0 and k < rows and l >= 0 and l < columns and displayed_field[k][l] == 'O':
							unknowns.append((k,l))
						elif k >= 0 and k < rows and l >= 0 and l < columns and displayed_field[k][l] == 'M':
							local_mines += 1
						l += 1
					k += 1
				# if len(unknowns) > 0 and len(unknowns) == displayed_field[i][j] - local_mines:
				# 	# print(f'Mines are at {unknowns}')
				# 	mark_mines(displayed_field, unknowns)
				# 	unknowns.clear()
				# 	del unknowns
				# 	successful_finds += 1
				# elif len(unknowns) > 0 and displayed_field[i][j] == local_mines:
				# 	# print(f'Mines are NOT at {unknowns}')
				# 	alive = reveal_cells(field, revealed_field, displayed_field, unknowns)
				# 	unknowns.clear()
				# 	del unknowns
				# 	if not alive:
				# 		return False
				# 	successful_finds += 1
				if are_neighbours(unknowns) and len(unknowns)-1 == displayed_field[i][j] - local_mines:
					# print(f'Possiblity of either/or at {unknowns} for ({i},{j})')
					common_neighbours = find_common_neighbours(unknowns)
					# print(f'Common Neighbours: {common_neighbours}')
					# print(f'Removing the original cell: ({i},{j})')
					common_neighbours.remove((i,j))
					# print(f'Common Neighbours for which second level checking needs to be done: {common_neighbours}')
					for cell in common_neighbours:
						result = second_level_check(cell, unknowns, 1, displayed_field)
						# print(f'result for {cell} is {result}')
						if result is None:
							continue
						action = result.pop(0)
						if action == 'empty':
							# print(f'Revealing {result}')
							alive = reveal_cells(field, revealed_field, displayed_field, result)
							if not alive:
								return False
							successful_finds += 1
						elif action == 'mines':
							# print(f'marking as mines {result}')
							mark_mines(displayed_field, result)
							successful_finds += 1
					# if len(common_neighbours) > 0:
					# 	show_displayed_field()
				elif are_one_away_neighbours(unknowns) and len(unknowns)-1 == displayed_field[i][j] - local_mines:
					# print(f'Possiblity of either/or at {unknowns}, one away neighbours of ({i},{j})')
					common_neighbours = find_common_neighbours(unknowns)
					# print(f'Common Neighbours: {common_neighbours}')
					# print(f'Removing the original cell: ({i},{j})')
					common_neighbours.remove((i,j))
					# print(f'Common Neighbours for which second level checking needs to be done: {common_neighbours}')
					for cell in common_neighbours:
						result = second_level_check(cell, unknowns, 1, displayed_field)
						# print(f'result for {cell} is {result}')
						if result is None:
							continue
						action = result.pop(0)
						if action == 'empty':
							# print(f'Revealing {result}')
							alive = reveal_cells(field, revealed_field, displayed_field, result)
							if not alive:
								return False
							successful_finds += 1
						elif action == 'mines':
							# print(f'marking as mines {result}')
							mark_mines(displayed_field, result)
							successful_finds += 1
					# if len(common_neighbours) > 0:
					# 	show_displayed_field()

	if successful_finds > 0:
		return find_and_mark_mines(field, revealed_field, displayed_field)
	return True

print(f'Total mines: {total_mines}')
reveal(field, revealed_field, 0, 0, displayed_field)
show_displayed_field()


while True:
	print('Your options:')
	print('1. Reveal a block')
	print('2. Mark a mine')
	print('3. Automatically mark the mines')
	print('4. Quit')
	path = input('Your selection: ')
	if path == '1':
		x = input('Enter row number: ')
		y = input('Enter column number: ')
		if not x.isdigit() or not y.isdigit() or int(x) < 0 or int(y) < 0 or int(x) >= rows or int(y) >= columns:
			print('Invalid input')
			continue
		alive = reveal(field, revealed_field, int(x), int(y), displayed_field)
		# display_field()
		show_displayed_field()
		if not alive:
			break
	elif path == '2':
		x = input('Enter row number: ')
		y = input('Enter column number: ')
		if not x.isdigit() or not y.isdigit() or int(x) < 0 or int(y) < 0 or int(x) >= rows or int(y) >= columns:
			print('Invalid input')
			continue
		mark_a_mine(displayed_field, int(x), int(y))
		show_displayed_field()
	elif path == '3':
		alive = find_and_mark_mines(field, revealed_field, displayed_field)
		show_displayed_field()
		if not alive:
			break
		# alive = find_and_mark_mines_after_second_level_check(field, revealed_field, displayed_field)
		# show_displayed_field()
		# if not alive:
		# 	break
	elif path == '4':
		break
	else:
		print('Invalid input')
	if revealed_count + total_mines == rows*columns:
		print('YAY! You did it!')
		break
