import { Activity, TrendingUp, Zap, Users } from 'lucide-react';

export function StatsCards() {
  const stats = [
    {
      title: 'Consumo Total',
      value: '52,450 MWh',
      change: '+12.5%',
      trend: 'up',
      icon: Zap,
      color: 'from-blue-500 to-blue-600'
    },
    {
      title: 'Promedio Mensual',
      value: '4,371 MWh',
      change: '+8.2%',
      trend: 'up',
      icon: Activity,
      color: 'from-cyan-500 to-cyan-600'
    },
    {
      title: 'Clientes Activos',
      value: '2.4M',
      change: '+5.1%',
      trend: 'up',
      icon: Users,
      color: 'from-indigo-500 to-indigo-600'
    },
    {
      title: 'Eficiencia',
      value: '87.3%',
      change: '+3.4%',
      trend: 'up',
      icon: TrendingUp,
      color: 'from-emerald-500 to-emerald-600'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <div
            key={index}
            className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`p-3 rounded-lg bg-gradient-to-br ${stat.color}`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <span className={`text-sm font-semibold px-2 py-1 rounded ${
                stat.trend === 'up' 
                  ? 'bg-green-100 text-green-700' 
                  : 'bg-red-100 text-red-700'
              }`}>
                {stat.change}
              </span>
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-1">{stat.value}</h3>
            <p className="text-sm text-gray-500">{stat.title}</p>
          </div>
        );
      })}
    </div>
  );
}
