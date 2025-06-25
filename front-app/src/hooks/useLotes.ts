import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getLotes, deleteLote, updateLote, createLote } from '../services/lotes';
import { Lote } from '../types/Lote';

export const useLotes = () => {
  return useQuery({
    queryKey: ['lotes'],
    queryFn: getLotes,
  });
};

export const useCreateLote = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: createLote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lotes'] });
    },
  });
};

export const useDeleteLote = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: deleteLote,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lotes'] });
    },
  });
};

export const useUpdateLote = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ id, lote }: { id: number; lote: Lote }) => updateLote(id, lote),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['lotes'] });
    },
  });
};