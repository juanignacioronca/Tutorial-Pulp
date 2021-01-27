"""
Enunciado:

Suponga que existe una empresa en la cual trabajan 50 personas. Estas 50 personas tienen que realizar
50 tareas en total. Las tareas se pueden realizar de a 1 o de 2. Si se realizan de 2 todos tienen que realizar
de a 2 las tareas. Realizarlas de a 2 demora un tercio de la suma del tiempo de ambos.
Ej: trabajador 1 en la tarea 1: 30 min; trabajador 2 en la tarea 1: 22 min
tiempo juntos = ((30+22)/2) = 26 min.

Cada trabajador puede estar en una tarea, no pueden haber tareas sin hacer y cada tarea tiene que tener
maximo un par de trabajadores.

Los tiempos de demora de cada trabajador se encuentran el el excel "Taller_inventado.xlsx" en la hoja de parametros.

Determine que trabajadores realizan cada tarea.

"""

import pulp as pl
import pandas as pd

# Leemos la informacion del excel
data = pd.read_excel("Taller_inventado.xlsx", sheet_name="Parametros")
# Tomamos la primera fila o los "headers" en una lista
columns = list(data.columns)

# Definimos I como los trabajadores y los ponemos en una lista
I = list(data[columns[0]])

# Definimos J como las tareas y las obtenemos de columns sin considerar la primera columna
J = columns[1:]

# Definimos T como lo tiempos en un diccionario

T = {}
for i in range(len(I)):
    for j in J:
        T[I[i], j] = data[j][i]

# Definimos el problema como Taller Inventado y de minimizacion
problema = pl.LpProblem(name="Taller Inventado", sense=pl.LpMinimize)

# Definimos las Variables en diccionario
X = pl.LpVariable.dicts(name="X[i,j]", indexs=[(i, j) for i in I for j in J], lowBound=0, upBound=1, cat=pl.LpBinary)

# Definimos las Restricciones
for i in I:                     # Los trabajadores tienen almenos 1 tarea
    problema += pl.lpSum(X[i, j] for j in J) >= 1

for j in J:                     # Cada tarea puede ser hecha por maximo 2 trabajadores
    problema += pl.lpSum(X[i, j] for i in I) <= 2
for j in J:                     # Cada tarea puede ser hecha por minimo 1 trabajadores
    problema += pl.lpSum(X[i, j] for i in I) >= 1
# Definimos la Funcion Objetivo

problema += pl.lpSum(T[i, j] * X[i, j] for i in I for j in J)


# Resolvemos el problema
solver = pl.PULP_CBC_CMD(msg=False)
solve = problema.solve(solver=solver)

# Pasamos las variables del problema una variable
variable = problema.variables()
# Pasamos los datos al excel denuevo en una nueva hoja
dict_to_excel = {}
# primero pasamos los nombres a la primera columna
dict_I = {}
for col in range(len(I)):
    dict_I[col] = I[col]
dict_to_excel[columns[0]] = dict_I
# Luego de tenermos los nombres agregamos los datos de las Variables
for j in range(len(J)):
    aux = j
    dict_col = {}
    for i in range(len(I)):
        dict_col[i] = variable[aux].varValue
        aux += len(J)
    dict_to_excel[J[j]] = dict_col
optimo = "Optimo"
dict_to_excel[optimo] = pl.value(problema.objective)
columns.append(optimo)
data_to_excel = pd.DataFrame(dict_to_excel, columns=columns)
writer = pd.ExcelWriter("Taller_inventado.xlsx")
data.to_excel(writer, sheet_name="Parametros", index=False)
data_to_excel.to_excel(writer, sheet_name="Resultados", index=False)
writer.save()
