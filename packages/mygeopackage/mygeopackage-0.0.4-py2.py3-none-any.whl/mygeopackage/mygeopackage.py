"""Main module."""
import json
import os
import requests
import numpy as np
import ipyleaflet
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, TileLayer
class Geo:
    uri = ""
    crs = ""
    attributes = []
    data = []

    def __init__(self,uri):
        self.uri = uri

        self.toArray()

    def toArray(self):

        if os.path.exists('json_to_load.geojson') == False:
            response = requests.get(self.uri)
            with open('json_to_load.geojson','w') as f:
                json_data = json.loads(response.text)
                json.dump(json_data,f)

        with open('json_to_load.geojson') as f:
            data = json.load(f)
            if data['crs'] != None:
                crs = data['crs']['properties']['name']
                self.crs = crs
            fields = list(data['features'][0]['properties'].keys())
            arr_list = []
            for feature in data['features']:
                arr_list.append((feature['geometry']['coordinates'][0],feature['geometry']['coordinates'][1],*list(feature['properties'].values())))
            arr = np.array(arr_list)
            
            self.attributes = fields
            self.data = arr
        

class Map(ipyleaflet.Map):
    def __init__(self,**kwargs):
        if "center" not in kwargs:
            kwargs["center"] = [40,-100]
        if "zoom" not in kwargs:
            kwargs['zoom'] = 4
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        super().__init__(**kwargs)

        if "height" not in kwargs:
            self.layout.height = "600px"
        else:
            self.layout.height = kwargs['height']

        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        if "google_map" not in kwargs or kwargs["google_map"] == "ROADMAP":
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Maps"
            )
            self.add_layer(layer)
        elif kwargs["google_map"] == "HYBRID":
            layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Satellite"
            )
            self.add_layer(layer)
