import analyze
import pandas
import plotly.express as px

coordinates = analyze.get_coordinates_for_user("Fizzie41")

coordinates_list = []

for d in coordinates:
    for c in coordinates[d]:
        c = list(c)
        coordinates_list.append(
            {'lat': c[0], 'lon': c[1], 'cnt': 1}
        )

df = pandas.DataFrame(coordinates_list, columns=['lat', 'lon', 'cnt'])

print(df)

color_scale = [(0, 'orange'), (1,'red')]

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
                        )

    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

#plot_heat_map()
plot_world_map()