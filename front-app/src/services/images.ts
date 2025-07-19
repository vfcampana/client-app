import axios from "axios";

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

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

// Listar imagens de um bloco específico
export const fetchImagensBloco = async (blocoId: number): Promise<ImagemBloco[]> => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/imagens/bloco/${blocoId}`, {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        }
    });

    return response.data;
};

// Upload de múltiplas imagens para um bloco
export const uploadImagensBloco = async (blocoId: number, files: FileList): Promise<any> => {
    const authToken = await localStorage.getItem('authToken');
    
    const formData = new FormData();
    
    // Adicionar todas as imagens ao FormData
    Array.from(files).forEach((file, index) => {
        formData.append('imagens', file);
    });

    const response = await axios.post(`${REACT_APP_API_URL}/imagens/bloco/${blocoId}/upload`, formData, {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'multipart/form-data'
        }
    });

    return response.data;
};

// Deletar uma imagem específica
export const deleteImagemBloco = async (imagemId: string): Promise<any> => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.delete(`${REACT_APP_API_URL}/imagens/${imagemId}`, {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        }
    });

    return response.data;
};

// Atualizar informações de uma imagem
export const updateImagemBloco = async (imagemId: string, dados: Partial<ImagemBloco>): Promise<any> => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.put(`${REACT_APP_API_URL}/imagens/${imagemId}`, dados, {
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        }
    });

    return response.data;
};
