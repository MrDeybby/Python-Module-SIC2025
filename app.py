import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import plotly.express as px
from datos_por_agno import provincias_por_region

# =========================
# Título de la App
# =========================
st.markdown("""
<h1 style='font-size:32px; color:#1f77b4; text-align:center;'>
Tendencias de consumo eléctrico entre distribuidoras en República Dominicana
para optimizar operaciones empresariales
</h1>
""", unsafe_allow_html=True)

# =========================
# Datos de ejemplo
# =========================
data = {
    "Categoría": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
    "Valores": [10, 20, 30, 40, 10, 20, 30, 40, 10, 20, 30, 40]
}
df = pd.DataFrame(data)

# st.subheader("Datos")
# st.dataframe(df, use_container_width=True)

# =========================
# Gráficos lado a lado
# =========================
# st.subheader("Visualizaciones Interactivas")
col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(df, x="Categoría", y="Valores", color="Categoría",
                     text="Valores", color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_bar.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Valores",
        title="Gráfico de Barras",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(df, names="Categoría", values="Valores", color="Categoría",
                     color_discrete_sequence=px.colors.qualitative.Vivid, hole=0.3)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        title="Gráfico de Pastel",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# =========================
# Slider seleccion de agno
# =========================
valor_decimal = st.slider("Selecciona un año", 2012, 2024, 2024, 1)
st.write(f"Año seleccionado: {valor_decimal}")

# =========================
# Mapa de RD con datos por región
# =========================
# st.subheader("Mapa de República Dominicana")

valores_por_region = {"CIBAO": 250, "ESTE": 180, "SUR": 120}

# Cargar GeoJSON
with open("provinces_municipality_summary.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)


# Crear mapa con límites estrictos
m = folium.Map(
    location=[18.7357, -69.6],
    zoom_start=8,
    width=900,
    height=500,
    max_bounds=True,
    min_zoom=7 
)

# Función para obtener color según valor
def get_color(region):
    if region == "CIBAO":
        return "#FFA500"  # naranja
    elif region == "ESTE":
        return "#00C853"  # verde
    else:
        return "#D50000"  # rojo

for feature in geojson_data["features"]:
    provincia = feature["properties"]["province_name"]
    region = None
    for r, provincias in provincias_por_region.items():
        if provincia in provincias:
            region = r
            break
    
    color = get_color(region) if region else "#BDBDBD"  # gris si no tiene región
    
    folium.GeoJson(
        feature,
        style_function=lambda x, color=color: {
            "fillColor": color, "color": "black", "weight": 1, "fillOpacity": 0.6
        },
        tooltip=f"{provincia}: {valores_por_region[region]:.2f}" if region else provincia
    ).add_to(m)

st_folium(m, width=900, height=500)

