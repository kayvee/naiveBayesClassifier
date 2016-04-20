import sys

def process_line(line):
	label, subject_line = line.strip().split('\t')
	bow = subject_line.split()
	return label, bow

def update_counts(label, bow, dc, ds, dh):
	# 1. update dc
#	if not label in dc: dc[label] = 1.0
#	else: dc[label] += 1
	if not label in dc: dc[label] = 0.0
	dc[label] += 1
	# 2. update ds
	if label == '1':
		for word in bow:
			if not word in ds: ds[word] = 0.0
			ds[word] += 1
	# 3. update dh
	elif label == '0':
		for word in bow:
			if not word in dh: dh[word] = 0.0
			dh[word] += 1
	return dc, ds, dh

if __name__ == '__main__':
	lines = sys.stdin.readlines()
	dc = {}
	ds = {}
	dh = {}
	for line in lines:
		label, bow = process_line(line)
		dc, ds, dh = update_counts(label, bow, dc, ds, dh)
	for word in ds: print word + ',' + str(ds[word])
