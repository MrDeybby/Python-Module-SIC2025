import { Zap } from 'lucide-react';

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-[#0d3b66] to-[#1f77b4] text-white shadow-lg">
      <div className="container mx-auto px-4 md:px-6 py-3 md:py-4">
        <div className="flex items-center gap-2 md:gap-3">
          <div className="bg-white/10 backdrop-blur-sm p-2 rounded-lg">
            <Zap className="w-6 h-6 md:w-8 md:h-8" />
          </div>
          <div className="flex-1">
            <h1 className="text-lg md:text-2xl font-bold">PowerSense AI RD</h1>
            <p className="text-xs md:text-sm text-blue-100 hidden sm:block">
              Tendencias de consumo eléctrico en República Dominicana
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}