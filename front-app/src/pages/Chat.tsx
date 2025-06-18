import React, { useState } from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, TextField, Button, Divider, ListItemButton } from '@mui/material';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [vendedores, setVendedores] = useState(['Vendedor 1', 'Vendedor 2', 'Vendedor 3']); // Exemplo de vendedores

  const sendMessage = () => {
    window.alert('Funcionalidade nao implementada')
  };

  return (
    <Box display="flex" flexDirection="column" height="100vh">
      {/* TopBar com título "Chat" */}

      {/* Área principal com barra lateral e área de chat */}
      <Box display="flex" flexGrow={1}>
        
        {/* Barra lateral de vendedores estilizada */}
        <Box width="250px" bgcolor="#0B2447" p={2} borderRight="1px solid #ddd" display="flex" flexDirection="column" alignItems="center">
          <Typography variant="h6" gutterBottom color="white">
            Vendedores
          </Typography>
          <Divider sx={{ bgcolor: '#1F4690', width: '100%' }} />
          <List>
            {vendedores.map((vendedor, index) => (
              <ListItemButton key={index} sx={{ textAlign: 'center', color: 'white' }}>
                <ListItemText primary={vendedor} />
              </ListItemButton>
            ))}
          </List>
        </Box>

        {/* Área de chat */}
        <Box flexGrow={1} p={2} component={Paper} sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          {/* Lista de mensagens */}
          <List sx={{ flexGrow: 1, overflow: 'auto' }}>
            {messages.map((msg, index) => (
              <ListItem key={index}>
                <ListItemText primary={msg} />
              </ListItem>
            ))}
          </List>

          {/* Campo de texto e botão de envio estilizado */}
          <Box display="flex" mt={2}>
            <TextField
              label="Digite sua mensagem"
              variant="outlined"
              fullWidth
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
            <Button 
              variant="contained" 
              onClick={sendMessage} 
              sx={{ 
                ml: 2, 
                bgcolor: '#0B2447', 
                color: 'white', 
                '&:hover': { bgcolor: '#1F4690' }
              }}
            >
              Enviar
            </Button>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Chat;
