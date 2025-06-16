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
import {
  Business as BusinessIcon,
  LocationOn as LocationIcon,
  Star as StarIcon,
  People as PeopleIcon,
  Inventory as InventoryIcon,
  ArrowForward as ArrowForwardIcon,
  AutoAwesome as SparklesIcon,
} from '@mui/icons-material';
import BlockCard from '../components/BlockCard';
import { useBlocks } from '../hooks/useBlocks';

export default function Home() {
  const { blocks, loading, error, refetch } = useBlocks();

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
        
        {error && (
          <Box sx={{ mb: 4, textAlign: 'center' }}>
            <Typography variant="h6" color="error">
              {error}
            </Typography>
          </Box>
        )}

        {/* Blocos Disponíveis */}
        <Box sx={{ mb: 8 }}>
          <Box textAlign="center" sx={{ mb: 6 }}>
            <Typography variant="h3" component="h2" gutterBottom fontWeight="bold" color="text.primary">
              Blocos Disponíveis
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {blocks.map((block) => (
              <Grid item xs={12} sm={6} md={4} key={block.id}>
                <BlockCard block={block} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Box>
  );
}
