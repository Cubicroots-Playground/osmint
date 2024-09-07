from OSMPythonTools.api import Api
import requests
import xml.etree.ElementTree as et

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

def user_from_xml(xml: et.Element):
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

def get_user_info(api: Api,user_id: int):
    response = requests.get(f'https://www.openstreetmap.org/api/0.6/user/{user_id}')
    print(response.text)
    return et.fromstring(response.text)


if __name__ == '__main__':
    api = Api()
    data = get_user_info(api, 461130)
    print(user_from_xml(data))