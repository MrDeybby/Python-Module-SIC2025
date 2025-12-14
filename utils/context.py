import streamlit as st
from typing import Dict, Any

def get_dashboard_context() -> Dict[str, Any]:
    """
    Build a clean snapshot of the dashboard state from st.session_state.
    Safely .get()s commonly used keys based on the current app:
      - Región seleccionada (selectbox)
      - Medida seleccionada (radio)
      - Filtro de año (slider) y posible mes
      - Inputs numéricos y parámetros para predicción
      - Vista actual (tabs/menú lateral si existen)
    """

    ss = st.session_state

    def _coalesce(*keys):
        for k in keys:
            if k in ss and ss.get(k) is not None:
                return ss.get(k)
        return None

    def _clean(obj):
        if isinstance(obj, dict):
            cleaned = {k: _clean(v) for k, v in obj.items() if v is not None}
            return {k: v for k, v in cleaned.items() if not (isinstance(v, dict) and len(v) == 0)}
        return obj

    context = {
        "region": _coalesce(
            "region",                      # explicit key (recommended)
            "region_select",               # alternative explicit key
            "Selecciona una región:"       # auto key if Streamlit used label as key
        ),
        "medida": _coalesce(
            "medida",
            "measure",
            "Selecciona una medida:"
        ),
        "filters": {
            "año": _coalesce(
                "agno",
                "year",
                "Selecciona un año"
            ),
            "mes": _coalesce(
                "mes",
                "month",
                "Selecciona un mes"
            ),
        },
        "inputs": {
            # Historical/last-month energy used in predictions
            "mes_pasado": _coalesce(
                "mes_pasado",
                "pred_mes_pasado"
            ),
            # Free numeric inputs you may add (e.g., manual consumo)
            "consumo_manual": _coalesce(
                "consumo",
                "consumo_input"
            ),
            # Prediction parameters (common keys)
            "prediccion": {
                "año": _coalesce("pred_año", "pred_year"),
                "mes": _coalesce("pred_mes", "pred_month"),
                "region": _coalesce("pred_region"),
                "resultado": _coalesce("pred_result", "prediction_result"),
            },
        },
        "view": {
            # Track current tab/menu if present
            "tab": _coalesce("active_tab", "current_tab"),
            "menu": _coalesce("active_menu", "sidebar_selection"),
        },
    }

    return _clean(context)