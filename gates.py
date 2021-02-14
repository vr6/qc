import cmath
#--------------------------------------------------
def ev (q, f, c=[], fv=None): # pairs 0,1
	a = 1 << q
	for i in c:
		a += 1 << i
	for i in range (len(bs)):
		if i & a == a:
			f(i - (1 << q), i, fv)	

def ev2 (q1, q2, f, c=[], fv=None): # pairs 01,10
	a = 1 << q1
	b = 1 << q2
	for i in c:
		a += 1 << i
	for i in range (len(bs)):
		if i & a == a  and not (i & b) :
			f(i - a + b, i, fv)	
#--------------------------------------------------
def _x (a, b, fv):
	bs[a], bs[b] = bs[b], bs[a]
	m[a], m[b] = m[b], m[a]

def _y (a, b, fv):
	es = complex(0, 1)
	bs[a], bs[b] = -es * bs[b], es * bs[a]

def _z (a, b, fv):
	bs[b] = -bs[b]

def _rx (a, b, t):
	cos = cmath.cos(t/2)
	es = complex(0, cmath.sin(t/2))
	bs[a], bs[b] = bs[a]*cos - bs[b]*es, bs[b]*cos - bs[a]*es

def _ry (a, b, t):
	cos = cmath.cos(t/2)
	sin = cmath.sin(t/2)
	bs[a], bs[b] = bs[a]*cos - bs[b]*sin, bs[b]*cos + bs[a]*sin

def _rz (a, b, t):
	bs[b] *= complex(cmath.cos(t), cmath.sin(t))

def _h (a, b, fv):
	r = cmath.sqrt(0.5)
	bs[a], bs[b] = r*(bs[a] + bs[b]), r*(bs[a] - bs[b]) 	

def _m (a, b, fv):
	if fv[0] == 1:
		bs[a], bs[b] = complex(0,0), bs[b]/cmath.sqrt(fv[1])
	else:
		bs[b], bs[a] = complex(0,0), bs[a]/cmath.sqrt(1-fv[1])

#--------------------------------------------------
def x (q):
	ev (q, _x)

def y (q):
	ev (q, _y)

def z (q):
	ev (q, _z)

def cx (q, c):
	ev (q, _x, c)

def cy (q, c):
	ev (q, _y, c)

def cz (q, c):
	ev (q, _z, c)

def rx (q, t):
	ev (q, _rx, fv=t)

def ry (q, t):
	ev (q, _ry, fv=t)

def rz (q, t):
	ev (q, _rz, fv=t)

def sw (q1, q2):
	ev2 (q1, q2, _x)

def csw (q1, q2, c):
	ev2 (q1, q2, _x, [c])

def cr (q, c, s):
	ev (q, _rz, c, s)

def h (q):
	ev (q, _h)

def measure (q, v):
	global bs
	global n
	a = 1 << q
	p1 = 0.0
	for i in range (len(bs)):
		if i & a == a:
			r = abs(bs[i])
			p1 += r*r	
	ev (q, _m, fv=[v, p1])
	# bs2 = []
	# for i in range (len(bs)):
	# 	if i & a == a:
	# 		bs2.append(bs[i] if v==1 else bs[i-a])
	# bs = bs2
	# n -= 1
	# print (n, len(bs))

