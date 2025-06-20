import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Container,
  CircularProgress,
  Paper,
} from '@mui/material';
import {
  Search,
} from '@mui/icons-material';
import BlockCard from '../components/blocks/BlockCard';
import { useBlocks } from '../hooks/useBlocks';
import { useState, useEffect } from 'react';
import { Block } from '../types/Blocks';
import BlockModal from '../components/blocks/BlockDetails';
import SearchBar from '../components/SearchBar';

export default function Home() {
  const { blocks, loading } = useBlocks();
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [safeBlocks, setSafeBlocks] = useState<Block[]>([]);

  useEffect(() => {
    try {
      setError(null);
      if (blocks && Array.isArray(blocks)) {
        setSafeBlocks(blocks);
      } else {
        setSafeBlocks([]);
      }
    } catch (err) {
      console.error('Erro ao processar blocos:', err);
      setError('Erro ao carregar blocos');
      setSafeBlocks([]);
    }
  }, [blocks]);

  const viewBlock = (block: Block) => {
    try {
      setChosenBlock(block);
      setOpen(true);
      console.log('Visualizando Bloco: ', block);
    } catch (err) {
      console.error('Erro ao visualizar bloco:', err);
    }
  };

  const filteredBlocks = React.useMemo(() => {
    try {
      if (!safeBlocks || !Array.isArray(safeBlocks)) {
        return [];
      }
      return safeBlocks.filter((block: Block) =>
        block?.titulo?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    } catch (err) {
      console.error('Erro ao filtrar blocos:', err);
      return [];
    }
  }, [safeBlocks, searchTerm]);

  if (loading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
      }}>
        <CircularProgress size={40} sx={{ color: '#001f2e' }} />
      </Box>
    );
  }

  return (
    <Box sx={{ backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Container maxWidth="lg" sx={{ py: 6 }}>
        <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} showRegisterButton={false}/>

        {/* Erro silencioso - só mostra em desenvolvimento */}
        {error && process.env.NODE_ENV === 'development' && (
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Não foi possível carregar alguns blocos
            </Typography>
          </Box>
        )}

        {/* Estado vazio */}
        {filteredBlocks.length === 0 && !loading && !searchTerm && (
          <Paper 
            elevation={0}
            sx={{ 
              textAlign: 'center', 
              py: 8,
              backgroundColor: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 2
            }}
          >
            <Typography variant="h6" sx={{ color: '#001f2e', mb: 1, fontWeight: 500 }}>
              Nenhum bloco disponível
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Não há blocos cadastrados no momento
            </Typography>
          </Paper>
        )}

        {/* Busca sem resultados */}
        {filteredBlocks.length === 0 && !loading && searchTerm && safeBlocks.length > 0 && (
          <Paper 
            elevation={0}
            sx={{ 
              textAlign: 'center', 
              py: 6,
              backgroundColor: '#ffffff',
              border: '1px solid #e0e0e0',
              borderRadius: 2
            }}
          >
            <Search sx={{ fontSize: 32, color: '#cccccc', mb: 2 }} />
            <Typography variant="body1" sx={{ color: '#001f2e', fontWeight: 500 }}>
              Nenhum resultado para "{searchTerm}"
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Tente usar palavras-chave diferentes
            </Typography>
          </Paper>
        )}

        {/* Blocos Disponíveis */}
        {filteredBlocks.length > 0 && (
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
      </Container>
    </Box>
  );
}