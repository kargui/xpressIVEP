## UTILIZANDO LIBRERIAS DE OPTIMIZACIÓN DE PYTHON 

from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value
import cvxpy as cp 
# Crear el problema de optimización
problem = LpProblem("Minimization Problem", LpMinimize)

n = 1000

# Variables de decisión
x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
p = LpVariable("p", lowBound=0, cat="Integer")
P = LpVariable("P", lowBound=0, cat="Continuous")
Cins = LpVariable("Cins", lowBound=0, cat="Integer")
Cop = LpVariable("Cop", lowBound=0, cat="Integer")
Cmtt = LpVariable("Cmtt", lowBound=0, cat="Integer")

# Un valor constante de instalar gasolineras
Cgas = 5 * 10

# Verificar si las variables están definidas
variables = ["x", "p", "P", "Cins", "Cop", "Cmtt"]  # Lista de variables a verificar
for var_name in variables:
    if var_name in globals():
        print(f"La variable '{var_name}' está definida.")
    else:
        print(f"La variable '{var_name}' no está definida.")

# Variables auxiliares
aux = [LpVariable(f"aux{i}", lowBound=0, cat="Integer") for i in range(n)]
y = [LpVariable(f"y{i}", lowBound=0, cat="Continuous") for i in range(n)]

# Función objetivo
problem += lpSum(aux[i] for i in range(n)) == lpSum(y[i] for i in range(n))

# Reformular la variable p para que tome valores enteros
p_integer = LpVariable("p_integer", lowBound=0, cat="Integer")
M = 100000000  # Constante suficientemente grande

# Restricción para garantizar que p sea entero
problem += p == p_integer / M # COMO DIVIDIR UNA VARIABLE DE DECISIÓN CON UN ENTERO =????? 

# Restricción para acotar p por debajo por cero
problem += p_integer >= 0
for i in range(n):
    problem += y[i] >= x[i] * p - (1 - x[i]) * M  # Restricción linealizada 1
    problem += y[i] <= x[i] * p + x[i] * M       # Restricción linealizada 2

# Crear variable auxiliar z y establecer la restricción para vincularla con P
z = LpVariable("z", lowBound=0, cat="Continuous")
problem += z >= P
problem += lpSum(x[i] * p for i in range(n)) <= P
problem += lpSum(x[i] * (Cop + Cmtt + Cins) for i in range(n)) <= Cgas

# Resolver el problema
problem.solve()

# Obtener el valor y la solución óptima
optimal_value = value(problem.objective)
optimal_solution = [value(x[i]) for i in range(n)]

print("Optimal Value:", optimal_value)
print("Optimal Solution:", optimal_solution)

