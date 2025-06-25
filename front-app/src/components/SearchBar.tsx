import React, { useState } from 'react';
import { Box, InputBase, IconButton, Paper } from '@mui/material';
import { Search as SearchIcon, FilterList as FilterIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import DropDownFilter from './DropDownFilter';
import StyledButton from './StyledButton';
import BlockModal from './blocks/BlockRegister';

interface Props {
  searchTerm: string;
  setSearchTerm: (value: string) => void;
  showRegisterButton?: boolean;
}
const SearchBar = ({ searchTerm, setSearchTerm, showRegisterButton = true }: Props) => {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: { xs: 'stretch', md: 'center' },
        gap: { xs: 1.5, md: 2 },
        maxWidth: '1200px',
        margin: '0 auto',
        padding: { xs: '16px', md: '20px 0' },
        flexDirection: { xs: 'column', md: 'row' },
      }}
    >
      {/* Container de Busca */}
      <Paper
        elevation={0}
        sx={{
          display: 'flex',
          alignItems: 'center',
          flex: { xs: 'none', md: 1 },
          width: { xs: '100%', md: 'auto' },
          minWidth: { xs: 'auto', md: '300px' },
          backgroundColor: '#ffffff',
          border: '2px solid #e5e7eb',
          borderRadius: { xs: '8px', md: '12px' },
          overflow: 'hidden',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: '#001f2e',
            boxShadow: '0 4px 12px rgba(0, 31, 46, 0.15)',
          },
          '&:focus-within': {
            borderColor: '#001f2e',
            boxShadow: '0 4px 12px rgba(0, 31, 46, 0.25)',
          }
        }}
      >
        <IconButton
          sx={{
            padding: { xs: '10px', md: '12px' },
            color: '#6b7280',
            '&:hover': {
              backgroundColor: 'transparent',
              color: '#001f2e',
            }
          }}
        >
          <SearchIcon />
        </IconButton>
        
        <InputBase
          placeholder="Buscar blocos..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{
            flex: 1,
            padding: { xs: '10px 6px', md: '12px 8px' },
            fontSize: { xs: '14px', md: '16px' },
            color: '#374151',
            '&::placeholder': {
              color: '#9ca3af',
              opacity: 1,
            },
            '& input': {
              padding: 0,
            }
          }}
        />
      </Paper>

      {/* Container Filtro e Botões */}
      <Box 
        sx={{ 
          display: 'flex', 
          gap: { xs: 1.5, md: 2 },
          flexDirection: { xs: 'column', sm: 'row' },
          width: { xs: '100%', md: 'auto' }
        }}
      >
        {/* Filtro */}
        <Paper
          elevation={0}
          sx={{
            backgroundColor: '#ffffff',
            border: '2px solid #e5e7eb',
            borderRadius: { xs: '8px', md: '12px' },
            overflow: 'hidden',
            transition: 'all 0.3s ease',
            flex: { xs: 1, sm: 'none' },
            '&:hover': {
              borderColor: '#001f2e',
              boxShadow: '0 4px 12px rgba(0, 31, 46, 0.15)',
            }
          }}
        >
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            minWidth: { xs: 'auto', md: '180px' },
            width: '100%'
          }}>
            <IconButton
              sx={{
                padding: { xs: '10px', md: '12px' },
                color: '#6b7280',
                '&:hover': {
                  backgroundColor: 'transparent',
                  color: '#001f2e',
                }
              }}
            >
              <FilterIcon />
            </IconButton>
            <Box sx={{ flex: 1 }}>
              <DropDownFilter />
            </Box>
          </Box>
        </Paper>

        {/* Botões de Ação */}
        <Box sx={{ 
          display: 'flex', 
          gap: 1.5, 
          flexShrink: 0,
          flexDirection: { xs: 'row', sm: 'row' },
          width: { xs: '100%', sm: 'auto' }
        }}>
          <StyledButton
            variant="outlined"
            sx={{
              borderRadius: { xs: '8px', md: '12px' },
              padding: { xs: '10px 16px', md: '12px 24px' },
              fontSize: { xs: '13px', md: '14px' },
              fontWeight: 600,
              textTransform: 'none',
              border: '2px solid #001f2e',
              color: '#001f2e',
              backgroundColor: '#ffffff',
              minWidth: { xs: '80px', md: '100px' },
              flex: { xs: 1, sm: 'none' },
              transition: 'all 0.3s ease',
              '&:hover': {
                borderColor: '#001f2e',
                backgroundColor: 'rgba(0, 31, 46, 0.05)',
                color: '#001f2e',
                transform: 'translateY(-1px)',
                boxShadow: '0 4px 12px rgba(0, 31, 46, 0.15)',
              }
            }}
          >
            BUSCAR
          </StyledButton>
          {showRegisterButton && (
            <StyledButton
              variant="contained"
              onClick={() => navigate('/blocks/create')}
              sx={{
              borderRadius: { xs: '8px', md: '12px' },
              padding: { xs: '10px 16px', md: '12px 24px' },
              fontSize: { xs: '13px', md: '14px' },
              fontWeight: 600,
              textTransform: 'none',
              backgroundColor: '#001f2e',
              color: '#ffffff',
              minWidth: { xs: '100px', md: '120px' },
              border: '2px solid #001f2e',
              flex: { xs: 1, sm: 'none' },
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: '#003547',
                borderColor: '#003547',
                transform: 'translateY(-1px)',
                boxShadow: '0 6px 20px rgba(0, 31, 46, 0.3)',
              }
              }}
            >
              CADASTRAR
            </StyledButton>
          )}
        </Box>
      </Box>

    </Box>
  );
};

export default SearchBar;
