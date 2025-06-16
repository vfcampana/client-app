import { Box, Paper, List, ListItem, ListItemText, Divider, styled } from '@mui/material';
import StyledButton from '../StyledButton';

const stoneImageExample = require('../../assets/stone.png') as string;


const StyledPaper = styled(Paper)(({ theme }) => ({
  width: '100%',
  maxWidth: 800,
  marginBottom: theme.spacing(2),
  padding: theme.spacing(2),
}));

const StyledListItem = styled(ListItem)({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
});

const StyledImage = styled('img')({
  border: '4px solid #0d1b2a', 
  borderRadius: '8px',         
});

const BlockList = () => {
  const blocks = [
    { id: 1, code: 'XXXX', date: 'XXX', value: 'XXXX', image: stoneImageExample },
    { id: 2, code: 'XXXX', date: 'XXX', value: 'XXXX', image: stoneImageExample },
    { id: 3, code: 'XXXX', date: 'XXX', value: 'XXXX', image: stoneImageExample },
  ];

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 4 }}>
      {blocks.map((block) => (
        <StyledPaper elevation={3} key={block.id}>
          <List>
            <StyledListItem>
              <ListItemText primary={`Bloco ${block.id}`} secondary={`código ${block.code}`} />
              <StyledButton variant="contained">Visualizar</StyledButton>
            </StyledListItem>
            <Divider />
            <StyledListItem>
              <ListItemText primary={`Data de registro ${block.date}`} secondary={`Valor ${block.value}`} />
              <StyledImage src={block.image} alt="Placeholder" width="200" height="150" />
            </StyledListItem>
          </List>
        </StyledPaper>
      ))}
    </Box>
  );
};

export default BlockList;