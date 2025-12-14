import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import plotly.express as px
from datos_por_agno import provincias_por_region
from datos_por_agno import resumen_consumo_por_agno, resumen_consumo_por_region
from predecir import EnergyModel



# para AI y context tracking
from utils.context import get_dashboard_context
from agent_backend.agent import setup_vector_store_and_model, update_agent_context
from langchain_core.messages import HumanMessage, AIMessage


# =========================
# Título
# =========================
st.markdown("""
<h1 style='font-size:32px; color:#1f77b4; text-align:center;'>
PowerSense RD: Tendencias de consumo eléctrico entre distribuidoras en República Dominicana
para optimizar operaciones empresariales
</h1>
""", unsafe_allow_html=True)

region = st.selectbox(
    "Selecciona una región:",
    ["Norte", "Sur", "Este"],
    key="region"
)
st.write(f"Has seleccionado la región: {region}")

medida = st.radio(
    "Selecciona una medida:",
    ["Energia", "Potencia"],
    horizontal=True,
    key="medida"
)
st.write(f"Medida seleccionada: {medida}")

# =========================
# Dataframe
# =========================
df_regiones_meses, df_regiones_clientes = resumen_consumo_por_region(region)
st.subheader(f"Consumo promedio por mes y tipo de cliente en la región {region}")


# st.subheader("Datos")
# st.dataframe(df, use_container_width=True)

# =========================
# Gráficos lado a lado
# =========================


fig_bar = px.bar(df_regiones_meses, x="Mes", y=medida, color="Mes",
                    text=medida, color_discrete_sequence=px.colors.qualitative.Vivid)
fig_bar.update_layout(
    xaxis_title="Mes",
    yaxis_title=medida,
    title="Gráfico de Barras",
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig_bar, use_container_width=True)

fig_pie = px.pie(df_regiones_clientes, names="Cliente", values=medida, color="Cliente",
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
agno = st.slider("Selecciona un año", 2012, 2024, 2024, 1, key="agno")
st.write(f"Año seleccionado: {agno}")

# =========================
# Mapa de RD con datos por región
# =========================
st.subheader(f"Mapa de consumo de {medida} por región")

valores_por_region = resumen_consumo_por_agno(agno).set_index("region")[medida].to_dict()

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
    if region == "Norte":
        return "#FFA500"  # naranja
    elif region == "Este":
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
        tooltip=f"{region}: {valores_por_region[region]:.2f}" if region else provincia
    ).add_to(m)

st_folium(m, width=900, height=500)

# =========================
# Predicción de consumo
# =========================
model = EnergyModel()
st.markdown("<h2 style='color:#1f77b4;'>Predicción de consumo</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    input_anio = st.number_input("Año", min_value=2000, max_value=2100, value=2025, step=1, key="pred_año")
    input_mes = st.number_input("Mes", min_value=1, max_value=12, value=1, step=1, key="pred_mes")

with col2:
    input_mes_pasado = st.number_input("Consumo del mes pasado", min_value=0.0, value=398.123055, key="pred_mes_pasado")
    input_region = st.selectbox("Región", ["Norte", "Sur", "Este"], key="pred_region")

if st.button("Predecir consumo"):
    try:
        prediccion = model.predict(
            año=input_anio,
            mes=input_mes,
            mes_pasado=input_mes_pasado,
            region=input_region.lower()
        )
        
        # Guardar resultado en session_state para context tracking
        st.session_state.pred_result = prediccion
        
        st.success(f"Predicción de consumo estimada: **{prediccion:.2f}**")

    except Exception as e:
        st.error(f"Error al predecir: {e}")


# =========================
# 🔍 DEBUG: Estado del Dashboard
# =========================


# Mostrar en un expander para no ocupar espacio

# =========================
# 🔍 DEBUG: Estado del Dashboard
# =========================
try:
    agent = setup_vector_store_and_model()
except Exception as e:
    st.error(f"Error al configurar el agente: {e}")
    st.stop()

# =========================
# CHATBOT EN SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## 💬 Asistente PowerSenseAI")
    st.markdown("---")
    
    # Inicializar mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Contenedor con scroll para historial
    chat_container = st.container()
    
    with chat_container:
        # Mostrar historial de mensajes (más antiguos arriba, más recientes abajo)
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                continue
            
            with st.chat_message(role):
                st.markdown(message.content)
    
    # Input del usuario al final (siempre visible)
    if prompt := st.chat_input("Pregunta sobre leyes o datos del dashboard..."):
        # Agregar mensaje del usuario
        st.session_state.messages.append(HumanMessage(content=prompt))
        
        # Actualizar contexto
        context = get_dashboard_context()
        update_agent_context(context)

        # Procesar respuesta del agente
        with st.spinner("Analizando..."):
            try:
                history_window = st.session_state.messages[-3:]
                response = agent.invoke({"messages": history_window})
                
                # Filtrar mensajes: separar razonamiento de respuesta final
                final_response = None
                reasoning_json = None
                
                for m in response["messages"]:
                    if isinstance(m, AIMessage):
                        if '"veredicto"' in m.content:
                            reasoning_json = m.content
                        elif not (hasattr(m, "tool_calls") and m.tool_calls):
                            final_response = m.content
                
                # Guardar respuesta final
                if final_response:
                    st.session_state.messages.append(AIMessage(content=final_response))
                    # Rerun para mostrar el mensaje en el historial
                    st.rerun()
                else:
                    st.warning("⚠️ No se generó una respuesta válida.")
                
                # Mostrar razonamiento en expander (solo si hay)
                if reasoning_json:
                    with st.expander("🧠 Ver razonamiento"):
                        st.code(reasoning_json, language="json")
                
            except Exception as e:
                st.error(f"Error: {e}")
                import traceback
                st.code(traceback.format_exc())
    
    # Debug expandible al final del sidebar
    st.markdown("---")
    with st.expander("🔍 Debug Estado"):
        st.json(get_dashboard_context())

# =========================
# Pie de página
# =========================
st.markdown("""
<hr style="margin-top:50px; border: none; height: 2px; background-color: #1f77b4;">

<div style='text-align:center; color:gray; font-size:14px;'>
Desarrollado con ⚡ por <span style='color:#1f77b4; font-weight:bold;'>SenpAI 先輩</span><br>
<em>Samsung Innovation Campus</em>
</div>
""", unsafe_allow_html=True)