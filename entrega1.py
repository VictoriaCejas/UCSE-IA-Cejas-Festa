from simpleai.search import SearchProblem
from simpleai.search.traditional import breadth_first, depth_first, limited_depth_first, iterative_limited_depth_first, uniform_cost, greedy, astar
from simpleai.search.viewers import WebViewer, ConsoleViewer, BaseViewer
from simpleai.search.models import SearchNode

ACTIONS={'abajo': (+1, 0),
         'arriba': (-1, 0),
         'derecha':(0,+1),
         'izquierda': (0, -1),
        }
ISLAND=(2,0)
HOME=(5,5)

def createState(french,pirates):
    """El estado inicial es una tupla con dos tuplas: piratas y francese,
    por cada pirata hay una tupla con la posicion del pirata + 'false' o 'true' si tiene el mapa"""
    list_pirates=[]
    for pirate in pirates:
        list_pirates.append((pirate,'false'))
    tuple_pirates=tuple(list_pirates)
    tuple_french=tuple(french)
    state=(tuple_pirates,tuple_french)
    return state

def in_limits_map(pirate):
    row,col=pirate
    return (0<=row<=5) and (0<=col<=5)


class Intelligents_Pirates(SearchProblem):

    def is_goal(self,state):
    #Si hay piratas, y uno tiene el mapa y ademas esta en FINAL es goal
        pirates,_=state
        if len(pirates)>0:
            for pirate,map in pirates:
                if pirate==HOME and map=='true':
                    return True
            return False
        return False

    def cost(self,state1,action,state2):
        #Recibe al los estados y acciones, se fija si la accion es attack y le pone mas peso que solo moverse
        return 1


    def actions(self,state):
        """Devuelve [accion en strig, la posicion del pirata, y el nombre de la accion para buscar en el diccionario]"""
        actions=[]
        pirates,french=state
        pirates_pos=[]
        for p,_ in pirates:
            pirates_pos.append(p)
        for pirate,map in pirates:
            for actn in ACTIONS:
                action=ACTIONS[actn]
                new_pos_pirate= pirate[0]+action[0],pirate[1]+action[1]
                if in_limits_map(new_pos_pirate):
                    index_pirate=pirates.index((pirate,map))
                    if new_pos_pirate in french:
                        if len(pirates)>1:
                            actions.append(('attack',index_pirate,actn))
                    else:
                        if not(new_pos_pirate in pirates_pos):
                            #Si no hay pirata en la nueva posicion
                            actions.append(('move',index_pirate,actn))
        return actions



    def result(self,state,action):
        pirates,french=state
        actn,pirate_index,move=action
        list_pirates=list(pirates)
        list_french= list(french)
        move_to=ACTIONS[move]

        old_pirate,map=list_pirates[pirate_index]
        new_pos_pirate=old_pirate[0]+move_to[0],old_pirate[1]+move_to[1]

        if actn=='attack':
            # elimina al frances y al pirata del estado en su correspondiente tupla
            list_pirates.pop(pirate_index)
            list_french.remove(new_pos_pirate)
            state=((tuple(list_pirates),tuple(list_french)))
        if actn=='move':
            #mueve al pirata y verifica si quedo en la isla o no
            if new_pos_pirate == ISLAND:
                map = 'true'
            new_tuple_pirate = (new_pos_pirate, map)
            list_pirates[pirate_index] = new_tuple_pirate
            state = (tuple(list_pirates), tuple(list_french))
        return state




    def heuristic(self, state):
        """Heuristica si nadie tiene el mapa: por cada pirata( manhattan del pirata hasta ISLA + manhattan de la ISLA hasta FINAL)
           Heuristica si alguien tiene el mapa: manhattan del pirata con mapa mas cercano a FINAL
        """
        pirates,french=state
        list_pirates=list(pirates)
        manhattan_to_Map=[]
        manhattan_to_Home=[]
        manhattan_Map_to_Home=abs(HOME[0]-ISLAND[0])+abs(HOME[1]-ISLAND[1])
        sum_manhattan=0
        if len(list_pirates)>0:
            for pirate,map in list_pirates:
                if map =='false':
                    manhattan= abs(pirate[0]-ISLAND[0])+abs(pirate[1]-ISLAND[1])
                    manhattan_to_Map.append((manhattan+manhattan_Map_to_Home))
                    sum_manhattan=sum_manhattan+manhattan+manhattan_Map_to_Home
                else:
                    manhattan= abs(pirate[0]-HOME[0])+abs(pirate[1]-HOME[1])
                    manhattan_to_Home.append(manhattan)

            if len(manhattan_to_Home)>0:
                min_to_Home= min(manhattan_to_Home)
                heuristic= min_to_Home
                return heuristic
            if len(manhattan_to_Map)>0:
                #Si ninguno tiene el mapa, es la suma manhattan de cada pirata a la isla ida y vuelta
                heuristic=sum_manhattan #con la suma va mas rapido
                #heuristic=max(manhattan_to_Map)
                return  heuristic

def resolver(metodo_busqueda,franceses,piratas):

    initial=createState(franceses,piratas)
    my_viewer= None
    #my_viewer=BaseViewer()
    if metodo_busqueda=='astar':
        result=astar(Intelligents_Pirates(initial),graph_search=True,viewer=my_viewer)
    elif metodo_busqueda=='breadth_first':
        result=breadth_first(Intelligents_Pirates(initial),graph_search=True,viewer=my_viewer)
    elif metodo_busqueda=='depth_first':
        result=depth_first(Intelligents_Pirates(initial),graph_search=True,viewer=my_viewer)
    elif metodo_busqueda=='greedy':
        result=greedy(Intelligents_Pirates(initial),graph_search=True,viewer=my_viewer)

    return result

if __name__ == '__main__':
    my_viewer=ConsoleViewer()
    #result=resolver('breadth_first', [], [(4, 4)])

    franceses_consigna = (
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (5, 0),
    )
    piratas_consigna = (
        (4, 4),
        (4, 5),
        (5, 4),
    )

    initial=createState(franceses_consigna,piratas_consigna)
    #result = breadth_first(Intelligents_Pirates(initial), graph_search=True, viewer=my_viewer)
    #result = depth_first(Intelligents_Pirates(initial), graph_search=True, viewer=my_viewer)
    #result = greedy(Intelligents_Pirates(initial), graph_search=True, viewer=my_viewer)
    result = astar(Intelligents_Pirates(initial), graph_search=True, viewer=my_viewer)

    print("visited nodes: {}".format(my_viewer.stats['visited_nodes']))
    print("depth: {}".format(len(result.path())))
    print("cost: {}".format(result.cost))
    print("max fringe size : {}".format(my_viewer.stats['max_fringe_size']))
