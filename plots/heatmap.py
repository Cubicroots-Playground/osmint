import plotly.express as px
import pandas

# heatmap plots a heatmap based on the given data frame.
#
# The dataframe needs columns 'lat', 'lon' and 'cnt'.
def heatmap(
        df: pandas.DataFrame,
        img_out: str = None,
        ):
    fig = px.density_mapbox(df, 
                        lat="lat", 
                        lon="lon", 
                        z="cnt",
                        radius=10,
                        zoom=2,
                        )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    if img_out:
        fig.write_image(img_out)
    else:
        fig.show()