import { useState } from 'react';
import { TrendingUp, Loader2, CheckCircle } from 'lucide-react';

export function PredictionSection() {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    year: 2025,
    month: 1,
    lastMonthConsumption: 4500,
    region: 'norte'
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);

    // Simulate API call
    setTimeout(() => {
      // Mock prediction calculation
      const baseValue = formData.lastMonthConsumption;
      const seasonalFactor = formData.month >= 6 && formData.month <= 9 ? 1.15 : 0.95;
      const predicted = Math.round(baseValue * seasonalFactor);
      
      setPrediction(predicted);
      setLoading(false);
    }, 1500);
  };

  const months = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
  ];

  return (
    <div className="bg-gradient-to-br from-[#1f77b4] to-[#0d3b66] rounded-xl shadow-lg p-8 mb-8 text-white">
      <div className="flex items-center gap-3 mb-6">
        <TrendingUp className="w-6 h-6" />
        <h3 className="text-2xl font-semibold">Predicción de Consumo</h3>
      </div>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-2 text-blue-100">
            Año
          </label>
          <input
            type="number"
            min="2025"
            max="2030"
            value={formData.year}
            onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
            className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-blue-100">
            Mes
          </label>
          <select
            value={formData.month}
            onChange={(e) => setFormData({ ...formData, month: parseInt(e.target.value) })}
            className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
            required
          >
            {months.map((month, index) => (
              <option key={index} value={index + 1} className="text-gray-900">
                {month}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-blue-100">
            Consumo del mes pasado (MWh)
          </label>
          <input
            type="number"
            min="0"
            step="100"
            value={formData.lastMonthConsumption}
            onChange={(e) => setFormData({ ...formData, lastMonthConsumption: parseInt(e.target.value) })}
            className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-blue-100">
            Región
          </label>
          <select
            value={formData.region}
            onChange={(e) => setFormData({ ...formData, region: e.target.value })}
            className="w-full px-4 py-2 rounded-lg bg-white/10 border border-white/20 text-white focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
            required
          >
            <option value="norte" className="text-gray-900">Norte</option>
            <option value="sur" className="text-gray-900">Sur</option>
            <option value="este" className="text-gray-900">Este</option>
          </select>
        </div>

        <div className="md:col-span-2 lg:col-span-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full md:w-auto px-8 py-3 bg-white text-[#1f77b4] rounded-lg font-semibold hover:bg-blue-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Calculando...
              </>
            ) : (
              'Predecir Consumo'
            )}
          </button>
        </div>
      </form>

      {prediction !== null && (
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 animate-fade-in">
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle className="w-6 h-6 text-green-300" />
            <h4 className="text-lg font-semibold">Predicción Completada</h4>
          </div>
          <p className="text-3xl font-bold mb-1">{prediction.toLocaleString()} MWh</p>
          <p className="text-sm text-blue-100">
            Consumo estimado para {months[formData.month - 1]} {formData.year} en la región {formData.region}
          </p>
        </div>
      )}
    </div>
  );
}
