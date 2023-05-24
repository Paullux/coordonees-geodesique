from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from tkintermapview import TkinterMapView
from functools import partial
import folium

class MapApp:
    def __init__(self):
        self.m = folium.Map()

        self.root = Tk()
        self.root.geometry("")
        self.frm = ttk.Frame(self.root)
        self.frm.grid()
        
        self.set_dark_theme()
        
        self.latitude_toggle = BooleanVar()
        self.longitude_toggle = BooleanVar()
        
        self.entry_description = []
        offset = 0
        self.latitude_toggle.set(False)
        self.longitude_toggle.set(False)
        ttk.Label(self.frm, text="Donnez vos coordonnées").grid(column=0, row=0, columnspan=10)
        self.dict_coord = {}
        for i in range(1, 6):
            long_lat = ("Latitude " + str(i), "Longitude " + str(i))
            for name in long_lat:
                self.dict_coord[name] = [
                    ttk.Label(self.frm, text=name), 
                    ttk.Entry(self.frm), 
                    ttk.Label(self.frm, text="°"),
                    ttk.Entry(self.frm),
                    ttk.Label(self.frm, text="'"),
                    ttk.Entry(self.frm),
                    ttk.Label(self.frm, text="''")
                ]
            switch = "button_switch" + str(i)    
            self.dict_coord[switch] = ttk.Button(self.frm, text="xx°yy'zz.aa''/xx.yyyyyyyyy", command=lambda i=i: self.hide_show_widget(i, i * 10 - 10, False))
        ttk.Label(self.frm, text=" ").grid(column=0, row=58, columnspan=10)
        ttk.Button(self.frm, text="Ajouter points", command=self.add_point).grid(column=0, row=59, columnspan=10)
      
        self.satellite = True
        
        self.hidden = []
        
        self.hidden.append(True)
        self.hidden.append(False)
        self.hidden.append(False)
        self.hidden.append(False)
        self.hidden.append(False)
        self.desc = ['PDL','Point 1','Point 2','Point 3','Point 4']
        offset = 0
        for i in range(1, 6):
            self.hide_show_widget(i, offset, True)
            offset = offset + 10
        ttk.Button(self.frm, text="Sat/Map", command=self.toogle_map).grid(column=0, row=60, columnspan=10)
        ttk.Button(self.frm, text="Nettoyer coordonnées", command=self.clear_value).grid(column=0, row=61, columnspan=10)
        ttk.Button(self.frm, text="Quitter", command=self.root.destroy).grid(column=0, row=62, columnspan=10)
        
        ttk.Label(self.frm, text=" ").grid(column=0, row=58, columnspan=10)
                
        self.load_map()

        self.text_description = None
        
    def hide_show_widget(self, i, offset, First):   
        lat_long = ("Latitude ", "Longitude ")
        if First:
            ttk.Label(self.frm, text="Description " + str(i)).grid(column=0, row=offset + i)
            entry_description = ttk.Entry(self.frm)
            self.entry_description.append(entry_description)
            entry_description.grid(column=1, row=offset + i, columnspan=6, sticky='ew')
            entry_description.insert(0, self.desc[i - 1])
        for orientation in lat_long:
            text_index = orientation + str(int(i))
            w = self.dict_coord[text_index]
            if self.hidden[i - 1]:
                p = [
                    {"f": ["grid"], "k": [{"column": 0, "row": offset + 1 + i}]},
                    {"f": ["grid", "delete"], "k": [{"column": 1, "row": offset + 1 + i, "columnspan": 6, "sticky": 'ew'}, {"first": 0, "last" : 100}]},
                    {"f": ["grid", "grid_remove"], "k": [{"column": 7, "row": offset + 1 + i}, {}]},
                    {"f": ["delete", "grid_remove"], "k": [{"first": 0, "last" : 100}, {}]},
                    {"f": ["grid_remove"], "k": [{}]},
                    {"f": ["delete", "grid_remove"], "k": [{"first": 0, "last" : 100}, {}]},
                    {"f": ["grid_remove"], "k": [{}]}
                ]
                
                for widget, param in zip(w, p):
                    for func, kwargs in zip(param["f"], param["k"]):
                        getattr(widget, func)(**kwargs)                 
            else:
                p = [
                    {"f": ["grid"], "k": [{"column": 0, "row": offset + 2 + i}]},
                    {"f": ["grid", "delete"], "k": [{"column": 1, "row": offset + 2 + i, "columnspan": 1}, {"first": 0, "last" : 100}]},
                    {"f": ["grid"], "k": [{"column": 2, "row": offset + 2 + i}, {}]},
                    {"f": ["grid", "delete"], "k": [{"column":3, "row":offset + 2 + i}, {"first": 0, "last" : 100}]},
                    {"f": ["grid"], "k": [{"column":4, "row":offset + 2 + i}]},
                    {"f": ["grid", "delete"], "k": [{"column":5, "row":offset + 2 + i}, {"first": 0, "last" : 100}]},
                    {"f": ["grid"], "k": [{"column":6, "row":offset + 2 + i}]}
                ]
                
                for widget, param in zip(w, p):
                    for func, kwargs in zip(param["f"], param["k"]):
                        getattr(widget, func)(**kwargs)
            switch = "button_switch" + str(i)               
            self.dict_coord[switch].grid(column=0, row=offset + 3 + i, columnspan = 10, sticky='ew')
            offset = offset + 5
        self.hidden[i - 1] = not self.hidden[i - 1]

    def load_map(self):
        # Créez une instance de HtmlFrame et attachez-la à la fenêtre principale
        self.map_widget = TkinterMapView(self.root, width=900, height=600, corner_radius=0)
        self.map_widget.grid(column=8,row=0,rowspan = 8, sticky="nsew")
        self.map_widget.set_address("Tours, France", marker=False)
    
        
    def toogle_map(self):
        if self.satellite == True:
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        else:
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png") # carte de base OSM
        self.satellite = not self.satellite
            
    def is_a_float(self, value):
        if str(value).replace(".", "").isnumeric():
            return isinstance(float(value), float)
        else:
            return False

    def add_point(self):
        coordonnees = []
        for i in range (1, 6):
            long_lat = ("Latitude " + str(i), "Longitude " + str(i))
            if self.entry_description[i - 1] != '':
                coordonnees.append(self.entry_description[i - 1].get())
            else:
                coordonnees.append("description non trouvé")
            for name in long_lat:
                coord = self.dict_coord[name]
                coordonnees.append(coord[1].get())
                if coord[1] is not None and coord[3] is not None and coord[5] is not None:                    
                    coordonnees.append(coord[3].get())
                    coordonnees.append(coord[5].get())
        
        offset = 0
        latitude = []
        longitude = []
        for i in range(0, 5):
            description = coordonnees[0 + i + offset]
            latitude_text, latitude_text_minuts, latitude_text_seconds = float(coordonnees[1 + i + offset]), coordonnees[2 + i + offset], coordonnees[3 + i + offset]
            longitude_text, longitude_text_minuts, longitude_text_seconds = float(coordonnees[4 + i + offset]), coordonnees[5 + i + offset], coordonnees[6 + i + offset]

            offset = offset + 6

            if self.is_a_float(latitude_text) and self.is_a_float(longitude_text):
                if self.is_a_float(latitude_text_minuts) and self.is_a_float(latitude_text_seconds) and self.is_a_float(longitude_text_minuts) and self.is_a_float(longitude_text_seconds):
                    latitude.append(float(float(latitude_text) + float(latitude_text_minuts) / 60 + float(latitude_text_seconds) / 3600))
                    longitude.append(float(float(longitude_text) + float(longitude_text_minuts) / 60 + float(longitude_text_seconds) / 3600))
                else:
                    latitude.append(float(latitude_text))
                    longitude.append(float(longitude_text))
            
                # Utiliser Geopy pour obtenir l'adresse à partir des coordonnées
                geolocator = Nominatim(user_agent="map_app")
                location = geolocator.reverse(f"{latitude[i]}, {longitude[i]}")
                
                address_raw = location.raw['address']
                
                house_number = address_raw['house_number'] if 'house_number' in address_raw else ''
                road = address_raw['road'] if 'road' in address_raw else "Lieu-dit " + address_raw['hamlet'] if 'hamlet' in address_raw else ''
                postcode = address_raw['postcode'] if 'postcode' in address_raw else ''
                city = address_raw['city'] if 'city' in address_raw else address_raw['village'] if 'village' in address_raw else ''
                
                address = f"{description}\n{house_number}, {road}\n{postcode} {city}" if 'house_number' in address_raw else f"{description}\n{road}\n{postcode} {city}"
                
                if self.is_a_float(latitude_text) and self.is_a_float(longitude_text) and i < len(latitude) and i < len(longitude):
                    self.map_widget.set_marker(latitude[i], longitude[i], text=address)
                    self.map_widget.set_position(latitude[i], longitude[i])
                    self.map_widget.set_zoom(22)
                else:
                    messagebox.showerror('Erreur', 'Veuillez entrer des coordonnées valides.')
            
                self.m.save('map.html')
            else:
                messagebox.showerror('Erreur', 'Veuillez entrer des coordonnées valides.')
        
    def clear_value(self):    
        for i in range (1, 6):
            long_lat = ("Latitude " + str(i), "Longitude " + str(i))
            self.entry_description[i-1].delete(first=0,last=100)
            for name in long_lat:
                coord = self.dict_coord[name]
                coord[1].delete(first=0,last=100)
                if coord[1] is not None and coord[3] is not None and coord[5] is not None:                    
                    coord[3].delete(first=0,last=100)
                    coord[5].delete(first=0,last=100)
        
        self.entry_latitude_deg.delete(first=0,last=100)
        self.entry_longitude_deg.delete(first=0,last=100)
        self.entry_description.delete(first=0,last=100)
        if self.entry_latitude_minuts and self.entry_longitude_minuts:
            self.entry_latitude_minuts.delete(first=0,last=100)
            self.entry_latitude_seconds.delete(first=0,last=100)
            self.entry_longitude_minuts.delete(first=0,last=100)
            self.entry_longitude_seconds.delete(first=0,last=100)
        
    def set_dark_theme(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configurez les couleurs des éléments spécifiques
        self.style.configure("TFrame", background="#363636")
        self.style.configure("TLabel", foreground="white", background="#363636")
        self.style.configure("TEntry", fieldbackground="white", background="white", foreground="black")
        self.style.configure("TButton", background="#555555", foreground="white")

        # Configurez les couleurs pour les barres de défilement
        self.style.configure("Vertical.TScrollbar", background="#252525", troughcolor="#363636", arrowcolor="white")
        self.style.map("Vertical.TScrollbar", background=[('active', "#252525"), ('!active', "#363636")], troughcolor=[('active', "#363636"), ('!active', "#363636")], arrowcolor=[('active', "white"), ('!active', "white")])

        # Configurez les couleurs pour les listes
        self.style.configure("TListbox", background="#252525", foreground="white", fieldbackground="#252525")
        self.style.map("TListbox", background=[('active', "#363636"), ('!active', "#252525")], foreground=[('active', "white"), ('!active', "white")], fieldbackground=[('active', "#363636"), ('!active', "#252525")])

        # Configurez les couleurs pour les cases à cocher et les boutons radio
        self.style.configure("TRadiobutton", background="#363636", foreground="white")
        self.style.configure("TCheckbutton", background="#363636", foreground="white")

        # Configurez les couleurs pour les messages d'erreur
        self.style.configure("TMessage", background="#363636", foreground="red")

    def run(self):
        self.root.mainloop()

app = MapApp()
app.run()