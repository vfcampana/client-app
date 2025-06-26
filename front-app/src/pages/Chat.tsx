import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import {
  Box,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Typography,
  TextField,
  IconButton,
  Badge,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Card,
  CardMedia,
  useTheme,
  useMediaQuery,
  CircularProgress
} from '@mui/material';
import {
  Send,
  AttachMoney,
  Message,
  Person
} from '@mui/icons-material';
import { useSelector } from 'react-redux';

// Interfaces
interface Usuario {
  id: number;
  nome: string;
  email: string;
}

interface Bloco {
  id: number;
  titulo: string;
  valor: string;
  imagem?: string;
}

interface UltimaMensagem {
  texto: string;
  data_envio: string;
  de_mim: boolean;
}

interface Conversa {
  id: number;
  outro_usuario: Usuario;
  bloco?: Bloco;
  ultima_mensagem?: UltimaMensagem;
  mensagens_nao_lidas: number;
  ultima_atividade: string;
}

interface MensagemChat {
  id: number;
  texto: string;
  tipo: 'texto' | 'proposta' | 'resposta_proposta' | 'sistema';
  data_envio: string;
  de_mim: boolean;
  usuario: Usuario;
  lida: boolean;
  proposta_valor?: string;
  proposta_status?: 'pendente' | 'aceita' | 'rejeitada';
}

