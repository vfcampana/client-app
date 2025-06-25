import axios from "axios";
import { Lote } from "../types/Lote";

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

const convertStatusToString = (status: number): 'privado' | 'anunciado' => {
  return status === 0 ? 'privado' : 'anunciado';
};

export const createLote = async (lote : Lote) => {
    const authToken = await localStorage.getItem('authToken');

    console.log("Creating lote with data:", lote);
    const response = await axios.post(`${REACT_APP_API_URL}/lote`,
        lote
    , { headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        } });

    return response.data
}

export const getLotes = async () => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/lote`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    console.log("Response from getLotes:", response.data);
    return response.data
}

export const getLoteById = async (id : number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/lote/${id}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}

export const updateLote = async (id: number, lote: Lote) => {
    const authToken = await localStorage.getItem('authToken');

    console.log("Updating lote with ID:", id, "and data:", lote);
    const response = await axios.put(`${REACT_APP_API_URL}/lote/${id}`,
        lote
    , { headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        } });

    return response.data;
}

export const deleteLote = async (id: number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.delete(`${REACT_APP_API_URL}/lote/${id}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data;
}


export const addBlocoToLote = async (idLote: number, idBloco: number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.post(`${REACT_APP_API_URL}/lote/${idLote}/bloco/${idBloco}`,
    {}, { headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    } });

    return response.data;
}

export const removeBlocoFromLote = async (idLote: number, idBloco: number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.delete(`${REACT_APP_API_URL}/lote/${idLote}/bloco/${idBloco}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data;
}