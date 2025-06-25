export interface Lote {
  id: number;
  nome: string;
  preco: number;
  observacoes?: string;
  status: 'privado' | 'anunciado';
  data_criacao: string;
  id_usuario: number;
  blocos?: number[] | LoteBloco[]; // IDs dos blocos associados ao lote ou objetos LoteBloco
}

export interface LoteBloco {
  id: number;
  id_lote: number;
  id_bloco: number;

  bloco?: {
    id: number;
    titulo: string;
    valor: number;
    material: string;
    imagem?: string;
  };
}  

export interface CreateLoteRequest {
  nome: string;
  preco: number;
  observacoes?: string;
  status: 'privado' | 'anunciado';
  blocos: number[]; // IDs dos blocos que serão inseridos na tabela intermediária
}

export interface LoteWithBlocks extends Lote {
  blocos: LoteBloco[];
}