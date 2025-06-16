import { useDispatch } from 'react-redux';
import { 
  loginRequest, loginSuccess, loginFailure,
  registerRequest, registerSuccess, registerFailure,
  logoutRequest, logoutSuccess, logoutFailure,
  setAuthStatus
} from '../redux/auth/actions';
import { login, register } from '../services/auth';

export const useAuth = () => {
  const dispatch = useDispatch();

  // Login hook
  const signin = async (email: string, password: string) => {
    dispatch(loginRequest());
    
    try {
      const response = await login(email, password);
      await localStorage.setItem('authToken', response.access_token);
      
      dispatch(loginSuccess(response.user));
      return true;
    } catch (error: any) {
      console.error("Erro ao fazer login:", error.message);
      dispatch(loginFailure(error.message));
      return false;
    }
  };

  // Register hook
  const signup = async (credentials: any) => {
    dispatch(registerRequest());
    
    try {
      const response = await register(credentials);
      await localStorage.setItem('authToken', response.access_token);
      dispatch(registerSuccess(response.user));
      return true;
    } catch (error: any) {
      console.error("Erro ao fazer cadastro:", error.message);
      dispatch(registerFailure(error.message));
      return false;
    }
  };

  // Logout hook
  const exit = async () => {
    dispatch(logoutRequest());
    
    try {
      await localStorage.removeItem('authToken');
      dispatch(logoutSuccess());
      return true;
    } catch (error: any) {
      console.error("Erro ao finalizar sessão", error.message);
      dispatch(logoutFailure(error.message));
      return false;
    }
  };

  // Check auth hook
  const checkAuth = async () => {
    const token = await localStorage.getItem('authToken');
    dispatch(setAuthStatus(!!token));
  };

  return { signin, signup, exit, checkAuth };
};