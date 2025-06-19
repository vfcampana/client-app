import { useState, useCallback } from 'react';
import { addToFavoritos, removeFavorito, getFavoritos } from '../services/favorito';

export const useFavoritos = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const addFavorito = useCallback(async (id_bloco: number) => {
    setLoading(true);
    setError(null);
    try {
      const result = await addToFavoritos({ id_bloco });
      setLoading(false);
      return { success: true, data: result };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Erro ao adicionar aos favoritos';
      setError(errorMessage);
      setLoading(false);
      return { success: false, error: errorMessage };
    }
  }, []);

  const checkIfFavorite = useCallback(async (id_bloco: number) => {
    setLoading(true);
    setError(null);
    try {
      const result = await getFavoritos();
      setLoading(false);
      const isFavorite = result.some((favorito: any) => favorito.id === id_bloco);
      return { success: true, isFavorite };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Erro ao verificar favoritos';
      setError(errorMessage);
      setLoading(false);
      return { success: false, error: errorMessage, isFavorite: false };
    }
  }, []); 

  const removeFavoritoById = useCallback(async (id_bloco: number) => {
    setLoading(true);
    setError(null);
    try {
      const result = await removeFavorito(id_bloco);
      setLoading(false);
      return { success: true, data: result };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Erro ao remover dos favoritos';
      setError(errorMessage);
      setLoading(false);
      return { success: false, error: errorMessage };
    }
  }, []);

  const fetchFavoritos = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getFavoritos();
      setLoading(false);
      return { success: true, data: result };
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Erro ao buscar favoritos';
      setError(errorMessage);
      setLoading(false);
      return { success: false, error: errorMessage };
    }
  }, []);

  return {
    addFavorito,
    removeFavoritoById,
    fetchFavoritos,
    checkIfFavorite,
    loading,
    error
  };
};