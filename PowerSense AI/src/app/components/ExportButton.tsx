import { Download, FileText, Image } from 'lucide-react';
import { useState } from 'react';

export function ExportButton() {
  const [isOpen, setIsOpen] = useState(false);

  const handleExport = (format: string) => {
    // Mock export function
    console.log(`Exporting data as ${format}`);
    
    // In production, this would:
    // - Call API endpoint to generate report
    // - Download file in the specified format
    // Example: downloadReport(format);
    
    setIsOpen(false);
    
    // Show success message (you could use a toast library like sonner)
    alert(`Exportando reporte en formato ${format.toUpperCase()}...`);
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors shadow-sm"
      >
        <Download className="w-4 h-4" />
        <span className="hidden md:inline">Exportar Reporte</span>
      </button>

      {isOpen && (
        <>
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-xl border border-gray-200 py-2 z-20">
            <button
              onClick={() => handleExport('pdf')}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 transition-colors"
            >
              <FileText className="w-4 h-4 text-red-600" />
              <span className="text-sm">Exportar como PDF</span>
            </button>
            <button
              onClick={() => handleExport('excel')}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 transition-colors"
            >
              <FileText className="w-4 h-4 text-green-600" />
              <span className="text-sm">Exportar como Excel</span>
            </button>
            <button
              onClick={() => handleExport('csv')}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 transition-colors"
            >
              <FileText className="w-4 h-4 text-blue-600" />
              <span className="text-sm">Exportar como CSV</span>
            </button>
            <button
              onClick={() => handleExport('png')}
              className="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center gap-3 transition-colors"
            >
              <Image className="w-4 h-4 text-purple-600" />
              <span className="text-sm">Exportar como imagen</span>
            </button>
          </div>
        </>
      )}
    </div>
  );
}
