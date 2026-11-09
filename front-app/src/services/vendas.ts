import { API_BASE_URL } from './config';

export interface BlocoParaVenda {
  id: number;
  titulo: string;
  classificacao: string;
  coloracao: string;
  material: string;
  valor: number;
  cidade: string;
  estado: string;
  proprietario: {
    id: number;
    nome: string;
    cidade: string;
    estado: string;
  };
  imagens: Array<{
    url: string;
    nome: string;
  }>;
}

export interface PropostaVenda {
  bloco_id: number;
  comprador_id: number;
  comprador_wallet_address: string;
  valor: number;
  observacoes?: string;
}

export interface BlockchainVendaResult {
  success: boolean;
  message: string;
  data?: {
    bloco_id: number;
    vendedor_id: number;
    comprador_id: number;
    valor: number;
    blockchain_data: any;
  };
}

class VendasService {
  private getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // Listar blocos disponíveis para venda
  async listarBlocosParaVenda(): Promise<{ blocos: BlocoParaVenda[]; total: number }> {
    const response = await fetch(`${API_BASE_URL}/blocos-venda`, {
      headers: this.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar blocos para venda');
    }

    return response.json();
  }

  // Obter detalhes de um bloco específico para venda
  async obterDetalhesBloco(blocoId: number): Promise<{ bloco: BlocoParaVenda }> {
    const response = await fetch(`${API_BASE_URL}/bloco-venda/${blocoId}`, {
      headers: this.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Erro ao carregar detalhes do bloco');
    }

    return response.json();
  }

  // Iniciar uma conversa para negociação
  async iniciarConversa(outroUsuarioId: number, blocoId: number): Promise<{ conversa_id: number }> {
    const response = await fetch(`${API_BASE_URL}/iniciar-conversa`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        vendedor_id: outroUsuarioId,
        bloco_id: blocoId
      })
    });

    if (!response.ok) {
      throw new Error('Erro ao iniciar conversa');
    }

    return response.json();
  }

  // Enviar proposta de compra via chat
  async enviarPropostaChat(
    conversaId: number, 
    blocoTitulo: string, 
    valor: number, 
    observacoes?: string
  ): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/conversas/${conversaId}/mensagens`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        tipo: 'proposta',
        texto: `💰 PROPOSTA DE COMPRA 💰\n\nBloco: "${blocoTitulo}"\nValor ofertado: R$ ${valor.toLocaleString('pt-BR')}\n${observacoes ? `\nObservações: ${observacoes}` : ''}\n\nAguardo sua resposta!`,
        proposta_valor: valor
      })
    });

    if (!response.ok) {
      throw new Error('Erro ao enviar proposta');
    }

    return response.json();
  }

  // Processar venda diretamente via blockchain (para transações diretas)
  async processarVendaBlockchain(proposta: PropostaVenda): Promise<BlockchainVendaResult> {
    const response = await fetch(`${API_BASE_URL}/blockchain/vendas`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(proposta)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro ao processar venda na blockchain');
    }

    return response.json();
  }

  // Verificar status da blockchain
  async verificarStatusBlockchain(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/blockchain/status`, {
      headers: this.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Erro ao verificar status da blockchain');
    }

    return response.json();
  }

  // Verificar informações do contrato
  async obterInfoContrato(): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/blockchain/contract`, {
      headers: this.getAuthHeaders()
    });

    if (!response.ok) {
      throw new Error('Erro ao obter informações do contrato');
    }

    return response.json();
  }
}

export const vendasService = new VendasService();