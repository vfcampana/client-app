import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Box,
  Typography,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Paper,
  Chip,
  CircularProgress,
  Divider,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import { Block } from '../../types/Blocks';
import { Lote } from '../../types/Lote';
import { useCreateLote } from '../../hooks/useLotes';

interface CreateLoteModalProps {
  open: boolean;
  onClose: () => void;
  selectedBlocks: number[];
  blocks: Block[];
  onSuccess: () => void;
}

const CreateLoteModal: React.FC<CreateLoteModalProps> = ({
  open,
  onClose,
  selectedBlocks,
  blocks,
  onSuccess,
}) => {
  const [nome, setNome] = useState('');
  const [preco, setPreco] = useState('');
  const [observacoes, setObservacoes] = useState('');
  const [status, setStatus] = useState<'privado' | 'anunciado'>('privado');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createLoteMutation = useCreateLote();

  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

  const selectedBlocksData = blocks.filter(block => selectedBlocks.includes(block.id));
  const totalValue = selectedBlocksData.reduce((sum, block) => sum + parseFloat(block.valor || '0'), 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const loteData: Lote = {
        id: 0,
        nome,
        preco: parseFloat(preco),
        observacoes: observacoes || undefined,
        status,
        blocos: selectedBlocks,
        data_criacao: new Date().toISOString(),
        id_usuario: 0,
      };

      await createLoteMutation.mutateAsync(loteData);
      onSuccess();
      handleClose();

      alert(`Lote "${nome}" criado com sucesso com ${selectedBlocks.length} bloco(s)!`);
    } catch (err: any) {
      console.error('Erro ao criar lote:', err);
      setError(err.response?.data?.message || 'Erro ao criar lote');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (!loading) {
      setNome('');
      setPreco('');
      setObservacoes('');
      setStatus('privado');
      setError(null);
      onClose();
    }
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          border: '1px solid #e0e0e0',
          width: isSmallScreen ? '95%' : '80%', // Ajusta o tamanho para telas maiores
          maxWidth: isSmallScreen ? '95%' : '800px', // Define um limite máximo para telas grandes
        },
      }}
    >
      <DialogTitle
        sx={{
          backgroundColor: '#001f2e',
          color: 'white',
          fontWeight: 600,
          textAlign: isSmallScreen ? 'center' : 'left',
        }}
      >
        Criar Novo Lote
      </DialogTitle>

      <form onSubmit={handleSubmit}>
        <DialogContent sx={{ p: isSmallScreen ? 2 : 3 }}>
          {error && (
            <Box
              sx={{
                mb: 2,
                p: 2,
                backgroundColor: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: 2,
              }}
            >
              <Typography color="error" variant="body2">
                {error}
              </Typography>
            </Box>
          )}

          <Paper
            elevation={0}
            sx={{
              p: 2,
              mb: 3,
              backgroundColor: '#f8f9fa',
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography
              variant="h6"
              sx={{
                mb: 2,
                color: '#001f2e',
                fontWeight: 600,
                textAlign: isSmallScreen ? 'center' : 'left',
              }}
            >
              Blocos Selecionados ({selectedBlocks.length})
            </Typography>

            <Box
              sx={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 1,
                mb: 2,
                justifyContent: isSmallScreen ? 'center' : 'flex-start',
              }}
            >
              {selectedBlocksData.map(block => (
                <Chip
                  key={block.id}
                  label={`${block.titulo} - R$ ${block.valor}`}
                  variant="outlined"
                  size="small"
                  sx={{
                    borderColor: '#001f2e',
                    color: '#001f2e',
                  }}
                />
              ))}
            </Box>

            <Divider sx={{ my: 2 }} />

            <Box
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexDirection: isSmallScreen ? 'column' : 'row',
                gap: isSmallScreen ? 1 : 0,
              }}
            >
              <Typography variant="body2" color="text.secondary">
                Valor total dos blocos individuais:
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  fontWeight: 600,
                  color: '#001f2e',
                }}
              >
                R$ {totalValue.toFixed(2)}
              </Typography>
            </Box>
          </Paper>

          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              gap: 3,
            }}
          >
            <TextField
              required
              fullWidth
              label="Nome do Lote"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              placeholder="Ex: Lote Granito Premium"
              helperText="Um nome descritivo para identificar o lote"
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#001f2e',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#001f2e',
                },
              }}
            />

            <TextField
              required
              fullWidth
              label="Preço do Lote"
              type="number"
              inputProps={{
                min: 0,
                step: 0.01,
                placeholder: '0.00',
              }}
              value={preco}
              onChange={(e) => setPreco(e.target.value)}
              helperText={`Sugestão baseada nos blocos: R$ ${totalValue.toFixed(2)}`}
              InputProps={{
                startAdornment: <Box sx={{ mr: 1, color: '#666' }}>R$</Box>,
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#001f2e',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#001f2e',
                },
              }}
            />

            <TextField
              fullWidth
              label="Observações"
              multiline
              rows={3}
              value={observacoes}
              onChange={(e) => setObservacoes(e.target.value)}
              placeholder="Informações adicionais sobre o lote, condições especiais, etc..."
              helperText="Campo opcional para detalhes adicionais"
              sx={{
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#001f2e',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#001f2e',
                },
              }}
            />

            <FormControl>
              <FormLabel
                sx={{
                  color: '#001f2e',
                  fontWeight: 600,
                  '&.Mui-focused': {
                    color: '#001f2e',
                  },
                }}
              >
                Status do Lote
              </FormLabel>
              <RadioGroup
                value={status}
                onChange={(e) => setStatus(e.target.value as 'privado' | 'anunciado')}
                sx={{ mt: 1 }}
              >
                <FormControlLabel
                  value="privado"
                  control={
                    <Radio
                      sx={{
                        color: '#001f2e',
                        '&.Mui-checked': {
                          color: '#001f2e',
                        },
                      }}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        Privado
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Apenas você pode visualizar este lote
                      </Typography>
                    </Box>
                  }
                />
                <FormControlLabel
                  value="anunciado"
                  control={
                    <Radio
                      sx={{
                        color: '#001f2e',
                        '&.Mui-checked': {
                          color: '#001f2e',
                        },
                      }}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        Anunciado
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Visível para outros usuários na busca
                      </Typography>
                    </Box>
                  }
                />
              </RadioGroup>
            </FormControl>
          </Box>
        </DialogContent>

        <DialogActions sx={{ p: isSmallScreen ? 2 : 3, gap: 2 }}>
          <Button
            onClick={handleClose}
            disabled={loading}
            sx={{
              color: '#666',
              borderColor: '#e0e0e0',
              '&:hover': {
                backgroundColor: '#f5f5f5',
              },
            }}
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !nome || !preco || selectedBlocks.length === 0}
            sx={{
              backgroundColor: '#001f2e',
              '&:hover': {
                backgroundColor: '#003547',
              },
              '&:disabled': {
                backgroundColor: '#cccccc',
              },
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                Criando Lote...
              </>
            ) : (
              `Criar Lote (${selectedBlocks.length} blocos)`
            )}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default CreateLoteModal;