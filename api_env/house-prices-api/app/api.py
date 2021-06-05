#Este es el código central de nuestra API
#Aquí definimos los endpoints o puntos donde podemos recibir peticiones.
#FastAPI estará traduciendo desde y hacia JSON sin que tengamos
#que hacer nada más.


#Cargamos los módulos necesarios
import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger #avanzado
from regression_model import __version__ as model_version #de nuestra librería, la versión
from regression_model.predict import make_prediction #de nuestra librería, la función para hacer predicción

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

#El primer "endpoint", le podemos dar un código
#Seguirá el esquema definido: nombre, versión de la api y del modelo.
#Podremos pedirle a la API que nos de esta información.
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


#El segundo "endpoint" es la propia predicción.
#Este es el objetivo principal de todo nuestro trabajo,
#queremos obtener la predicción del precio de la vivienda dadas unas
#características.
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleHouseDataInputs) -> Any:
    """
    Hace la predicción del precio de las viviendas con el modelo entrenado
    """

    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    # Avanzado: Se puede mejorar el rendimiento de la API reescribiendo
    # la función `make prediction` para que se asíncrona.
    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = make_prediction(input_data=input_df.replace({np.nan: None}))
    
	#Si hay algún error, por ejemplo, los datos de entrada no validan el esquema
	#nos dará un código 400 y nos dirá qué error hemos cometido.
	#Esto es así por la buena integración de FastAPI con Python.
    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")
	#Si no hay errores obtendremos la predicción.
    return results
