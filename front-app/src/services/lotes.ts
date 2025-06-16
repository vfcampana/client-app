import axios from "axios";
import { Lote } from "../types/lote.type";

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

export const createLote = async (lote : Lote) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.post(`${REACT_APP_API_URL}/lote`,
        lote
    , { headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        } });

    return response.data
}

export const fetchLotes = async () => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/lote`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}

export const getLote = async (id : number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/lote/${id}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}