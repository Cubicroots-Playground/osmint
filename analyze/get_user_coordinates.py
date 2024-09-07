import osm

def get_coordinates_for_user(user_display_name: str) -> dict:
    coordinates_per_day = {}

    change_sets = osm.get_changesets(user_display_name)
    for change_set in change_sets:
        date = change_set.created_at.strftime('%Y-%m-%d')

        if change_set.area.size() != 0.0:
            # TODO get changeset content for coordinates
            continue

        if date not in coordinates_per_day:
            coordinates_per_day[date] = []

        coordinates_per_day[date].append({change_set.area.min_lat, change_set.area.min_long})

    return coordinates_per_day
