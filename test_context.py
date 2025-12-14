"""
Script de prueba para visualizar el contexto del dashboard.
Copia y pega este código al FINAL de app.py para ver el estado en tiempo real.
"""

# ============================================
# 🔍 SECCIÓN DE DEBUG - COPIAR A app.py
# ============================================
"""
# =========================
# 🔍 DEBUG: Estado del Dashboard
# =========================
from utils.context import get_dashboard_context

# Mostrar en un expander para no ocupar espacio
with st.expander("🔍 Ver estado actual del dashboard (Debug)", expanded=False):
    context = get_dashboard_context()
    
    st.subheader("📊 Contexto Capturado")
    st.json(context)
    
    # Vista más legible
    st.subheader("📋 Resumen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Región seleccionada", context.get("region", "N/A"))
        st.metric("Medida seleccionada", context.get("medida", "N/A"))
        st.metric("Año filtrado", context.get("filters", {}).get("año", "N/A"))
    
    with col2:
        pred = context.get("inputs", {}).get("prediccion", {})
        st.metric("Predicción - Año", pred.get("año", "N/A"))
        st.metric("Predicción - Mes", pred.get("mes", "N/A"))
        st.metric("Predicción - Región", pred.get("region", "N/A"))
    
    # Resultado de predicción
    resultado = context.get("inputs", {}).get("prediccion", {}).get("resultado")
    if resultado:
        st.success(f"✅ Última predicción: {resultado:.2f}")
    else:
        st.info("ℹ️ No hay predicción realizada aún")
    
    # Ver todo el session_state (útil para debug avanzado)
    if st.checkbox("Ver todo st.session_state (avanzado)"):
        st.write("🔧 session_state completo:")
        st.json(dict(st.session_state))

"""

print("""
╔════════════════════════════════════════════════════════════╗
║  📝 INSTRUCCIONES PARA USAR                                ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  1. Copia el código de arriba (entre las triple quotes)   ║
║  2. Pégalo AL FINAL de app.py (antes del pie de página)   ║
║  3. Ejecuta: streamlit run app.py                         ║
║  4. Abre el expander "🔍 Ver estado actual del dashboard" ║
║  5. Verás el contexto actualizado cada vez que interactúes║
║                                                            ║
║  ✅ Cuando termines de testear, borra esa sección         ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")
