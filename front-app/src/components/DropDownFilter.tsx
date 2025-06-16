import React, { useState } from 'react';
import { Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { styled } from '@mui/material/styles';

// Estilizando o Select
const StyledSelect = styled(Select)(({ theme }) => ({
  borderRadius: '50px',
  width: '30ch',
  height: '40px',
  backgroundColor: '#f1f1f1',
  '&:hover': {
    borderColor: 'primary',
  },
  '& .MuiOutlinedInput-root': {
    '& fieldset': {
      borderColor: 'primary',
    },
    '&:hover fieldset': {
      borderColor: 'primary',
    },
    '&.Mui-focused fieldset': {
      borderColor: 'primary',
    },
  },
}));

const DropDownFilter = () => {
  const [value, setValue] = useState('');

  const handleChange = (event : any) => {
    setValue(event.target.value);
  };

  return (
    <FormControl fullWidth variant="outlined">
      <InputLabel id="dropdown-label">Filtrar a Busca</InputLabel>
      <StyledSelect
        labelId="dropdown-label"
        value={value}
        onChange={handleChange}
        label="Filtrar a Busca2"
      >
        <MenuItem value="todos">Todos</MenuItem>
        <MenuItem value="opcao1">Opção 1</MenuItem>
        <MenuItem value="opcao2">Opção 2</MenuItem>
        <MenuItem value="opcao3">Opção 3</MenuItem>
      </StyledSelect>
    </FormControl>
  );
};

export default DropDownFilter;
