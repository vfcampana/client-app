import axios from 'axios';

const REACT_APP_API_URL = process.env.REACT_APP_BACKEND_URL as string;

export const login = async (email : string, password : string): Promise<any> => {
    const response = await axios.post(`${REACT_APP_API_URL}/login`, {
        email: email,
        senha: password,
    }, { headers: { 'Content-Type': 'application/json' } });
    return response.data
}

export const register = async (credentials : any): Promise<any> => {
    const response = await axios.post(`${REACT_APP_API_URL}/cadastro`, {
        ...credentials
    }, { headers: { 'Content-Type': 'application/json' } });
    return response.data
}