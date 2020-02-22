try:
	import contextlib # for removing default text {it redirects Output to None}
	with contextlib.redirect_stdout(None):
		import pygame
		from tkinter import *
		from tkinter import ttk
		from tkinter import messagebox
		import random_board

	from solver import solve, valid
	import time

except ModuleNotFoundError as E:
	print('NOT ENOUGH RESOURCES ,\n Read requirements.txt \n press Enter for more Info')
	input()
	print(E)

pygame.font.init()

def get_board():
	return random_board.get()
	

class Grid:
	board = get_board()

	def __init__(self, rows, cols, width, height):
		self.rows = rows
		self.cols = cols
		self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
		self.width = width
		self.height = height
		self.model = None
		self.selected = None


	def update_model(self):
		self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

	def place(self, val:int)  -> bool:
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set(val)
			self.update_model()

			if valid(self.model, val, (row,col)) and solve(self.model):
				return True
			else:
				self.cubes[row][col].set(0)
				self.cubes[row][col].set_temp(0)
				self.update_model()
				return False

	def sketch(self, val:int)  -> None:
		row, col = self.selected
		self.cubes[row][col].set_temp(val)

	def draw(self, win) -> None:
		_line_col = (127, 140, 141)
		# Draw Grid Lines
		gap = self.width / 9
		for i in range(self.rows+1):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(win, _line_col, (0, i*gap), (self.width, i*gap), thick)
			pygame.draw.line(win, _line_col, (i * gap, 0), (i * gap, self.height), thick)

		# Draw Cubes
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].draw(win)

	def select(self, row:int, col:int) -> None:
		# Reset all other
		for i in range(self.rows):
			for j in range(self.cols):
				self.cubes[i][j].selected = False

		self.cubes[row][col].selected = True
		self.selected = (row, col)

	def clear(self) -> None:
		row, col = self.selected
		if self.cubes[row][col].value == 0:
			self.cubes[row][col].set_temp(0)

	def click(self, pos:tuple) -> int:
		"""
		:param: pos
		:return: (row, col)
		"""
		if pos[0] < self.width and pos[1] < self.height:
			gap = self.width / 9
			x = pos[0] // gap
			y = pos[1] // gap
			return (int(y),int(x))
		else:
			return None

	def is_finished(self)  -> bool:
		for i in range(self.rows):
			for j in range(self.cols):
				if self.cubes[i][j].value == 0:
					return False
		return True


class Cube(object):
	_font = "lucidasansregular" 
	rows = 9
	cols = 9

	def __init__(self, value:int, row:int, col:int, width:int ,height:int):
		self.value = value
		self.temp = 0
		self.row = row
		self.col = col
		self.width = width
		self.height = height
		self.selected = False

	def draw(self, win :object) -> None:
		fnt = pygame.font.SysFont("comicsans", 40)

		gap = self.width / 9
		x = self.col * gap
		y = self.row * gap

		if self.temp != 0 and self.value == 0:
			# temp color = 0, 205, 208
			text = fnt.render(str(self.temp), 1, (0, 205, 208))
			win.blit(text, (x+5, y+5))
		elif not(self.value == 0):
			# num color
			text = fnt.render(str(self.value), 1, (0, 200, 100))
			win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

		if self.selected:
			# red box (selected element)
			pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

	def set(self, val:int) -> None:
		self.value = val

	def set_temp(self, val:int) -> None:
		self.temp = val


def format_time(secs :int) -> str:
	sec = secs%60
	minute = secs//60
	hour = minute//60
	mat = " " + str(minute) + ":" + str(sec)
	return mat


def redraw_window(win :object, board :list, time :int, strikes :int) -> None:
	_color = (27, 27, 27)
	win.fill(_color)
	# Draw time
	fnt = pygame.font.SysFont("comicsans", 40)
	text = fnt.render("Time: " + format_time(time), 1, (241, 196, 15))
	win.blit(text, (540 - 160, 560))
	# Draw Strikes
	text = fnt.render("X " * strikes, 1, (255, 0, 0))
	win.blit(text, (20, 560))
	# Draw grid and board
	board.draw(win)


# Difficulty Window
#  ==================
N = 0

def onsubmit() -> None:
	global N
	st = startBox.get()
	N = 10 - int(st)%11
	window.quit()
	window.destroy()
	
window = Tk()
label = Label(window, text='Difficulty [1 - 10]: ')
startBox = Entry(window)
submit = Button(window, text='Submit', command=onsubmit)
window.update()
submit.grid(columnspan=2, row=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
mainloop()

# ============

def main() -> None:
	global N
	# __def__
	_res = (540,600)
	_caption = "Sudoku"
	key = None
	run = True
	strikes = 0

	# initialize the window(game)
	_icon = pygame.image.load('static/favicon.png')
	win = pygame.display.set_mode(_res)
	pygame.display.set_caption(_caption)
	pygame.display.set_icon(_icon)
	board = Grid(9, 9, 540, 540) # row ,col , width ,height    
	start = time.time()

	while run:

		play_time = round(time.time() - start)

		# key mapping the input from keyboard
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					key = 1
				if event.key == pygame.K_2:
					key = 2
				if event.key == pygame.K_3:
					key = 3
				if event.key == pygame.K_4:
					key = 4
				if event.key == pygame.K_5:
					key = 5
				if event.key == pygame.K_6:
					key = 6
				if event.key == pygame.K_7:
					key = 7
				if event.key == pygame.K_8:
					key = 8
				if event.key == pygame.K_9:
					key = 9
				if event.key == pygame.K_DELETE:
					board.clear()
					key = None
				if event.key == pygame.K_RETURN:
					i, j = board.selected
					if board.cubes[i][j].temp != 0:
						if board.place(board.cubes[i][j].temp):
							print("Success")
						else:
							print("Wrong")
							strikes += 1
							# implement difficulty
							if strikes >= N:
								print("Game over")
								run = False
						key = None

						if board.is_finished():
							print("Game over")
							run = False
							exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				clicked = board.click(pos)
				if clicked:
					board.select(clicked[0], clicked[1])
					key = None

		if board.selected and key != None:
			board.sketch(key)

		redraw_window(win, board, play_time, strikes)
		pygame.display.update()


if __name__ == '__main__':
	main()
	pygame.quit()