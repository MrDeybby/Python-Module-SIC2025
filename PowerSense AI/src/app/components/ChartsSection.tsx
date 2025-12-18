import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const monthlyData = [
  { mes: 'Ene', consumo: 4200 },
  { mes: 'Feb', consumo: 3800 },
  { mes: 'Mar', consumo: 4100 },
  { mes: 'Abr', consumo: 4500 },
  { mes: 'May', consumo: 4800 },
  { mes: 'Jun', consumo: 5200 },
  { mes: 'Jul', consumo: 5600 },
  { mes: 'Ago', consumo: 5500 },
  { mes: 'Sep', consumo: 5100 },
  { mes: 'Oct', consumo: 4700 },
  { mes: 'Nov', consumo: 4300 },
  { mes: 'Dic', consumo: 4400 },
];

const clientTypeData = [
  { name: 'Residencial', value: 45, color: '#1f77b4' },
  { name: 'Comercial', value: 30, color: '#90caf9' },
  { name: 'Industrial', value: 20, color: '#0d3b66' },
  { name: 'Gubernamental', value: 5, color: '#64b5f6' },
];

export function ChartsSection() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      {/* Bar Chart */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Consumo Promedio Mensual</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="mes" stroke="#666" />
            <YAxis stroke="#666" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
            <Legend />
            <Bar dataKey="consumo" fill="#1f77b4" name="Consumo (MWh)" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Pie Chart */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Distribución por Tipo de Cliente</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={clientTypeData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, value }) => `${name}: ${value}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {clientTypeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
