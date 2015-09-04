# iris
from time import time
import sys
from Queue import Queue
class Vertex:
	def __init__(self,pos1, pos2, SVrange):
		self.range = SVrange
		self.pos1 = pos1
		self.pos2 = pos2
	def __str__(self):
		return '['+str(self.pos1) + ' ' +  str(self.pos2)+']'
	def __eq__(self, other):
		return (self.pos1 == other.pos1) and (self.pos2 == other.pos2) and (self.range == other.range)
	def __hash__(self):
		return id(self)
class Edge:
	def __init__(self, vertex1,vertex2, weigth):
		self.weigth = weigth
		self.vertex1 = vertex1
		self.vertex2 = vertex2
	def __str__(self):
		return '('+ str(self.vertex1) + ','+ str(self.vertex2) + ')'
class Graph(object):
	def __init__(self, graph_dict={}):
		self.graph_dict = graph_dict
	def vertex(self):
		return list(self.graph_dict.keys())
	def edge(self):
		return self.generate_edges()
	def add_vertex(self, vertex):
		self.graph_dict[vertex] = [] 
	def add_edge(self, edge):
			self.graph_dict[edge.vertex1].append(edge)
			e = Edge(edge.vertex2, edge.vertex1, edge.weigth)
			self.graph_dict[edge.vertex2].append(e)
	def generate_edges(self):
		Listedges = set()
		for vertex, edges in self.graph_dict.items():
			for edge in edges:
				Listedges.add(edge)
		return Listedges
	def __str__(self):
		res = str()
		for v in self.sort_vertex():
			res += str(v)+':'
			for e in self.graph_dict[v]:	
				res += str(e) + ' '
			res+='\n'
		return res
	def sort_vertex(self):
		vertexs = self.graph_dict.keys()
        	for i in range(len(vertexs)):
                	for j in range(len(vertexs)-1-i):
                        	if vertexs[j].pos1 > vertexs[j+1].pos1:
                                	vertexs[j], vertexs[j+1] = vertexs[j+1], vertexs[j]
        	return vertexs
	def __len__(self):
		return len(list(self.graph_dict.keys()))
def inversion(value):
        FLAG = binary(int(value[1]))
        result = (FLAG[:4]=='0101') 
        return result
def discordant(value,range):
	FLAG = binary(int(value[1])) 
	sv=abs(int(value[8]))
       	result =FLAG[6] == '0' and sv > 1000 and sv<10000 
        return result
def binary(num):
        result = ''
        c = {0:'0', 1:'1'}
        while num != 0 :
                charnum = num%2
                result+=c[charnum]
                num = int(num/2)
        while len(result) != 8:
                result+='0'
        return result[::-1]
visited = {}
G = Graph({})
def min_weigth(edges):
	minW = set()
	for edge in edges:
		minW.add(edge.weigth)
	return sorted(minW)[0]
def depth_search(vertex):
	if not visited[vertex]:
		visited[vertex] = True
		if G.graph_dict[vertex] != []:
			neighbors = []
			flag = False
			for edge in G.graph_dict[vertex]:
				if visited[edge.vertex2] == False:
					flag = True
					neighbors.append(edge.vertex2)					
			if flag:
				for neighbor in neighbors:
					depth_search(neighbor)						
def check_clique(vertexs):
	vertexs = set(vertexs)
	flag = True
	for vertex in vertexs:
		neighbors = set([vertex])
		for edge in G.graph_dict[vertex]:
			neighbors.add(edge.vertex2)
		if not vertexs < neighbors:
			flag = False
			break
	return flag
def sort_vertex(vertexs):
	for i in range(len(vertexs)):
                for j in range(len(vertexs)-1-i):
                        if vertexs[j].pos1 > vertexs[j+1].pos1:
                                vertexs[j], vertexs[j+1] = vertexs[j+1], vertexs[j]
	return vertexs
def sort_edge(edges):
	for i in range(len(edges)):
		for j in range(len(edges)-1-i):
			if edges[j].vertex1.pos1 > edges[j+1].vertex1.pos1:
				edges[j], edges[j+1] = edges[j+1], edges[j]
			elif (edges[j].vertex1.pos1 == edges[j+1].vertex1.pos1) and (edges[j].vertex2.pos1 > edges[j+1].vertex2.pos1):
				edges[j], edges[j+1] = edges[j+1], edges[j]
	return edges
