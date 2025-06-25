import * as React from 'react';
import { Box, Modal, Typography, styled, Chip, Divider, Grid, Paper } from '@mui/material';
import { AttachMoneyOutlined, CalendarTodayOutlined, Group, LocalOffer } from '@mui/icons-material';

const stoneImageExample = require('../../assets/stone.png') as string;

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  maxWidth: 800,
  bgcolor: 'background.paper',
  border: '2px solid #00334ed',
  borderRadius: 4,
  boxShadow: 24,
  p: 0,
  maxHeight: '90vh',
  overflow: 'auto',
};

const StyledImage = styled('img')({
  border: '3px solid #00334e',
  borderRadius: '8px',
  width: '100%',
  height: 120,
  objectFit: 'cover',
});

type LoteDetailsProps = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  lote: any;
  blocks?: any[];
};

export default function LoteDetails({ open, setOpen, lote, blocks = [] }: LoteDetailsProps) {
  if (!lote) return null;

  const getStatusText = (status: number | string): 'privado' | 'anunciado' => {
    if (typeof status === 'number') {
      return status === 0 ? 'privado' : 'anunciado';
    }
    return status as 'privado' | 'anunciado';
  };

  const statusText = getStatusText(lote.status);

  // Filtrar os blocos que pertencem ao lote
  const loteBlocos = blocks.filter(block => 
    lote.blocos?.includes(block.id)
  );

  return (
    <Modal
      open={open}
      onClose={() => setOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        {/* Header */}
        <Box sx={{
          background: '#00334e',
          color: 'white',
          padding: 3,
          borderRadius: '16px 16px 0 0',
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
            <LocalOffer sx={{ fontSize: 32 }} />
            <Typography variant="h4" component="h2" sx={{ fontWeight: 700 }}>
              {lote.nome}
            </Typography>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            <Chip
              icon={<Group />}
              label={`${lote.blocos?.length || 0} blocos`}
              sx={{
                backgroundColor: 'rgba(255,255,255,0.15)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.2)',
              }}
            />
            <Chip
              label={statusText === 'privado' ? 'Privado' : 'Anunciado'}
              sx={{
                backgroundColor: statusText === 'privado' 
                  ? 'rgba(239, 68, 68, 0.8)' 
                  : 'rgba(34, 197, 94, 0.8)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.2)',
              }}
            />
          </Box>
        </Box>

        {/* Conteúdo */}
        <Box sx={{ padding: 3 }}>
          {/* Informações principais */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={6}>
              <Paper sx={{
                padding: 2,
                backgroundColor: '#f0fdf4',
                border: '1px solid #bbf7d0',
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                gap: 1.5,
              }}>
                <AttachMoneyOutlined sx={{ color: '#059669', fontSize: 28 }} />
                <Box>
                  <Typography variant="body2" color="#065f46" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                    PREÇO DO LOTE
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, color: '#065f46' }}>
                    R$ {lote.preco?.toFixed(2) || '0.00'}
                  </Typography>
                </Box>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{
                padding: 2,
                backgroundColor: '#fef3c7',
                border: '1px solid #fcd34d',
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                gap: 1.5,
              }}>
                <CalendarTodayOutlined sx={{ color: '#d97706', fontSize: 28 }} />
                <Box>
                  <Typography variant="body2" color="#92400e" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                    CRIADO EM
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 600, color: '#92400e' }}>
                    {new Date(lote.data_criacao).toLocaleDateString('pt-BR')}
                  </Typography>
                </Box>
              </Paper>
            </Grid>
          </Grid>

          {/* Observações */}
          {lote.observacoes && (
            <>
              <Paper sx={{
                padding: 2,
                backgroundColor: '#f8fafc',
                border: '1px solid #e2e8f0',
                borderRadius: 2,
                mb: 3,
              }}>
                <Typography variant="body2" color="#6b7280" sx={{ fontSize: '0.75rem', fontWeight: 500, mb: 1 }}>
                  OBSERVAÇÕES
                </Typography>
                <Typography variant="body1" sx={{ color: '#374151' }}>
                  {lote.observacoes}
                </Typography>
              </Paper>
            </>
          )}

          {/* Blocos do Lote */}
          <Divider sx={{ mb: 3 }} />
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, color: '#00334e' }}>
            Blocos inclusos no lote ({loteBlocos.length})
          </Typography>

          {loteBlocos.length === 0 ? (
            <Paper sx={{
              padding: 3,
              textAlign: 'center',
              backgroundColor: '#f9fafb',
              border: '1px solid #e5e7eb',
              borderRadius: 2,
            }}>
              <Typography variant="body2" color="#6b7280">
                Nenhum bloco encontrado para este lote
              </Typography>
            </Paper>
          ) : (
            <Grid container spacing={2}>
              {loteBlocos.map((block: any) => (
                <Grid item xs={12} sm={6} md={4} key={block.id}>
                  <Paper sx={{
                    padding: 2,
                    border: '1px solid #e5e7eb',
                    borderRadius: 2,
                    '&:hover': {
                      borderColor: '#00334e',
                      boxShadow: '0 4px 12px #00334e',
                    },
                    transition: 'all 0.3s ease',
                  }}>
                    <StyledImage 
                      src={block.imagem || stoneImageExample} 
                      alt={`Imagem do bloco ${block.titulo}`}
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = stoneImageExample;
                      }}
                    />
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                        {block.titulo}
                      </Typography>
                      <Chip
                        label={block.material}
                        size="small"
                        sx={{
                          backgroundColor: '#f3f4f6',
                          color: '#374151',
                          fontSize: '0.75rem',
                        }}
                      />
                      <Typography variant="body2" sx={{ mt: 1, color: '#059669', fontWeight: 600 }}>
                        R$ {block.valor}
                      </Typography>
                    </Box>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      </Box>
    </Modal>
  );
}