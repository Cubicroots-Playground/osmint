import os
import pickle
from . import ChangeSet

def load_changesets(
        user_display_name: str,
) -> list[ChangeSet]:
    file = open(f".osmint-cache/changesets_{user_display_name}",'rb')
    changesets = pickle.load(file)
    file.close()
    
    return changesets