def maximal_clique(component):
	if len(component) == 1:
		return component.vertex()
	else:	
		Edges = component.generate_edges()
		seed = min_weigth(Edges)
		argmin = []
		M = []
		for edge in Edges:
			if edge.weigth == seed:
				argmin.append(edge)
		argmin = sort_edge(argmin)[:]
		M.append(argmin[0].vertex1)
		M.append(argmin[0].vertex2)
		for i in range(1, len(argmin)):
			if (argmin[i].vertex1 in M)^(argmin[i].vertex2 in M):
				print ' Adding vertex to clique'
				temp = M[:]
				temp.append(argmin[i].vertex1)
				temp.append(argmin[i].vertex2)
				print 'Check clique'
				if check_clique(temp):
					print 'True'
					M = temp[:]
				else:
					print 'False'
		return M
records = {}
def confirm_clique(pos1, pos2, d):
	pos1 = pos1+3*d
	pos2 = pos2-3*d
	flags = {'Real':True, 'DelDup': True}
	breakpos = 0
	for i in range(pos1, pos2):
		try:
			tmp = records[i]
		except KeyError:
			continue
		else:
			flags['Real'] = False
			breakpos = i
			break
	if breakpos !=0:
		for i in range(breakpos+1, pos2):
			try:
				tmp = records[i]
                	except KeyError:
                        	continue
                	else:
				if records[i][4] == '0':
					continue
				else:
					flags['DelDup'] == False
					break
	for flag in flags.keys():
		if flags[flag] == True:
			return flag
			break
def main(path, distance, svrange):
	##########################
	print path
	print 'Reading SAM file...'
	input = open(path)
	output = open(path + '.sv', 'w')	
	vertexs = []
	##########################
	for line in input:
		if line[0]=='@':
			continue
		else:
			value = line.split()
			if int(value[8])>0:
				records[int(value[3])] = value[:]
                        if discordant(value,svrange):
				if value[1] == '97' and int(value[8])>0:
					vertexs.append(Vertex(int(value[3]), int(value[7]), abs(int(value[8]))))
				elif value[1] == '81'and int(value[8])<0:
					vertexs.append(Vertex(int(value[7]), int(value[3]), abs(int(value[8]))))
	vertexs = sort_vertex(vertexs)[:]
	for vertex in vertexs:
		G.add_vertex(vertex)
	##########################
	print 'Finding Deletion'
	for i in range(len(vertexs)):
		trace = i+1
		flag = False
		v1 = vertexs[i]
		while flag == False and trace<len(vertexs):
			v2 = vertexs[trace]
			if (abs(v2.pos1 - v1.pos1) <= distance or abs(v2.pos2-v1.pos2) <= distance) and abs(v2.range - v1.range)<=svrange:
				G.add_edge(Edge(v1,v2,abs(v2.range -v1.range)))
			else: 
				flag = True
			trace += 1
	##############################
	print 'Finding Connected Components'
	for vertex in G.vertex():
		visited[vertex] = False
	Components = []
	while vertexs != []:
		tempvertexs = []
		Ci = Graph({})
		depth_search(vertexs[0])
		for vertex in vertexs:
			if visited[vertex] == False:
				tempvertexs.append(vertex)
			else:
				Ci.graph_dict[vertex] = G.graph_dict[vertex][:]
		vertexs = tempvertexs[:]
		if len(Ci) > 1:
			Components.append(Ci)
	print 'Found ', str(len(Components)), 'Components'
	#==================================
	Cliques = []
	print 'Finding Cliques'
	for component in Components:
		Cliques.append(maximal_clique(component))
	print 'Found ' , str(len(Cliques)), 'Cliques'
	for clique in  Cliques:
		start,end = [], []
		for vertex in clique:
			start.append(vertex.pos1)
			end.append(vertex.pos2)
		pos1 = max(start)
		pos2 = min(end)
		output.write(str(pos1)+'\t' + str(pos2) + '\t'+ str(pos2 - pos1)+ '\t' +confirm_clique(pos1,pos2,distance))
		output.write('\n')
if __name__ == "__main__":
    try:
        sam_path, distance, svrange = sys.argv[1:]
    except ValueError:
        print "Usage: DEL.py SAM_PATH distance range"
    else:
	start = time()
        main(str(sam_path), int(distance), int(svrange))
	print time() - start
