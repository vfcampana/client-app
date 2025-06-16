import { Box, Paper, List, ListItem, ListItemText, Divider, styled } from '@mui/material';
import StyledButton from '../StyledButton';
import { fetchBlocks, getBlock } from '../../services/blocks';
import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import BlockModal from './BlockDetails';
import { Block } from '../../types/Blocks';
import SearchBar from '../SearchBar';

const stoneImageExample = require('../../assets/stone.png') as string;

const MyBlocks = () => {
  const { data: blocks, isLoading, error } = useQuery({
    queryKey: ['blocos'],
    queryFn: fetchBlocks,
  });
  const [chosenBlock, setChosenBlock] = useState<Block>();
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const viewBlock = async (block : Block) => {
    setChosenBlock(block)
    setOpen(true);
  }

  const filteredBlocks = blocks?.filter((block: Block) =>
    block.titulo.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 4 }}>
        {filteredBlocks?.map((block : Block) => (
          <StyledPaper elevation={3} key={block.id}>
            <List sx={{marginTop:-2}}>
              <StyledListItem>
                <ListItemText primary={`${block.titulo}`} secondary={`${block.material}`} primaryTypographyProps={{ fontWeight: 'bold' }}/>
                <Box sx={{ display:'flex', gap: 1 }}>          
                  <StyledButton variant="contained" onClick={() => viewBlock(block)}>Visualizar</StyledButton>
                  <StyledButton variant="contained">Editar</StyledButton>
                  <StyledButton variant="contained">Arquivar</StyledButton>
                </Box>
              </StyledListItem>
              <Divider />
              <StyledListItem sx={{marginTop: 2.5}}>
                <ListItemText primary={`Data de registro ${block.data_criacao}`} secondary={`Valor ${block.valor}`} />
                <StyledImage src={stoneImageExample} alt="Placeholder" width="200" height="150" />
              </StyledListItem>
            </List>
          </StyledPaper>
        ))}
        {chosenBlock && <BlockModal open={open} setOpen={setOpen} chosenBlock={chosenBlock} />}
      </Box>
    </div>
  );
};

// Estilos
const StyledPaper = styled(Paper)({
  width: '100%',
  maxWidth: 800,
  marginBottom: 16,
  padding: 16,
});

const StyledListItem = styled(ListItem)({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
});

const StyledImage = styled('img')({
  border: '4px solid #0d1b2a', 
  borderRadius: '8px',         
});

export default MyBlocks;