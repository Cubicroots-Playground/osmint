import osm

def get_coordinates_for_user(user_display_name: str) -> dict:
    coordinates_per_day = {}

    change_sets = osm.get_changesets(user_display_name)
    for change_set in change_sets:
        if change_set.area.size() == 0.0:
            # Change set is single point, add it.
            date = change_set.created_at.strftime('%Y-%m-%d')

            if date not in coordinates_per_day:
                coordinates_per_day[date] = []

            coordinates_per_day[date].append({change_set.area.min_lat, change_set.area.min_long})

        else:
            # Change set is area, get single node points contained in it.
            changes = osm.get_changes(change_set.id)
            for change in changes:
                date = change.created_at.strftime('%Y-%m-%d')

                if date not in coordinates_per_day:
                    coordinates_per_day[date] = []

                coordinates_per_day[date].append({change.lat, change.long})

            continue


    return coordinates_per_day
