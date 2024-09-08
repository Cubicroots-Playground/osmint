import analyze
import pandas
import plotly.express as px

coordinates = analyze.get_coordinates_for_user("Fizzie41")

coordinates_list = []

for d in coordinates:
    for c in coordinates[d]:
        c = list(c)
        coordinates_list.append(
            {'lat': c[0], 'lon': c[1]}
        )

df = pandas.DataFrame(coordinates_list, columns=['lat', 'lon'])

print(df)

color_scale = [(0, 'orange'), (1,'red')]

fig = px.scatter_geo(df, 
                        lat="lat", 
                        lon="lon",
                        )

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()