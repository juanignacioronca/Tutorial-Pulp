import pulp as pl
import pandas as pd
# Creamos un data frame de pandas con los datos leidos de un archivo excel
data = pd.read_excel("Taller_2.xlsx", sheet_name="Parametros")
# Obtenemos los nombres de las columnas
columns = list(data.columns)                            # Me entrega la primera fila en una lista
# Luego definimos I como los trabajadores y para eso usamos la primera columna y extraemos los datos de esta manera
I = list(data[columns[0]])                             # I es una lista con todos los trabajadores
# print(I)

# Ahora definimos J como todas las tareas
J = columns                                            # J es una lista con todas las tareas
# Pero no hay que considerar la primera fila ya que son los trabajadores
J = J[1:]
# print(J)

# Para obtener los tiempos tenemos que recorrer todos los datos del data frame (como si fueran tablas)

T = {}
for i in range(len(I)):                                 # Recorro la cantidad de trabajadores (filas)
    for j in J:                                         # Recorro la cantidad de elementos dentro de cada fila
        t = list(data[j])                               # Tenemos la  lista de todos los valores de la columna j
        T[I[i], j] = t[i]                               # Agregamos al diccionario el elemento i de la lista t


# Definimos el Problema
problema = pl.LpProblem(name="Taller_2", sense=pl.LpMinimize)

# Definimos las Variables
X = pl.LpVariable.dicts(name="X[i,j]", indexs=[(i, j) for i in I for j in J], lowBound=0, upBound=1, cat=pl.LpBinary)

# Definimos las Restricciones
for i in I:
    problema += pl.lpSum(X[i, j] for j in J) == 1

for j in J:
    problema += pl.lpSum(X[i, j] for i in I) == 1

# Definimos la Funcion Objetivo

problema += pl.lpSum(T[i, j] * X[i, j] for i in I for j in J)

# Finalmente resolvemos el modelo

solver = pl.PULP_CBC_CMD(msg=False)
solve = problema.solve(solver=solver)

# Tomamos las variables y los valores y los asignamos a un diccionario para pasarlos a pandas y luego a excel
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

export_data = pd.DataFrame(dict_to_excel, columns=columns)
writer = pd.ExcelWriter("Taller_2.xlsx")
data.to_excel(writer, sheet_name="Parametros", index=False)
export_data.to_excel(writer, sheet_name="Resultados", index=False)
writer.save()
