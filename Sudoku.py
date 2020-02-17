grid = [[3,0,6,5,0,8,4,0,0], 
		[5,2,0,0,0,0,0,0,0], 
		[0,8,7,0,0,0,0,3,1], 
		[0,0,3,0,1,0,0,8,0], 
		[9,0,0,8,6,3,0,0,5], 
		[0,5,0,0,9,0,6,0,0], 
		[1,3,0,0,0,0,2,5,0], 
		[0,0,0,0,0,0,0,7,4], 
		[0,0,5,2,0,6,3,0,0]]

def check(i:int , j:int , k:int) -> bool:
	'''
	checks if the number to be inserted is right or not
	'''
	# horizontal
	if k in grid[i]: return False
	# vertical
	for a in range(len(grid)):
		if grid[a][j] == k: return False

	# box
	i0 = (i//3) * 3
	j0 = (j//3) * 3
	for x in range(3):
		for y in range(3):
			if grid[i0 + x][j0 + y] == k: return False
	
	return True

def find_empty() -> tuple:
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == 0:
				return (i, j)
	return False

def solve() -> None:

	find = find_empty()
	if not find:
		return True

	i , j = find
	for k in range(1 ,10 ,1):
		if check(i ,j ,k):
			grid[i][j] = k
			if solve():
				return True
			grid[i][j] = 0
	return False

def solve_2():
	solve_u()

def solve_u():
	for i in range(9):
		for j in range(9):
			if grid[i][j] == 0:
				for k in range(1 ,10):
					if check(i ,j ,k):
						grid[i][j] = k
						solve_2()
						grid[i][j] = 0
				return
	print(f'\t' , *grid , sep = "\n\t")
	input("More ?")

if __name__ == '__main__':
	print(*grid , sep = "\n")
	solve()
	# solve_u()
	print(f'\t' , *grid , sep = "\n\t")
