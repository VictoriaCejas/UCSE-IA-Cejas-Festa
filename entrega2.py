import itertools
import re
from simpleai.search import (backtrack, CspProblem, LEAST_CONSTRAINING_VALUE,HIGHEST_DEGREE_VARIABLE,
                             min_conflicts, MOST_CONSTRAINED_VARIABLE)
from simpleai.search.csp import _find_conflicts,convert_to_binary,_min_conflicts_value
from datetime import datetime

VARIABLES=['Taller de Django Girls','Taller de introducción a Python','Keynote sobre diversidad','Keynote sobre cómo ser core developer de Python','Cómo hacer APIs rest en Django','Diseño de sistemas accesibles','Cómo hacer unit testing en Python','Editores de código para Python','Cómo hacer música con Python','Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más','Python para análisis de imágenes','Python para satélites espaciales','Cómo publicar tu lib en PyPI','Introducción a Pandas para procesamiento de datos']

ROOMS=['Aula magna','Aula 42','Laboratorio']

HOURS=[10, 11, 14, 15, 16 ,17]
GRID=[]

MORNING=['Taller de introducción a Python','Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más']
LAB=['Taller de Django Girls','Taller de introducción a Python','Cómo hacer APIs rest en Django','Diseño de sistemas accesibles','Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más']
MAGNA=['Keynote sobre diversidad','Keynote sobre cómo ser core developer de Python','Cómo hacer APIs rest en Django','Diseño de sistemas accesibles','Cómo hacer unit testing en Python','Editores de código para Python','Cómo hacer música con Python','Python para análisis de imágenes','Python para satélites espaciales','Cómo publicar tu lib en PyPI']
AULA=['Cómo hacer APIs rest en Django','Cómo hacer unit testing en Python','Cómo hacer música con Python','Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más','Python para análisis de imágenes','Python para satélites espaciales','Cómo publicar tu lib en PyPI','Introducción a Pandas para procesamiento de datos']


for room in ROOMS:
 for hour in HOURS:
     tuple= (room,hour)
     GRID.append(tuple)

DOMAINS = {var: GRID for var in VARIABLES}

def unary():
    need_compueter('Taller de Django Girls')
    need_compueter('Taller de introducción a Python')
    morning('Taller de introducción a Python')
    in_room('Aula magna','Keynote sobre diversidad')
    afternoon('Keynote sobre diversidad')
    in_room('Aula magna','Keynote sobre cómo ser core developer de Python')
    afternoon('Keynote sobre cómo ser core developer de Python')
    need_projector('Cómo hacer APIs rest en Django')
    low_level('Diseño de sistemas accesibles')
    need_projector('Cómo hacer unit testing en Python')
    need_projector('Editores de código para Python')
    need_sound('Editores de código para Python')
    need_projector('Cómo hacer música con Python')
    not_in_room('Aula magna','Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más')
    morning('Cómo ser un buen vendedor de software, negocios, contabilidad y mucho más')
    not_in_room('Laboratorio','Python para análisis de imágenes')
    need_projector('Python para satélites espaciales')
    afternoon('Python para satélites espaciales')
    need_projector('Cómo publicar tu lib en PyPI')
    need_projector('Introducción a Pandas para procesamiento de datos')
    top_level('Introducción a Pandas para procesamiento de datos')

def low_level(key):
    unary = DOMAINS[key]
    copy = unary[:]
    room = 'Aula 42'
    for element in unary:
        if element[0] == room:
            copy.remove(element)
    DOMAINS[key] = copy

def top_level(key):
    unary = DOMAINS[key]
    copy = unary[:]
    room = 'Aula 42'
    for element in unary:
        if element[0] != room:
            copy.remove(element)
    DOMAINS[key] = copy

def need_sound(key):
    unary = DOMAINS[key]
    copy = unary[:]
    room = 'Aula magna'
    for element in unary:
        if element[0] != room:
            copy.remove(element)
    DOMAINS[key] = copy

