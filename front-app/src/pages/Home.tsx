import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Button,
  Paper,
  Container,
  Avatar,
  Stack,
  CircularProgress,
} from '@mui/material';
import BlockCard from '../components/blocks/BlockCard';
import { useBlocks } from '../hooks/useBlocks';
import { useState } from 'react';
import { Block } from '../types/Blocks';
import BlockModal from '../components/blocks/BlockDetails';
import SearchBar from '../components/SearchBar';

export default function Home() {
  const { blocks, loading, error} = useBlocks();
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const viewBlock = (block: Block) => {
    setChosenBlock(block);
    setOpen(true);
    console.log('Visualizando Bloco: ', block);
  };

  const filteredBlocks = blocks?.filter((blocks: Block) =>
    blocks.titulo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    
    <Box sx={{ backgroundColor: '#f5f5f5', minHeight: '100vh' }}>
      <Container maxWidth="lg" sx={{ py: 6 }}>
          <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} showRegisterButton={false}/>

        {error && (
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h6" color="error">
              {error}
            </Typography>
          </Box>
        )}

        {/* Blocos Disponíveis */}
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
      </Container>
    </Box>
  );
}
