xs = [-.2, 1.1, 1, 1.4, 1.6, 2.8, 3, 3.1, 3.2, 3.1]
ys = [-1.2, -1.7, -2.2,-2.6,-3.6,-2.7,-2.5,-3.1,-2.3, -5.6]

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
