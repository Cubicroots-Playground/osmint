import requests
import xml.etree.ElementTree as et
import json

class User:
    def __init__(
        self,
        id: int,
        display_name: str,
        img_url: str,
        changeset_count: int,
    ):
        self.id = id
        self.display_name = display_name
        self.img_url = img_url
        self.changeset_count = changeset_count

    def __str__(self):
        return json.dumps({'id': self.id, 'display_name': self.display_name, 'img_url': self.img_url, 'changeset_count': self.changeset_count})


def user_from_xml(xml: et.Element) -> User:
    attrs = {
        'img_url': None
    }

    for child in xml:
        if child.tag == 'user':
            attrs['id'] = child.attrib['id']
            attrs['display_name'] = child.attrib['display_name']
            
            for c in child:
                if c.tag == 'img':
                    attrs['img_url'] = c.attrib['href']
                elif c.tag == 'changesets':
                    attrs['changeset_count'] = c.attrib['count']

            break

    return User(attrs['id'], attrs['display_name'], attrs['img_url'], attrs['changeset_count'])

def get_user_info(user_id: int):
    response = requests.get(f'https://www.openstreetmap.org/api/0.6/user/{user_id}')
    return et.fromstring(response.text)
