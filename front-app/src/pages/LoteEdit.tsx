import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  Grid, 
  Chip, 
  IconButton,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Skeleton,
  Divider,
  Checkbox,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stack,
  useTheme,
  useMediaQuery
} from '@mui/material';
import { 
  ArrowBack, 
  AttachMoneyOutlined, 
  CalendarTodayOutlined, 
  Group, 
  LocalOffer,
  Save,
  Cancel,
  Add,
  Remove,
  Edit
} from '@mui/icons-material';
import { useLotes, useUpdateLote } from '../hooks/useLotes';
import { useQuery } from '@tanstack/react-query';
import { fetchBlocks } from '../services/blocks';
import StyledButton from '../components/StyledButton';
import { Block } from '../types/Blocks';
import { updateLote } from '../services/lotes';

const stoneImageExample = require('../assets/stone.png') as string;

const LoteEdit = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));
  
  const { data: lotes, isLoading: lotesLoading } = useLotes();
  const { data: blocks, isLoading: blocksLoading } = useQuery<Block[]>({
    queryKey: ['blocos'],
    queryFn: fetchBlocks,
  });
  const updateLoteMutation = useUpdateLote();

  const [editForm, setEditForm] = useState({
    nome: '',
    preco: '',
    observacoes: '',
    status: 'privado' as 'privado' | 'anunciado'
  });
  const [loading, setLoading] = useState(false);
  const [selectedBlockIds, setSelectedBlockIds] = useState<number[]>([]);
  const [showAddBlocksModal, setShowAddBlocksModal] = useState(false);

  // Encontrar o lote específico
  const lote = lotes?.find((l: any) => l.id === parseInt(id || '0'));

  // Função para converter status do banco (0/1) para texto
  const getStatusText = (status: number | string): 'privado' | 'anunciado' => {
    if (typeof status === 'number') {
      return status === 0 ? 'privado' : 'anunciado';
    }
    return status as 'privado' | 'anunciado';
  };

  // Carregar dados do lote quando encontrado
  useEffect(() => {
    if (lote) {
      setEditForm({
        nome: lote.nome || '',
        preco: lote.preco?.toString() || '0',
        observacoes: lote.observacoes || '',
        status: getStatusText(lote.status || 0)
      });
      setSelectedBlockIds(lote.blocos || []);
    }
  }, [lote]);

  // Filtrar os blocos que pertencem ao lote
  const loteBlocos = blocks?.filter((block: Block) => 
    selectedBlockIds.includes(block.id)
  ) || [];

  // Blocos disponíveis para adicionar (que não estão no lote)
  const availableBlocks = blocks?.filter((block: Block) => 
    !selectedBlockIds.includes(block.id)
  ) || [];

  const handleSave = async () => {
    if (!lote) return;
    
    setLoading(true);
    try {
      const updatedLote = {
        ...lote,
        nome: editForm.nome,
        preco: parseFloat(editForm.preco),
        observacoes: editForm.observacoes,
        status: editForm.status,
        blocos: selectedBlockIds 
      };
      
      await updateLote(lote.id, updatedLote);
      alert('Lote atualizado com sucesso!');
      navigate('/blocks');
    } catch (error) {
      alert('Erro ao atualizar lote');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/blocks');
  };

  const handleRemoveBlock = (blockId: number) => {
    setSelectedBlockIds(prev => prev.filter(id => id !== blockId));
  };

  const handleAddBlocks = (blockIds: number[]) => {
    setSelectedBlockIds(prev => [...prev, ...blockIds]);
    setShowAddBlocksModal(false);
  };

  if (lotesLoading || blocksLoading) {
    return (
      <Box sx={{ 
        padding: { xs: 1, sm: 2, md: 4 }, 
        maxWidth: '1200px', 
        margin: '0 auto' 
      }}>
        <Stack spacing={2}>
          <Skeleton variant="rectangular" width="100%" height={120} sx={{ borderRadius: 3 }} />
          <Skeleton variant="rectangular" width="100%" height={300} sx={{ borderRadius: 3 }} />
          <Skeleton variant="rectangular" width="100%" height={200} sx={{ borderRadius: 3 }} />
        </Stack>
      </Box>
    );
  }

  if (!lote) {
    return (
      <Box sx={{ 
        padding: { xs: 2, sm: 3, md: 4 }, 
        maxWidth: '1200px', 
        margin: '0 auto',
        textAlign: 'center'
      }}>
        <Typography variant={isMobile ? 'h6' : 'h5'} color="error" sx={{ mb: 2 }}>
          Lote não encontrado
        </Typography>
        <Button 
          onClick={() => navigate('/blocks')} 
          sx={{ mt: 2 }}
          variant="contained"
          fullWidth={isMobile}
        >
          Voltar
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      minHeight: '100vh',
      backgroundColor: '#f8fafc',
      padding: { xs: 1, sm: 2, md: 4 }
    }}>
      <Box sx={{ 
        maxWidth: '1200px', 
        margin: '0 auto',
        px: { xs: 1, sm: 0 }
      }}>
        {/* Header Responsivo */}
        <Paper sx={{
          background: 'linear-gradient(135deg, #001f2e 0%, #003547 100%)',
          color: 'white',
          padding: { xs: 2, sm: 2.5, md: 3 },
          borderRadius: { xs: 2, md: 3 },
          mb: { xs: 2, md: 3 },
          display: 'flex',
          flexDirection: { xs: 'column', sm: 'row' },
          alignItems: { xs: 'flex-start', sm: 'center' },
          gap: { xs: 2, sm: 2, md: 2 }
        }}>
          <IconButton 
            onClick={handleCancel}
            sx={{ 
              color: 'white',
              backgroundColor: 'rgba(255,255,255,0.15)',
              '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' },
              alignSelf: { xs: 'flex-start', sm: 'center' }
            }}
          >
            <ArrowBack />
          </IconButton>
          
          <Box sx={{ flex: 1, width: { xs: '100%', sm: 'auto' } }}>
            <Typography 
              variant={isMobile ? 'h5' : 'h4'} 
              sx={{ 
                fontWeight: 700, 
                mb: 1,
                wordBreak: 'break-word'
              }}
            >
              {isMobile ? 'Editando:' : 'Editando Lote:'} {lote.nome}
            </Typography>
            <Stack 
              direction={isMobile ? 'column' : 'row'} 
              spacing={1} 
              sx={{ flexWrap: 'wrap' }}
            >
              <Chip
                icon={<Group />}
                label={`${selectedBlockIds.length} blocos`}
                size={isMobile ? 'small' : 'medium'}
                sx={{
                  backgroundColor: 'rgba(255,255,255,0.15)',
                  color: 'white',
                  border: '1px solid rgba(255,255,255,0.2)',
                  alignSelf: 'flex-start'
                }}
              />
              <Chip
                icon={<LocalOffer />}
                label={`ID: ${lote.id}`}
                size={isMobile ? 'small' : 'medium'}
                sx={{
                  backgroundColor: 'rgba(255,255,255,0.15)',
                  color: 'white',
                  border: '1px solid rgba(255,255,255,0.2)',
                  alignSelf: 'flex-start'
                }}
              />
            </Stack>
          </Box>

          <Stack 
            direction={isMobile ? 'column' : 'row'} 
            spacing={1}
            sx={{ 
              width: { xs: '100%', sm: 'auto' },
              mt: { xs: 1, sm: 0 }
            }}
          >
            <StyledButton
              variant="outlined"
              onClick={handleCancel}
              size={isMobile ? 'medium' : 'large'}
              fullWidth={isMobile}
              sx={{
                color: 'white',
                borderColor: 'rgba(255,255,255,0.5)',
                '&:hover': {
                  borderColor: 'white',
                  backgroundColor: 'rgba(255,255,255,0.1)'
                }
              }}
              startIcon={<Cancel />}
            >
              Cancelar
            </StyledButton>
            <StyledButton
              variant="contained"
              onClick={handleSave}
              disabled={loading}
              size={isMobile ? 'medium' : 'large'}
              fullWidth={isMobile}
              sx={{
                backgroundColor: 'white',
                color: '#001f2e',
                '&:hover': {
                  backgroundColor: '#f8fafc'
                }
              }}
              startIcon={<Save />}
            >
              {loading ? 'Salvando...' : 'Salvar'}
            </StyledButton>
          </Stack>
        </Paper>

        {/* Conteúdo Principal Responsivo */}
        <Grid container spacing={{ xs: 2, md: 3 }}>
          {/* Formulário de Edição */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ 
              padding: { xs: 2, sm: 2.5, md: 3 }, 
              borderRadius: { xs: 2, md: 3 },
              height: 'fit-content'
            }}>
              <Typography 
                variant={isMobile ? 'subtitle1' : 'h6'} 
                sx={{ 
                  mb: { xs: 2, md: 3 }, 
                  color: '#001f2e', 
                  fontWeight: 600 
                }}
              >
                Informações do Lote
              </Typography>

              <Stack spacing={{ xs: 2, md: 3 }}>
                <TextField
                  fullWidth
                  label="Nome do Lote"
                  value={editForm.nome}
                  onChange={(e) => setEditForm({ ...editForm, nome: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
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
                  label="Preço"
                  type="number"
                  value={editForm.preco}
                  onChange={(e) => setEditForm({ ...editForm, preco: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
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
                  InputProps={{
                    startAdornment: <Box sx={{ mr: 1, color: '#666' }}>R$</Box>,
                  }}
                />

                <TextField
                  fullWidth
                  label="Observações"
                  multiline
                  rows={isMobile ? 3 : 4}
                  value={editForm.observacoes}
                  onChange={(e) => setEditForm({ ...editForm, observacoes: e.target.value })}
                  size={isMobile ? 'small' : 'medium'}
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
                      fontSize: { xs: '0.875rem', md: '1rem' },
                      '&.Mui-focused': {
                        color: '#001f2e',
                      },
                    }}
                  >
                    Status do Lote
                  </FormLabel>
                  <RadioGroup
                    value={editForm.status}
                    onChange={(e) => setEditForm({ ...editForm, status: e.target.value as 'privado' | 'anunciado' })}
                    sx={{ mt: 1 }}
                    row={!isMobile}
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
                      label="Privado"
                      sx={{
                        '& .MuiFormControlLabel-label': {
                          fontSize: { xs: '0.875rem', md: '1rem' }
                        }
                      }}
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
                      label="Anunciado"
                      sx={{
                        '& .MuiFormControlLabel-label': {
                          fontSize: { xs: '0.875rem', md: '1rem' }
                        }
                      }}
                    />
                  </RadioGroup>
                </FormControl>
              </Stack>
            </Paper>
          </Grid>

          {/* Informações Atuais */}
          <Grid item xs={12} lg={6}>
            <Paper sx={{ 
              padding: { xs: 2, sm: 2.5, md: 3 }, 
              borderRadius: { xs: 2, md: 3 },
              height: 'fit-content'
            }}>
              <Typography 
                variant={isMobile ? 'subtitle1' : 'h6'} 
                sx={{ 
                  mb: { xs: 2, md: 3 }, 
                  color: '#001f2e', 
                  fontWeight: 600 
                }}
              >
                Informações Atuais
              </Typography>

              <Stack spacing={2}>
                <Box sx={{
                  padding: { xs: 1.5, md: 2 },
                  backgroundColor: '#f0fdf4',
                  border: '1px solid #bbf7d0',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1.5,
                }}>
                  <AttachMoneyOutlined sx={{ 
                    color: '#059669', 
                    fontSize: { xs: 24, md: 28 } 
                  }} />
                  <Box>
                    <Typography 
                      variant="body2" 
                      color="#065f46" 
                      sx={{ 
                        fontSize: { xs: '0.7rem', md: '0.75rem' }, 
                        fontWeight: 500 
                      }}
                    >
                      PREÇO ATUAL
                    </Typography>
                    <Typography 
                      variant={isMobile ? 'h6' : 'h5'} 
                      sx={{ fontWeight: 700, color: '#065f46' }}
                    >
                      R$ {lote.preco?.toFixed(2) || '0.00'}
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{
                  padding: { xs: 1.5, md: 2 },
                  backgroundColor: '#fef3c7',
                  border: '1px solid #fcd34d',
                  borderRadius: 2,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1.5,
                }}>
                  <CalendarTodayOutlined sx={{ 
                    color: '#d97706', 
                    fontSize: { xs: 24, md: 28 } 
                  }} />
                  <Box>
                    <Typography 
                      variant="body2" 
                      color="#92400e" 
                      sx={{ 
                        fontSize: { xs: '0.7rem', md: '0.75rem' }, 
                        fontWeight: 500 
                      }}
                    >
                      CRIADO EM
                    </Typography>
                    <Typography 
                      variant={isMobile ? 'body1' : 'h6'} 
                      sx={{ fontWeight: 600, color: '#92400e' }}
                    >
                      {lote.data_criacao 
                        ? new Date(lote.data_criacao).toLocaleDateString('pt-BR')
                        : 'Data não disponível'
                      }
                    </Typography>
                  </Box>
                </Box>
              </Stack>
            </Paper>
          </Grid>

          {/* Blocos do Lote */}
          <Grid item xs={12}>
            <Paper sx={{ 
              padding: { xs: 2, sm: 2.5, md: 3 }, 
              borderRadius: { xs: 2, md: 3 } 
            }}>
              <Box sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: { xs: 'flex-start', sm: 'center' },
                flexDirection: { xs: 'column', sm: 'row' },
                gap: { xs: 2, sm: 0 },
                mb: { xs: 2, md: 3 }
              }}>
                <Typography 
                  variant={isMobile ? 'subtitle1' : 'h6'} 
                  sx={{ color: '#001f2e', fontWeight: 600 }}
                >
                  Blocos inclusos no lote ({loteBlocos.length})
                </Typography>
                <StyledButton
                  variant="contained"
                  onClick={() => setShowAddBlocksModal(true)}
                  startIcon={<Add />}
                  size={isMobile ? 'small' : 'medium'}
                  fullWidth={isMobile}
                  sx={{
                    backgroundColor: '#001f2e',
                    '&:hover': {
                      backgroundColor: '#003547'
                    }
                  }}
                >
                  Adicionar Blocos
                </StyledButton>
              </Box>

              {loteBlocos.length === 0 ? (
                <Box sx={{
                  padding: { xs: 2, md: 3 },
                  textAlign: 'center',
                  backgroundColor: '#f9fafb',
                  border: '1px solid #e5e7eb',
                  borderRadius: 2,
                }}>
                  <Typography 
                    variant="body2" 
                    color="#6b7280"
                    sx={{ fontSize: { xs: '0.875rem', md: '1rem' } }}
                  >
                    Nenhum bloco selecionado para este lote
                  </Typography>
                </Box>
              ) : (
                <Grid container spacing={{ xs: 1.5, sm: 2 }}>
                  {loteBlocos.map((block: Block) => (
                    <Grid 
                      item 
                      xs={6} 
                      sm={4} 
                      md={3} 
                      lg={2.4} 
                      key={block.id}
                    >
                      <Paper sx={{
                        padding: { xs: 1, sm: 1.5, md: 2 },
                        border: '1px solid #e5e7eb',
                        borderRadius: 2,
                        position: 'relative',
                        '&:hover': {
                          borderColor: '#001f2e',
                          boxShadow: '0 4px 12px rgba(0, 31, 46, 0.15)',
                        },
                        transition: 'all 0.3s ease',
                      }}>
                        {/* Botão de remover */}
                        <IconButton
                          onClick={() => handleRemoveBlock(block.id)}
                          sx={{
                            position: 'absolute',
                            top: { xs: 4, md: 8 },
                            right: { xs: 4, md: 8 },
                            backgroundColor: '#ef4444',
                            color: 'white',
                            width: { xs: 24, md: 32 },
                            height: { xs: 24, md: 32 },
                            '&:hover': {
                              backgroundColor: '#dc2626'
                            },
                            zIndex: 1
                          }}
                          size="small"
                        >
                          <Remove fontSize="small" />
                        </IconButton>

                        <Box sx={{
                          width: '100%',
                          height: { xs: 80, sm: 100, md: 120 },
                          borderRadius: 2,
                          overflow: 'hidden',
                          border: '2px solid #001f2e',
                          mb: { xs: 1, md: 2 }
                        }}>
                          <img 
                            src={block.imagem || stoneImageExample} 
                            alt={`Imagem do bloco ${block.titulo}`}
                            style={{
                              width: '100%',
                              height: '100%',
                              objectFit: 'cover'
                            }}
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.src = stoneImageExample;
                            }}
                          />
                        </Box>
                        
                        <Typography 
                          variant={isMobile ? 'caption' : 'subtitle2'} 
                          sx={{ 
                            fontWeight: 600, 
                            mb: 0.5,
                            wordBreak: 'break-word',
                            fontSize: { xs: '0.75rem', sm: '0.875rem' }
                          }}
                        >
                          {block.titulo}
                        </Typography>
                        
                        <Chip
                          label={block.material}
                          size="small"
                          sx={{
                            backgroundColor: '#f3f4f6',
                            color: '#374151',
                            fontSize: { xs: '0.65rem', sm: '0.75rem' },
                            mb: 0.5,
                            height: { xs: 20, sm: 24 }
                          }}
                        />
                        
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: '#059669', 
                            fontWeight: 600,
                            fontSize: { xs: '0.75rem', sm: '0.875rem' }
                          }}
                        >
                          R$ {block.valor}
                        </Typography>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Paper>
          </Grid>
        </Grid>

        {/* Modal para Adicionar Blocos */}
        <AddBlocksModal
          open={showAddBlocksModal}
          onClose={() => setShowAddBlocksModal(false)}
          availableBlocks={availableBlocks}
          onAddBlocks={handleAddBlocks}
          isMobile={isMobile}
        />
      </Box>
    </Box>
  );
};

