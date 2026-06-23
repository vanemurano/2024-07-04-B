import flet as ft
from UI.view import View
from model.modello import Model
from model.state import State


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year=None
        self._state: State=None

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        anno=self._view.ddyear.value
        stato=self._state
        if anno is None or stato is None:
            self._view.create_alert("Selezionare prima un anno e uno stato")
            return
        try:
            intAnno=int(anno)
        except ValueError:
            self._view.create_alert("Errore conversione anno in intero")
            return
        self._model.buildGraph(intAnno, stato)
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNNodes()}\n"
                    f"Numero di archi: {self._model.getNEdges()}")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNComp()} componenti connesse")
        )
        self._view.txt_result1.controls.append(
            ft.Text(f"La componente connessa più grande è costituita da {len(self._model.compMax())} nodi")
        )
        for n in self._model.compMax():
            self._view.txt_result1.controls.append(ft.Text(n))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        if self._model.getNNodes()==0:
            self._view.create_alert("Creare prima il grafo!")
            return
        cammino, punteggio = self._model.getBestPath()
        self._view.txt_result2.controls.append(
            ft.Text(f"Miglior cammino trovato, con punteggio {punteggio}:")
        )
        for s in cammino:
            self._view.txt_result2.controls.append(ft.Text(s))
        self._view.update_page()

    def fillDDYears(self):
        years=self._model.get_all_years()
        yearsOpt=list(map(lambda x: ft.dropdown.Option(data=x,
                                                       text=x,
                                                       on_click=self.fillDDState), years))
        self._view.ddyear.options = yearsOpt
        self._view.update_page()

    def fillDDState(self, e):
        self.readDDYear(e)
        self._view.ddstate.options.clear()
        stati=self._model.get_states_for_year(self._year)
        statiOpt=list(map(lambda x: ft.dropdown.Option(text=x.name,
                                                       data=x,
                                                       key=x.id,
                                                       on_click=self.readDDState), stati))
        self._view.ddstate.options=statiOpt
        self._view.update_page()

    def readDDYear(self, e):
        self._year=e.control.data

    def readDDState(self, e):
        self._state=e.control.data


