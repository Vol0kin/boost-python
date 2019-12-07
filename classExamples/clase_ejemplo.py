import claseEjemplo

p1 = claseEjemplo.Punto3D(1,1,1)
p2 = claseEjemplo.Punto3D(1,2,4)
p3 = p1

print(f"Punto 1 {p1}")
print(f"Punto 2 {p2}")
print(f"Punto 3 {p3}")


p3.y = 4

print(f"\nPunto 1 {p1}")
print(f"Punto 3 {p3}")

dist = p1.distancia(p2)

print(f"\nDistancia entre los dos puntos: {dist}")

print(f"\nSuma de los dos puntos: {p1 + p2}")