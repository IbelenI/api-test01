#Todo lo que tiene que ver con testar y mantener
#el modelo una vez publicado queda fuera del
#alcance de las sesiones. 

import math

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient


def test_make_prediction(client: TestClient, test_data: pd.DataFrame) -> None:
    # Dado
    payload = {
        # se asegura que pydantic va bien con np.nan
        "inputs": test_data.replace({np.nan: None}).to_dict(orient="records")
    }

    # Cuando
    response = client.post(
        "http://localhost:8001/api/v1/predict",
        json=payload,
    )

    # Entonces
    assert response.status_code == 200
    prediction_data = response.json()
    assert prediction_data["predictions"]
    assert prediction_data["errors"] is None
    assert math.isclose(prediction_data["predictions"][0], 113422, rel_tol=100)
