import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Container,
  CircularProgress,
  Paper,
  Divider,
} from '@mui/material';
import {
  FavoriteBorder,
  Search,
} from '@mui/icons-material';
import BlockCard from '../components/blocks/BlockCard';
import { useState, useEffect } from 'react';
import { Block } from '../types/Blocks';
import BlockModal from '../components/blocks/BlockDetails';
import SearchBar from '../components/SearchBar';
import { useFavoritos } from '../hooks/useFavoritos';

export default function Favorites() {
  const { fetchFavoritos, loading } = useFavoritos();
  const [favoriteBlocks, setFavoriteBlocks] = useState<Block[]>([]);
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadFavorites = async () => {
      try {
        setError(null);
        const result = await fetchFavoritos();
        if (result.success && result.data) {
          setFavoriteBlocks(result.data);
        } else {
          setFavoriteBlocks([]);
        }
      } catch (err) {
        console.error('Erro ao carregar favoritos:', err);
        setError('Erro ao carregar favoritos');
        setFavoriteBlocks([]);
      }
    };

    loadFavorites();
  }, [fetchFavoritos]);

  const viewBlock = (block: Block) => {
    try {
      setChosenBlock(block);
      setOpen(true);
    } catch (err) {
      console.error('Erro ao visualizar bloco:', err);
    }
  };

  const filteredBlocks = React.useMemo(() => {
    try {
      if (!favoriteBlocks || !Array.isArray(favoriteBlocks)) {
        return [];
      }
      return favoriteBlocks.filter((block: Block) =>
        block?.titulo?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    } catch (err) {
      console.error('Erro ao filtrar blocos:', err);
      return [];
    }
  }, [favoriteBlocks, searchTerm]);

  if (loading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        backgroundColor: '#ffffff'
      }}>
        <CircularProgress size={40} sx={{ color: '#001f2e' }} />
      </Box>
    );
  }

  return (
    <Box sx={{ backgroundColor: '#ffffff', minHeight: '100vh' }}>
      <Container maxWidth="lg" sx={{ py: 6 }}>

        <Box sx={{ mb: 4 }}>
          <SearchBar 
            searchTerm={searchTerm} 
            setSearchTerm={setSearchTerm} 
            showRegisterButton={false}
          />
          {favoriteBlocks.length > 0 && (
            <Typography 
              variant="body2" 
              sx={{ color: '#666666' }}
            >
              Favoritos - {favoriteBlocks.length} bloco{favoriteBlocks.length !== 1 ? 's' : ''}
            </Typography>
          )}
        </Box>
        
        <Divider sx={{ mb: 4, borderColor: '#e0e0e0' }} />


        {/* Erro silencioso*/}
        {error && process.env.NODE_ENV === 'development' && (
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Não foi possível carregar os favoritos
            </Typography>
          </Box>
        )}

        {/* Estado vazio */}
        {favoriteBlocks.length === 0 && !loading && (
          <Paper 
            elevation={0}
            sx={{ 
              textAlign: 'center', 
              py: 8,
              backgroundColor: '#f8f9fa',
              border: '1px solid #e0e0e0',
              borderRadius: 2
            }}
          >
            <FavoriteBorder sx={{ fontSize: 48, color: '#cccccc', mb: 2 }} />
            <Typography variant="h6" sx={{ color: '#001f2e', mb: 1, fontWeight: 500 }}>
              Nenhum favorito encontrado
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Adicione blocos aos favoritos para vê-los aqui
            </Typography>
          </Paper>
        )}

        {/* Grid de blocos */}
        {favoriteBlocks.length > 0 && (
          <Box sx={{ mb: 8 }}>
            <Grid container spacing={4}>
              {filteredBlocks.map((block) => (
                <Grid item xs={12} sm={6} md={4} key={block.id}>
                  <BlockCard block={block} onView={viewBlock} />
                </Grid>
              ))}
            </Grid>
            {chosenBlock && <BlockModal open={open} setOpen={setOpen} chosenBlock={chosenBlock} />}
          </Box>
        )}

        {/* Busca sem resultados */}
        {filteredBlocks.length === 0 && favoriteBlocks.length > 0 && searchTerm && (
          <Paper 
            elevation={0}
            sx={{ 
              textAlign: 'center', 
              py: 6,
              backgroundColor: '#f8f9fa',
              border: '1px solid #e0e0e0',
              borderRadius: 2
            }}
          >
            <Search sx={{ fontSize: 32, color: '#cccccc', mb: 2 }} />
            <Typography variant="body1" sx={{ color: '#001f2e', fontWeight: 500 }}>
              Nenhum resultado para "{searchTerm}"
            </Typography>
          </Paper>
        )}

      </Container>
    </Box>
  );
}