from flask import Flask, request, jsonify
from flask_api import status
from flask_cors import CORS
from podio_auth import *
from user_manager import *
from dotenv import load_dotenv
import subprocess
import ast
load_dotenv()

app = Flask(__name__)  # create the Flask app
# app.config['FLASK_ENV'] = 'development'
app.config.from_envvar('ENV_FILE_LOCATION')
CORS(app)


@app.route('/', methods=['GET'])
def item_exists():

    req_data = request.get_json()

    return jsonify(item_exists_by_filter(podio_client_expedientes, int(
        os.getenv("PODIO_EXPEDIENTES_APP_ID")), req_data))


@app.route('/inasistencias-new-item', methods=['POST'])
def new_inasistencias():
    
    if request.form["motivo-comentarios"] == "":
        fields = {
            "periodo-de-inasistencia": {"start": request.form["fecha-inicio"] + " 00:00:00", "end": request.form["fecha-fin"] + " 00:00:00"},
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": request.form["numero-de-empleado"]}),
            "numero-de-dias": request.form["numero-de-dias"]
        }
        
    else: 
        fields = {
            "periodo-de-inasistencia": {"start": request.form["fecha-inicio"] + " 00:00:00", "end": request.form["fecha-fin"] + " 00:00:00"},
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": request.form["numero-de-empleado"]}),
            "numero-de-dias": request.form["numero-de-dias"],
            "motivo-comentarios": request.form["motivo-comentarios"]
        }

    resp = find_item_by_filter(podio_client_expedientes, int(
        os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"codigo-de-solicitudes": request.form["codigo-de-solicitudes"]})

    employee = {}
    employee["numero-de-empleado"] = 0

    if resp['filtered'] > 0:
        employee = get_all_item_fields(resp['items'][0]['fields'])

    if employee["numero-de-empleado"] == request.form["numero-de-empleado"]:

        resp = create_item(podio_client_inasistencias, int(
            os.getenv("PODIO_INASISTENCIAS_APP_ID")), fields)

        working_dict = os.getcwd()
        # upload to flask app

        if request.files.get('my-file', None):
            if request.method == 'POST':
                file = request.files['my-file']
                file_name = file.filename.replace(" ", "")
                new_file_path = working_dict + '/uploadfile/' + file_name
                file.save(new_file_path)

            if os.path.isfile(new_file_path):
                proc = subprocess.Popen(
                    "php {}/uploadfile/index.php {} {} {}".format(
                        working_dict, new_file_path, file_name, resp["item_id"]
                    ),
                    shell=True, stdout=subprocess.PIPE)

            file_load_resp = proc.stdout.read()

            os.remove(new_file_path)
            return file_load_resp

        else:
            return resp
    else:
        return {
            'msg': 'El codigo de solicitudes no coincide'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/home-office-new-item', methods=['POST'])
def new_home_office():

    req_data = request.get_json()

    
    
    if req_data["comentarios"] == "":
        fields = {
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": req_data["numero-de-empleado"]}),
            "dia": {"start": req_data["fecha"] + " 09:12:22"}
        }

    else:
        fields = {
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": req_data["numero-de-empleado"]}),
            "dia": {"start": req_data["fecha"] + " 09:12:22"},
            "comentarios": req_data["comentarios"]
        }
        
    resp = find_item_by_filter(podio_client_expedientes, int(
        os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"codigo-de-solicitudes": req_data["codigo-de-solicitudes"]})

    employee = {}
    employee["numero-de-empleado"] = 0

    if resp['filtered'] > 0:
        employee = get_all_item_fields(resp['items'][0]['fields'])

    if employee["numero-de-empleado"] == req_data["numero-de-empleado"]:

        resp = create_item(podio_client_home_office, int(
            os.getenv("PODIO_HOME_OFFICE_APP_ID")), fields)

        return resp

    else:
        return {
            'msg': 'El codigo de solicitudes no coincide'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/vacaciones-new-item', methods=['POST'])
def new_vacaciones():

    req_data = request.get_json()

    
    
    if req_data["comentarios"] == "":
        fields = {
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": req_data["numero-de-empleado"]}),
            "dias-por-gozar": req_data["numero-de-dias"],
            "rango-de-fechas": {"start": req_data["fecha-inicio"] + " 00:00:00", "end": req_data["fecha-fin"] + " 00:00:00"}
        }
        
    else:
        fields = {
            "colaborador": get_item_id(podio_client_expedientes, int(
                os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"numero-de-empleado": req_data["numero-de-empleado"]}),
            "dias-por-gozar": req_data["numero-de-dias"],
            "rango-de-fechas": {"start": req_data["fecha-inicio"] + " 00:00:00", "end": req_data["fecha-fin"] + " 00:00:00"},
            "comentarios": req_data["comentarios"]
        }

    resp = find_item_by_filter(podio_client_expedientes, int(
        os.getenv("PODIO_EXPEDIENTES_APP_ID")), {"codigo-de-solicitudes": req_data["codigo-de-solicitudes"]})

    employee = {}
    employee["numero-de-empleado"] = 0

    if resp['filtered'] > 0:
        employee = get_all_item_fields(resp['items'][0]['fields'])

    if employee["numero-de-empleado"] == req_data["numero-de-empleado"]:

        resp = create_item(podio_client_vacaciones, int(
            os.getenv("PODIO_VACACIONES_APP_ID")), fields)
        return resp

    else:
        return {
            'msg': 'El codigo de solicitudes no coincide'
        }, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/org-chart', methods=['GET'])
def org_chart_construct():

    item = podio_client_configuracion.Item.find(1500878952)

    item_fields = get_all_item_fields(item['fields'])

    podio_dict = ast.literal_eval(item_fields['valor'])

    items_list = podio_dict['datos']

    children = list(
        filter(lambda x: x['title'] != 'Director General', items_list))

    main = list(filter(lambda x: x['title'] == "Director General", items_list))

    main = main[0]

    def get_children(child_list):
        for element in child_list:
            for child in children:
                if element['id'] == child['id']:
                    if 'children' in child:
                        element['children'] = child['children']
                        get_children(element['children'])
                    else:
                        continue

    get_children(main['children'])

    return jsonify(main)


if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
