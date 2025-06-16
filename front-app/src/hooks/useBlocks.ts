import { useState, useEffect } from 'react';

interface Block {
  id: number;
  titulo: string;
  classificacao: string;
  coloracao: string;
  material: string;
  medida_bruta: string;
  volume_bruto: string;
  medida_liquida: string;
  volume_liquido: string;
  pedreira: string;
  observacoes: string;
  cep: string;
  logradouro: string;
  pais: string;
  cidade: string;
  valor: string;
  data_criacao: string;
  data_alteracao: string;
  estado: string;
  id_usuario: number;
  status: string;
}

interface UseBlocksReturn {
  blocks: Block[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

export const useBlocks = (): UseBlocksReturn => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBlocks = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/bloco`);
    
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setBlocks(data);
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      console.error('❌ Erro ao buscar blocos:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBlocks();
  }, []);

  return {
    blocks,
    loading,
    error,
    refetch: fetchBlocks // Para recarregar quando necessário
  };
};