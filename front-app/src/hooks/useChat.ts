import { useState, useEffect, useCallback } from 'react';
import { chatService, Conversa, Mensagem } from '../services/chat';

export const useChat = (userId: number) => {
  const [conversas, setConversas] = useState<Conversa[]>([]);
  const [mensagens, setMensagens] = useState<{ [conversaId: number]: Mensagem[] }>({});
  const [loading, setLoading] = useState(true);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const conectar = async () => {
      try {
        await chatService.conectarSocket(userId);
        setConnected(true);
        
        // Configurar listeners
        chatService.onNovaMensagem((mensagem) => {
          setMensagens(prev => ({
            ...prev,
            [mensagem.conversa_id]: [
              ...(prev[mensagem.conversa_id] || []),
              mensagem
            ]
          }));
          
          // Atualizar lista de conversas
          carregarConversas();
        });

        chatService.onNovaConversa((data) => {
          carregarConversas();
        });

        chatService.onRespostaProposta((data) => {
          setMensagens(prev => ({
            ...prev,
            [data.conversa_id]: [
              ...(prev[data.conversa_id] || []),
              data
            ]
          }));
        });

        await carregarConversas();
      } catch (error) {
        console.error('Erro ao conectar chat:', error);
      } finally {
        setLoading(false);
      }
    };

    conectar();

    return () => {
      chatService.desconectarSocket();
      setConnected(false);
    };
  }, [userId]);

  const carregarConversas = useCallback(async () => {
    try {
      const conversasData = await chatService.buscarConversas();
      setConversas(conversasData);
    } catch (error) {
      console.error('Erro ao carregar conversas:', error);
    }
  }, []);

  const carregarMensagens = useCallback(async (conversaId: number) => {
    try {
      if (!mensagens[conversaId]) {
        const mensagensData = await chatService.buscarMensagens(conversaId);
        setMensagens(prev => ({
          ...prev,
          [conversaId]: mensagensData
        }));
      }
      
      chatService.entrarNaConversa(conversaId, userId);
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error);
    }
  }, [mensagens, userId]);

  const enviarMensagem = useCallback((conversaId: number, texto: string, tipo: string = 'texto', propostaValor?: number) => {
    chatService.enviarMensagem(conversaId, userId, texto, tipo, propostaValor);
  }, [userId]);

  const responderProposta = useCallback((mensagemId: number, resposta: 'aceita' | 'rejeitada') => {
    chatService.responderProposta(mensagemId, userId, resposta);
  }, [userId]);

  const iniciarConversa = useCallback(async (blocoId: number, vendedorId: number, mensagemInicial?: string) => {
    try {
      const result = await chatService.iniciarConversa(blocoId, vendedorId, mensagemInicial);
      await carregarConversas();
      return result;
    } catch (error) {
      console.error('Erro ao iniciar conversa:', error);
      throw error;
    }
  }, [carregarConversas]);

  return {
    conversas,
    mensagens,
    loading,
    connected,
    carregarMensagens,
    enviarMensagem,
    responderProposta,
    iniciarConversa,
    carregarConversas
  };
};