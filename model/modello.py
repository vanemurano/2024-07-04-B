import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph=nx.Graph() # semplice, non orientato
        self._nodes=[]
        self._idMapStates = {}
        for stato in DAO.get_all_states():
            self._idMapStates[stato.id] = stato
        self._idMapSighting={}
        for s in DAO.get_all_sightings():
            self._idMapSighting[s.id]=s
        self._bestPath = []
        self._bestScore = 0
        self.i=0

    def get_all_years(self):
        return DAO.get_all_years()

    def get_states_for_year(self, year):
        return DAO.get_states_for_year(year)

    def buildGraph(self, year, state):
        self._graph.clear()
        self._nodes = DAO.get_all_nodes(year, state.id)
        self._graph.add_nodes_from(self._nodes)
        for s1, s2 in DAO.get_all_edges(year, state.id, self._idMapSighting):
            if s1 in self._nodes and s2 in self._nodes and s1.distance_HV(s2)<100:
                self._graph.add_edge(s1, s2)

    def getBestPath(self):
        parziale=[]
        self._bestPath=[]
        self._bestScore=0
        for n in self._nodes:
            parziale.append(n)
            self._ricorsione(parziale, 100) #punteggio iniziale 100 perché abbiamo già un nodo
            parziale.pop() # backtracking
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, score):
        self.i+=1
        if score>self._bestScore:
            self._bestScore=score
            self._bestPath=copy.deepcopy(parziale)
        # condizione ricorsiva
        for n in self._graph.neighbors(parziale[-1]):
            mese=n.datetime.month
            if n not in parziale and n.duration>parziale[-1].duration and self.controlloMesi(parziale, mese)<3:
                new_score=score+100
                if mese==parziale[-1].datetime.month:
                    new_score+=200
                parziale.append(n)
                self._ricorsione(parziale, new_score)
                parziale.pop() # backtracking

    def controlloMesi(self, parziale, month):
        i=0
        for s in parziale:
            if s.datetime.month==month:
                i+=1
        return i

    def getNComp(self):
        return nx.number_connected_components(self._graph)

    def compMax(self):
        comp=max(nx.connected_components(self._graph), key=len)
        return comp

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)

