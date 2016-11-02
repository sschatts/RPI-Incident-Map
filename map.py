import folium
import pandas as pd
import bs4
import json

def create_map():
	'''html = '''
		#	<h5> TEsting Test  <br> asdfsaddfsdf </h5>'''
	'''iframe = folium.element.IFrame(html=html, width=200, height=200)
	popup = folium.Popup(iframe, max_width=2650)'''
	#map = folium.Map(location = RPI_COORD, zoom_start = 16, height = 600, width = 400) #can play around with this to adjust size of map
	#folium.Marker([42.731693,-73.6818865], popup = popup).add_to(map)
	RPI_COORD = (42.730105,-73.6771229)
	map = folium.Map(location = RPI_COORD, zoom_start = 16)
	folium.Marker([42.731693,-73.6818865], popup = 'Test <br> 1234').add_to(map)
	folium.Marker([42.731593,-73.6728765], popup = 'Test2', icon = folium.Icon(icon = 'cloud', color = 'pink')).add_to(map)
	
	'''
	for j in file.readlines():
		j_obj = json.load(j)
		print j_obj['coordinates']
		#folium.Marker(line[coordinates])
	'''
	

	map.save('demo.html')

def html_clean():
	f = open('newdemo.html', 'w')
	with open('demo.html') as inf:
		for line in inf.readlines():
			if '&lt;br&gt;' in line:
				#print line
				line = line.replace('&lt;br&gt;', '<br />')
			f.write(line + '\n')
		
	#for line in txt:
	#	print line


def main():
	#f = open('tester.txt', 'r')
	create_map()
	html_clean()

if __name__ == "__main__":
    main()
