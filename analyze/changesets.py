from osm import ChangeSet
import pandas
from . import Point
import random

colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'pink', 'orange', 'grey']

def changesets_to_heatmap_df(
        changesets: list[ChangeSet],
) -> pandas.DataFrame:
    points = _changesets_to_points(changesets)

    points_counted = {}
    for point in points:
        if point in points_counted:
            points_counted[point] += 1
        else:
            points_counted[point] = 1

    coordinates_list = []
    for point, cnt in points_counted.items():
        coordinates_list.append(
            {'lat': point.lat, 'lon': point.lon, 'cnt': cnt},
        )

    return pandas.DataFrame(coordinates_list, columns=['lat', 'lon', 'cnt'])


def _changesets_to_points(
        changesets: list[ChangeSet]
) -> list[Point]:
    points = []
    for changeset in changesets:
        if changeset.changes:
            for change in changeset.changes:
                points.append(Point(
                    change.lat,
                    change.long,
                ))
        else:
            points.append(Point(
                changeset.area.min_lat,
                changeset.area.min_long,
            ))

    return points

def changesets_to_daily_colored_df(
        changesets: list[ChangeSet],
) -> pandas.DataFrame:
    coordinates_list = []
    colors_per_day = {}

    for change_set in changesets:
        date = change_set.created_at.strftime('%Y-%m-%d')
        if date not in colors_per_day:
            colors_per_day[date] = random.choice(colors)
        color = colors_per_day[date]            

        if change_set.area.size() == 0.0:
            # Change set is single point, add it.
            coordinates_list.append({
                'lat': change_set.area.min_lat,
                'lon': change_set.area.min_long,
                'color': color,
                'date': date,
            })
        else:
            for change in change_set.changes:
                date = change.created_at.strftime('%Y-%m-%d')
                if date not in colors_per_day:
                    colors_per_day[date] = random.choice(colors)
                color = colors_per_day[date] 

                coordinates_list.append({
                    'lat': change.lat,
                    'lon': change.long,
                    'color': color,
                    'date': date,
                })


    return pandas.DataFrame(coordinates_list, columns=['lat', 'lon', 'color', 'date'])