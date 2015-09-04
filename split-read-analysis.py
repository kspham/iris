#input: predicted deletion sites
#output: deletion range at nucleotide resolution
"""
For each structural variants detected in the first step, I confirm the exact break points for each site by using split-read alignment result. 
Split read is the one that has been mapped partially on reference, one part of that read is soft clipped.
"""
import sys
sampath,svpath, insertsz = sys.argv[1:]
insertsize = int(insertsz)
def Extract_pos(CIGAR):
	result =''
	key = CIGAR.find('M')
	while True:
		try: 
			key-=1
			temp = int(CIGAR[key])
		except ValueError or IndexError:
			break
		else:	
			result += CIGAR[key]
	return int(result[::-1])
SVdata = []
data = {}
def Collect_candidate(path):
	SAMf = open(path)
	for line in SAMf:
		if line[0] == '@':
			continue
		else:
			read = line.split()
			if read[5] not in ['150M', '152M', '*']:
                        	try:
                                	data[int(read[3])].append(read[:])
                        	except KeyError:
                                	data[int(read[3])] = []
                                	data[int(read[3])].append(read[:])

def Collect_Sv_pos(path):
	SVpos = open(path)
	for line in SVpos:
        	l = line.split()
        	record = [int(l[0]), int(l[1])]
        	SVdata.append(record)
def Find_Breakpoint(first, last):
	break1st, break2nd = {}, {}
	result =[]
	for start in range(first-insertsize, first+insertsize):
		try:
			reads = data[start]
		except KeyError:
			continue
		else:
			for read in reads:
				breakpoint = int(read[3]) + Extract_pos(read[5])
				try:
					break1st[breakpoint] +=1
				except KeyError:
					break1st[breakpoint] = 1
        for end in range(last-insertsize, last+insertsize):
                try:
                        reads = data[end]
                except KeyError:
                        continue
                else:
                        for read in reads:
				breakpoint = int(read[3])
                        	try:
                                	break2nd[breakpoint] +=1
                        	except KeyError:
                                	break2nd[breakpoint] = 1
	if break1st!={} and break2nd!={}:
		bp1st = max([value for value in break1st.values()])
		bp2nd = max([value for value in break2nd.values()])
	try:
		if bp1st!=1 and bp2nd!=1:
			for key, value in break1st.items():
				if value == bp1st:
					result.append(key)
					result.append(value)
			for key, value in break2nd.items():
				if value == bp2nd:
					result.append(key)
					result.append(value)
	except UnboundLocalError:
		return result
	return result
Collect_candidate(str(sampath))
Collect_Sv_pos(str(svpath))
output = open(str(sampath)+'.spl','w')
for record in SVdata:
	breakpoints =  Find_Breakpoint(record[0], record[1])
	if breakpoints != []:
		for element in breakpoints:
			output.write(str(element) + '\t')
		output.write('\n')

		 		
						
