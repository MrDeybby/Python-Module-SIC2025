// API utility functions for PowerSense AI RD
// This file contains mock functions that would connect to a Python backend

const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000/api';

export interface ConsumptionData {
  region: string;
  year: number;
  month: number;
  consumption: number;
  measure: string;
}

export interface PredictionRequest {
  year: number;
  month: number;
  lastMonthConsumption: number;
  region: string;
}

export interface PredictionResponse {
  predicted_consumption: number;
  confidence: number;
  factors: string[];
}

// Mock function - would call Python backend API
export async function fetchConsumptionData(
  region: string,
  year: number,
  measure: string
): Promise<ConsumptionData[]> {
  // In production, this would be:
  // const response = await fetch(`${API_BASE_URL}/consumption?region=${region}&year=${year}&measure=${measure}`);
  // return response.json();
  
  // Mock data for demonstration
  return Promise.resolve([
    { region, year, month: 1, consumption: 4200, measure },
    { region, year, month: 2, consumption: 3800, measure },
    // ... more data
  ]);
}

// Mock function - would call Python ML model via API
export async function predictConsumption(
  request: PredictionRequest
): Promise<PredictionResponse> {
  // In production, this would be:
  // const response = await fetch(`${API_BASE_URL}/predict`, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(request)
  // });
  // return response.json();
  
  // Mock prediction
  const baseValue = request.lastMonthConsumption;
  const seasonalFactor = request.month >= 6 && request.month <= 9 ? 1.15 : 0.95;
  const predicted = Math.round(baseValue * seasonalFactor);
  
  return Promise.resolve({
    predicted_consumption: predicted,
    confidence: 0.85,
    factors: ['Seasonal pattern', 'Historical trend', 'Regional demand']
  });
}

// Mock function - would call chatbot API
export async function sendChatMessage(message: string): Promise<string> {
  // In production, this would be:
  // const response = await fetch(`${API_BASE_URL}/chat`, {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ message })
  // });
  // const data = await response.json();
  // return data.response;
  
  // Mock responses
  const responses = [
    'Basándome en los datos históricos, el consumo eléctrico en la región Norte tiende a aumentar un 15% durante los meses de verano.',
    'Te recomiendo revisar el gráfico de consumo mensual para identificar patrones estacionales en tu región.',
    'Los datos muestran que el sector residencial representa el 45% del consumo total en República Dominicana.',
    'Puedo ayudarte a interpretar las tendencias de consumo. ¿Qué región te interesa analizar?',
    'La predicción de consumo utiliza modelos avanzados que consideran factores estacionales y tendencias históricas.'
  ];
  
  return Promise.resolve(responses[Math.floor(Math.random() * responses.length)]);
}

// Error handling wrapper
export async function apiCall<T>(
  apiFunction: () => Promise<T>,
  errorMessage: string = 'Error en la llamada API'
): Promise<T> {
  try {
    return await apiFunction();
  } catch (error) {
    console.error(errorMessage, error);
    throw new Error(errorMessage);
  }
}
