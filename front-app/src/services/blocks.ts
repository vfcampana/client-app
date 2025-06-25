import axios from "axios";
import { Block } from "../types/Blocks";

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

export const createBlock = async (blockData: any) => {
    const authToken = await localStorage.getItem('authToken');

    // Se houver arquivo de imagem, usar FormData
    if (blockData instanceof FormData) {
        const response = await axios.post(`${REACT_APP_API_URL}/bloco`, blockData, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'multipart/form-data'
            }
        });
        
        // Construir URL da imagem na resposta
        const createdBlock = {
            ...response.data,
            imagem: response.data.imagem ? `${REACT_APP_API_URL}/imagens/${response.data.imagem}` : null
        };
        
        return createdBlock;
    }

    // Caso contrário, usar JSON
    const response = await axios.post(`${REACT_APP_API_URL}/bloco`, blockData, {
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        }
    });

    return response.data;
}
export const fetchBlocks = async () => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/blocos`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    console.log('Blocks fetched:', response.data);
    return response.data
}

export const fetchBlocksByUser = async (userId : number) => {
    const authToken = await localStorage.getItem('authToken');
    const response = await axios.get(`${REACT_APP_API_URL}/blocos`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    return response.data
}

export const getBlock = async (id : number) => {
    console.log('Fetching block with ID:', id);
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/bloco/${id}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}

export const updateBlock = async (id: number, blockData: any) => {
    const authToken = await localStorage.getItem('authToken');
    // Se houver arquivo de imagem, usar FormData
    if (blockData instanceof FormData) {
        const response = await axios.put(`${REACT_APP_API_URL}/bloco/${id}`, blockData, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'multipart/form-data'
            }
        });
        return response.data;
    }

    // Caso contrário, usar JSON
    const response = await axios.put(`${REACT_APP_API_URL}/bloco/${id}`, blockData, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        }
    });

    return response.data;
}