import axios from 'axios';

export interface FavoritoRequest {
    id_bloco: number;
}

const api = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

export const addToFavoritos = async (data: FavoritoRequest) => {
  const authToken = await localStorage.getItem('authToken');
    const response = await axios.post(`${api}/favorito`, data, {
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        },
    });
    return response.data;
}

export const getFavoritos = async () => {
  const authToken = await localStorage.getItem('authToken');
    const response = await axios.get(`${api}/favorito`, {
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        },
    });
    return response.data;
};

export const removeFavorito = async (id_bloco: number) => {
  const authToken = await localStorage.getItem('authToken');
    const response = await axios.delete(`${api}/favorito/${id_bloco}`, {
        headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
        },
    });
    return response.data;
};