const Chat: React.FC = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Usar o redux para pegar o usuário logado
  const authState = useSelector((state: any) => state.authReducer);
  const { user, signed: isAuthenticated } = authState;
  
  // Estados locais
  const [conversas, setConversas] = useState<Conversa[]>([]);
  const [mensagens, setMensagens] = useState<{ [conversaId: number]: MensagemChat[] }>({});
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);
  const [conversaSelecionada, setConversaSelecionada] = useState<number | null>(null);
  const [novaMensagem, setNovaMensagem] = useState('');
  const [mostrarProposta, setMostrarProposta] = useState(false);
  const [valorProposta, setValorProposta] = useState('');
  const [error, setError] = useState<string | null>(null);
  
  // OTIMIZAÇÃO: Refs para evitar re-renders desnecessários
  const mensagensEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const cacheTimeRef = useRef<number>(0);
  
  // OTIMIZAÇÃO: Memoizar token
  const token = useMemo(() => localStorage.getItem('authToken'), []);

  // OTIMIZAÇÃO: Scroll automático otimizado
  const scrollToBottom = useCallback(() => {
    if (mensagensEndRef.current) {
      mensagensEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);

  // OTIMIZAÇÃO: Carregar conversas com cache
  const carregarConversas = useCallback(async (forceRefresh = false) => {
    // Cache de 30 segundos
    const now = Date.now();
    if (!forceRefresh && (now - cacheTimeRef.current) < 30000 && conversas.length > 0) {
      return;
    }

    try {
      setLoading(true);
      
      if (!token) {
        setError('Token não encontrado');
        return;
      }

      // Cancelar requisição anterior se existir
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      
      abortControllerRef.current = new AbortController();

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000'}/conversas`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        signal: abortControllerRef.current.signal
      });

      if (!response.ok) {
        throw new Error('Erro ao carregar conversas');
      }

      const data = await response.json();
      setConversas(data);
      setConnected(true);
      cacheTimeRef.current = now;
      setError(null);
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        console.error('Erro ao carregar conversas:', error);
        setError(error.message);
        setConnected(false);
      }
    } finally {
      setLoading(false);
    }
  }, [token, conversas.length]);

  useEffect(() => {
    scrollToBottom();
  }, [mensagens, conversaSelecionada, scrollToBottom]);


  // OTIMIZAÇÃO: Carregar mensagens com cache
  const carregarMensagens = useCallback(async (conversaId: number) => {
    // Se já tem mensagens carregadas, não recarregar
    if (mensagens[conversaId] && mensagens[conversaId].length > 0) {
      return;
    }

    try {
      if (!token) {
        setError('Token não encontrado');
        return;
      }

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000'}/conversas/${conversaId}/mensagens`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Erro ao carregar mensagens');
      }

      const data = await response.json();
      setMensagens(prev => ({
        ...prev,
        [conversaId]: data
      }));
    } catch (error: any) {
      console.error('Erro ao carregar mensagens:', error);
      setError(error.message);
    }
  }, [token, mensagens]);

  // OTIMIZAÇÃO: Enviar mensagem sem recarregar tudo
  const handleEnviarMensagem = useCallback(async () => {
    if (!novaMensagem.trim() || !conversaSelecionada || !user) return;

    const mensagemTexto = novaMensagem;
    setNovaMensagem(''); // Limpar imediatamente para UX

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000'}/conversas/${conversaSelecionada}/mensagens`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          texto: mensagemTexto,
          tipo: 'texto'
        })
      });

      if (response.ok) {
        // OTIMIZAÇÃO: Adicionar mensagem localmente em vez de recarregar
        const novaMensagemObj: MensagemChat = {
          id: Date.now(), // ID temporário
          texto: mensagemTexto,
          tipo: 'texto',
          data_envio: new Date().toISOString(),
          de_mim: true,
          usuario: { id: user.id, nome: user.nome, email: user.email },
          lida: false
        };

        setMensagens(prev => ({
          ...prev,
          [conversaSelecionada]: [...(prev[conversaSelecionada] || []), novaMensagemObj]
        }));

        // Recarregar conversas apenas se necessário
        setTimeout(() => carregarConversas(true), 1000);
      }
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      setNovaMensagem(mensagemTexto); // Restaurar mensagem em caso de erro
    }
  }, [novaMensagem, conversaSelecionada, user, token, carregarConversas]);

  // Função para selecionar conversa
  const handleSelecionarConversa = useCallback(async (conversaId: number) => {
    setConversaSelecionada(conversaId);
    // Carregar mensagens quando selecionar a conversa
    await carregarMensagens(conversaId);
  }, [carregarMensagens]);

  // Função para enviar proposta
  const handleEnviarProposta = useCallback(async () => {
    if (!valorProposta.trim() || !conversaSelecionada || !user) return;

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000'}/conversas/${conversaSelecionada}/mensagens`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          texto: `Proposta: R$ ${valorProposta}`,
          tipo: 'proposta',
          proposta_valor: valorProposta
        })
      });

      if (response.ok) {
        // Adicionar proposta localmente
        const novaProposta: MensagemChat = {
          id: Date.now(),
          texto: `Proposta: R$ ${valorProposta}`,
          tipo: 'proposta',
          data_envio: new Date().toISOString(),
          de_mim: true,
          usuario: { id: user.id, nome: user.nome, email: user.email },
          lida: false,
          proposta_valor: valorProposta,
          proposta_status: 'pendente'
        };

        setMensagens(prev => ({
          ...prev,
          [conversaSelecionada]: [...(prev[conversaSelecionada] || []), novaProposta]
        }));

        // Fechar dialog e limpar valor
        setMostrarProposta(false);
        setValorProposta('');

        // Recarregar conversas
        setTimeout(() => carregarConversas(true), 1000);
      }
    } catch (error) {
      console.error('Erro ao enviar proposta:', error);
    }
  }, [valorProposta, conversaSelecionada, user, token, carregarConversas]);

  // OTIMIZAÇÃO: Memoizar conversa selecionada
  const conversaAtual = useMemo(() => {
    return conversas.find((c: Conversa) => c.id === conversaSelecionada);
  }, [conversas, conversaSelecionada]);

  // OTIMIZAÇÃO: Memoizar mensagens da conversa atual
  const mensagensAtuais = useMemo(() => {
    return conversaSelecionada ? mensagens[conversaSelecionada] || [] : [];
  }, [mensagens, conversaSelecionada]);

  // OTIMIZAÇÃO: Função de formatação memoizada
  const formatarData = useCallback((dataString: string) => {
    try {
      const data = new Date(dataString);
      const agora = new Date();
      const diffMs = agora.getTime() - data.getTime();
      const diffMins = Math.floor(diffMs / 60000);
      const diffHoras = Math.floor(diffMs / 3600000);
      const diffDias = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return 'Agora';
      if (diffMins < 60) return `${diffMins}m`;
      if (diffHoras < 24) return `${diffHoras}h`;
      if (diffDias < 7) return `${diffDias}d`;
      
      return data.toLocaleDateString('pt-BR');
    } catch {
      return 'Agora';
    }
  }, []);

  // Carregar conversas na montagem
  useEffect(() => {
    if (isAuthenticated && user && token) {
      carregarConversas(true);
    }
  }, [isAuthenticated, user, token, carregarConversas]);

  // OTIMIZAÇÃO: Component memoizado para mensagem
  const MensagemComponent = React.memo(({ mensagem }: { mensagem: MensagemChat }) => {
    const ehProposta = mensagem.tipo === 'proposta';
    const ehMinhaMensagem = mensagem.de_mim;

    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: ehMinhaMensagem ? 'flex-end' : 'flex-start',
          mb: 2
        }}
      >
        <Paper
          elevation={1}
          sx={{
            maxWidth: '70%',
            p: 2,
            backgroundColor: ehMinhaMensagem 
              ? (ehProposta ? theme.palette.success.main : theme.palette.primary.main)
              : theme.palette.grey[100],
            color: ehMinhaMensagem ? 'white' : 'inherit',
            borderRadius: ehMinhaMensagem 
              ? '20px 20px 5px 20px' 
              : '20px 20px 20px 5px'
          }}
        >
          {!ehMinhaMensagem && (
            <Typography variant="caption" sx={{ fontWeight: 600, mb: 0.5, display: 'block' }}>
              {mensagem.usuario.nome}
            </Typography>
          )}
          
          {ehProposta && (
            <Chip
              label="💰 PROPOSTA"
              size="small"
              sx={{ mb: 1, color: 'white', backgroundColor: 'rgba(255,255,255,0.2)' }}
            />
          )}
          
          <Typography variant="body2" sx={{ mb: 1 }}>
            {mensagem.texto}
          </Typography>

          <Typography 
            variant="caption" 
            sx={{ 
              display: 'block', 
              textAlign: 'right', 
              opacity: 0.7,
              mt: 1
            }}
          >
            {formatarData(mensagem.data_envio)}
          </Typography>
        </Paper>
      </Box>
    );
  });

  // Verificar autenticação
  if (!isAuthenticated || !user) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Alert severity="warning">
          Você precisa estar logado para acessar o chat.
        </Alert>
      </Box>
    );
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', gap: 2 }}>
        <CircularProgress />
        <Typography>Carregando chat...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={() => carregarConversas(true)}>
            Tentar Novamente
          </Button>
        }>
          {error}
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper elevation={1} sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Message color="primary" />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Chat de Negociação
          </Typography>
          <Chip
            label={connected ? 'Online' : 'Offline'}
            color={connected ? 'success' : 'error'}
            size="small"
          />
        </Box>
      </Paper>

      <Grid container sx={{ flex: 1, overflow: 'hidden' }}>
        {/* Lista de Conversas */}
        <Grid 
          item 
          xs={12} 
          md={4} 
          sx={{ 
            borderRight: { md: 1 }, 
            borderColor: 'divider',
            height: '100%',
            overflow: 'auto'
          }}
        >
          <Box sx={{ p: 2 }}>
            <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
              Conversas ({conversas.length})
            </Typography>
            
            {conversas.length === 0 ? (
              <Alert severity="info" sx={{ mt: 2 }}>
                Nenhuma conversa iniciada. Visite a página de blocos e clique em "Negociar" para começar uma conversa.
              </Alert>
            ) : (
              <List>
                {conversas.map((conversa: Conversa) => (
                  <ListItem
                    key={conversa.id}
                    disablePadding
                    sx={{ mb: 1 }}
                  >
                    <ListItemButton
                      selected={conversaSelecionada === conversa.id}
                      onClick={() => handleSelecionarConversa(conversa.id)}
                      sx={{
                        borderRadius: 2,
                        '&.Mui-selected': {
                          backgroundColor: theme.palette.primary.light + '20'
                        }
                      }}
                    >
                      <ListItemAvatar>
                        <Badge badgeContent={conversa.mensagens_nao_lidas} color="error">
                          <Avatar>
                            <Person />
                          </Avatar>
                        </Badge>
                      </ListItemAvatar>
                      
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                              {conversa.outro_usuario.nome}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {formatarData(conversa.ultima_atividade)}
                            </Typography>
                          </Box>
                        }
                        secondary={
                          <Box>
                            {conversa.bloco && (
                              <Typography variant="caption" color="primary" sx={{ fontWeight: 500 }}>
                                {conversa.bloco.titulo} - R$ {conversa.bloco.valor}
                              </Typography>
                            )}
                            {conversa.ultima_mensagem && (
                              <Typography variant="body2" color="text.secondary" noWrap>
                                {conversa.ultima_mensagem.de_mim ? 'Você: ' : ''}
                                {conversa.ultima_mensagem.texto}
                              </Typography>
                            )}
                          </Box>
                        }
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        </Grid>

        {/* Área de Mensagens */}
        <Grid item xs={12} md={8} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          {conversaSelecionada ? (
            <>
              {/* Header da Conversa */}
              <Paper elevation={1} sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                {conversaAtual && (
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar>
                      <Person />
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {conversaAtual.outro_usuario.nome}
                      </Typography>
                      {conversaAtual.bloco && (
                        <Typography variant="caption" color="text.secondary">
                          Negociando: {conversaAtual.bloco.titulo}
                        </Typography>
                      )}
                    </Box>
                    
                    <Button
                      variant="contained"
                      size="small"
                      startIcon={<AttachMoney />}
                      onClick={() => setMostrarProposta(true)}
                    >
                      Fazer Proposta
                    </Button>
                    
                    {conversaAtual.bloco && conversaAtual.bloco.imagem && (
                      <Card sx={{ width: 60, height: 60 }}>
                        <CardMedia
                          component="img"
                          height="60"
                          image={conversaAtual.bloco.imagem}
                          alt={conversaAtual.bloco.titulo}
                        />
                      </Card>
                    )}
                  </Box>
                )}
              </Paper>

              {/* Mensagens */}
              <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
                {mensagensAtuais.map((mensagem) => (
                  <MensagemComponent key={mensagem.id} mensagem={mensagem} />
                ))}
                <div ref={mensagensEndRef} />
              </Box>

              {/* Input de Mensagem */}
              <Paper elevation={3} sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    placeholder="Digite sua mensagem..."
                    value={novaMensagem}
                    onChange={(e) => setNovaMensagem(e.target.value)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleEnviarMensagem();
                      }
                    }}
                    size="small"
                  />
                  <IconButton
                    color="primary"
                    onClick={handleEnviarMensagem}
                    disabled={!novaMensagem.trim()}
                  >
                    <Send />
                  </IconButton>
                </Box>
              </Paper>
            </>
          ) : (
            <Box sx={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              height: '100%',
              flexDirection: 'column',
              gap: 2
            }}>
              <Message sx={{ fontSize: 64, color: 'text.secondary' }} />
              <Typography variant="h6" color="text.secondary">
                Selecione uma conversa para começar
              </Typography>
            </Box>
          )}
        </Grid>
      </Grid>

      {/* Dialog de Proposta */}
      <Dialog open={mostrarProposta} onClose={() => setMostrarProposta(false)}>
        <DialogTitle>Fazer Proposta</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Valor da Proposta (R$)"
            type="number"
            fullWidth
            variant="outlined"
            value={valorProposta}
            onChange={(e) => setValorProposta(e.target.value)}
            placeholder="0,00"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setMostrarProposta(false)}>
            Cancelar
          </Button>
          <Button 
            onClick={handleEnviarProposta} 
            variant="contained"
            disabled={!valorProposta}
          >
            Enviar Proposta
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Chat;