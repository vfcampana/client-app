import { Box, Paper, Typography, Chip, IconButton, Skeleton, Checkbox, Tabs, Tab, Dialog, DialogTitle, DialogContent, DialogActions, TextField, FormControl, FormLabel, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import { VisibilityOutlined, EditOutlined, ArchiveOutlined, CalendarTodayOutlined, AttachMoneyOutlined, Delete, Group, LocalOffer, Visibility, VisibilityOff } from '@mui/icons-material';
import StyledButton from '../StyledButton';
import { fetchBlocks } from '../../services/blocks';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import BlockModal from './BlockDetails';
import { Block } from '../../types/Blocks';
import SearchBar from '../SearchBar';
import { useNavigate } from 'react-router-dom';
import CreateLoteModal from '../lotes/CreateLoteModal';
import { useLotes, useDeleteLote, useUpdateLote } from '../../hooks/useLotes';
import LoteDetails from '../lotes/LoteDetails';

const stoneImageExample = require('../../assets/stone.png') as string;

const MyBlocks = () => {
  const { data: blocks, isLoading: blocksLoading } = useQuery({
    queryKey: ['blocos'],
    queryFn: fetchBlocks,
  });
  
  const { data: lotes, isLoading: lotesLoading } = useLotes();
  const deleteLoteMutation = useDeleteLote();
  const updateLoteMutation = useUpdateLote();
  
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState(0); // 0 = Blocos, 1 = Lotes
  
  // Estados para o sistema de lotes
  const [isSelectionMode, setIsSelectionMode] = useState(false);
  const [selectedBlocks, setSelectedBlocks] = useState<number[]>([]);
  const [showCreateLoteModal, setShowCreateLoteModal] = useState(false);
  
  //Função para abrir o modal de detalhes do bloco
  const [viewingLote, setViewingLote] = useState<any>(null);
  const [showViewModal, setShowViewModal] = useState(false);

  // Estados para editar lote
  const [editingLote, setEditingLote] = useState<any>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editForm, setEditForm] = useState({
    nome: '',
    preco: '',
    observacoes: '',
    status: 'privado' as 'privado' | 'anunciado'
  });
  
  const navigate = useNavigate();

  const filteredBlocks = blocks?.filter((block: Block) =>
    block.titulo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredLotes = lotes?.filter((lote: any) =>
    lote.nome.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Função para converter status do banco (0/1) para texto
  const getStatusText = (status: number | string | undefined): 'privado' | 'anunciado' => {
    // Se for undefined/null, assumir privado
    if (status === undefined || status === null) {
      return 'privado';
    }
    
    if (typeof status === 'number') {
      return status === 0 ? 'privado' : 'anunciado';
    }
    
    if (typeof status === 'string') {
      const lowerStatus = status.toLowerCase();
      if (lowerStatus === 'privado' || lowerStatus === '0') {
        return 'privado';
      }
      if (lowerStatus === 'anunciado' || lowerStatus === '1') {
        return 'anunciado';
      }
    }
    
    // Default
    return 'privado';
  };

  const handleViewLote = (lote: any) => {
    setViewingLote(lote);
    setShowViewModal(true);
  };

  // Função para alternar seleção de bloco
  const handleBlockSelection = (blockId: number) => {
    setSelectedBlocks(prev => 
      prev.includes(blockId) 
        ? prev.filter(id => id !== blockId)
        : [...prev, blockId]
    );
  };

  const handleEditBlock = (block: Block) => {
    navigate(`/blocks/${block.id}/edit`);
  };

  // Função para criar lote
  const handleCreateLote = () => {
    if (selectedBlocks.length === 0) {
      alert('Selecione pelo menos um bloco para criar o lote');
      return;
    }
    setShowCreateLoteModal(true);
  };

  // Função para cancelar seleção
  const handleCancelSelection = () => {
    setIsSelectionMode(false);
    setSelectedBlocks([]);
  };

  // Função chamada quando o lote é criado com sucesso
  const handleLoteSuccess = () => {
    setShowCreateLoteModal(false);
    setIsSelectionMode(false);
    setSelectedBlocks([]);
    alert('Lote criado com sucesso!');
  };

  // Função para excluir lote
  const handleDeleteLote = async (loteId: number) => {
    if (window.confirm('Tem certeza que deseja excluir este lote?')) {
      try {
        await deleteLoteMutation.mutateAsync(loteId);
        alert('Lote excluído com sucesso!');
      } catch (error) {
        alert('Erro ao excluir lote');
      }
    }
  };

  // Função para abrir modal de edição
  const handleEditLote = (lote: any) => {
    navigate(`/lotes/${lote.id}/edit`);
  };

  // Função para salvar edições do lote
  const handleSaveEdit = async () => {
    if (!editingLote) return;
    
    try {
      const updatedLote: any = {
        ...editingLote,
        nome: editForm.nome,
        preco: parseFloat(editForm.preco),
        observacoes: editForm.observacoes,
        status: editForm.status
      };
      
      await updateLoteMutation.mutateAsync({ id: editingLote.id, lote: updatedLote });
      setShowEditModal(false);
      setEditingLote(null);
      alert('Lote atualizado com sucesso!');
    } catch (error) {
      alert('Erro ao atualizar lote');
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
    setIsSelectionMode(false); // Desativa modo seleção ao trocar de aba
    setSelectedBlocks([]);
  };

  const isLoading = blocksLoading || lotesLoading;

  if (isLoading) {
    return (
      <div>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: 3, 
          padding: { xs: 2, md: 4 },
          maxWidth: '1200px',
          margin: '0 auto'
        }}>
          {[1, 2, 3].map((item) => (
            <Skeleton key={item} variant="rectangular" height={200} sx={{ borderRadius: 3 }} />
          ))}
        </Box>
      </div>
    );
  }

  return (
    <div>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      
      {/* Tabs para alternar entre Blocos e Lotes */}
      <Box sx={{ 
        padding: { xs: 2, md: 4 },
        maxWidth: '1200px',
        margin: '0 auto',
      }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          sx={{
            mb: 3,
            '& .MuiTab-root': {
              color: '#666',
              fontWeight: 600,
              '&.Mui-selected': {
                color: '#001f2e',
              }
            },
            '& .MuiTabs-indicator': {
              backgroundColor: '#001f2e',
            }
          }}
        >
          <Tab label={`Meus Blocos (${blocks?.length || 0})`} />
          <Tab label={`Meus Lotes (${lotes?.length || 0})`} />
        </Tabs>

        {/* Controles baseados na aba ativa */}
        <Box sx={{ 
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          mb: 2
        }}>
          
          {activeTab === 0 && (
            <Box sx={{ display: 'flex', gap: 2 }}>
              {!isSelectionMode ? (
                <StyledButton
                  variant="contained"
                  onClick={() => setIsSelectionMode(true)}
                  sx={{
                    backgroundColor: '#001f2e',
                    '&:hover': { backgroundColor: '#003547' }
                  }}
                >
                  Criar Lote
                </StyledButton>
              ) : (
                <>
                  <StyledButton
                    variant="outlined"
                    onClick={handleCancelSelection}
                    sx={{
                      borderColor: '#001f2e',
                      color: '#001f2e'
                    }}
                  >
                    Cancelar
                  </StyledButton>
                  <StyledButton
                    variant="contained"
                    onClick={handleCreateLote}
                    disabled={selectedBlocks.length === 0}
                    sx={{
                      backgroundColor: '#001f2e',
                      '&:hover': { backgroundColor: '#003547' }
                    }}
                  >
                    Criar Lote ({selectedBlocks.length})
                  </StyledButton>
                </>
              )}
            </Box>
          )}
        </Box>
      </Box>

      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: 3, 
        padding: { xs: 2, md: 4 },
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        {/* Conteúdo baseado na aba ativa */}
        {activeTab === 0 ? (
          // ABA DE BLOCOS
          <>
            {filteredBlocks?.length === 0 ? (
              <Box sx={{ 
                textAlign: 'center', 
                py: 8,
                color: '#6b7280'
              }}>
                <Typography variant="h6" gutterBottom>
                  Nenhum bloco encontrado
                </Typography>
                <Typography variant="body2">
                  Tente ajustar os filtros de busca
                </Typography>
              </Box>
            ) : (
              filteredBlocks?.map((block: Block) => {
                const statusText = getStatusText(block.status);
                
                return (
                  <Paper
                    key={block.id}
                    elevation={0}
                    sx={{
                      borderRadius: 4,
                      overflow: 'hidden',
                      border: isSelectionMode && selectedBlocks.includes(block.id) 
                        ? '2px solid #001f2e' 
                        : '1px solid #e5e7eb',
                      transition: 'all 0.3s ease',
                      backgroundColor: isSelectionMode && selectedBlocks.includes(block.id) 
                        ? '#f0f9ff' 
                        : '#ffffff',
                      '&:hover': {
                        borderColor: '#001f2e',
                        boxShadow: '0 12px 32px rgba(0, 31, 46, 0.12)',
                        transform: 'translateY(-2px)',
                      }
                    }}
                  >
                    {/* Header do Card de Bloco */}
                    <Box sx={{
                      background: 'linear-gradient(135deg, #001f2e 0%, #003547 100%)',
                      color: 'white',
                      padding: { xs: 2, md: 3 },
                    }}>
                      <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'flex-start',
                        flexDirection: { xs: 'column', sm: 'row' },
                        gap: 2
                      }}>
                        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
                          {isSelectionMode && (
                            <Checkbox
                              checked={selectedBlocks.includes(block.id)}
                              onChange={() => handleBlockSelection(block.id)}
                              sx={{
                                color: 'rgba(255,255,255,0.7)',
                                '&.Mui-checked': { color: 'white' }
                              }}
                            />
                          )}
                          
                          <Box>
                            <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                              {block.titulo}
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                              <Chip
                                label={block.material}
                                size="small"
                                sx={{
                                  backgroundColor: 'rgba(255,255,255,0.15)',
                                  color: 'white',
                                  border: '1px solid rgba(255,255,255,0.2)',
                                }}
                              />
                              {/* TAG DE STATUS DO BLOCO */}
                              <Chip
                                label={statusText === 'privado' ? 'Privado' : 'Anunciado'}
                                size="small"
                                sx={{
                                  backgroundColor: statusText === 'privado' 
                                    ? 'rgba(239, 68, 68, 0.9)' 
                                    : 'rgba(34, 197, 94, 0.9)',
                                  color: 'white',
                                  fontWeight: 'bold',
                                  '& .MuiChip-icon': {
                                    color: 'white'
                                  }
                                }}
                              />
                            </Box>
                          </Box>
                        </Box>
                        
                        {!isSelectionMode && (
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <IconButton
                              onClick={() => navigate(`/blocks/${block.id}`)}
                              sx={{
                                backgroundColor: 'rgba(255,255,255,0.15)',
                                color: 'white',
                                border: '1px solid rgba(255,255,255,0.2)',
                                borderRadius: 2,
                                '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' }
                              }}
                            >
                              <VisibilityOutlined fontSize="small" />
                            </IconButton>
                            
                            <IconButton
                              onClick={() => handleEditBlock(block)}
                              sx={{
                                backgroundColor: 'rgba(255,255,255,0.15)',
                                color: 'white',
                                border: '1px solid rgba(255,255,255,0.2)',
                                borderRadius: 2,
                                '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' }
                              }}
                            >
                              <EditOutlined fontSize="small" />
                            </IconButton>
                            
                            <IconButton
                              sx={{
                                backgroundColor: 'rgba(255,255,255,0.15)',
                                color: 'white',
                                border: '1px solid rgba(255,255,255,0.2)',
                                borderRadius: 2,
                                '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' }
                              }}
                            >
                              <ArchiveOutlined fontSize="small" />
                            </IconButton>
                          </Box>
                        )}
                      </Box>
                    </Box>

                    {/* Conteúdo do Card de Bloco */}
                    <Box sx={{ 
                      padding: { xs: 2, md: 3 },
                      display: 'flex',
                      flexDirection: { xs: 'column', md: 'row' },
                      gap: 3,
                      alignItems: { xs: 'center', md: 'flex-start' }
                    }}>
                      <Box sx={{ 
                        flex: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 2,
                        width: { xs: '100%', md: 'auto' }
                      }}>
                        <Box sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1.5,
                          padding: 2,
                          backgroundColor: '#f8fafc',
                          borderRadius: 2,
                          border: '1px solid #e2e8f0'
                        }}>
                          <CalendarTodayOutlined sx={{ color: '#001f2e', fontSize: 20 }} />
                          <Box>
                            <Typography variant="body2" color="#6b7280" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                              DATA DE REGISTRO
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 600, color: '#374151' }}>
                              {block.data_criacao}
                            </Typography>
                          </Box>
                        </Box>

                        <Box sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1.5,
                          padding: 2,
                          backgroundColor: '#f0fdf4',
                          borderRadius: 2,
                          border: '1px solid #bbf7d0'
                        }}>
                          <AttachMoneyOutlined sx={{ color: '#059669', fontSize: 20 }} />
                          <Box>
                            <Typography variant="body2" color="#065f46" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                              VALOR
                            </Typography>
                            <Typography variant="h6" sx={{ fontWeight: 700, color: '#065f46' }}>
                              R$ {block.valor}
                            </Typography>
                          </Box>
                        </Box>
                      </Box>

                      <Box sx={{
                        position: 'relative',
                        borderRadius: 3,
                        overflow: 'hidden',
                        boxShadow: '0 8px 24px rgba(0, 31, 46, 0.12)',
                        width: { xs: '100%', md: 250 },
                        height: { xs: 200, md: 180 },
                        maxWidth: { xs: 300, md: 'none' },
                        border: '3px solid #001f2e',
                        backgroundColor: '#f8fafc'
                      }}>
                        <img
                          src={block.imagem || stoneImageExample}
                          alt={`Imagem do bloco ${block.titulo}`}
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover',
                            display: 'block'
                          }}
                          onError={(e) => {
                            const target = e.target as HTMLImageElement;
                            target.src = stoneImageExample;
                          }}
                        />
                      </Box>
                    </Box>
                  </Paper>
                );
              })
            )}
          </>
        ) : (
          // ABA DE LOTES (mantém o código existente)
          <>
            {filteredLotes?.length === 0 ? (
              <Box sx={{ 
                textAlign: 'center', 
                py: 8,
                color: '#6b7280'
              }}>
                <LocalOffer sx={{ fontSize: 64, color: '#ccc', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Nenhum lote encontrado
                </Typography>
                <Typography variant="body2">
                  Crie lotes selecionando blocos na aba "Meus Blocos"
                </Typography>
              </Box>
            ) : (
              filteredLotes?.map((lote: any) => {
                // Converter status aqui para cada lote
                console.log("BLOCOS LOTE", lote.blocos);
                const statusText = getStatusText(lote.status);
                
                return (
                  <Paper
                    key={lote.id}
                    elevation={0}
                    sx={{
                      borderRadius: 4,
                      overflow: 'hidden',
                      border: '1px solid #e5e7eb',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        borderColor: '#001f2e',
                        boxShadow: '0 12px 32px rgba(0, 31, 46, 0.12)',
                        transform: 'translateY(-2px)',
                      }
                    }}
                  >
                    <Box sx={{
                      background: '#00334e',
                      color: 'white',
                      padding: { xs: 2, md: 3 },
                    }}>
                      <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'flex-start',
                        flexDirection: { xs: 'column', sm: 'row' },
                        gap: 2
                      }}>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                            {lote.nome}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            <Chip
                              icon={<Group />}
                              label={`${lote.blocos?.length || 0} blocos`}
                              size="small"
                              sx={{
                                backgroundColor: 'rgba(255,255,255,0.15)',
                                color: 'white',
                                border: '1px solid rgba(255,255,255,0.2)',
                              }}
                            />
                            <Chip
                              label={statusText === 'privado' ? 'Privado' : 'Anunciado'}
                              size="small"
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

                        <Box sx={{ display: 'flex', gap: 1 }}>
                          {/* Botão para VISUALIZAR */}
                          <IconButton
                            onClick={() => handleViewLote(lote)}
                            sx={{
                              backgroundColor: 'rgba(255,255,255,0.15)',
                              color: 'white',
                              border: '1px solid rgba(255,255,255,0.2)',
                              borderRadius: 2,
                              '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' }
                            }}
                          >
                            <VisibilityOutlined fontSize="small" />
                          </IconButton>

                          {/* Botão para EDITAR */}
                          <IconButton
                            onClick={() => handleEditLote(lote)}
                            sx={{
                              backgroundColor: 'rgba(255,255,255,0.15)',
                              color: 'white',
                              border: '1px solid rgba(255,255,255,0.2)',
                              borderRadius: 2,
                              '&:hover': { backgroundColor: 'rgba(255,255,255,0.25)' }
                            }}
                          >
                            <EditOutlined fontSize="small" />
                          </IconButton>
                          
                          {/* Botão para EXCLUIR */}
                          <IconButton
                            onClick={() => handleDeleteLote(lote.id)}
                            sx={{
                              backgroundColor: 'rgba(255,255,255,0.15)',
                              color: 'white',
                              border: '1px solid rgba(255,255,255,0.2)',
                              borderRadius: 2,
                              '&:hover': { backgroundColor: 'rgba(239, 68, 68, 0.8)' }
                            }}
                          >
                            <Delete fontSize="small" />
                          </IconButton>
                        </Box>
                      </Box>
                    </Box>

                    {/* Conteúdo do Card de Lote */}
                    <Box sx={{ padding: { xs: 2, md: 3 } }}>
                      <Box sx={{ 
                        display: 'flex',
                        flexDirection: { xs: 'column', md: 'row' },
                        gap: 3,
                      }}>
                        <Box sx={{ flex: 1 }}>
                          <Box sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1.5,
                            padding: 2,
                            backgroundColor: '#f0fdf4',
                            borderRadius: 2,
                            border: '1px solid #bbf7d0',
                            mb: 2
                          }}>
                            <AttachMoneyOutlined sx={{ color: '#059669', fontSize: 24 }} />
                            <Box>
                              <Typography variant="body2" color="#065f46" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                                PREÇO DO LOTE
                              </Typography>
                              <Typography variant="h5" sx={{ fontWeight: 700, color: '#065f46' }}>
                                R$ {lote.preco?.toFixed(2) || '0.00'}
                              </Typography>
                            </Box>
                          </Box>

                          {lote.observacoes && (
                            <Box sx={{
                              padding: 2,
                              backgroundColor: '#f8fafc',
                              borderRadius: 2,
                              border: '1px solid #e2e8f0'
                            }}>
                              <Typography variant="body2" color="#6b7280" sx={{ fontSize: '0.75rem', fontWeight: 500, mb: 1 }}>
                                OBSERVAÇÕES
                              </Typography>
                              <Typography variant="body2" sx={{ color: '#374151' }}>
                                {lote.observacoes}
                              </Typography>
                            </Box>
                          )}
                        </Box>

                        <Box sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 1.5,
                          padding: 2,
                          backgroundColor: '#fef3c7',
                          borderRadius: 2,
                          border: '1px solid #fcd34d',
                          width: { xs: '100%', md: 'auto' }
                        }}>
                          <CalendarTodayOutlined sx={{ color: '#d97706', fontSize: 20 }} />
                          <Box>
                            <Typography variant="body2" color="#92400e" sx={{ fontSize: '0.75rem', fontWeight: 500 }}>
                              CRIADO EM
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 600, color: '#92400e' }}>
                              {new Date(lote.data_criacao).toLocaleDateString('pt-BR')}
                            </Typography>
                          </Box>
                        </Box>
                      </Box>
                    </Box>
                  </Paper>
                );
              })
            )}
          </>
        )}
        
        {chosenBlock && (
          <BlockModal 
            open={open} 
            setOpen={setOpen} 
            chosenBlock={chosenBlock} 
          />
        )}

        {/* Modal para VISUALIZAR Lote */}
        {viewingLote && (
          <LoteDetails
            open={showViewModal}
            setOpen={setShowViewModal}
            lote={viewingLote}
            blocks={blocks || []}
          />
        )}

        {/* Modal de Criar Lote */}
        <CreateLoteModal
          open={showCreateLoteModal}
          onClose={() => setShowCreateLoteModal(false)}
          selectedBlocks={selectedBlocks}
          blocks={blocks || []}
          onSuccess={handleLoteSuccess}
        />

        {/* Modal de Editar Lote */}
        <Dialog 
          open={showEditModal} 
          onClose={() => setShowEditModal(false)}
          maxWidth="sm"
          fullWidth
          PaperProps={{
            sx: {
              borderRadius: 3,
              border: '1px solid #e0e0e0'
            }
          }}
        >
          <DialogTitle sx={{ 
            backgroundColor: '#7c3aed', 
            color: 'white',
            fontWeight: 600
          }}>
            Editar Lote
          </DialogTitle>
          <DialogContent sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Nome do Lote"
              value={editForm.nome}
              onChange={(e) => setEditForm({ ...editForm, nome: e.target.value })}
              sx={{ 
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#7c3aed',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#7c3aed',
                },
              }}
            />
            
            <TextField
              fullWidth
              label="Preço"
              type="number"
              value={editForm.preco}
              onChange={(e) => setEditForm({ ...editForm, preco: e.target.value })}
              sx={{ 
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#7c3aed',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#7c3aed',
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
              rows={3}
              value={editForm.observacoes}
              onChange={(e) => setEditForm({ ...editForm, observacoes: e.target.value })}
              sx={{ 
                mb: 2,
                '& .MuiOutlinedInput-root': {
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#7c3aed',
                  },
                },
                '& .MuiInputLabel-root.Mui-focused': {
                  color: '#7c3aed',
                },
              }}
            />
            
            <FormControl>
              <FormLabel 
                sx={{ 
                  color: '#7c3aed', 
                  fontWeight: 600,
                  '&.Mui-focused': {
                    color: '#7c3aed',
                  },
                }}
              >
                Status
              </FormLabel>
              <RadioGroup
                value={editForm.status}
                onChange={(e) => setEditForm({ ...editForm, status: e.target.value as 'privado' | 'anunciado' })}
                sx={{ mt: 1 }}
              >
                <FormControlLabel 
                  value="privado" 
                  control={
                    <Radio 
                      sx={{
                        color: '#7c3aed',
                        '&.Mui-checked': {
                          color: '#7c3aed',
                        },
                      }}
                    />
                  } 
                  label="Privado" 
                />
                
              </RadioGroup>
            </FormControl>
          </DialogContent>
          <DialogActions sx={{ p: 3, gap: 2 }}>
            <StyledButton 
              onClick={() => setShowEditModal(false)}
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
              onClick={handleSaveEdit}
              sx={{ 
                backgroundColor: '#7c3aed',
                '&:hover': {
                  backgroundColor: '#6d28d9',
                },
              }}
            >
              Salvar
            </StyledButton>
          </DialogActions>
        </Dialog>
      </Box>
    </div>
  );
};

export default MyBlocks;