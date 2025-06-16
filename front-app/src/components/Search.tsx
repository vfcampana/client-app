// Search.tsx
import React from 'react';
import { TextField, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { styled } from '@mui/material/styles';

const StyledTextField = styled(TextField)(({ theme }) => ({
  width: '50ch',
  '& .MuiOutlinedInput-root': {
    borderRadius: '50px',
    height: '40px',
    backgroundColor: '#f1f1f1',
    '& fieldset': {
      borderColor: '#0d1b2a',
    },
    '&:hover fieldset': {
      borderColor: '#0d1b2a',
    },
    '&.Mui-focused fieldset': {
      borderColor: '#0d1b2a',
    },
  },
}));

interface Props {
  searchTerm: string;
  setSearchTerm: (value: string) => void;
}

const Search = ({ searchTerm, setSearchTerm }: Props) => {
  return (
    <StyledTextField
      placeholder="Nome"
      variant="outlined"
      size="small"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <SearchIcon style={{ color: '#7d7d7d' }} />
          </InputAdornment>
        ),
      }}
    />
  );
};

export default Search;
