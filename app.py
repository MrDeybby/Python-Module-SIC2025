import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la app
st.title("Gráficos en Streamlit")

# Datos de ejemplo
data = {
    "Categoría": ["A", "B", "C", "D"],
    "Valores": [10, 20, 30, 40]
}

df = pd.DataFrame(data)

st.subheader("Datos")
st.dataframe(df)
st.subheader("Gráfico de Barras")

fig_bar, ax = plt.subplots()
ax.bar(df["Categoría"], df["Valores"], color='skyblue')
ax.set_xlabel("Categoría")
ax.set_ylabel("Valores")
ax.set_title("Gráfico de Barras")
st.pyplot(fig_bar)

st.subheader("Gráfico de Pastel")

fig_pie, ax = plt.subplots()
ax.pie(df["Valores"], labels=df["Categoría"], autopct="%1.1f%%", startangle=90)
ax.set_title("Gráfico de Pastel")
st.pyplot(fig_pie)

st.title("Ejemplo de Slider")

# Slider que va de 0 a 100 con valor inicial 50
valor_decimal = st.slider("Selecciona un valor decimal", 0.0, 10.0, 5.0, 0.1)
st.write("Valor decimal seleccionado:", valor_decimal)

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

st.title("Mapa de República Dominicana con Datos por Región")

# Datos de ejemplo: provincias y valores
data = {
    "Provincia": ["DISTRITO NACIONAL", "SANTIAGO", "LA VEGA", "SAN CRISTÓBAL"],
    "Valor": [50, 70, 30, 90]
    
}
df = pd.DataFrame(data)
provincias_por_region = {
    "CIBAO": [
        "MONTE CRISTI",
        "PUERTO PLATA",
        "SANTIAGO",
        "VALVERDE",
        "SANTIAGO RODRÍGUEZ",
        "LA VEGA",
        "ESPAILLAT",
        "HERMANAS MIRABAL",
        "DAJABÓN",
        "DUARTE",
        "MARÍA TRINIDAD SÁNCHEZ",
        "SAMANÁ",
    ],
    "SUR": [
        "SAN JUAN",
        "AZUA",
        "BARAHONA",
        "PEDERNALES",
        "INDEPENDENCIA",
        "BAORUCO",
        "SAN CRISTÓBAL",
        "PERAVIA",
        "MONSEÑOR NOUEL",
        "ELÍAS PIÑA",
        "SAN JOSÉ DE OCOA"
    ],
    "ESTE": [
        "LA ALTAGRACIA",
        "LA ROMANA",
        "SAN PEDRO DE MACORÍS",
        "SANCHEZ RAMÍREZ",
        "EL SEIBO",
       "SANTO DOMINGO",
        "DISTRITO NACIONAL",
        "MONTE PLATA",
        "HATO MAYOR",
    ]
}

st.dataframe(df)

# Cargar GeoJSON
with open("C:\\Users\\Isaac\\Downloads\\provinces_municipality_summary.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Crear mapa centrado en RD
m = folium.Map(location=[18.7357, -70.1627], zoom_start=7)

# Función para obtener color según valor
def get_color(region):
    if region == "CIBAO":
        return "orange"
    elif region == "ESTE":
        return "green"
    else:
        return "red"


for feature in geojson_data["features"]:
    provincia = feature["properties"]["province_name"]
    print(provincia)
    region = None
    for r, provincias in provincias_por_region.items():
        if provincia in provincias:
            region = r
            break
    
    if region is None:
        color = "gray"
    else:
        color = get_color(region)

    
    # valor = df_regiones[df_regiones["Provincia"] == provincia]["Valor"].values
    # if len(valor) > 0:
    #     color = get_color(valor[0])
    # else:
    #     color = "gray"
    
    folium.GeoJson(
        feature,
        style_function=lambda x, color=color: {
            "fillColor": color, "color": "black", "weight": 1, "fillOpacity": 0.6
        },
        tooltip=f"{provincia}"
    ).add_to(m)


st_folium(m, width=700, height=500)
