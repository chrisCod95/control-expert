from flask import jsonify
import os
# from podio_auth import *
from dotenv import load_dotenv
load_dotenv()


def get_field_index(field, f_list):
    # Here we check on wich list index we have the field
    fields_list = f_list
    list_limit = len(fields_list)
    i = 0
    while i < list_limit:
        if fields_list[i]['label'] == field:
            index = i

        i += 1

    return index



def find_item_by_filter(client, app_id, filters):
    resp = client.Item.filter(
        app_id=app_id, attributes={
            'filters': filters})

    return resp


def create_item(client, app_id, fields):
    resp = client.Item.create(
        app_id=app_id, attributes={
            "fields": fields})

    return resp


def update_item(client, item_id, fields):
    resp = client.Item.update(
        item_id, attributes={
            "fields": fields})

    return resp


def delete_item(client, item_id):
    resp = client.Item.delete(item_id)

    return resp


def get_user_mipyme_id(email):
    resp = podio_client_users.Item.filter(app_id=int(os.getenv("PODIO_USERS_APP_ID")),
                                          attributes={
        'limit': 1,
        'filters': {"email": ['values', 'value', email]}})

    fields_data = resp['items'][0]['fields']

    # Here we check on wich index we have the MiPyme ID field
    index_of_MipymeID = get_field_index("MiPyme", fields_data)

    # And then get miPymeID

    mipymeID = fields_data[index_of_MipymeID]['values'][0]['value']['item_id']

    return mipymeID


def get_item_id(client, app_id, filters):
    # try:
      resp = client.Item.filter(
          app_id=app_id, attributes={
              'limit': 1,
              'filters': filters})

      return resp['items'][0]['item_id']
    # except:
    #     return False


def item_exists(client, item_id):
    try:
        resp = client.Item.find(item_id)

        return True
    except:
        return False
    
def item_exists_by_filter(client, app_id, filters):
    try:
        resp = client.Item.filter(
            app_id=app_id, attributes={
                'filters': filters})
        
        if resp["filtered"] == 0:
            return False
        else: 
            return True
    except:
        return """ERROR"""
    


def create_file(client, filename):
    resp = client.Files.create(
        attributes={
            'filename': filename,
            'source': 'demo.docx'
        }
    )
    return resp


def get_all_mipyme_items(current_user, client, app_id):
    # Getting the MiPyME item id:
    mipymeID = get_user_mipyme_id(current_user)
    ########################################################################

    filters = {
        'mipyme': mipymeID
    }
    resp = find_item_by_filter(
        client, app_id, filters)

    items_list = resp['items']
    items_limit = len(items_list)
    i = 0

    ejecutivos = [None] * items_limit

    while i < items_limit:

        fields_list = items_list[i]['fields']
        fields_limit = len(fields_list)
        j = 0

        while j < (fields_limit):
            if j == 0:
                ejecutivos[i] = {
                    fields_list[j]['external_id']: fields_list[j]['values'][0]['value']
                }

            ejecutivos[i].update(
                {fields_list[j]['external_id']: fields_list[j]['values'][0]['value']})

            j += 1

        ejecutivos[i]['mipyme'] = ejecutivos[i]['mipyme']['title']

        ejecutivos[i].update(
            {"item_id": items_list[i]['item_id']}
        )

        i += 1

    return jsonify(ejecutivos)


###############################################################
#################### ABE #########################
###################################################################

def filter_all_items_from_app(client, app_id, filter_dict):
    resp = client.Item.filter(
        app_id=app_id,
        attributes={'filters': filter_dict}
    )

    items_list = resp['items']
    all_items_fields_list = []

    for item in items_list:
        all_items_fields_list.append(item['fields'])

    items_list.clear()

    for fields_list in all_items_fields_list:
        podio_fields = {}

        for field in fields_list:

            if field["type"] == "email":
                podio_fields.update({field["label"]: field["values"]})
            elif field["type"] == "category":
                podio_fields.update(
                    {field["label"]: field["values"][0]['value']['text']})
            elif field["type"] == "category":
                podio_fields.update(
                    {field["label"]: field["values"][0]["value"]["id"]})
            elif field["type"] == "app":
                podio_fields.update(
                    {field["label"]: field["values"][0]["value"]["item_id"]})
            elif field["external_id"] == "introduccion" or field["external_id"] == "informacion-adicional" or field["external_id"] == "bombas-hp" or field["external_id"] == "descripcion":
                podio_fields.update(
                    {field["label"]: BeautifulSoup(field["values"][0]["value"]).text})
            # elif field["type"] == "money":
            #     podio_fields.update(
            #         {field["label"]: "${:,.2f}".format(float(field["values"][0]["value"]), grouping=True)})
            elif field["type"] == "number":
                podio_fields.update(
                    {field["label"]: str(int(float(field["values"][0]["value"])))})
            else:
                podio_fields.update(
                    {field["label"]: field["values"][0]["value"]})

        items_list.append(podio_fields)

    return items_list


def get_all_item_fields(fields_list):
    podio_fields = {}
    index = 0
    relations = []

    for field in fields_list:
        if field["type"] == "email":
            podio_fields.update({field["external_id"]: field["values"]})
        elif field["type"] == "category":
            podio_fields.update(
                {field["external_id"]: field["values"][0]['value']['text']})
        elif field["type"] == "date":
            podio_fields.update(
                {field["external_id"]: field["values"][0]["start_date"]})
        elif field["type"] == "app":
            podio_fields.update(
                {field["external_id"]: {"item_id": field["values"][0]["value"]["item_id"], "title": field["values"][0]["value"]["title"]}})

            # while index < len(field["values"]):
            #     relations.append({"item_id": field["values"][0]["value"]["item_id"], "title": field["values"][0]["value"]["title"]})
            #     index += 1
        elif field["external_id"] == "introduccion" or field["external_id"] == "informacion-adicional":
            podio_fields.update(
                {field["external_id"]: BeautifulSoup(field["values"][0]["value"]).text})

        else:
            podio_fields.update(
                {field["external_id"]: field["values"][0]["value"]})

    return podio_fields
