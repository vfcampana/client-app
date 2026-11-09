import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  CircularProgress,
  Alert
} from '@mui/material';
import { ShoppingCart, AccountBalanceWallet } from '@mui/icons-material';

interface CompraModalProps {
  open: boolean;
  onClose: () => void;
  bloco: {
    id: number;
    titulo: string;
    valor: string | number;
    id_usuario: number;
  };
  onCompraRealizada: () => void;
}

export default function CompraModal({ open, onClose, bloco, onCompraRealizada }: CompraModalProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Função para converter o valor para número, seja string ou number
  const getNumericValue = (valor: string | number): number => {
    if (typeof valor === 'number') {
      return valor;
    }
    return parseFloat(valor.replace(/[^\d,]/g, '').replace(',', '.'));
  };

  const handleComprar = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('authToken');
      if (!token) {
        setError('Você precisa estar logado para fazer uma compra');
        return;
      }

      // Fazer a compra direta
      const response = await fetch('http://localhost:5000/blockchain/comprar-bloco', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          bloco_id: bloco.id,
          valor: getNumericValue(bloco.valor)
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erro ao processar compra');
      }

      const resultado = await response.json();
      
      if (resultado.success) {
        setSuccess(`🎉 Compra realizada com sucesso! 
        Transação blockchain: ${resultado.transaction_hash || 'Processada'}
        O bloco agora é seu!`);
        
        // Fechar modal após 3 segundos e recarregar página
        setTimeout(() => {
          onCompraRealizada();
          onClose();
        }, 3000);
      } else {
        setError(resultado.message || 'Erro ao processar compra');
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const valorFormatado = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(getNumericValue(bloco.valor));

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
        <ShoppingCart sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
        <Typography variant="h5">Confirmar Compra</Typography>
      </DialogTitle>

      <DialogContent>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {success && (
          <Alert severity="success" sx={{ mb: 2, whiteSpace: 'pre-line' }}>
            {success}
          </Alert>
        )}

        <Box sx={{ textAlign: 'center', py: 2 }}>
          <Typography variant="h6" gutterBottom>
            {bloco.titulo}
          </Typography>
          
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            gap: 1,
            my: 3,
            p: 2,
            backgroundColor: 'primary.light',
            borderRadius: 2,
            color: 'primary.contrastText'
          }}>
            <AccountBalanceWallet />
            <Typography variant="h4" fontWeight="bold">
              {valorFormatado}
            </Typography>
          </Box>

          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            Tem certeza que deseja comprar este bloco?
          </Typography>

          <Typography variant="body2" color="text.secondary">
            ⚠️ Esta ação não pode ser desfeita. A transação será processada via blockchain.
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 2 }}>
        <Button 
          onClick={onClose} 
          disabled={loading}
          variant="outlined"
          fullWidth
        >
          Cancelar
        </Button>
        
        <Button
          onClick={handleComprar}
          disabled={loading}
          variant="contained"
          color="primary"
          fullWidth
          startIcon={loading ? <CircularProgress size={20} /> : <ShoppingCart />}
        >
          {loading ? 'Processando...' : 'Comprar Agora'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}