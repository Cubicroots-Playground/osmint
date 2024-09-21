import plotly.graph_objects as go
import pandas
import random
from rich.console import Console

from plots import autozoom

# heatmap plots a heatmap based on the given data frame.
#
# The dataframe needs columns 'lat', 'lon' and 'cnt'.
def plot(
        console: Console,
        points_per_day: dict,
        img_out: str = None,
        ):
    items = 0
    for _, points in points_per_day.items():
        items += len(points)
    if items > 1000 and not img_out:
        console.log(f"[red italic]Plotting huge amount of datapoints ({items}). Interactive browser output might have bad performance.[/red italic]")

    fig = go.Figure()
    # TODO move to separate file.
    colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'pink', 'orange', 'grey']
    max_lon = -200
    min_lon = 200
    max_lat = -200
    min_lat = 200

    for day in points_per_day:
        color = random.choice(colors)

        # Print dots.
        lons = []
        lats = []
        for point in points_per_day[day]:
            if point.lon > max_lon:
                max_lon = point.lon
            if point.lon < min_lon:
                min_lon = point.lon
            if point.lat > max_lat:
                max_lat = point.lat
            if point.lat < min_lat:
                min_lat = point.lat
            
            lons.append(point.lon)
            lats.append(point.lat)

        fig.add_trace(go.Scattergeo(
            lon = lons,
            lat = lats,
            hoverinfo = 'text',
            mode = 'markers',
            marker = dict(
                size = 10,
                color = color,
            ),
            name=day,
            ))
            
        # Print lines between dots of the same day.
        fig.add_trace(
        go.Scattergeo(
            lon = [points_per_day[day][i].lon for i in range(len(points_per_day[day]))],
            lat = [points_per_day[day][i].lat for i in range(len(points_per_day[day]))],
            mode = 'lines',
            line = dict(width = 2,color = color),
            name=day,
        )
        )

    console.log("Added data to plot.")

    center = autozoom.center_from_coordinates(max_lon=max_lon, min_lon=min_lon, max_lat=max_lat, min_lat=min_lat)
    fig.update_layout(
        mapbox_style="open-street-map",
        geo = dict(
            projection_scale=autozoom.from_coordinates(max_lon=max_lon, min_lon=min_lon, max_lat=max_lat, min_lat=min_lat),
            center=dict(lat=center[1], lon=center[0])
        )
    )

    console.log("Calculated zoom and center")

    if img_out:
        fig.write_image(img_out, width=2250, height=1500)
    else:
        fig.show()

    console.log("Plot rendered.")