"""
Apuentes
Pasos de instalacion
CMD: pip install pulp

Ejemplo:
 Se tienen J tareas y hay que asignar I trabajadores para realizar dichas tareas en el menor tiempo posible
 para este ejemplo tenemos 3 tareas y 3 trabajadores. El tiempo esta descrito en la siguiente tabla:

  Ejemplo 1  | Tarea 1 | Tarea 2 | Tarea 3 |
Trabajador 1 |    27   |    18   |    24   |
Trabajador 2 |    31   |    11   |    16   |
Trabajador 3 |    44   |    46   |    15   |

Parametros:
I: Trabajadores
J: Tareas
T_ij: Tiempo en que demora el trabajador i en hacer la tarea j

Variables:
      | 1: Si asigno al trabajador i a la tarea j
X_ij: | Variable binaria.
      | 0: ---

Restricciones:

Rest_i : Sum_i(X_ij) = 1 para todo j    # Solo puede haber un trabajador asignado a una tarea
Rest_j : Sum_j(X_ij) = 1 para todo i    # Cada tarea tiene que tener a un trabajador

Funcion Objetivo

FO: MIN(Sum_i(Sum_j(T_ij*X_ij)))
"""

# Importamos pulp
import pulp as pl

# Definimos el problema
problem = pl.LpProblem(name="Ejemplo_1", sense=pl.LpMinimize)          # Problema llamado ejemplo 1 de minimizacion

# Definimos los Parametros
I = ["Trabajador 1", "Trabajador 2", "Trabajador 3"]        # Lista con los trabajadores
J = ["Tarea 1", "Tarea 2", "Tarea 3"]                       # Lista con las tareas
T = {
    ("Trabajador 1", "Tarea 1"): 27, ("Trabajador 1", "Tarea 2"): 18, ("Trabajador 1", "Tarea 3"): 24,
    ("Trabajador 2", "Tarea 1"): 31, ("Trabajador 2", "Tarea 2"): 11, ("Trabajador 2", "Tarea 3"): 16,
    ("Trabajador 3", "Tarea 1"): 44, ("Trabajador 3", "Tarea 2"): 46, ("Trabajador 3", "Tarea 3"): 15
}                                                          # Diccionario de tiempos

# Definimos la Variables
X = pl.LpVariable.dicts(name="X[i,j]", indexs=[(i, j) for i in I for j in J], lowBound=0, upBound=1, cat=pl.LpBinary)
# X = pl.LpVariable.dicts("X[i,j]", [(i, j) for i in I for j in J], 0, 1, pl.LpBinary)

# Definimos las Restricciones:
for i in I:                                                # Para cada trabajador (i) hay una tarea (j)
    problem += pl.lpSum(X[i, j] for j in J) == 1           # Rest_j
    # No hay trabajadores sin tareas
for j in J:                                                # Para cada tarea (j) hay un unico trabajador (i)
    problem += pl.lpSum(X[i, j] for i in I) == 1           # Rest_i
    # Ni hay tareas sin trabajadores

# Definimos la Funcion Objetivo
problem += pl.lpSum(T[i, j] * X[i, j] for i in I for j in J)

# Resolvemos el modelo
solver = pl.PULP_CBC_CMD(msg=False)                       # msg = False no muestra el resumen.
solve = problem.solve(solver=solver)                      # solver=solver permite utilizar un solvers pre definido.

# Con problem.solve tenemos la solucion al problema, solo faltaria revisar los estados y valores
# asignados tanto a las variables como el valor de la funcion objetivo.

# Ver estado de la solucion
status = pl.LpStatus[solve]
print("Estado: ", status)

# Vemos los valores de la Variables
for var in problem.variables():
    print(var.name, var.varValue)

# Por ultimo vemos el valor de la Funcion Objetivo
value_FO = pl.value(problem.objective)
print("Valor FO:", value_FO)
