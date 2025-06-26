import axios from 'axios';
import io, { Socket } from 'socket.io-client';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

export interface Conversa {
  id: number;
  outro_usuario: {
    id: number;
    nome: string;
    email: string;
  };
  bloco?: {
    id: number;
    titulo: string;
    valor: string;
    imagem?: string;
  };
  ultima_mensagem?: {
    texto: string;
    data_envio: string;
    de_mim: boolean;
  };
  mensagens_nao_lidas: number;
  ultima_atividade: string;
}

export interface Mensagem {
  id: number;
  texto: string;
  tipo: 'texto' | 'proposta' | 'resposta_proposta' | 'sistema';
  data_envio: string;
  de_mim: boolean;
  usuario: {
    id: number;
    nome: string;
  };
  lida: boolean;
  proposta_valor?: string;
  proposta_status?: 'pendente' | 'aceita' | 'rejeitada';
}

class ChatService {
  private socket: Socket | null = null;
  private isConnected = false;

  async getAuthToken(): Promise<string | null> {
    return localStorage.getItem('authToken');
  }

  async conectarSocket(userId: number): Promise<void> {
    if (this.socket && this.isConnected) {
      return;
    }

    const token = await this.getAuthToken();
    
    this.socket = io(API_BASE_URL, {
      auth: {
        token: token
      }
    });

    this.socket.on('connect', () => {
      console.log('🔗 Conectado ao chat');
      this.isConnected = true;
      this.socket?.emit('join_room', { user_id: userId });
    });

    this.socket.on('disconnect', () => {
      console.log('❌ Desconectado do chat');
      this.isConnected = false;
    });

    this.socket.on('error', (error: unknown) => {
      console.error('Erro no socket:', error);
    });
  }

  desconectarSocket(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }

  entrarNaConversa(conversaId: number, userId: number): void {
    if (this.socket) {
      this.socket.emit('join_room', {
        conversa_id: conversaId,
        user_id: userId
      });
    }
  }

  sairDaConversa(conversaId: number, userId: number): void {
    if (this.socket) {
      this.socket.emit('leave_room', {
        conversa_id: conversaId,
        user_id: userId
      });
    }
  }

  enviarMensagem(conversaId: number, userId: number, texto: string, tipo: string = 'texto', propostaValor?: number): void {
    if (this.socket) {
      this.socket.emit('send_message', {
        conversa_id: conversaId,
        user_id: userId,
        texto: texto,
        tipo: tipo,
        proposta_valor: propostaValor
      });
    }
  }

  responderProposta(mensagemId: number, userId: number, resposta: 'aceita' | 'rejeitada'): void {
    if (this.socket) {
      this.socket.emit('respond_proposal', {
        mensagem_id: mensagemId,
        user_id: userId,
        resposta: resposta
      });
    }
  }

  onNovaMensagem(callback: (mensagem: any) => void): void {
    if (this.socket) {
      this.socket.on('new_message', callback);
    }
  }

  onNovaConversa(callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on('nova_conversa', callback);
    }
  }

  onRespostaProposta(callback: (data: any) => void): void {
    if (this.socket) {
      this.socket.on('proposal_response', callback);
    }
  }

  async buscarConversas(): Promise<Conversa[]> {
    const token = await this.getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/conversas`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  }

  async buscarMensagens(conversaId: number): Promise<Mensagem[]> {
    const token = await this.getAuthToken();
    const response = await axios.get(`${API_BASE_URL}/conversas/${conversaId}/mensagens`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  }

  async iniciarConversa(blocoId: number, vendedorId: number, mensagem: string = 'Olá! Tenho interesse neste bloco.'): Promise<{ conversa_id: number }> {
    const token = await this.getAuthToken();
    const response = await axios.post(`${API_BASE_URL}/iniciar-conversa`, {
      bloco_id: blocoId,
      vendedor_id: vendedorId,
      mensagem: mensagem
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  }
}

export const chatService = new ChatService();