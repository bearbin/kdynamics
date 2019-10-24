xs = [-2.8, -0.5, 0.3, -0.4, -0.2, -0.5,  0.7,  0.8,  2.2,  5]
ys = [ 4.4,  3.4, 3.3,  2.6,  1.7, -0.6,  0.4, -0.4,  0.8, -3.2]

n = len(xs)

Sx = sum(xs)
xb = Sx / n

Sy = sum(ys)
yb = Sy / n

Sxx = sum([(x - xb) * (x - xb) for x in xs]) / n
Syy = sum([(y - yb) * (y - yb) for y in ys]) / n
Sxy = sum([(xs[i] - xb) * (ys[i] - yb) for i in range(n)]) / n
Syx = sum([(ys[i] - yb) * (xs[i] - xb) for i in range(n)]) / n

print("%f \t %f" % (Sxx, Sxy))
print("%f \t %f" % (Syx, Syy))
