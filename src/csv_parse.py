import csv
import json

def main():
	with open("sudoku.txt" , "r") as _file:
		csv_reader = csv.reader(_file, delimiter=',')
		data = {1:[] , 2:[]}
		line = 1
		for row in csv_reader:
			if line : # skip headings
				line = 0 
				continue
			temp_puz = []
			temp_ans = []
			temp_str = str(row[1])
			temp_str_ans = str(row[2])
			for i in range(9):
				temp_puz1 = []
				temp_ans1 = []
				for j in row[1][9*i:9*(i+1)]:
					temp_puz1.append(int(j))
				temp_puz.append(temp_puz1)
				for j in row[2][9*i:9*(i+1)]:
					temp_ans1.append(int(j))
				temp_ans.append(temp_ans1)
			data[2].append(temp_ans)
			data[1].append(temp_puz)

	with open("random_sudoku.json" ,"w") as json_file:
		json.dump(data ,json_file)
		
if __name__ == '__main__':
	main()