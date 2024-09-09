import osm

class Point:

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon
        

def get_coordinates_for_user_by_day(user_display_name: str) -> dict[str, list[Point]]:
    coordinates_per_day = {}

    change_sets = osm.get_changesets(user_display_name, limit=100)
    for change_set in change_sets:
        if change_set.area.size() == 0.0:
            # Change set is single point, add it.
            date = change_set.created_at.strftime('%Y-%m-%d')

            if date not in coordinates_per_day:
                coordinates_per_day[date] = []

            coordinates_per_day[date].append(Point(change_set.area.min_lat, change_set.area.min_long))

        else:
            # Change set is area, get single node points contained in it.
            changes = osm.get_changes(change_set.id)
            for change in changes:
                date = change.created_at.strftime('%Y-%m-%d')

                if date not in coordinates_per_day:
                    coordinates_per_day[date] = []

                coordinates_per_day[date].append(Point(change.lat, change.long))

            continue


    return coordinates_per_day

def get_coordinates_for_user_count(user_disply_name: str) -> dict[Point, int]:
    counted_points = {}
    coordinates = get_coordinates_for_user_by_day(user_display_name=user_disply_name)

    for day in coordinates:
        for point in coordinates[day]:
            if point in counted_points:
                counted_points[point] += 1
            else:
                counted_points[point] = 1

    return counted_points