<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white&color=blue" />
    <img src="https://img.shields.io/github/contributors/MrDeybby/Python-Module-SIC2025"/>
    <img src="https://img.shields.io/github/last-commit/MrDeybby/Python-Module-SIC2025"/>
  </a>
</p>
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=github,py,vscode" />
  </a>
</p>

# SenpAI 先輩: PowerSense AI RD

> **Evolución del proyecto para el Samsung Innovation Campus 2025 (Módulo de IA).**
> De la visualización de datos a la auditoría inteligente de cumplimiento.

## Descripción General

**PowerSense AI RD** es una plataforma avanzada de análisis para el sector eléctrico de la República Dominicana. Evolucionando más allá de un dashboard tradicional, este sistema integra Inteligencia Artificial para no solo visualizar *qué* está pasando con el consumo eléctrico, sino entender *por qué*, bajo la lupa del marco regulatorio nacional.

La aplicación combina el análisis cuantitativo de datos históricos (CSV) con el razonamiento cualitativo basado en las normativas de la Superintendencia de Electricidad (SIE) y leyes vigentes.

---

## Presentando a: Ohmni

**El Auditor de Cumplimiento Técnico-Comercial**

El corazón de la nueva etapa de PowerSense es **Ohmni**, un agente conversacional de IA diseñado para actuar como un ente regulador automatizado.

Ohmni no es un simple chatbot de preguntas y respuestas; es un sistema con capacidad de razonamiento que cruza fronteras de datos:

* **Capacidad Dual:** Ohmni entiende los datos "duros" (KPIs de consumo, potencia, pérdidas) y los interpreta utilizando datos "blandos" (leyes, reglamentos y normas de la SIE).
* **Uso de Herramientas (Tools):** El chatbot cuenta con herramientas especializadas que le permiten extraer métricas específicas del dataset en tiempo real cuando el usuario lo solicita.
* **Auditoría en Lenguaje Natural:** Puedes preguntarle: *"¿El consumo en la región Norte cumple con la normativa de crecimiento esperada para 2023?"*. Ohmni extraerá el dato cuantitativo, consultará su base de conocimiento regulatoria y emitirá un juicio técnico-comercial basado en evidencia.

---

## Funcionalidades Principales

### Módulo de Inteligencia Artificial (Nuevo)
-   **Chatbot Auditor "Ohmni":** Interfaz conversacional para consultas regulatorias y técnicas.
-   **Cruce de Información Cuantitativa/Cualitativa:** Análisis de cumplimiento normativo basado en datos reales del SENI (Sistema Eléctrico Nacional Interconectado).
-   **Extracción Dinámica de KPIs:** El agente de IA puede consultar la base de datos en tiempo real para sustentar sus respuestas.

### Módulo de Visualización (Dashboard)
-   Visualización del consumo eléctrico promedio por región, tipo de cliente y mes.
-   Comparación interactiva de medidas de energía (kWh) vs. potencia (kW).
-   Mapa geográfico dinámico de la República Dominicana segmentado por región.
-   Análisis de tendencias históricas (2012–2024).

---

## Stack Tecnológico

Este proyecto combina análisis de datos tradicional con ingeniería de IA moderna:

* **Python 3.8+**: Lenguaje principal.
* **Streamlit**: Framework para la interfaz web interactiva.
* **Pandas/Plotly**: Manipulación y visualización de datos cuantitativos.
* **LLM (Modelo de Lenguaje Grande):** Cerebro detrás de Ohmni para el razonamiento y procesamiento de lenguaje natural.
* **LangChain/LlamaIndex (Framework de IA):** Orquestación del agente, gestión de "tools" para acceso a datos y conexión con bases de conocimiento regulatorio (RAG).

---

## Enlace a la Plataforma

**Explora la aplicación y conversa con Ohmni aquí:**
[PowerSense AI RD - Streamlit App](https://powersense-rd-tendencias-de-consumo-electrico.streamlit.app/)
*(Nota: Asegúrate de acceder a la sección del Chatbot en la barra de navegación lateral)*

---

## Instalación y Ejecución Local

Asegúrate de tener **Python 3.8+** instalado.

1.  Clona el repositorio y navega al directorio.
2.  Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
