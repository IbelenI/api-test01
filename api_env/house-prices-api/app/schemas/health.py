#Vamos a dar la opción de poder obtener
#info de la API: versión, versión del modelo y nombre.
#Aquí indicamos el esquema que tendrá el resultado cuando se haga esta petición.

from pydantic import BaseModel

class Health(BaseModel):
    name: str
    api_version: str
    model_version: str
