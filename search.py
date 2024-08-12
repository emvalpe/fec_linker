from pyvis.network import Network
import time as t
import math

def smoothing(num):
	if num <= 100:
		return 1
	else:
		return math.log(num)

cn = open("cn.txt", "r")
cand = (input("Name(last, first): ").lower()).replace(" ", "")
names = cand.split(",")

cands = []
cand_matches = []
while True:#candidate search
	line = cn.readline()
	if line == "":break

	line = line.split(":")
	line[1]=line[1].lower()
	if line[1].find(names[0]) != -1 and line[1].find(names[1]) != -1:
		print(line)
		cand_matches.append(line[0])
		cands.append(line)
cn.close()
cand_matches = list(set(cand_matches))

net = Network()#directed=True)

for i in cands:
	if i[2].upper() == "DEM":
		color = "#0000ff"
	elif i[2].upper() == "REP":
		color = "#ff0000"
	else:
		color = "#ffff00"

	net.add_node(i[0], label=i[1]+":"+i[3], color=color, shape="dot")

ccl_matches = []#commity candidate linkage
print("ccl")

start = t.time()
ccl = open("ccl.txt", "r")
tccl = open("tccl.txt", "w+")
while True:
	line = ccl.readline()
	if line == "":break

	line = line.split(":")
	for i in cand_matches:
		if i == line[0]:
			ccl_matches.append(line)
			tccl.write(str(line)+"\n")
			break
ccl.close()
print("ccl finish(sec): "+str(t.time()-start))

cn_cm = []
for i in ccl_matches:cn_cm.append(i[2])	
cn_cm = list(set(cn_cm))#cut duplicates

#del cands
del cand_matches

start = t.time()
print("oth: 22934197 records as of 2023")

oth_matches = []
all_cms = cn_cm
oth = open("oth.txt", "r")#basically committee committee linkages
inte = 0

start = t.time()
while True:
	line = oth.readline()
	if line == "":break
	if inte%10000000 == 0:
		print("oth " + str(inte)+": time(sec): "+str(t.time()-start))
		start = t.time()

	for i in cn_cm:
		if i in line:
			oth_matches.append(line.split(":"))
			break
	inte+=1


inte = 0
start = t.time()
print("Matches "+str(len(oth_matches)))

for i in oth_matches:
	if inte%100000 == 0 and inte != 0:print(str(inte)+" (min) "+str((t.time()-start)/60))
	all_cms.append(i[0])
	try:
		if i[4][0] == "C" and i[4] not in cn_cm:
			all_cms.append(i[4])
		elif i[6][0] == "C" and i[6] not in cn_cm and len(i[6]) > 1:
			all_cms.append(i[6].replace("\n", ""))

	except Exception:
		if i[6] not in cn_cm and len(i[6]) > 1:
			all_cms.append(i[6].replace("\n", ""))

	inte +=1

all_cms = list(set(all_cms))#cuts out duplicates
c = open("all_cms.txt", "w+")
for i in all_cms:
	c.write(i+"\n")

c.close()
del cn_cm

print(str(len(all_cms))+ " nodes to search for")
print("cm, ~30 minutes")

start = t.time()
cm_matches = []
cm = open("cm.txt", "r")
inte = 0
start = t.time()
while True:
	line = cm.readline()
	if line == "":break
	if inte%1000000 == 0:
		print(str(inte)+": time(sec): "+str(t.time()-start))
		start = t.time()

	line = line.split(":")

	for i in all_cms:
		if i == line[0]:
			cm_matches.append(line)
			break

	inte+=1

cm.close()
print("cm finish(min): "+str((t.time()-start)/60))

print("indiv")
indivs = []
indiv = open("indiv.txt", "r")
while True:
	line = indiv.readline()
	if line == "":break

	line = line.split(":")
	for i in all_cms:
		if line[0] == i[0]:
			net.add_node(line[3], label=line[2], color="#999999", shape="dot")
			net.add_edge(i[0], line[3], label=line[5], width=smoothing(int(line[5])))
			break


del all_cms
cmcolor = ""

for i in cm_matches:
	if i[0][0] != "C":i[0]="C"+i[0]
	if i[2] == "B" or i[2] == "D":
		net.add_node(i[0], label=i[1], color="#ff33cc", shape="dot")
	elif i[2] == "U":
		net.add_node(i[0], label=i[1], color="#ffc61a", shape="dot")
	elif i[2] == "P" or "A":
		net.add_node(i[0], label=i[1], color="#660066", shape="dot")
	else:
		net.add_node(i[0], label=i[1], color="#0000ff", shape="dot")

	

for i in ccl_matches:
	net.add_edge(i[0], i[2], label="Year: "+i[1], color="#000000")

pas2 = []
pf = open("pas2.txt", "r")
while True:
	line = pf.readline()

	if line == "":break
	line = line.split(":")

	for i in cm_matches:
		if i == line[0] or line[15] == i or line[16] == i:
			if not net.get_node(line[0]):
				net.add_node(i[0], label=i[3], color="#ff33cc", shape="dot")
			
			if not net.get_node(line[15]):
				net.add_node(i[15], label=i[3], color="#ff33cc", shape="dot")
			
			if not net.get_node(line[16]):
				net.add_node(i[16], label=i[3], color="#ff33cc", shape="dot")

			if line[15]:
				net.add_edge(i[0], i[15], label="$"+i[14], color="#000000", width=smoothing(int(i[5])))
			else:
				net.add_edge(i[0], i[16], label="$"+i[14], color="#000000", width=smoothing(int(i[5])))

net.add_node("IND", label="individual contributions", color="#4d4d4d", shape="dot")
net.add_node("UNKNOWN", label="Unlabeled Source Data", color="#4d4d4d", shape="dot")

oth_errors = open("oth_errors.txt", "w+")

for i in oth_matches:#change line thickness
	if i[2] == "IND" and len(i[6]) <= 1:
		net.add_edge(i[0], "IND", label="$"+i[5], color="#000000", width=smoothing(int(i[5])))
	elif i[2] == "IND" and len(i[6]) > 1 and i[6][0]=="C":
		try:
			net.add_edge(i[0], i[6].replace("\n",""), label="$"+i[5], color="#000000", width=smoothing(int(i[5])))
		except Exception as e:
			print(i)
			print(e)
	else:
		try:
			if i[4] == "":
				net.add_edge(i[0], i[6], label="$"+i[5], color="#000000", width=smoothing(int(i[5])))
			elif i[4][0] == "C":
				net.add_edge(i[0], i[4], label="$"+i[5], color="#000000", width=smoothing(int(i[5])))
			elif i[4][0] != "C" and len(i[6]) > 8:
				net.add_edge(i[0], i[6].replace("\n",""), label="$"+i[5], color="#000000", width=smoothing(int(i[5])))
			elif i[4][0] != "C" and i[6] == "\n":
				net.add_edge(i[0], "UNKNOWN", label="$"+i[5], color="#000000", width=smoothing(int(i[5])))

		except Exception as e:#IndexError and AssertionError
			oth_errors.write(str(i)+"\n")
			oth_errors.write(str(e)+"\n")

oth_errors.close()
net.show_buttons()
net.show("nodes.html", notebook=False)

#pas2 untested
