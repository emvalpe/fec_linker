'''
indiv-individual donations
cm-committee list
cn-candidate list
oth-committee to committee
pas2-committee to candidates
ccl-candidate committee relations
'''

from pathlib import Path#Donald J. Trump is not a girl boss
from os import mkdir, remove #path has one but I had some issues with it previously, I only call this once anyway
from shutil import rmtree

import time as t

def remove_slash(inp):
	while True:
		if inp.find("/") != -1:
			inp = inp[inp.find("/")+1:]
		else:
			break

	return inp


def cm_processor(file):
	f = open("cm.txt", "a+")

	while True:
		line = file.readline()
		if not line:break

		to_write = []
		info = line.split("|")

		to_write.append(info[0])
		to_write.append(info[1])
		to_write.append(info[8])
		to_write.append(info[9])
		to_write.append(info[12])

		if info[10] == "":
			to_write.append("not party affiliated")
		else:
			to_write.append(info[10])

		if info[13] == "":
			to_write.append("not organization based")
		else:
			to_write.append(info[13])

		if info[14] == "\n":
			to_write.append("not candidate affiliated")
		else:
			to_write.append(info[14])

		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()

def cn_processor(file):
	f = open("cn.txt", "a+")
	
	while True:
		line = file.readline()
		if not line:break
		to_write = []

		info = line.split("|")

		to_write.append(info[0])
		to_write.append(info[1])
		to_write.append(info[2])
		to_write.append(info[3])
		to_write.append(info[4])
		to_write.append(info[5])
				
		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()

def ccl_processor(file):
	f = open("ccl.txt", "a+")

	while True:
		line = file.readline()
		if not line:break 

		to_write = []
		info = line.split("|")

		to_write.append(info[0])
		to_write.append(info[1])
		to_write.append(info[3])
		to_write.append(info[4])
		to_write.append(info[5])

		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()

def oth_processor(file):
	f = open("oth.txt", "a+")

	while True:
		line = file.readline()
		if not line:break

		to_write = []
		info = line.split("|")

		to_write.append(info[0])#s for sender
		to_write.append(info[1])
		to_write.append(info[6])
		to_write.append(info[7])
		to_write.append(info[13])
		to_write.append(info[14])
		to_write.append(info[15])

		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()

def pas2_processor(file):
	f = open("pas2.txt", "a+")

	while True:
		line = file.readline()
		if not line:break

		to_write = []
		info = line.split("|")

		to_write.append(info[0])#s for sender
		to_write.append(info[1])
		to_write.append(info[6])
		to_write.append(info[7])
		to_write.append(info[13])
		to_write.append(info[14])
		to_write.append(info[16])

		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()


def indiv_processor(file):
	runs = 0
	start = t.time()
	f = open("indiv.txt", "a+")

	while True:
		try:
			line = file.readline()
		except UnicodeDecodeError:
			print("unicode error here")
			continue
		if not line:break

		to_write = []
		info = line.split("|")
		try:#seems some of the logs don't have certain things 13 and 14
			to_write.append(info[0])
			to_write.append(info[6])
			to_write.append(info[7])
			to_write.append(remove_slash(info[11].lower()))
			to_write.append(info[13])
			to_write.append(info[14])

		except IndexError:
			print("index error at: " +line)

		outp = ""
		for i in to_write:
			outp = outp+i+":"
		outp = outp[:-1]
		f.write(outp+"\n")

	f.close()


cd = Path(".")
desired_data = ["ccl", "cm", "cn", "indiv", "oth", "pas2"]

for i in desired_data:
	try:
		remove("./"+i+".txt")
	except Exception:
		pass

for category in cd.iterdir():#returns path, if is_dir() or is_file()
	if category.is_dir() and str(category) in desired_data:
		iter = 0
		for folder in category.iterdir():
			for data in folder.iterdir():
				if str(data).find(".txt") != -1:
					with data.open() as file:
						print(file.name)
						match str(category):
							case "cm":
								cm_processor(file)
								iter += 1
							case "cn":
								cn_processor(file)
								iter += 1
							case "indiv":
								start = t.time()
								indiv_processor(file)
								change = t.time()-start
								print("Time to process an indiv: (sec)"+str(change)+" (min)"+str(change/60))
								iter += 1
							case "ccl":
								ccl_processor(file)
								iter += 1
							case "oth":
								oth_processor(file)
								iter += 1
							case "pas2":
								pas2_processor(file)
								iter += 1
							case _:
								continue

		print(iter)
