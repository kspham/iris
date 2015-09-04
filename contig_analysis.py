import sys
sampath = sys.argv[1]
def Filter_Quality(sampath):
	data = []
	SAM = open(sampath)
	for line in SAM:
		if line[0] == '@':
			continue
		else:
			read = line.split()
			if read[4] == '60':
				data.append(read)
	return data
def Extract_map_size(CIGAR):
        size = 0
        for i in CIGAR:
                if i !='M':
                        try:
                                t =int(i)
                        except ValueError:
                                CIGAR = CIGAR.replace(i,' ')
                        else:
                                continue
        CIGARs = CIGAR.split(' ')
        for site in CIGARs:
                if 'M' in site:
                        pos = site.split('M')
                        size+=int(pos[0])
        return size
def getref():
	ref = open('emrsa15.fasta')
        seq =''
        for line in ref:
                seq+= line.strip()
        return  seq
def main(path):
	output = open(path+'.contig.sv','w')
	seq = getref()
	mapped = {}
	for i in range(len(seq)):
		mapped[i] = False
	Q60 = Filter_Quality(path)
	for read in Q60:
		start = int(read[3])
		Mappedsize = Extract_map_size(read[5])
		for i in range(start, start+Mappedsize+1):
			mapped[i] = True
	start = 1
	while start<len(mapped)-1:
		size = []
		if mapped[start] == False:
			size.append(start),
			for end in range(start, len(mapped)):
				if mapped[end] == True:
					size.append(end)
					break
				elif end == len(mapped)-1:
					size.append(end)
			start = end
			output.write(str(size[0]) + '\t' + str(size[1]))
		else:
			start+=1	
main(sampath)		
						
