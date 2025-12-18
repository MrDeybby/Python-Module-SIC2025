from fastapi import FastAPI
from pydantic import BaseModel
from predecir import EnergyModel

from langchain_core.messages import HumanMessage, AIMessage

from utils.context import get_dashboard_context
from agent_backend.agent import setup_vector_store_and_model, update_agent_context

app = FastAPI()
modelo_ia = EnergyModel()
agent = setup_vector_store_and_model()
chat_history = []

class PredictRequest(BaseModel):
    año: int
    mes: int
    mes_pasado: float
    region: str

@app.post("/predict")
def predict(req: PredictRequest):
    result = modelo_ia.predict(
        año=req.año,
        mes=req.mes,
        mes_pasado=req.mes_pasado,
        region=req.region
    )
    return { "prediccion": result }



class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    chat_history.append(HumanMessage(content=req.message))

    context = get_dashboard_context()
    update_agent_context(context)

    history_window = chat_history[-3:]

    response = agent.invoke({"messages": history_window})

    final_response = None

    for m in response["messages"]:
        if isinstance(m, AIMessage):
            if not (hasattr(m, "tool_calls") and m.tool_calls):
                final_response = m.content

    if not final_response:
        final_response = "No pude generar una respuesta válida."

    chat_history.append(AIMessage(content=final_response))

    return {"response": final_response}