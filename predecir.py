import joblib
import pandas as pd

class EnergyModel:
    def __init__(self):
        self.modelo =  joblib.load("modelo_ridge.pkl")

    def predict(self, año, mes, mes_pasado, region):
        base_year = 2012
        time_idx = (año - base_year) * 12 + mes


        regio = {
            "este": [1, 0, 0],
            "norte": [0, 1, 0],
            "sur": [0, 0, 1]
        }

        este, norte, sur = regio.get(region.lower(), [0, 0, 0])

        fila = pd.DataFrame([{
            "mes": mes,
            "time_idx": time_idx,
            "mes_pasado": mes_pasado,
            "este": este,
            "norte": norte,
            "sur": sur
        }])

        pred = self.modelo .predict(fila)[0]
        return pred


model = EnergyModel()
print(model.predict(
    año=2025,
    mes=1,
    mes_pasado= 398.123055,
    region="sur")
)