// Componente Modal para Adicionar Blocos - Também Responsivo
const AddBlocksModal = ({ 
  open, 
  onClose, 
  availableBlocks, 
  onAddBlocks,
  isMobile 
}: {
  open: boolean;
  onClose: () => void;
  availableBlocks: Block[];
  onAddBlocks: (blockIds: number[]) => void;
  isMobile: boolean;
}) => {
  const [selectedBlocks, setSelectedBlocks] = useState<number[]>([]);

  const handleToggleBlock = (blockId: number) => {
    setSelectedBlocks(prev => 
      prev.includes(blockId) 
        ? prev.filter(id => id !== blockId)
        : [...prev, blockId]
    );
  };

  const handleAdd = () => {
    onAddBlocks(selectedBlocks);
    setSelectedBlocks([]);
  };

  const handleClose = () => {
    setSelectedBlocks([]);
    onClose();
  };

  return (
    <Dialog 
      open={open} 
      onClose={handleClose}
      maxWidth="md"
      fullWidth
      fullScreen={isMobile}
      PaperProps={{
        sx: {
          borderRadius: isMobile ? 0 : 3,
          border: isMobile ? 'none' : '1px solid #e0e0e0',
          margin: isMobile ? 0 : 2,
          width: isMobile ? '100%' : 'auto',
          height: isMobile ? '100%' : 'auto'
        }
      }}
    >
      <DialogTitle sx={{ 
        backgroundColor: '#001f2e', 
        color: 'white',
        fontWeight: 600,
        fontSize: { xs: '1.1rem', md: '1.25rem' },
        padding: { xs: 2, md: 3 }
      }}>
        Adicionar Blocos ao Lote
      </DialogTitle>
      <DialogContent sx={{ 
        mt: 2, 
        padding: { xs: 2, md: 3 },
        height: isMobile ? 'calc(100vh - 140px)' : 'auto',
        overflow: 'auto'
      }}>
        {availableBlocks.length === 0 ? (
          <Typography 
            variant="body1" 
            sx={{ 
              textAlign: 'center', 
              py: 4,
              fontSize: { xs: '0.875rem', md: '1rem' }
            }}
          >
            Todos os blocos já estão inclusos no lote ou não há blocos disponíveis.
          </Typography>
        ) : (
          <Grid container spacing={{ xs: 1.5, sm: 2 }}>
            {availableBlocks.map((block) => (
              <Grid item xs={6} sm={4} md={4} key={block.id}>
                <Paper sx={{
                  padding: { xs: 1, sm: 1.5, md: 2 },
                  border: selectedBlocks.includes(block.id) 
                    ? '2px solid #001f2e' 
                    : '1px solid #e5e7eb',
                  borderRadius: 2,
                  cursor: 'pointer',
                  backgroundColor: selectedBlocks.includes(block.id) 
                    ? '#f0f9ff' 
                    : '#ffffff',
                  '&:hover': {
                    borderColor: '#001f2e',
                    boxShadow: '0 4px 12px rgba(0, 31, 46, 0.15)',
                  },
                  transition: 'all 0.3s ease',
                }}
                onClick={() => handleToggleBlock(block.id)}
                >
                  <Box sx={{ position: 'relative' }}>
                    <Checkbox
                      checked={selectedBlocks.includes(block.id)}
                      sx={{
                        position: 'absolute',
                        top: -8,
                        right: -8,
                        color: '#001f2e',
                        zIndex: 1,
                        '&.Mui-checked': {
                          color: '#001f2e',
                        },
                        '& .MuiSvgIcon-root': {
                          fontSize: { xs: '1.2rem', md: '1.5rem' }
                        }
                      }}
                    />
                    
                    <Box sx={{
                      width: '100%',
                      height: { xs: 60, sm: 70, md: 80 },
                      borderRadius: 2,
                      overflow: 'hidden',
                      border: '2px solid #001f2e',
                      mb: 1
                    }}>
                      <img 
                        src={block.imagem || require('../assets/stone.png')} 
                        alt={`Imagem do bloco ${block.titulo}`}
                        style={{
                          width: '100%',
                          height: '100%',
                          objectFit: 'cover'
                        }}
                      />
                    </Box>
                    
                    <Typography 
                      variant={isMobile ? 'caption' : 'subtitle2'} 
                      sx={{ 
                        fontWeight: 600, 
                        mb: 0.5,
                        wordBreak: 'break-word',
                        fontSize: { xs: '0.7rem', sm: '0.875rem' }
                      }}
                    >
                      {block.titulo}
                    </Typography>
                    
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: '#059669', 
                        fontWeight: 600,
                        fontSize: { xs: '0.7rem', sm: '0.875rem' }
                      }}
                    >
                      R$ {block.valor}
                    </Typography>
                  </Box>
                </Paper>
              </Grid>
            ))}
          </Grid>
        )}
      </DialogContent>
      <DialogActions sx={{ 
        p: { xs: 2, md: 3 }, 
        gap: { xs: 1, md: 2 },
        flexDirection: { xs: 'column', sm: 'row' }
      }}>
        <StyledButton 
          onClick={handleClose}
          fullWidth={isMobile}
          sx={{
            color: '#666',
            borderColor: '#e0e0e0',
            '&:hover': {
              backgroundColor: '#f5f5f5',
            },
          }}
        >
          Cancelar
        </StyledButton>
        <StyledButton 
          variant="contained" 
          onClick={handleAdd}
          disabled={selectedBlocks.length === 0}
          fullWidth={isMobile}
          sx={{ 
            backgroundColor: '#001f2e',
            '&:hover': {
              backgroundColor: '#003547',
            },
          }}
        >
          Adicionar ({selectedBlocks.length})
        </StyledButton>
      </DialogActions>
    </Dialog>
  );
};

export default LoteEdit;