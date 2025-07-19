import React, { useState } from 'react';
import { Box, IconButton, Typography, Card, CardMedia } from '@mui/material';
import { ArrowBackIos, ArrowForwardIos, Delete } from '@mui/icons-material';
import { ImagemBloco } from '../types/Blocks';

interface ImageCarouselProps {
  imagens: ImagemBloco[];
  onDeleteImage?: (imagemId: string) => void;
  showDeleteButton?: boolean;
}

export default function ImageCarousel({ 
  imagens, 
  onDeleteImage, 
  showDeleteButton = false 
}: ImageCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  if (!imagens || imagens.length === 0) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: 200, 
        bgcolor: 'grey.100',
        borderRadius: 1
      }}>
        <Typography variant="body2" color="text.secondary">
          Nenhuma imagem disponível
        </Typography>
      </Box>
    );
  }

  const nextImage = () => {
    setCurrentIndex((prev) => (prev + 1) % imagens.length);
  };

  const prevImage = () => {
    setCurrentIndex((prev) => (prev - 1 + imagens.length) % imagens.length);
  };

  const handleDeleteImage = () => {
    if (onDeleteImage && imagens[currentIndex]) {
      onDeleteImage(imagens[currentIndex].id);
      // Ajustar índice se necessário
      if (currentIndex >= imagens.length - 1) {
        setCurrentIndex(Math.max(0, imagens.length - 2));
      }
    }
  };

  return (
    <Box sx={{ 
      position: 'relative', 
      width: '100%', 
      height: '100%',
      overflow: 'hidden'
    }}>
      {/* Imagem Principal */}
      <Card sx={{ 
        position: 'relative', 
        width: '100%', 
        height: '100%',
        boxShadow: 'none',
        borderRadius: 0
      }}>
        <CardMedia
          component="img"
          image={imagens[currentIndex].url_imagem}
          alt={imagens[currentIndex].nome_arquivo}
          sx={{ 
            objectFit: 'cover',
            width: '100%',
            height: '100%'
          }}
        />
        
        {/* Botão de Deletar */}
        {showDeleteButton && onDeleteImage && (
          <IconButton
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              bgcolor: 'rgba(255, 255, 255, 0.8)',
              '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.9)' }
            }}
            onClick={handleDeleteImage}
            color="error"
          >
            <Delete />
          </IconButton>
        )}

        {/* Navegação */}
        {imagens.length > 1 && (
          <>
            <IconButton
              sx={{
                position: 'absolute',
                left: 8,
                top: '50%',
                transform: 'translateY(-50%)',
                bgcolor: 'rgba(0, 0, 0, 0.5)',
                color: 'white',
                '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.7)' }
              }}
              onClick={prevImage}
            >
              <ArrowBackIos />
            </IconButton>

            <IconButton
              sx={{
                position: 'absolute',
                right: 8,
                top: '50%',
                transform: 'translateY(-50%)',
                bgcolor: 'rgba(0, 0, 0, 0.5)',
                color: 'white',
                '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.7)' }
              }}
              onClick={nextImage}
            >
              <ArrowForwardIos />
            </IconButton>
          </>
        )}

        {/* Indicadores */}
        {imagens.length > 1 && (
          <Box
            sx={{
              position: 'absolute',
              bottom: 16,
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              gap: 1
            }}
          >
            {imagens.map((_, index) => (
              <Box
                key={index}
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  bgcolor: index === currentIndex ? 'white' : 'rgba(255, 255, 255, 0.5)',
                  cursor: 'pointer',
                  transition: 'background-color 0.3s'
                }}
                onClick={() => setCurrentIndex(index)}
              />
            ))}
          </Box>
        )}
      </Card>

      {/* Informações da Imagem */}
      <Box sx={{ mt: 1, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          {imagens[currentIndex].nome_arquivo}
        </Typography>
        {imagens.length > 1 && (
          <Typography variant="caption" color="text.secondary" sx={{ ml: 2 }}>
            {currentIndex + 1} de {imagens.length}
          </Typography>
        )}
      </Box>

      {/* Miniaturas */}
      {imagens.length > 1 && (
        <Box sx={{ 
          display: 'flex', 
          gap: 1, 
          mt: 2, 
          justifyContent: 'center',
          flexWrap: 'wrap',
          maxHeight: 100,
          overflow: 'auto'
        }}>
          {imagens.map((imagem, index) => (
            <Box
              key={imagem.id}
              sx={{
                width: 60,
                height: 60,
                border: index === currentIndex ? 2 : 1,
                borderColor: index === currentIndex ? 'primary.main' : 'grey.300',
                borderRadius: 1,
                overflow: 'hidden',
                cursor: 'pointer',
                transition: 'border-color 0.3s'
              }}
              onClick={() => setCurrentIndex(index)}
            >
              <img
                src={imagem.url_imagem}
                alt={imagem.nome_arquivo}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover'
                }}
              />
            </Box>
          ))}
        </Box>
      )}
    </Box>
  );
}
