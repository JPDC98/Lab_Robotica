import math

L0 = 0.2039
L1 = 0.2912
L2 = 0.3236

x = 0.3
z = 0.1

h = math.sqrt((z-L0)**2+x**2)
fi = math.atan((z-L0)/x)
b = math.acos(((h**2)-(L1**2)-(L2**2))/(-2*L1*L2))
alfa = math.asin(L2*math.sin(b)/h)

q1 = fi+alfa-math.pi/2
q2 = b-math.pi/2

print(math.degrees(fi))
print(math.degrees(alfa))

print(math.degrees(q1))
print(math.degrees(q2))