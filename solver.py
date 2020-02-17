'''
this package helps in processing and checking
'''

def find_empty(grid:list) -> tuple:
	'''
	this function finds the empty spaces in the 
	grid and return as None/tuple
	'''
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j] == 0:
				return (i, j)  # row, col

	return None

def solve(grid:list) -> bool:
	find = find_empty(grid)
	if not find: return True

	row, col = find

	for i in range(1,10 ,1):
		if valid(grid, i, (row, col)):
			grid[row][col] = i

			if solve(grid):
				return True

			grid[row][col] = 0

	return False


def valid(grid:list, num:int, pos:tuple) -> bool:
	'''
	checks if input is valid or not
	'''
	# Check row
	for i in range(len(grid[0])):
		if grid[pos[0]][i] == num and pos[1] != i:
			return False

	# Check column
	for i in range(len(grid)):
		if grid[i][pos[1]] == num and pos[0] != i:
			return False

	# Check grid[]
	gridx_x = pos[1] // 3
	gridx_y = pos[0] // 3

	for i in range(gridx_y*3, gridx_y*3 + 3):
		for j in range(gridx_x * 3, gridx_x*3 + 3):
			if grid[i][j] == num and (i,j) != pos:
				return False

	return True
