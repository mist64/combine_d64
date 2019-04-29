import sys
import sets

def unlinear(l):
	if (l<17*21):
		t = l/21 + 1;
		s = l % 21;
		return (t, s);
	l -= 17*21;
	if (l<(24-17)*19):
		t = l/19 + 17 + 1;
		s = l % 19;
		return (t, s);
	l -= (24-17)*19;
	if (l<(30-24)*18):
		t = l/18 + 24 + 1;
		s = l % 18;
		return (t, s);
	l -= (30-24)*18;
	t = l/17 + 30 + 1;
	s = l % 17;
	return (t, s);

filenames = sys.argv[1:]
numfiles = len(filenames)
data = []
errors = []
good_indexes = []

if not numfiles:
	print "Usage: {} <file1.d64> <file2.d64> [...]".format(sys.argv[0])
	sys.exit()

# read all files

for i in range(0, numfiles):
	d64 = bytearray(open(filenames[i], 'rb').read())
	data.append(d64)
	if len(d64) > 0x2ab00:
		errors.append(data[0x2ab00:])
	else:
		errors.append(None)

# 1. Are two images the same?

identical_sets = []
for i in range(0, numfiles):
	for j in range(i + 1, numfiles):
		if data[i] == data[j]:
			merged = False
			for set in identical_sets:
				if i in set:
					set.add(j)
					merged = True
				elif j in set:
					id.add(i)
					merged = True
			if not merged:
				identical_sets.append(sets.Set([i, j]))
if len(identical_sets) == 1:
	print "The following images are identical:"
	for i in identical_sets[0]:
		print filenames[i],
	print
	sys.exit()
elif len(identical_sets) > 1:
	print "The following sets of images are identical:"
	sn = 0
	for set in identical_sets:
		print sn,":",
		for i in set:
			print filenames[i],
		print
		sn += 1
	sys.exit()

# Analyze Blocks

for block_number in range(0, 683):
	block_variants = []
	for file in range(0, numfiles):
		if not errors[file] or errors[file][block_number] == 1: # no error
			block_variants.append(data[file][block_number * 256:(block_number + 1) * 256])
		else:
			block_variants.append(None)

	copies = [0] * len(block_variants)

	for i in range(0, len(block_variants)):
		for j in range(0, len(block_variants)):
			if block_variants[i] == block_variants[j]:
				copies[i] += 1

	maxnum = max(copies)

	gi = []
	if maxnum > 1:
		for i in range(0, numfiles):
			if copies[i] == maxnum:
				gi.append(i)

	good_indexes.append(gi)

min_copies = None
for i in range(0, 683):
	if min_copies == None or len(good_indexes[i]) <= min_copies:
		min_copies = len(good_indexes[i])

if min_copies >= 3:
	print "All blocks had at least {} copies.".format(min_copies)
elif min_copies:
	print "The following blocks only had a limited number of copies:"
	for i in range(0, 683):
		if len(good_indexes[i]) <= 2:
			(t, s) = unlinear(i)
			print "{} copies of block {} (Trk {} Sec {}) in".format(len(good_indexes[i]), i, t, s),
			for j in good_indexes[i]:
				print filenames[j],
			print
else:
	print "For the following blocks, no duplicates exist:"
	for i in range(0, 683):
		if good_indexes[i] == []:
			(t, s) = unlinear(i)
			print "{} (Trk {} Sec {})".format(i, t, s),
	sys.exit()

# 2. Is there is an image where every block is also found in another image?

perfect_indexes = []

for i in range(0, numfiles):
	bad = False
	for block_number in range(0, 683):
		if i not in good_indexes[block_number]:
			bad = True
			break
	if not bad:
		perfect_indexes.append(i)

if len(perfect_indexes):
	print "Every block of the following images is also contained in at least one other file:"
	for i in perfect_indexes:
		print filenames[i]
	sys.exit()

# 3. Create a combined image from blocks that were seen multiple times

result_d64 = bytearray()
source_usage = [0] * numfiles

for block_number in range(0, 683):
	good_index = good_indexes[block_number][0]
	result_d64 += data[good_index][block_number * 256:(block_number + 1) * 256]
	source_usage[good_index] += 1

print "The result was combined from the following images:"
for i in range(0, numfiles):
	if source_usage[i]:
		print "{} ({} blocks)".format(filenames[i], source_usage[i])

open("result.d64", "wb").write(result_d64)
