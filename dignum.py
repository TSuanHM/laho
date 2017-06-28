import random

fo = open("num.txt", "wb")

s = 0

for x in xrange(1,10000):
	n =  random.uniform(0, 1000000000) 
	v = random.uniform(10,1000)
	fo.write(str(n/v)+"      ")
	s = s+1
	if (s>30):
		fo.write("\n")
		s = 0
	pass

fo.close()
