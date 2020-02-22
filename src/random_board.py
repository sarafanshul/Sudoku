import json
import random

def get():
	with open("random_sudoku.json" , "r") as json_file:
		json_data = json.load(json_file)
		# print(json_data[str(1)][6])

	return json_data["1"][random.randint(0 ,len(json_data["1"]))]

def main():
	print(get())

if __name__ == '__main__':
	main()