#--------------------------------------------------
def qft (nq, inv=False):
	qpi = -cmath.pi if inv else cmath.pi 
	for i in range (nq):
		h (i)
		for k in range (i+1, nq):
			cr (i, [k], qpi/(1 << (k-i)))
	for i in range (nq//2):
		sw (i, nq-1 - i)

def mef(r1, a, N): # r2 is the mef (mod exp) register (vertical), r1 is qft reg (horiz)
	N1 = 1<<r1
	for i in range (N1): # the first row
		k = a**i % N
		bs[k*N1 + i] = bs[i] # move from first row to kth row 
		bs[i] = complex(0, 0)

#--------------------------------------------------
n=0
bs=[]
m=[]
# r1=0
# r2=0
def init (nq, encode=0):
	global n
	global bs
	global m
	n = nq
	bs = [complex(0, 0)] * (1<<n)
	for i in range (1 << n):
		m.append(i)
		# bs.append( complex(0, 0) ) 
	bs[encode] = ( complex(1, 0) ) 
	init_cube(n)

def init_cube(n):
	global sp
	sp = [None]*(n+1)
	c = []
	sp[0] = c
	c.append(0)
	for i in range (1, 1 << n):
		bc = bin(i).count("1")
		c = sp[bc]
		if c == None:
			c = []
			sp[bc] = c
		c.append(i)
#--------------------------------------------------
def print_top():
	# bs2 = sorted(range(len(bs)), key=lambda k: abs(bs[k]))
	bs2 = [i for i in sorted(enumerate(bs), key=lambda x:abs(x[1]), reverse=True)]
	for i in range(10 if len(bs2) >= 10 else len(bs2)):
		print(f'{bs2[i][0]:03d}', f'{bs2[i][0]:b}'.zfill(n), f'{bs2[i][1]:+.5f}', f'{abs(bs2[i][1]):.5f}', 
			f'{(cmath.phase(bs2[i][1])/cmath.pi):+.5f}')

def print_st():
	# for i in range (len(bs)):
	# 	print(f'{i:03d}', f'{i:b}'.zfill(n), f'{bs[i]:+.5f}', f'{abs(bs[i]):.5f}', 
	# 		f'{(cmath.phase(bs[i])/cmath.pi):+.5f}')
    i = 0
    while i < len(bs):
        start = i
        v = bs[i]
        print(f'{i:03d}', f'{i:b}'.zfill(n), f'{v:+.5f}', f'{abs(v):.5f}', 
            f'{(cmath.phase(v)/cmath.pi):+.5f}')
        
        if abs(bs[i]) < 0.00001:
            while i < len(bs) and abs(bs[i]) < 0.00001:
                i += 1
        else:
            while i < len(bs) and bs[i] == v:
                i += 1
        if i > start+1:
            print (" ..  ..  ..", start, "-", i-1, "(", (i-start), "states)")

# def print_reg(r1, r2):
# 	if r1+r2 != n:
# 		print ("*** r1+r2 != n ***")
# 		return
# 	N1 = 1<<r1
# 	N2 = 1<<r2
# 	print("==== Reg1 ========================")
# 	for i in range (N1):  # N1 is horizontal, N2 is vertical. bs array scans horizontal (aligns with N1)
# 		bs1 = complex(0, 0)
# 		for k in range (N2):
# 			# print(k*N1 + i)
# 			bs1 += bs[k*N1 + i] * bs[k*N1 + i]
# 		bs1 = cmath.sqrt(bs1)
# 		print(f'{i:03d}', f'{i:b}'.zfill(r1), f'{bs1:+.5f}', f'{abs(bs1):.5f}', 
# 			f'{(cmath.phase(bs1)/cmath.pi):+.5f}')
# 	print("==== Reg2 ========================")
# 	for i in range (N2):
# 		bs2 = complex(0, 0)
# 		for k in range (N1):
# 			# print(i*N1 + k, bs[i*N1 + k])
# 			bs2 += bs[i*N1 + k] * bs[i*N1 + k]
# 		bs2 = cmath.sqrt(bs2)
# 		print(f'{i:03d}', f'{i:b}'.zfill(r2), f'{bs2:+.5f}', f'{abs(bs2):.5f}', 
# 			f'{(cmath.phase(bs2)/cmath.pi):+.5f}')

def print_sp():
	for i in sp:
		print ("---------")
		for k in range(len(i)):
			v = bs[i[k]]
			print(f'{i[k]:03d}', f'{i[k]:b}'.zfill(n), f'{v:+.5f}', f'{abs(v):.5f}', 
			f'{(cmath.phase(v)/cmath.pi):+.5f}')
	print ("---------")
#--------------------------------------------------
