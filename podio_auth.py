import os
from pypodio2 import api
from dotenv import load_dotenv
load_dotenv()
# Authenticate as App in podio, variables below contains a client object that
# allow us to do all the diferent requests to Podio API


#Client to do requests to "" app
podio_client_expedientes = api.OAuthAppClient(
    client_id=os.getenv("PODIO_CLIENT_ID"),
    client_secret=os.getenv("PODIO_CLIENT_SECRET"),
    app_id=os.getenv("PODIO_EXPEDIENTES_APP_ID"),
    app_token=os.getenv("PODIO_EXPEDIENTES_APP_TOKEN"),
)


#Client to do requests to "inasistencias" app
podio_client_inasistencias = api.OAuthAppClient(
    client_id=os.getenv("PODIO_CLIENT_ID"),
    client_secret=os.getenv("PODIO_CLIENT_SECRET"),
    app_id=os.getenv("PODIO_INASISTENCIAS_APP_ID"),
    app_token=os.getenv("PODIO_INASISTENCIAS_APP_TOKEN"),
)


#Client to do requests to "vacaciones" app
podio_client_vacaciones = api.OAuthAppClient(
    client_id=os.getenv("PODIO_CLIENT_ID"),
    client_secret=os.getenv("PODIO_CLIENT_SECRET"),
    app_id=os.getenv("PODIO_VACACIONES_APP_ID"),
    app_token=os.getenv("PODIO_VACACIONES_APP_TOKEN"),
)


#Client to do requests to "home_office" app
podio_client_home_office = api.OAuthAppClient(
    client_id=os.getenv("PODIO_CLIENT_ID"),
    client_secret=os.getenv("PODIO_CLIENT_SECRET"),
    app_id=os.getenv("PODIO_HOME_OFFICE_APP_ID"),
    app_token=os.getenv("PODIO_HOME_OFFICE_APP_TOKEN"),
)




#Client to do requests to "configuracion" app
podio_client_configuracion = api.OAuthAppClient(
    client_id=os.getenv("PODIO_CLIENT_ID"),
    client_secret=os.getenv("PODIO_CLIENT_SECRET"),
    app_id=os.getenv("PODIO_CONFIGURACION_APP_ID"),
    app_token=os.getenv("PODIO_CONFIGURACION_APP_TOKEN"),
)