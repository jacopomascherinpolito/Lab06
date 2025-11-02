import flet as ft
from UI.view import View
from database.DB_connect import get_connection
from model.automobile import Automobile
from model.model import Autonoleggio
from UI.alert import AlertManager as Alert

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view : View, model : Autonoleggio):
        self._model = model
        self._view = view
        self._alert = Alert(self._view.page)

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_automobili(self, e):
        self._view.lista_auto.controls.clear()
        lista = self._model.get_automobili()
        for auto in lista:
            stato = "✅" if auto.disponibile else "⛔"
            self._view.lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        self._view.update()

    def cerca_automobili(self, e):
        self._view.lista_auto_ricerca.controls.clear()
        mod = self._view.input_modello_auto.value
        automobili_list = []
        cnx = get_connection()
        cursor = cnx.cursor()
        query = """SELECT * FROM automobile
                   WHERE modello = %s"""
        cursor.execute(query, (mod,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            self._alert.show_alert("Modello non trovato")
        else:
            for row in rows:
                automobili_list.append(Automobile(codice=row[0], marca=row[1], modello=row[2], anno=row[3], posti=row[4]))
            for auto in automobili_list:
                stato = "✅" if auto.disponibile else "⛔"
                self._view.lista_auto_ricerca.controls.append(ft.Text(f"{stato} {auto}"))
        self._view.update()



