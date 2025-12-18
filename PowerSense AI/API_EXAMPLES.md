# PowerSense AI RD - Ejemplos de API

Este documento muestra ejemplos de las estructuras de datos que el backend Python debería retornar.

## 1. Endpoint: Obtener Datos de Consumo

**Request:**
```http
GET /api/consumption?region=norte&year=2024&measure=energia
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "region": "norte",
      "year": 2024,
      "month": 1,
      "consumption": 4200,
      "measure": "energia",
      "clientType": {
        "residential": 1890,
        "commercial": 1260,
        "industrial": 840,
        "government": 210
      }
    },
    {
      "id": 2,
      "region": "norte",
      "year": 2024,
      "month": 2,
      "consumption": 3800,
      "measure": "energia",
      "clientType": {
        "residential": 1710,
        "commercial": 1140,
        "industrial": 760,
        "government": 190
      }
    }
    // ... más meses
  ],
  "metadata": {
    "total_records": 12,
    "region": "norte",
    "year": 2024,
    "measure": "energia"
  }
}
```

## 2. Endpoint: Predicción de Consumo

**Request:**
```http
POST /api/predict
Content-Type: application/json

{
  "year": 2025,
  "month": 6,
  "lastMonthConsumption": 4500,
  "region": "norte"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "predicted_consumption": 5175,
    "confidence": 0.87,
    "confidence_interval": {
      "lower": 4850,
      "upper": 5500
    },
    "factors": [
      {
        "name": "Seasonal Pattern",
        "impact": 0.45,
        "description": "Aumento estacional del 15% en meses de verano"
      },
      {
        "name": "Historical Trend",
        "impact": 0.35,
        "description": "Tendencia histórica de crecimiento del 3% anual"
      },
      {
        "name": "Regional Demand",
        "impact": 0.20,
        "description": "Demanda regional basada en actividad económica"
      }
    ],
    "model_info": {
      "algorithm": "Random Forest Regressor",
      "version": "1.2.0",
      "last_trained": "2024-12-01"
    }
  }
}
```

## 3. Endpoint: Chat con Asistente IA

**Request:**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "¿Cuál es el consumo promedio en la región Norte?",
  "context": {
    "current_region": "norte",
    "current_year": 2024
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": {
    "text": "Basándome en los datos del año 2024, el consumo promedio mensual en la región Norte es de 4,371 MWh. Los meses de verano (junio-septiembre) registran los picos más altos, con un promedio de 5,350 MWh, mientras que los meses de invierno promedian 3,800 MWh.",
    "sources": [
      {
        "type": "historical_data",
        "period": "2024",
        "region": "norte"
      }
    ],
    "suggestions": [
      "Ver gráfico de consumo mensual",
      "Comparar con otras regiones",
      "Predecir consumo futuro"
    ]
  }
}
```

## 4. Endpoint: Estadísticas Generales

**Request:**
```http
GET /api/stats?region=norte&year=2024
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_consumption": 52450,
    "average_monthly": 4371,
    "active_clients": 2400000,
    "efficiency_rate": 87.3,
    "growth_rate": 12.5,
    "peak_month": {
      "month": 7,
      "consumption": 5600
    },
    "lowest_month": {
      "month": 2,
      "consumption": 3800
    }
  }
}
```

## 5. Endpoint: Datos del Mapa por Región

**Request:**
```http
GET /api/map-data?year=2024
```

**Response:**
```json
{
  "success": true,
  "regions": [
    {
      "id": "norte",
      "name": "Norte",
      "coordinates": {
        "latitude": 19.4569,
        "longitude": -70.6993
      },
      "total_consumption": 62400,
      "average_consumption": 5200,
      "population": 3500000,
      "consumption_per_capita": 17.8,
      "growth_rate": 12.5,
      "color_intensity": 0.85
    },
    {
      "id": "sur",
      "name": "Sur",
      "coordinates": {
        "latitude": 18.4861,
        "longitude": -69.9312
      },
      "total_consumption": 45600,
      "average_consumption": 3800,
      "population": 2800000,
      "consumption_per_capita": 16.3,
      "growth_rate": 8.2,
      "color_intensity": 0.62
    },
    {
      "id": "este",
      "name": "Este",
      "coordinates": {
        "latitude": 18.7357,
        "longitude": -68.5056
      },
      "total_consumption": 54000,
      "average_consumption": 4500,
      "population": 3100000,
      "consumption_per_capita": 17.4,
      "growth_rate": 10.1,
      "color_intensity": 0.73
    }
  ]
}
```

## 6. Endpoint: Exportar Reporte

**Request:**
```http
POST /api/export
Content-Type: application/json

{
  "format": "pdf",
  "filters": {
    "region": "norte",
    "year": 2024,
    "measure": "energia"
  },
  "sections": [
    "summary",
    "charts",
    "predictions",
    "recommendations"
  ]
}
```

**Response:**
```json
{
  "success": true,
  "file": {
    "url": "https://api.powersense.com/reports/12345.pdf",
    "filename": "reporte_norte_2024.pdf",
    "size": 2457600,
    "expires_at": "2024-12-17T10:00:00Z"
  }
}
```

## Códigos de Error Comunes

### 400 - Bad Request
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETERS",
    "message": "La región especificada no es válida",
    "details": {
      "field": "region",
      "received": "oeste",
      "expected": ["norte", "sur", "este"]
    }
  }
}
```

### 404 - Not Found
```json
{
  "success": false,
  "error": {
    "code": "DATA_NOT_FOUND",
    "message": "No se encontraron datos para los parámetros especificados",
    "details": {
      "region": "norte",
      "year": 2025
    }
  }
}
```

### 500 - Internal Server Error
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "Error al procesar la solicitud",
    "request_id": "req_abc123xyz"
  }
}
```

## Notas de Implementación

### Headers Requeridos
```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
X-API-Version: 1.0
```

### Rate Limiting
- 100 requests por minuto por IP
- 1000 requests por hora por usuario autenticado

### CORS
```python
# Configuración CORS recomendada para desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://powersense-ai-rd.vercel.app"
]
```

### Base URL
```
Desarrollo: http://localhost:8000/api
Producción: https://api.powersense-rd.com/api
```
