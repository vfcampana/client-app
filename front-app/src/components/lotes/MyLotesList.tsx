import { Box, Paper, ListItem, styled, List, ListItemText, Divider } from '@mui/material';
import SearchBar from '../SearchBar';
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchLotes } from '../../services/lotes';
import { Lote } from '../../types/lote.type';
import StyledButton from '../StyledButton';

const MyLotes = () => {
    const { data: blocks, isLoading, error } = useQuery({
      queryKey: ['lotes'],
      queryFn: fetchLotes,
    });
    const [searchTerm, setSearchTerm] = useState('');
    const filteredLotes = blocks?.filter((lote: Lote) =>
      lote.nome.toLowerCase().includes(searchTerm.toLowerCase())
    );
    const viewLote = async (lote : Lote) => {
      // setChosenLote(lote)
      // setOpen(true);
    }
  return (
    <div>
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 4 }}>
        {filteredLotes?.map((lote : Lote) => (
          <StyledPaper elevation={3} key={lote.id}>
            <List sx={{marginTop:-2}}>
              <StyledListItem>
                <ListItemText primary={`${lote.nome}`} secondary={`${lote.observacoes}`} primaryTypographyProps={{ fontWeight: 'bold' }}/>
                <Box sx={{ display:'flex', gap: 1 }}>          
                  <StyledButton variant="contained" onClick={() => viewLote(lote)}>Visualizar</StyledButton>
                  <StyledButton variant="contained">Editar</StyledButton>
                  <StyledButton variant="contained">Arquivar</StyledButton>
                </Box>
              </StyledListItem>
              <Divider />
              <StyledListItem sx={{marginTop: 2.5}}>
                {/* <ListItemText primary={`Data de registro ${block.data_criacao}`} secondary={`Valor ${block.valor}`} /> */}
                {/* <StyledImage src={stoneImageExample} alt="Placeholder" width="200" height="150" /> */}
              </StyledListItem>
            </List>
          </StyledPaper>
        ))}
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

export default MyLotes;