import os
import json
import streamlit as st
import operator
from typing import Annotated, TypedDict, Union, List, Literal, Optional
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage, BaseMessage, AIMessage, AnyMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END, START

#from google.colab import userdata
# En su lugar
from dotenv import find_dotenv, load_dotenv
env_path = find_dotenv()
load_dotenv(env_path)

# PARA MANEJO DE EMBEDDINGS Y tools de retrieval
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma 


CONTEXTO_GLOBAL = {"status": "Iniciando..."}

def update_agent_context(nuevo_contexto: dict):
    """Actualiza la 'visión' del agente con lo que pasa en Streamlit"""
    global CONTEXTO_GLOBAL
    CONTEXTO_GLOBAL = nuevo_contexto

def get_context_string():
    return json.dumps(CONTEXTO_GLOBAL, indent=2, ensure_ascii=False)


class MessageState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    llm_calls: int

    

class PlanRazonamiento(BaseModel):
    veredicto: Literal["SOCIAL", "LEGAL", "DATOS"] = Field( #AGREGAMOS 'DATOS'
        ..., description="SOCIAL: Saludo/Charla. LEGAL: Pregunta sobre leyes/reglamentos. DATOS: Pregunta sobre números, regiones o info visible en el dashboard."
    )
    razon: str = Field(..., description="Por qué tomaste esta decisión.")
    accion: Literal["BUSCAR", "RESPONDER"] = Field(..., description="Acción a tomar.")
    query: Optional[str] = Field(None, description="Query de búsqueda si aplica.")
    


# PROMPT Y NODO DE RAZONAMIENTO (SCRATCHPAD)
reasoner_prompt = """
Eres el CEREBRO ESTRATÉGICO de PowerSenseAI.
Tu misión es analizar la entrada del usuario combinada con lo que él ve en su pantalla (Contexto) y decidir el plan de acción.

CONTEXTO ACTUAL DEL DASHBOARD (Lo que ve el usuario):
{dashboard_context}

GUÍA DE CLASIFICACIÓN:
1.  **SOCIAL:** Saludos, chistes, agradecimientos, despedidas.
    *   Acción: RESPONDER (Amablemente).
2.  **DATOS:** Preguntas sobre números, filtros, regiones o predicciones que aparecen en el Contexto del Dashboard.
    *   Acción: RESPONDER (Usando la info del contexto, NO la herramienta).
3.  **LEGAL:** Preguntas sobre regulaciones, leyes, multas, derechos, SIE, Protecom o procedimientos.
    *   Acción: BUSCAR (Usando la herramienta de leyes).

EJEMPLOS DE RAZONAMIENTO (FEW-SHOT):

---
Usuario: "Hola, buenos días."
Plan: {{
"veredicto": "SOCIAL",
"razon": "Saludo de cortesía inicial.",
"accion": "RESPONDER",
"query": null
}}
---
Usuario: "¿Qué dice la ley sobre robar luz?"
Plan: {{
"veredicto": "LEGAL",
"razon": "Pregunta sobre normativa y fraude (Art. 125). Requiere búsqueda externa.",
"accion": "BUSCAR",
"query": "fraude eléctrico sanciones ley general electricidad"
}}
---
Usuario: "¿Cuál es la predicción de consumo para febrero?"
Plan: {{
"veredicto": "DATOS",
"razon": "El usuario pregunta por un dato específico visible en el dashboard (inputs.prediccion).",
"accion": "RESPONDER",
"query": null
}}
---
Usuario: "¿Tengo derecho a reclamar si la predicción es muy alta?"
Plan: {{
"veredicto": "LEGAL",
"razon": "Aunque menciona 'predicción', la intención central es sobre DERECHOS DE RECLAMO.",
"accion": "BUSCAR",
"query": "derechos usuario reclamación alta facturación"
}}
---

INSTRUCCIONES FINALES:
*   Si eliges **DATOS**, tu razón debe indicar qué campo del JSON usarás.
*   Si eliges **LEGAL**, tu query debe ser específico para el buscador vectorial.
"""

actor_prompt = """
Eres PowerSenseAI (Ejecutor).
Tienes acceso al DASHBOARD del usuario.

CONTEXTO DEL DASHBOARD:
{dashboard_context}

INSTRUCCIONES:
1.  Si tu instrucción es **RESPONDER**:
    *   Si es sobre DATOS: Usa los valores del JSON de arriba (ej: region, inputs, prediccion) para responder con precisión.
    *   Si es SOCIAL: Responde natural.
2.  Si tu instrucción es **BUSCAR**: Ejecuta la herramienta.

IMPORTANTE:
*   Si te preguntan "¿Qué región estoy viendo?", mira el campo "region" del contexto.
*   Si te preguntan por la predicción, mira "inputs.prediccion".
*   NO inventes números. Usa solo lo que ves en el contexto.
"""

