
from gates import *
import math
import py_compile
py_compile.compile("gates.py")

PI = math.pi
n=8
init(n)
r1, r2 = 4, 4 
for i in range (r1):
	h(i)

print ("============")

mef (r1, 2, 15)
# print_reg(r1, r2)
# print ("============")
# print_st()
measure (4, 0)
measure (4, 1)
measure (4, 0)
measure (4, 0)
# print_reg(r1, r2-4)
print ("============")
qft(True)

print_st()
print ("============")

# qft()
# print_reg(r1, r2)
# print ("============")

# print_st()

# qft()
# rz (1, 2.82845)
# ry (1, -2.86070)
# # cx (5, [0])
# rz (3, -2.18618)
# # cx (1, [5])
# # rx (4, 1.25695)
# # cx (1, [5])
# ry (2, -0.86815)
# rz (0, 0.50301)
# # rz (5, -0.04937)
# cr (2, [0], 2.86133)
# cx (2, [1])
# cr (3, [1], 1.57048)
# # ry (5, -1.03128)
# h (2)
# cr (0, [2], -1.82237)
# rx (1, -0.41778)
# h (1)
# h (3)
# ry (3, -1.74223)

