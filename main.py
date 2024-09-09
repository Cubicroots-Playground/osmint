import analyze
import pandas
import plotly.express as px
import plotly.io as pio

#pio.renderers.default = "chrome"

points = analyze.get_coordinates_for_user_count("Fizzie41")
coordinates_list = []

for point, cnt in points.items():
        coordinates_list.append(
            {'lat': point.lat, 'lon': point.lon, 'cnt': cnt}
        )

df = pandas.DataFrame(coordinates_list, columns=['lat', 'lon', 'cnt'])

def plot_world_map():
    fig = px.scatter_geo(df, 
                        lat="lat", 
                        lon="lon", 
                        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

def plot_heat_map():
    fig = px.density_mapbox(df, 
                        lat="lat", 
                        lon="lon", 
                        z="cnt",
                        radius=10,
                        zoom=2,
                        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

plot_heat_map()
plot_world_map()