import React, { useState } from 'react';
import { AppBar, Toolbar, Box } from '@mui/material';
import DropDownFilter from './DropDownFilter';
import Search from './Search';
import StyledButton from './StyledButton';
import BlockModal from './blocks/BlockRegister';

// BARRA DE BUSCA
interface Props {
  searchTerm: string;
  setSearchTerm: (value: string) => void;
}

const SearchBar = ({ searchTerm, setSearchTerm }: Props) => {
  return (
    <AppBar position="static" sx={{ backgroundColor: '#ffffff', paddingX: 2 }}>
      <Toolbar sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Search searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
          <DropDownFilter />
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <StyledButton sx={{ minWidth: 100 }}>Buscar</StyledButton>
          <BlockModal />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default SearchBar;

