import plotly.express as px
import pandas
from rich.console import Console

from plots import autozoom

# heatmap plots a heatmap based on the given data frame.
#
# The dataframe needs columns 'lat', 'lon' and 'cnt'.
def plot(
        console: Console,
        df: pandas.DataFrame,
        img_out: str = None,
        zoom: float = None,
        ):
    max_lon = -200
    min_lon = 200
    max_lat = -200
    min_lat = 200
    for _, row in df.iterrows():
        if row.lat > max_lat:
            max_lat = row.lat
        if row.lat < min_lat:
            min_lat = row.lat
        if row.lon > max_lon:
            max_lon = row.lon
        if row.lon < min_lon:
            min_lon = row.lon

    center = autozoom.center_from_coordinates(max_lon=max_lon, min_lon=min_lon, max_lat=max_lat, min_lat=min_lat)
    if not zoom:
        zoom = autozoom.from_coordinates(max_lon=max_lon, min_lon=min_lon, max_lat=max_lat, min_lat=min_lat)

    console.log(f"Calculated center and zoom level ({zoom}).")

    fig = px.density_mapbox(df, 
                        lat="lat", 
                        lon="lon", 
                        z="cnt",
                        radius=10,
                        zoom=zoom,
                        center=dict(lat=center[1], lon=center[0])
                        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(geo = dict(
            projection_scale=10
        ))
    
    console.log("Added density to figure.")

    if img_out:
        fig.write_image(img_out, width=2250, height=1500)
    else:
        fig.show()