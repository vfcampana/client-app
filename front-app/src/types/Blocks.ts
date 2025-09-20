export interface Block {
  imagem: string;
  imagens?: ImagemBloco[]; // Nova propriedade para múltiplas imagens do Supabase
  id: number;
  titulo: string;
  classificacao: string;
  coloracao: string;
  material: string;
  medida_bruta: string;
  volume_bruto: string;
  medida_liquida: string;
  volume_liquido: string;
  pedreira: string;
  observacoes: string;
  cep: string;
  logradouro: string;
  pais: string;
  cidade: string;
  valor: string;
  data_criacao: string;
  data_alteracao: string;
  estado: string;
  id_usuario: number;
  status: string;
}

export interface ImagemBloco {
  id: string;
  id_bloco: number;
  url_imagem: string;
  nome_arquivo: string;
  tamanho_arquivo?: number;
  tipo_mime?: string;
  data_upload: string;
  data_atualizacao: string;
  ativo: boolean;
}