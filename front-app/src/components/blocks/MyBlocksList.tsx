import { Box, Paper, Typography, Chip, IconButton, Skeleton } from '@mui/material';
import { VisibilityOutlined, EditOutlined, ArchiveOutlined, CalendarTodayOutlined, AttachMoneyOutlined } from '@mui/icons-material';
import StyledButton from '../StyledButton';
import { fetchBlocks, getBlock } from '../../services/blocks';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import BlockModal from './BlockDetails';
import { Block } from '../../types/Blocks';
import SearchBar from '../SearchBar';
import { useNavigate } from 'react-router-dom';

const stoneImageExample = require('../../assets/stone.png') as string;

const MyBlocks = () => {
  const { data: blocks, isLoading, error } = useQuery({
    queryKey: ['blocos'],
    queryFn: fetchBlocks,
  });
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const filteredBlocks = blocks?.filter((block: Block) =>
    block.titulo.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        gap: 3, 
        padding: { xs: 2, md: 4 },
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
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
          filteredBlocks?.map((block: Block) => (
            <Paper
              key={block.id}
              elevation={0}
              sx={{
                borderRadius: 4,
                overflow: 'hidden',
                border: '1px solid #e5e7eb',
                transition: 'all 0.3s ease',
                backgroundColor: '#ffffff',
                '&:hover': {
                  borderColor: '#001f2e',
                  boxShadow: '0 12px 32px rgba(0, 31, 46, 0.12)',
                  transform: 'translateY(-2px)',
                }
              }}
            >
              {/* Header do Card */}
              <Box sx={{
                background: 'linear-gradient(135deg, #001f2e 0%, #003547 100%)',
                color: 'white',
                padding: { xs: 2, md: 3 },
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: 0,
                  right: 0,
                  width: '100px',
                  height: '100px',
                  background: 'rgba(255,255,255,0.05)',
                  borderRadius: '50%',
                  transform: 'translate(30px, -30px)',
                }
              }}>
                <Box sx={{ 
                  display: 'flex', 
                  justifyContent: 'space-between', 
                  alignItems: 'flex-start',
                  flexDirection: { xs: 'column', sm: 'row' },
                  gap: 2
                }}>
                  <Box sx={{ flex: 1 }}>
                    <Typography 
                      variant="h5" 
                      sx={{ 
                        fontWeight: 700,
                        fontSize: { xs: '1.25rem', md: '1.5rem' },
                        marginBottom: 1,
                        letterSpacing: '-0.025em'
                      }}
                    >
                      {block.titulo}
                    </Typography>
                    <Chip
                      label={block.material}
                      size="small"
                      sx={{
                        backgroundColor: 'rgba(255,255,255,0.15)',
                        color: 'white',
                        fontWeight: 500,
                        border: '1px solid rgba(255,255,255,0.2)',
                        '&:hover': {
                          backgroundColor: 'rgba(255,255,255,0.2)',
                        }
                      }}
                    />
                  </Box>
                  
                  {/* Botões de Ação */}
                  <Box sx={{ 
                    display: 'flex', 
                    gap: 1,
                    flexDirection: { xs: 'row', sm: 'row' },
                    width: { xs: '100%', sm: 'auto' }
                  }}>
                    <IconButton
                      onClick={() => navigate(`/blocks/${block.id}`)}
                      sx={{
                        backgroundColor: 'rgba(255,255,255,0.15)',
                        color: 'white',
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: 2,
                        padding: { xs: 1, md: 1.5 },
                        flex: { xs: 1, sm: 'none' },
                        '&:hover': {
                          backgroundColor: 'rgba(255,255,255,0.25)',
                          transform: 'translateY(-2px)',
                        }
                      }}
                    >
                      <VisibilityOutlined fontSize="small" />
                    </IconButton>
                    
                    <IconButton
                      sx={{
                        backgroundColor: 'rgba(255,255,255,0.15)',
                        color: 'white',
                        border: '1px solid rgba(255,255,255,0.2)',
                        borderRadius: 2,
                        padding: { xs: 1, md: 1.5 },
                        flex: { xs: 1, sm: 'none' },
                        '&:hover': {
                          backgroundColor: 'rgba(255,255,255,0.25)',
                          transform: 'translateY(-2px)',
                        }
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
                        padding: { xs: 1, md: 1.5 },
                        flex: { xs: 1, sm: 'none' },
                        '&:hover': {
                          backgroundColor: 'rgba(255,255,255,0.25)',
                          transform: 'translateY(-2px)',
                        }
                      }}
                    >
                      <ArchiveOutlined fontSize="small" />
                    </IconButton>
                  </Box>
                </Box>
              </Box>

              {/* Conteúdo do Card */}
              <Box sx={{ 
                padding: { xs: 2, md: 3 },
                display: 'flex',
                flexDirection: { xs: 'column', md: 'row' },
                gap: 3,
                alignItems: { xs: 'center', md: 'flex-start' }
              }}>
                {/* Informações */}
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

                {/* Imagem */}
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
                      transition: 'transform 0.3s ease',
                      display: 'block'
                    }}
                    onError={(e) => {
                      // Fallback para imagem padrão se a imagem do bloco falhar
                      const target = e.target as HTMLImageElement;
                      target.src = stoneImageExample;
                    }}
                    onMouseEnter={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.transform = 'scale(1.05)';
                    }}
                    onMouseLeave={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.transform = 'scale(1)';
                    }}
                  />
                  <Box sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: 'linear-gradient(135deg, transparent 60%, rgba(0, 31, 46, 0.08) 100%)',
                    pointerEvents: 'none'
                  }} />
                </Box>
              </Box>
            </Paper>
          ))
        )}
        
        {chosenBlock && (
          <BlockModal 
            open={open} 
            setOpen={setOpen} 
            chosenBlock={chosenBlock} 
          />
        )}
      </Box>
    </div>
  );
};

export default MyBlocks;