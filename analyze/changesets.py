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

def changesets_to_points_per_day(
        changesets: list[ChangeSet],
) -> dict[str, list[Point]]:
    coordinates_per_day = {}
    for change_set in changesets:
        if change_set.area.size() == 0.0:
            # Change set is single point, add it.
            date = change_set.created_at.strftime('%Y-%m-%d')

            if date not in coordinates_per_day:
                coordinates_per_day[date] = []

            coordinates_per_day[date].append(Point(change_set.area.min_lat, change_set.area.min_long))

        else:
            for change in change_set.changes:
                date = change.created_at.strftime('%Y-%m-%d')

                if date not in coordinates_per_day:
                    coordinates_per_day[date] = []

                coordinates_per_day[date].append(Point(change.lat, change.long))

            continue


    return coordinates_per_day