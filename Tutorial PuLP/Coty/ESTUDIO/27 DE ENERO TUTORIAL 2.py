import pulp as pl
import pandas as pd
# Creamos un data frame de pandas con los datos leidos de un archivo excel
data = pd.read_excel("TUTORIAL 2.xlsx", sheet_name="PARAMETROS")
# Obtenemos los nombres de las columnas
columns = list(data.columns)                            # Me entrega la primera fila (titulos) en una lista (Las llaves del diccionario de pandas)
# print(data)
# print("___")
# print(columns)
I = list(data[columns[0]])                             # I es una lista con todos los trabajadores
# print(I)

# Ahora definimos J como todas las tareas
J = columns                                            # J es una lista con todas las tareas
# Pero no hay que considerar la primera fila ya que son los trabajadores
J = J[1:]
# no hacer J.pop(0) ya que tambien lo eliminará en colums, por eso lo trabajamos como lista
print(J)
print(columns)

# Para obtener los tiempos tenemos que recorrer todos los datos del data frame (como si fueran tablas)

T = {}                                                  # diccionario de los tiempos
for i in range(len(I)):                                 # Recorro la cantidad de trabajadores (filas)
    for j in J:                                         # Recorro la cantidad de elementos dentro de cada fila
        t = list(data[j])                               # Tenemos la  lista de todos los valores de la columna j
        print(t)
        T[I[i], j] = t[i]                               # Agregamos al diccionario el elemento i de la lista t
# I[i]: trabajo con la lista de todos los trabajdores seleccionando el trabajador i
# diccionario T tiene como llave I[i] y j y su valor es de la lista t el elemento
# queda: [trabajo 1, tarea 1] = 27
#        [trabajador1, tarea 2] = 18

# Definimos el Problema
problema = pl.LpProblem(name="TUTORIAL 2", sense=pl.LpMinimize)

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
for var in variable:
    print(var.name, " : ", var.varValue)

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
writer = pd.ExcelWriter("TUTORIAL 2.xlsx")
data.to_excel(writer, sheet_name="PARAMETROS", index=False)
export_data.to_excel(writer, sheet_name="RESULTADOS", index=False)
writer.save()
