import analyze
import pandas
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import sys
import random

if sys.argv[1] == "" or sys.argv[2] == "":
     print("use like this: 'python3 main.py $USERNAME $CHANGE_SET_LIMIT'")

points_per_day = analyze.get_coordinates_for_user_by_day(sys.argv[1], change_set_limit=int(sys.argv[2]))
#points = analyze.get_coordinates_for_user_count(sys.argv[1], change_set_limit=int(sys.argv[2]))
points = {}
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

def plot_daily_world_map():
    fig = go.Figure()
    colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'pink', 'orange', 'grey']

    for day in points_per_day:
        color = random.choice(colors)
        for point in points_per_day[day]:
            fig.add_trace(go.Scattergeo(
                lon = [point.lon],
                lat = [point.lat],
                hoverinfo = 'text',
                mode = 'markers',
                marker = dict(
                    size = 10,
                    color = color,
                )))
            
        fig.add_trace(
        go.Scattergeo(
            lon = [points_per_day[day][i].lon for i in range(len(points_per_day[day]))],
            lat = [points_per_day[day][i].lat for i in range(len(points_per_day[day]))],
            mode = 'lines',
            line = dict(width = 2,color = color),
        )
    )

    fig.update_layout(
        mapbox_style="open-street-map"
    )

    fig.show()

#plot_heat_map()
#plot_world_map()

plot_daily_world_map()