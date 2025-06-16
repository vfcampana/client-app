import { createContext, useEffect, useState } from "react";
import { login, register } from "../services/auth"

interface AuthContextType {
    signin: (email: string, password: string) => Promise<boolean>;
    signup: (credentials : any) => Promise<boolean>;
    exit: () => Promise<boolean>;
    isLoading: boolean;
    signed: boolean
}
interface AuthProviderProps {
    children: React.ReactNode;
}

export const AuthContext = createContext<AuthContextType>({} as AuthContextType);


export function AuthProvider({ children } : AuthProviderProps) {
    const [user, setUser] = useState()
    const [isLoading, setIsLoading] = useState<boolean>(false)
    const [signed, setSigned] = useState<boolean>(false)

    const signin = async (email : string, password : string) => {
        setIsLoading(true)
        try {
            const response = await login(email, password)
            await localStorage.setItem('authToken', response.access_token)
            setSigned(true)
            return true
        } catch (error : any) {
            console.error("Erro ao fazer login:", error.message)
            return false
        } finally {
            setIsLoading(false)
        }
    }

    const signup = async (credentials : any) => {
        setIsLoading(true)
        try {
            const response = await register(credentials)
            await localStorage.setItem('authToken', response.access_token)
            setSigned(true)
            return true
        } catch (error : any) {
            console.error("Erro ao fazer cadastro:", error.message)
            return false
        } finally {
            setIsLoading(false)
        }
    }

    const exit = async () => {
        setIsLoading(true)
        try {
            await localStorage.removeItem('authToken')
            setSigned(false)
            return true
        } catch (error : any) {
            console.error("Erro ao finalizar sessão", error.message)
            return false
        } finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        const checkToken = async () => {
            const token = await localStorage.getItem('authToken')
            if (token) {
                setSigned(true)
            }
        }
        checkToken()
    }, [])

    return (
    <AuthContext.Provider value={{signin, signup, isLoading, exit, signed}}>
        {children}
    </AuthContext.Provider>
    )
}