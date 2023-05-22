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
        self.root.geometry("1205x618")
        self.frm = ttk.Frame(self.root)
        self.frm.grid()
        
        self.set_dark_theme()
        
        self.latitude_toggle = BooleanVar()
        self.longitude_toggle = BooleanVar()

        self.latitude_toggle.set(False)
        self.longitude_toggle.set(False)

        ttk.Label(self.frm, text="Donnez vos coordonnées").grid(column=0, row=0, columnspan=10)

        self.label_latitude = ttk.Label(self.frm, text="Latitude")
        self.entry_latitude_deg = ttk.Entry(self.frm)
        self.label_latitude_deg = ttk.Label(self.frm, text="°")
        self.entry_latitude_minuts = ttk.Entry(self.frm)
        self.label_latitude_minuts = ttk.Label(self.frm, text="'")
        self.entry_latitude_seconds = ttk.Entry(self.frm)
        self.label_latitude_seconds = ttk.Label(self.frm, text="''")

        self.label_longitude = ttk.Label(self.frm, text="Longitude")
        self.entry_longitude_deg = ttk.Entry(self.frm)
        self.label_longitude_deg = ttk.Label(self.frm, text="°")
        self.entry_longitude_minuts = ttk.Entry(self.frm)
        self.label_longitude_minuts = ttk.Label(self.frm, text="'")
        self.entry_longitude_seconds = ttk.Entry(self.frm)
        self.label_longitude_seconds = ttk.Label(self.frm, text="''")

        ttk.Label(self.frm, text="Description").grid(column=0, row=3)
        self.entry_description = ttk.Entry(self.frm)
        self.entry_description.grid(column=1, row=3, columnspan=6, sticky='ew')
        
        ttk.Button(self.frm, text="xx°yy'zz.aa''/xx.yyyyyyyyy", command=self.hide_show_widget).grid(column=0, row=4, columnspan=10)    
        
        self.points_listbox = Listbox(self.frm, height=25, width=50, bg="#252525", fg="white", selectbackground="#555555", selectforeground="white")
        self.points_listbox.grid(column=0, row=5, columnspan=10, pady=5)       
        
        self.satellite = True
        self.hidden = True
        self.hide_show_widget()
        
        ttk.Button(self.frm, text="Ajouter point", command=self.add_point).grid(column=0, row=7, columnspan=10)
        ttk.Button(self.frm, text="Sat/Map", command=self.toogle_map).grid(column=0, row=8, columnspan=10)   
        ttk.Button(self.frm, text="Quitter", command=self.root.destroy).grid(column=0, row=10, columnspan=10)
                
        self.load_map()

        self.text_description = None
        
    def hide_show_widget(self):
        self.label_latitude.grid(column=0, row=1)
        self.label_longitude.grid(column=0, row=1)
        self.entry_latitude_deg.delete(first=0,last=100)
        self.entry_longitude_deg.delete(first=0,last=100)
        self.entry_description.delete(first=0,last=100)
        if self.entry_latitude_minuts and self.entry_longitude_minuts:
            self.entry_latitude_minuts.delete(first=0,last=100)
            self.entry_latitude_seconds.delete(first=0,last=100)
            self.entry_longitude_minuts.delete(first=0,last=100)
            self.entry_longitude_seconds.delete(first=0,last=100)
        if self.hidden :
            self.entry_latitude_deg.grid(column=1, row=1, columnspan=6, sticky='ew')
            self.label_latitude_deg.grid(column=7, row=1)
            self.entry_latitude_minuts.grid_remove()
            self.label_latitude_minuts.grid_remove()
            self.entry_latitude_seconds.grid_remove()
            self.label_latitude_seconds.grid_remove()
            self.label_longitude.grid(column=0, row=2)
            self.entry_longitude_deg.grid(column=1, row=2, columnspan=6, sticky='ew')
            self.label_longitude_deg.grid(column=7, row=2)
            self.entry_longitude_minuts.grid_remove()
            self.label_longitude_minuts.grid_remove()
            self.entry_longitude_seconds.grid_remove()
            self.label_longitude_seconds.grid_remove()
        else:
            self.entry_latitude_deg.grid(column=1, row=1, columnspan=1)
            self.label_latitude_deg.grid(column=2, row=1)
            self.entry_latitude_minuts.grid(column=3, row=1)
            self.label_latitude_minuts.grid(column=4, row=1)
            self.entry_latitude_seconds.grid(column=5, row=1)
            self.label_latitude_seconds.grid(column=6, row=1)
            self.entry_longitude_deg.grid(column=1, row=2, columnspan=1)
            self.label_longitude_deg.grid(column=2, row=2)
            self.entry_longitude_minuts.grid(column=3, row=2)
            self.label_longitude_minuts.grid(column=4, row=2)
            self.entry_longitude_seconds.grid(column=5, row=2)
            self.label_longitude_seconds.grid(column=6, row=2)
        self.hidden = not self.hidden

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
            

    def add_point(self):
        latitude_text = self.entry_latitude_deg.get()
        longitude_text = self.entry_longitude_deg.get()
        latitude_text_minuts = self.entry_latitude_minuts.get()
        longitude_text_minuts = self.entry_longitude_minuts.get()
        latitude_text_seconds = self.entry_latitude_seconds.get()
        longitude_text_seconds = self.entry_longitude_seconds.get()
        description = self.entry_description.get()

        if latitude_text and longitude_text:
            if '°' in latitude_text:
                latitude_text = float(latitude_text) + float(latitude_text_minuts) / 60 + float(latitude_text_seconds) / 3600
            if '°' in longitude_text:
                longitude_text = float(longitude_text) + float(longitude_text_minuts) / 60 + float(longitude_text_seconds) / 3600
            
            latitude = float(latitude_text)
            longitude = float(longitude_text)

        # Utiliser Geopy pour obtenir l'adresse à partir des coordonnées
        geolocator = Nominatim(user_agent="map_app")
        location = geolocator.reverse((latitude, longitude))
        
        address_raw = location.raw['address']
        
        house_number = address_raw['house_number'] if 'house_number' in address_raw else ""
        road = address_raw['road'] if 'road' in address_raw else ""
        postcode = address_raw['postcode'] if 'postcode' in address_raw else ""
        city = address_raw['city'] if 'city' in address_raw else ""
        
        address = f"{description}\n{house_number}, {road}\n{postcode} {city}" if 'house_number' in address_raw else f"{description}\n{road}\n{postcode} {city}"
        
        if latitude_text and longitude_text:
            self.map_widget.set_marker(latitude, longitude, text=address)
            self.points_listbox.insert(END, f"{description}")
            if self.entry_latitude_minuts and self.entry_longitude_minuts and self.entry_latitude_seconds and self.entry_longitude_seconds:
                self.points_listbox.insert(END, f"Lat : {latitude_text}°{latitude_text_minuts}'{latitude_text_seconds}''")
                self.points_listbox.insert(END, f"Long : {longitude_text}°{longitude_text_minuts}'{longitude_text_seconds}''")
            elif self.entry_latitude_minuts and self.entry_longitude_minuts:
                self.points_listbox.insert(END, f"Lat : {latitude_text}°{latitude_text_minuts}'")
                self.points_listbox.insert(END, f"Long : {longitude_text}°{longitude_text_minuts}'")
            else:
                self.points_listbox.insert(END, f"Lat : {latitude}")
                self.points_listbox.insert(END, f"Long : {longitude}")
            self.points_listbox.insert(END, f"")
            self.map_widget.set_position(latitude, longitude)
            self.map_widget.set_zoom(22)
        else:
            messagebox.showerror('Erreur', 'Veuillez entrer des coordonnées valides.')
        
        self.m.save('map.html')
        
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