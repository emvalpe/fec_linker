from pyvis.network import Network

desired_data = ["ccl", "cm", "cn", "indiv", "oth", "pas2"]
net = Network()

print("starting candidates")
cn = open("cn"+".txt", "r")
while True:
	line = cn.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")

	net.add_node(data[0], label=data[1], shape="dot", color="#00ff1e")

cn.close()
print("Finished candidates")

print("starting committees")
cm = open("cm.txt", "r")
while True:
	line = cm.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")

	net.add_node(data[0], label=data[1], shape="dot", color="#e23535")

cm.close()
print("Finished committees")

ite = 0
indiv = open("indiv.txt", "r")
print("starting individuals")
while True:
	line = indiv.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")

	net.add_node(data[3], label=data[3], color="#0000ff", shape="dot")
	try:
		net.add_edge(data[3], data[0], color="#000000", physics=True, title=data[5])
	except AssertionError:
		print("error "+str(ite+1)+":"+line[:-1])
		ite+=1

ite = 0
indiv.close()
print("Finished individuals")

pas = open("pas2.txt", "r")
print("starting cm-cn")
while True:
	line = pas.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")

	net.add_edge(data[6], data[0], color="#000000", physics=True, title=data[5])

pas.close()
print("Finished cm-cn")

pas = 0
prog = 0
print("starting committee-candidate linkages")
ccl = open("ccl.txt", "r")
while True:
	prog +=1
	line = ccl.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")
	if prog%10000==0:
		print("prog: "+str(prog))

	try:
		net.add_edge(data[0], data[2], color="#000000", physics=True, title=data[1])
		#print("success "+str(pas+1))
		pas+=1

	except AssertionError:
		print("error "+str(ite+1)+":"+line[:-1])
		ite+=1

ccl.close()
print("Finished committee-candidate linkages")

oth = open("oth.txt", "r")
print("starting cm-cm")
while True:
	line = oth.readline()
	if line=="":break
	if line == "\n":continue
	data = line.split(":")

	net.add_edge(data[5], data[0], color="#000000", physics=True, title=data[4])

oth.close()
print("Finished cm-cm")

#net.generate_html(name="net.html", local=True, notebook=False)
net.show("nodes.html", notebook=False)
'''
.add_edge(nid1,nid2) to connect nodes
.add_node(n_id(str or int), "label")#lots of other aesthetic options
.generate_html(name=, local=True, notebook=False)//save_graph()
'''