import os
import pickle
from . import get_changes, get_changesets
from rich.console import Console

def store_changesets(
        console: Console,
        user_display_name: str, 
        changesets_limit: int = 100):
    try:
        os.mkdir(".osmint-cache")
    except FileExistsError:
        pass
    
    changesets = get_changesets(user_display_name=user_display_name, limit=changesets_limit)

    console.log(f"Downloaded {len(changesets)} changesets.")

    for changeset in changesets:
        changes = get_changes(change_set_id=changeset.id)
        changeset.changes = changes

    _write_to_file(changesets, f".osmint-cache/changesets_{user_display_name}")

def _write_to_file(obj: any, filename: str):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file, pickle.HIGHEST_PROTOCOL)