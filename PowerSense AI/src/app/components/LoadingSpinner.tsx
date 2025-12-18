import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export function LoadingSpinner({ message = 'Cargando datos...' }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="w-12 h-12 text-[#1f77b4] animate-spin mb-4" />
      <p className="text-gray-600">{message}</p>
    </div>
  );
}

export function LoadingOverlay({ message = 'Procesando...' }: LoadingSpinnerProps) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-2xl p-8 flex flex-col items-center">
        <Loader2 className="w-16 h-16 text-[#1f77b4] animate-spin mb-4" />
        <p className="text-lg font-semibold text-gray-800">{message}</p>
      </div>
    </div>
  );
}
