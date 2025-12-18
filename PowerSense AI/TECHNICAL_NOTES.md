# PowerSense AI RD - Notas Técnicas

## Arquitectura de la Aplicación

### Frontend (React + TypeScript + Tailwind CSS)
La aplicación está construida con componentes modulares y reutilizables:

#### Componentes Principales:
- **Header**: Navegación fija con branding
- **FilterPanel**: Controles de filtrado (región, medida, año)
- **StatsCards**: Tarjetas con métricas clave
- **ChartsSection**: Visualizaciones con Recharts (barras y pastel)
- **InteractiveMap**: Mapa SVG interactivo de República Dominicana
- **PredictionSection**: Formulario de predicción con IA
- **ChatSidebar**: Asistente conversacional
- **Footer**: Información de copyright

### Integración con Backend Python

#### Endpoints API Esperados:

**1. Obtener datos de consumo**
```
GET /api/consumption
Query params: region, year, measure
Response: ConsumptionData[]
```

**2. Predecir consumo**
```
POST /api/predict
Body: { year, month, lastMonthConsumption, region }
Response: { predicted_consumption, confidence, factors }
```

**3. Chat con IA**
```
POST /api/chat
Body: { message }
Response: { response }
```

### Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
VITE_API_URL=http://localhost:8000/api
```

### Estructura de Datos

#### Filtros
```typescript
interface FilterState {
  region: string;    // 'norte' | 'sur' | 'este'
  measure: string;   // 'energia' | 'potencia'
  year: number;      // 2012-2024
}
```

#### Predicción
```typescript
interface PredictionRequest {
  year: number;
  month: number;
  lastMonthConsumption: number;
  region: string;
}
```

### Paleta de Colores

- **Azul Principal**: `#1f77b4`
- **Azul Oscuro**: `#0d3b66`
- **Celeste**: `#90caf9`
- **Blanco**: `#ffffff`
- **Negro**: `#000000`

### Dependencias Clave

- **recharts**: Gráficos y visualizaciones
- **lucide-react**: Iconos modernos
- **tailwindcss**: Estilos utilitarios

### Responsividad

- **Desktop**: Vista completa con sidebar visible
- **Tablet**: Sidebar oculto, botón toggle
- **Móvil**: Layout vertical, sidebar overlay

### Mejoras Futuras Sugeridas

1. **Autenticación**: Integrar login/registro
2. **Exportación**: Permitir descargar gráficos y reportes
3. **Notificaciones**: Alertas de consumo anormal
4. **Comparativas**: Comparar múltiples regiones
5. **Histórico**: Vista de datos históricos extendidos
6. **Personalización**: Temas claro/oscuro
7. **PWA**: Convertir en Progressive Web App
8. **Caché**: Implementar estrategia de caché de datos

### Testing

Para implementar tests:
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

### Deployment

Recomendaciones:
- **Frontend**: Vercel, Netlify, o AWS Amplify
- **Backend**: Railway, Render, o AWS Lambda
- **Base de datos**: PostgreSQL o MongoDB Atlas

### Notas de Seguridad

- No incluir API keys en el código
- Usar variables de entorno
- Implementar CORS en el backend
- Validar todos los inputs del usuario
- Sanitizar datos antes de mostrar