@st.cache_resource
def load_vector_store():
    """Carga o crea el vector store SOLO UNA VEZ"""
    persist_directory = "./sie_db_"
    
    # Si ya existe el directorio con datos, solo carga
    if os.path.exists(persist_directory) and os.path.exists(f"{persist_directory}/chroma.sqlite3"):
        print("[INFO]: Vector store ya existe, cargándolo...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        return vector_store
    
    # Si no existe, crear desde cero
    print("[INFO]: Creando vector store por primera vez...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\nARTÍCULO", "\nARTICULO", "\nArtículo", "\nPÁRRAFO", "\n\n", "\n", ". "]
    )

    urls = [
        "https://sie.gob.do/wp-content/uploads/2020/09/Ley_No._186-07_Modif._LGE_-_Gaceta_Oficial.pdf",
        "https://sie.gob.do/wp-content/uploads/2021/05/Dec._No._306-03_que_ratifica_y_enmienda_el_Reglamento_para_la_Aplicacion_de_la_Ley_General_de_Electricidad_No._125-01.pdf",
        "https://sie.gob.do/wp-content/uploads/2021/05/Dec._No._321-03_que_modifica_Reglamento_para_la_Aplicacion_de_la_Ley_General_de_Electricidad_No._125-01.pdf"
    ]

    raw_docs = []
    for url in urls:
        try:
            loader = PyPDFLoader(url)
            raw_docs.extend(loader.load())
        except Exception as e:
            print(f"[ERROR] No se pudo cargar {url}: {e}")

    print("[INFO]: Cortando leyes por Artículos...")
    splits = text_splitter.split_documents(raw_docs)
    print(f"[INFO]: Se crearon {len(splits)} fragmentos.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    vector_store = Chroma.from_documents(
        documents=splits,
        persist_directory=persist_directory,
        embedding=embeddings
    )
    
    print("[INFO]: Vector store creado y persistido correctamente.")
    return vector_store

@st.cache_resource
def setup_vector_store_and_model():
    """Configura el agente completo SOLO UNA VEZ"""
    vector_store = load_vector_store()
    
    chat_model = ChatGroq(
        model= "openai/gpt-oss-120b", #"llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    @tool
    def buscar_leyes(pregunta: str):
        """Busca información sobre leyes eléctricas, reglamentos, fraude eléctrico y derechos del usuario en República Dominicana."""
        docs = retriever.invoke(pregunta)
        return "\n\n---\n\n".join([d.page_content for d in docs])

    tools = [buscar_leyes]
    tools_by_name = {tool.name: tool for tool in tools}
    chat_model_with_tools = chat_model.bind_tools(tools)

    def reasoner_node(state: MessageState):
        structured_llm = chat_model.with_structured_output(PlanRazonamiento)
        current_context = get_context_string()
        formatted_prompt = reasoner_prompt.format(dashboard_context=current_context)
        messages = [SystemMessage(content=formatted_prompt)] + state["messages"]
        plan_obj = structured_llm.invoke(messages)
        json_str = json.dumps(plan_obj.model_dump(), indent=2, ensure_ascii=False)
        return {"messages": [AIMessage(content=json_str)]}

    def llm_call(state: MessageState):
        current_context = get_context_string()
        formatted_actor_prompt = actor_prompt.format(dashboard_context=current_context)
        messages = [SystemMessage(content=formatted_actor_prompt)] + state["messages"]
        response = chat_model_with_tools.invoke(messages)
        return {"messages": [response]}

    def tool_node(state: dict):
        result = []
        for tool_call in state["messages"][-1].tool_calls:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        return {"messages": result}

    def should_continue(state: MessageState) -> Literal["tool_node", END]:
        messages = state["messages"]
        last_message = messages[-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tool_node"
        return END

    agent_builder = StateGraph(MessageState)
    agent_builder.add_node("reasoner", reasoner_node)
    agent_builder.add_node("actor", llm_call)
    agent_builder.add_node("tools", tool_node)
    
    agent_builder.add_edge(START, "reasoner")
    agent_builder.add_edge("reasoner", "actor")
    agent_builder.add_conditional_edges("actor", should_continue, {"tool_node": "tools", END: END})
    agent_builder.add_edge("tools", "actor")

    agent = agent_builder.compile()
    print("[INFO]: Agente compilado y listo.")
    return agent
