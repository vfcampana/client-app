import { Button, styled } from '@mui/material';

// ESTILO PADRAO PARA OS BOTOES DO SITE
export default styled(Button)({
    borderRadius: '4px',
    padding: '6px 16px',
    backgroundColor: '#0d1b2a',
    color: '#ffffff',
    '&:hover': {
      backgroundColor: '#0b1624',
    },
  });