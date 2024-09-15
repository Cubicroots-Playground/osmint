from osm import ChangeSet
import pandas
from . import Point

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