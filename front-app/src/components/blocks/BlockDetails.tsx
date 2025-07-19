import * as React from 'react';
import { Box, Modal, Typography, styled, useTheme, useMediaQuery } from '@mui/material';
import { Block } from '../../types/Blocks';
import { formatDate } from '../../utils/utils';
import ImageCarousel from '../ImageCarousel';

const stoneImageExample = require('../../assets/stone.png') as string;

type BlockModalProps = {
  open: boolean;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
  chosenBlock: Block;
};

export default function BlockModal({ open, setOpen, chosenBlock }: BlockModalProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: { xs: '95%', sm: '90%', md: 700, lg: 800 },
    maxHeight: { xs: '90vh', sm: '85vh' },
    bgcolor: 'background.paper',
    border: '2px solid #0d1b2a',
    borderRadius: 4,
    boxShadow: 24,
    p: { xs: 2, sm: 3, md: 4 },
    overflow: 'auto'
  };

  return (
    <Modal
      open={open}
      onClose={() => setOpen(false)}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={modalStyle}>
        <Typography 
          id="modal-modal-title" 
          align="center" 
          variant={isMobile ? "h6" : "h5"} 
          component="h2"
          sx={{ 
            mb: { xs: 2, sm: 3 },
            fontWeight: 'bold',
            color: '#0d1b2a'
          }}
        >
          {chosenBlock.titulo}
        </Typography>

        <Box sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', md: 'row' },
          gap: { xs: 3, md: 4 },
          alignItems: { xs: 'center', md: 'flex-start' }
        }}>
          {/* Carrossel de imagens ou imagem padrão */}
          <Box sx={{ 
            width: { xs: '100%', md: 350 },
            maxWidth: { xs: 400, md: 350 },
            minWidth: { md: 350 },
            height: { xs: 250, sm: 280, md: 300 },
            flexShrink: 0
          }}>
            {chosenBlock.imagens && chosenBlock.imagens.length > 0 ? (
              <Box sx={{ 
                height: '100%',
                border: '3px solid #0d1b2a',
                borderRadius: 2,
                overflow: 'hidden',
                backgroundColor: '#f5f5f5'
              }}>
                <ImageCarousel 
                  imagens={chosenBlock.imagens} 
                  showDeleteButton={false}
                />
              </Box>
            ) : (
              <Box sx={{
                width: '100%',
                height: '100%',
                border: '3px solid #0d1b2a',
                borderRadius: 2,
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: '#f5f5f5'
              }}>
                <img 
                  src={stoneImageExample} 
                  alt="Imagem do bloco"
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover'
                  }}
                />
              </Box>
            )}
          </Box>
          
          {/* Informações do bloco */}
          <Box sx={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: { xs: 2, sm: 2.5 },
            width: { xs: '100%', md: 'auto' },
            minWidth: 0
          }}>
            <Box sx={{
              p: { xs: 2, sm: 3 },
              backgroundColor: '#f8fafc',
              borderRadius: 2,
              border: '1px solid #e2e8f0'
            }}>
              <Typography 
                variant={isMobile ? "body1" : "h6"} 
                sx={{ 
                  fontWeight: 'bold',
                  color: '#0d1b2a',
                  mb: 1
                }}
              >
                Material
              </Typography>
              <Typography 
                variant={isMobile ? "body2" : "body1"}
                color="text.secondary"
              >
                {chosenBlock.material}
              </Typography>
            </Box>

            <Box sx={{
              p: { xs: 2, sm: 3 },
              backgroundColor: '#f0fdf4',
              borderRadius: 2,
              border: '1px solid #bbf7d0'
            }}>
              <Typography 
                variant={isMobile ? "body1" : "h6"} 
                sx={{ 
                  fontWeight: 'bold',
                  color: '#059669',
                  mb: 1
                }}
              >
                Valor
              </Typography>
              <Typography 
                variant={isMobile ? "body1" : "h6"}
                sx={{ 
                  fontWeight: 'bold',
                  color: '#059669'
                }}
              >
                R$ {chosenBlock.valor}
              </Typography>
            </Box>

            <Box sx={{
              p: { xs: 2, sm: 3 },
              backgroundColor: '#fef3f2',
              borderRadius: 2,
              border: '1px solid #fecaca'
            }}>
              <Typography 
                variant={isMobile ? "body1" : "h6"} 
                sx={{ 
                  fontWeight: 'bold',
                  color: '#dc2626',
                  mb: 1
                }}
              >
                Data de Criação
              </Typography>
              <Typography 
                variant={isMobile ? "body2" : "body1"}
                color="text.secondary"
              >
                {formatDate(chosenBlock.data_criacao ?? '')}
              </Typography>
            </Box>

            {/* Informações adicionais */}
            {(chosenBlock.pedreira || chosenBlock.cidade) && (
              <Box sx={{
                p: { xs: 2, sm: 3 },
                backgroundColor: '#fffbeb',
                borderRadius: 2,
                border: '1px solid #fed7aa'
              }}>
                {chosenBlock.pedreira && (
                  <Box sx={{ mb: chosenBlock.cidade ? 2 : 0 }}>
                    <Typography 
                      variant={isMobile ? "body2" : "body1"} 
                      sx={{ 
                        fontWeight: 'bold',
                        color: '#ea580c'
                      }}
                    >
                      Pedreira
                    </Typography>
                    <Typography 
                      variant={isMobile ? "caption" : "body2"}
                      color="text.secondary"
                    >
                      {chosenBlock.pedreira}
                    </Typography>
                  </Box>
                )}
                
                {chosenBlock.cidade && (
                  <Box>
                    <Typography 
                      variant={isMobile ? "body2" : "body1"} 
                      sx={{ 
                        fontWeight: 'bold',
                        color: '#ea580c'
                      }}
                    >
                      Localização
                    </Typography>
                    <Typography 
                      variant={isMobile ? "caption" : "body2"}
                      color="text.secondary"
                    >
                      {chosenBlock.cidade}, {chosenBlock.estado}
                    </Typography>
                  </Box>
                )}
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </Modal>
  );
}
