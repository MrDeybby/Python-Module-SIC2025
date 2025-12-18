import { useState } from 'react';
import { MapPin } from 'lucide-react';

const regionsData = [
  { id: 'norte', name: 'Norte', consumo: 5200, x: 50, y: 25, color: '#1f77b4', lightColor: '#64b5f6' },
  { id: 'sur', name: 'Sur', consumo: 3800, x: 50, y: 70, color: '#90caf9', lightColor: '#bbdefb' },
  { id: 'este', name: 'Este', consumo: 4500, x: 75, y: 50, color: '#0d3b66', lightColor: '#1565c0' },
];

export function InteractiveMap() {
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  const handleMouseEnter = (region: typeof regionsData[0], event: React.MouseEvent) => {
    setHoveredRegion(region.id);
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipPos({ x: rect.left + rect.width / 2, y: rect.top });
  };

  const handleMouseLeave = () => {
    setHoveredRegion(null);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-8">
      <h3 className="text-lg font-semibold mb-6 text-gray-800">Mapa de Consumo por Región</h3>
      
      <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg p-6">
        <div className="relative w-full" style={{ minHeight: '400px' }}>
          {/* SVG Map */}
          <svg viewBox="0 0 100 100" className="w-full h-full">
            {/* Background */}
            <rect x="0" y="0" width="100" height="100" fill="#f5f5f5" rx="4" />
            
            {/* Norte Region */}
            <path
              d="M 20,10 L 80,10 L 70,35 L 30,35 Z"
              fill={hoveredRegion === 'norte' ? regionsData[0].lightColor : regionsData[0].color}
              stroke="#fff"
              strokeWidth="0.5"
              className="cursor-pointer transition-all duration-300 hover:opacity-90"
              style={{ filter: hoveredRegion === 'norte' ? 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' : 'none' }}
              onMouseEnter={(e) => handleMouseEnter(regionsData[0], e)}
              onMouseLeave={handleMouseLeave}
            />
            <text x="50" y="25" textAnchor="middle" fill="white" fontSize="4" fontWeight="bold">
              Norte
            </text>
            
            {/* Este Region */}
            <path
              d="M 70,35 L 90,40 L 85,70 L 60,65 Z"
              fill={hoveredRegion === 'este' ? regionsData[2].lightColor : regionsData[2].color}
              stroke="#fff"
              strokeWidth="0.5"
              className="cursor-pointer transition-all duration-300 hover:opacity-90"
              style={{ filter: hoveredRegion === 'este' ? 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' : 'none' }}
              onMouseEnter={(e) => handleMouseEnter(regionsData[2], e)}
              onMouseLeave={handleMouseLeave}
            />
            <text x="75" y="53" textAnchor="middle" fill="white" fontSize="4" fontWeight="bold">
              Este
            </text>
            
            {/* Sur Region */}
            <path
              d="M 30,35 L 70,35 L 60,65 L 85,70 L 80,85 L 20,85 L 15,70 L 40,65 Z"
              fill={hoveredRegion === 'sur' ? regionsData[1].lightColor : regionsData[1].color}
              stroke="#fff"
              strokeWidth="0.5"
              className="cursor-pointer transition-all duration-300 hover:opacity-90"
              style={{ filter: hoveredRegion === 'sur' ? 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' : 'none' }}
              onMouseEnter={(e) => handleMouseEnter(regionsData[1], e)}
              onMouseLeave={handleMouseLeave}
            />
            <text x="50" y="63" textAnchor="middle" fill="white" fontSize="4" fontWeight="bold">
              Sur
            </text>
          </svg>

          {/* Tooltip */}
          {hoveredRegion && (
            <div 
              className="absolute bg-gray-900 text-white px-4 py-3 rounded-lg shadow-xl text-sm pointer-events-none z-10 animate-fade-in"
              style={{
                left: '50%',
                top: '10%',
                transform: 'translateX(-50%)'
              }}
            >
              <div className="flex items-center gap-2 mb-1">
                <MapPin className="w-4 h-4 text-blue-300" />
                <div className="font-bold">
                  {regionsData.find(r => r.id === hoveredRegion)?.name}
                </div>
              </div>
              <div className="text-xs text-gray-300">
                Consumo: <span className="font-semibold text-white">{regionsData.find(r => r.id === hoveredRegion)?.consumo} MWh</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap gap-4 justify-center">
        {regionsData.map((region) => (
          <div key={region.id} className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow-sm">
            <div 
              className="w-4 h-4 rounded"
              style={{ backgroundColor: region.color }}
            />
            <span className="text-sm font-medium text-gray-700">
              {region.name}
            </span>
            <span className="text-sm text-gray-500">
              {region.consumo} MWh
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}