def need_projector(key):
    unary=DOMAINS[key]
    copy= unary[:]
    room='Laboratorio'
    for element in unary:
        if element[0]==room:
            copy.remove(element)
    DOMAINS[key]=copy

def need_compueter(key):
    unary= DOMAINS[key]
    copy=unary[:]
    room='Laboratorio'
    for element in unary:
        if element[0] != room:
            copy.remove(element)
    DOMAINS[key]= copy

def not_in_room(room,key):
    unary= DOMAINS[key]
    copy=unary[:]
    for element in unary:
        if element[0] == room:
            copy.remove(element)
    DOMAINS[key]=copy

def in_room(room,key):
    unary= DOMAINS[key]
    copy=unary[:]
    for element in unary:
        if element[0] != room:
            copy.remove(element)
    DOMAINS[key]=copy

def morning(key):
    unary=DOMAINS[key]
    copy= unary[:]
    for element in unary:
        if element[1] > 11:
            copy.remove(element)
    DOMAINS[key]=copy

def afternoon(key):
    unary=DOMAINS[key]
    copy= unary[:]
    for element in unary:
        if element[1] < 14:
            copy.remove(element)
    DOMAINS[key]=copy

def differentHour(vars,vals):
    conference1=vals[0]
    conference2=vals[1]
    return conference1[1] != conference2[1]

def different(vars,vals):
    conference1=vals[0]
    conference2=vals[1]
    return  conference1!=conference2

restricciones=[]

for var1,var2 in itertools.combinations(LAB,2):
	#compara que los que puedan estar en LAB sean diferentes
    restricciones.append(((var1,var2),different))

for var1,var2 in itertools.combinations(MAGNA,2):
	#compara que los que puedan estar en AULA MAGNA sean diferentes
    restricciones.append(((var1,var2),different))

for var1,var2 in itertools.combinations(AULA,2):
	#compara que los que puedan estar en AULA 42 sean diferentes
    restricciones.append(((var1,var2),different))



for var in VARIABLES:
	#Cuando haya keynotes que no haya otro evente al mismo horario en el LAB o en el Aula
    keynote1='Keynote sobre diversidad'
    keynote2='Keynote sobre cómo ser core developer de Python'
    if (var != keynote1 and var!=keynote2) and (var not in MORNING) and (var in LAB or var in AULA):
		#Que la variable no sea un keynote, que no se pueda dar solo en la mañana y que que puedan ir al LAB o al Aula en diferentes horarios. A magna no, ya compare que sea diferente
        restricciones.append(((keynote1,var),differentHour))
        restricciones.append(((keynote2,var),differentHour))

#Que los keynotes tambien esten en distinto horario
#restricciones.append((('Keynote sobre diversidad','Keynote sobre cómo ser core developer de Python'),differentHour))

def resolver(metodo_busqueda, iteraciones):
    unary()
    problem = CspProblem(VARIABLES, DOMAINS, restricciones)
    if metodo_busqueda== 'backtrack':
        result = backtrack(problem, value_heuristic=HIGHEST_DEGREE_VARIABLE, variable_heuristic=MOST_CONSTRAINED_VARIABLE,inference=False)
    if metodo_busqueda == 'min_conflicts':
        result= min_conflicts(problem,iterations_limit=iteraciones)
    return result

if __name__ == '__main__':

    inicio=datetime.now()
    problem= CspProblem(VARIABLES,DOMAINS,restricciones)
    resultBacktrack=resolver('backtrack',None)
    fin=datetime.now()
    diferencia = (fin - inicio).total_seconds()
    print('result: {}'.format(resultBacktrack))
    print('time: {}'.format(diferencia))

    inicio = datetime.now()
    problem = CspProblem(VARIABLES, DOMAINS, restricciones)
    resultMin = resolver('min_conflicts', None)
    fin = datetime.now()
    diferencia = (fin - inicio).total_seconds()
    print('result: {}'.format(resultMin))
    print('time: {}'.format(diferencia))