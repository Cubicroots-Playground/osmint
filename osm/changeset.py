import requests
import xml.etree.ElementTree as et
import json
import datetime
from typing import Optional
import urllib.parse

# Area defines a rectangle.
class Area:
    def __init__(
            self,
            min_lat: float,
            max_lat: float,
            min_long: float,
            max_long: float,
    ):
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_long = min_long
        self.max_long = max_long

    def size(self) -> float:
        return (self.max_lat-self.min_lat)*(self.max_long-self.min_long)

# Change defines a change according to the OSM API.
class Change:
    def __init__(
            self,
            id: int,
            created_at: datetime.datetime,
            lat: float,
            long: float,
    ):
        self.id = id
        self.created_at = created_at
        self.lat = lat
        self.long = long

# ChangeSet defines a changeset according to the OSM API.
class ChangeSet:
    def __init__(
        self,
        id: int,
        created_at: datetime.datetime,
        area: Area,
        changes: list[Change]=None,
    ):
        self.id = id
        self.created_at = created_at
        self.area = area
        self.changes = changes

def _changesets_from_xml(xml: et.Element) -> list[ChangeSet]:
    sets = []

    for child in xml:
        if 'min_lat' in child.attrib:
            sets.append(ChangeSet(
            child.attrib['id'],
            datetime.datetime.strptime(child.attrib['created_at'], '%Y-%m-%dT%H:%M:%S%z'),
            Area(
                float(child.attrib['min_lat']),
                float(child.attrib['max_lat']),
                float(child.attrib['min_lon']),
                float(child.attrib['max_lon']),
            )
            ))        

    return sets

def _get_changesets(user_display_name: str, created_before: Optional[datetime.datetime] = None, limit: int = 100) -> et.Element:
    url =  f'https://www.openstreetmap.org/api/0.6/changesets/?display_name={urllib.parse.quote(user_display_name)}&limit={limit}'
    if created_before:
        # First time is "closed after" time.
        url += '&time=2001-01-01,' + urllib.parse.quote(created_before.isoformat())

    response = requests.get(
       url
        )
    return et.fromstring(response.text)

def _changes_from_xml(xml: et.Element) -> list[Change]:
    changes = []

    for create_node in xml:
        for child in create_node:
            if 'lon' in child.attrib:
                changes.append(Change(
                    int(child.attrib['id']),
                    datetime.datetime.strptime(child.attrib['timestamp'], '%Y-%m-%dT%H:%M:%S%z'),
                    float(child.attrib['lat']),
                    float(child.attrib['lon']),
                ))

    return changes


def _get_changeset_content(change_set_id: int) -> et.Element:
    url =  f'https://www.openstreetmap.org/api/0.6/changeset/{change_set_id}/download'

    response = requests.get(
       url
        )
    return et.fromstring(response.text)

def get_changesets(user_display_name: str, created_before: Optional[datetime.datetime] = None, limit: int = 100) -> list[ChangeSet]:
    xml = _get_changesets(user_display_name, created_before=created_before, limit=limit)
    return _changesets_from_xml(xml)

def get_changes(change_set_id: int) -> list[Change]:
    xml = _get_changeset_content(change_set_id)
    return _changes_from_xml(xml)