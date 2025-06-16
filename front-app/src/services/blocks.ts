import axios from "axios";
import { Block } from "../types/Blocks";

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

export const createBlock = async (block : Block) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.post(`${REACT_APP_API_URL}/bloco`,
        block
    , { headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`,
        } });

    return response.data
}

export const fetchBlocks = async () => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/bloco`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}

export const getBlock = async (id : number) => {
    const authToken = await localStorage.getItem('authToken');

    const response = await axios.get(`${REACT_APP_API_URL}/bloco/${id}`,
    { headers : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
    }})
    
    return response.data
}