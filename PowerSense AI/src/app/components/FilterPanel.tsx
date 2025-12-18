import { useState } from 'react';
import { ExportButton } from './ExportButton';

interface FilterPanelProps {
  onFilterChange: (filters: FilterState) => void;
}

export interface FilterState {
  region: string;
  measure: string;
  year: number;
}

export function FilterPanel({ onFilterChange }: FilterPanelProps) {
  const [region, setRegion] = useState('norte');
  const [measure, setMeasure] = useState('energia');
  const [year, setYear] = useState(2024);

  const handleChange = (field: keyof FilterState, value: string | number) => {
    const newFilters: FilterState = { region, measure, year };
    newFilters[field] = value as never;
    
    if (field === 'region') setRegion(value as string);
    if (field === 'measure') setMeasure(value as string);
    if (field === 'year') setYear(value as number);
    
    onFilterChange(newFilters);
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-800">Filtros de Análisis</h2>
        <ExportButton />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Region Select */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Región
          </label>
          <select
            value={region}
            onChange={(e) => handleChange('region', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1f77b4] focus:border-transparent transition-all"
          >
            <option value="norte">Norte</option>
            <option value="sur">Sur</option>
            <option value="este">Este</option>
          </select>
        </div>

        {/* Measure Radio Buttons */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Medida
          </label>
          <div className="flex gap-4 pt-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="measure"
                value="energia"
                checked={measure === 'energia'}
                onChange={(e) => handleChange('measure', e.target.value)}
                className="w-4 h-4 text-[#1f77b4] focus:ring-[#1f77b4]"
              />
              <span className="text-sm text-gray-700">Energía (kWh)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="measure"
                value="potencia"
                checked={measure === 'potencia'}
                onChange={(e) => handleChange('measure', e.target.value)}
                className="w-4 h-4 text-[#1f77b4] focus:ring-[#1f77b4]"
              />
              <span className="text-sm text-gray-700">Potencia (kW)</span>
            </label>
          </div>
        </div>

        {/* Year Slider */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Año: {year}
          </label>
          <input
            type="range"
            min="2012"
            max="2024"
            value={year}
            onChange={(e) => handleChange('year', parseInt(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-thumb"
            style={{
              accentColor: '#1f77b4'
            }}
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>2012</span>
            <span>2024</span>
          </div>
        </div>
      </div>
    </div>
  );
}