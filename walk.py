import os

for dirPath, dirNames, fileNames in os.walk(os.getcwd()):
	if (dirPath[-11:] == '__pycache__'):
		print(dirPath)
		os.rmdir(dirPath)