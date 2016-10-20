import folium
import pandas as pd

RPI_COORD = (42.730105,-73.6771229)

#map = folium.Map(location = RPI_COORD, zoom_start = 16, height = 600, width = 400) #can play around with this to adjust size of map
map = folium.Map(location = RPI_COORD, zoom_start = 16)
folium.Marker([42.731693,-73.6818865], popup='Test').add_to(map)
folium.Marker([42.731593,-73.6728765], popup = 'Test2', icon = folium.Icon(icon = 'cloud', color = 'pink')).add_to(map)

map.save('demo.html')

#display(map)
