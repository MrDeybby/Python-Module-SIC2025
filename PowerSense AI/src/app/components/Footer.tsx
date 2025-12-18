import { Brain } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-gradient-to-r from-gray-900 to-gray-800 text-gray-300 py-8 mt-12">
      <div className="container mx-auto px-4 md:px-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="text-sm mb-1">
              © {new Date().getFullYear()} PowerSense AI RD - Todos los derechos reservados
            </p>
            <p className="text-xs text-gray-400">
              Sistema de análisis y predicción de consumo eléctrico
            </p>
          </div>
          
          <div className="flex items-center gap-2 bg-white/5 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/10">
            <Brain className="w-5 h-5 text-[#1f77b4]" />
            <span className="text-sm">
              Desarrollado por <span className="font-bold text-white">SenpAI</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}