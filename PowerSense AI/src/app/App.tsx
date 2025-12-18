import { useState } from 'react';
import { Header } from './components/Header';
import { FilterPanel, FilterState } from './components/FilterPanel';
import { StatsCards } from './components/StatsCards';
import { ChartsSection } from './components/ChartsSection';
import { InteractiveMap } from './components/InteractiveMap';
import { PredictionSection } from './components/PredictionSection';
import { ChatSidebar } from './components/ChatSidebar';
import { Footer } from './components/Footer';

export default function App() {
  const [filters, setFilters] = useState<FilterState>({
    region: 'norte',
    measure: 'energia',
    year: 2024
  });

  const handleFilterChange = (newFilters: FilterState) => {
    setFilters(newFilters);
    // Here you would typically fetch new data based on filters
    console.log('Filters changed:', newFilters);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <Header />
      
      {/* Main Content */}
      <main className="pt-20 md:pt-24 pb-20 md:pb-12 pr-0 md:pr-96 min-h-screen">
        <div className="container mx-auto px-4 md:px-6">
          {/* Filter Panel */}
          <FilterPanel onFilterChange={handleFilterChange} />

          {/* Stats Cards */}
          <StatsCards />

          {/* Charts Section */}
          <ChartsSection />

          {/* Interactive Map */}
          <InteractiveMap />

          {/* Prediction Section */}
          <PredictionSection />
        </div>
      </main>

      {/* Chat Sidebar */}
      <ChatSidebar />

      {/* Footer */}
      <div className="pr-0 md:pr-96">
        <Footer />
      </div>
    </div>
  );
}