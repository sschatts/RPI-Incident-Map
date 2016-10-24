import folium
import pandas as pd

'''from jinja2 import Template
popup_template = Template(u
            var {{this.get_name()}} = L.popup({maxWidth: '{{this.max_width}}'});
            {% for name, element in this.html._children.items() %}
                var raw_html = String.raw`{{element.render(**kwargs).replace('\\n',' ')}}`
                var {{name}} = $('<div/>').html(raw_html).text()
                {{this.get_name()}}.setContent({{name}});
            {% endfor %}
            {{this._parent.get_name()}}.bindPopup({{this.get_name()}});
            {% for name, element in this.script._children.items() %}
                {{element.render()}}
            {% endfor %}) # noqa
html = <img width="{width}" height="{height}" src="{href}"><a href="{href}" target="_new">{href}</a>
popup = folium.Popup(html)
popup._template = popup_template'''

RPI_COORD = (42.730105,-73.6771229)

#map = folium.Map(location = RPI_COORD, zoom_start = 16, height = 600, width = 400) #can play around with this to adjust size of map
map = folium.Map(location = RPI_COORD, zoom_start = 16)
folium.Marker([42.731693,-73.6818865], popup = 'Test <br> 1234').add_to(map)
folium.Marker([42.731593,-73.6728765], popup = 'Test2', icon = folium.Icon(icon = 'cloud', color = 'pink')).add_to(map)

map.save('demo.html')

#display(map)
