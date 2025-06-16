import AuthActionTypes from './action.types';

const INITIAL_STATE = {
  user: null,
  isLoading: false,
  signed: false,
  error: null
};

const authReducer = (state = INITIAL_STATE, action: any) => {
  switch (action.type) {
    // Login cases
    case AuthActionTypes.LOGIN_REQUEST:
      return {
        ...state,
        isLoading: true,
        error: null
      };
    case AuthActionTypes.LOGIN_SUCCESS:
      return {
        ...state,
        isLoading: false,
        signed: true,
        user: action.payload,
        error: null
      };
    case AuthActionTypes.LOGIN_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
    
    // Register cases
    case AuthActionTypes.REGISTER_REQUEST:
      return {
        ...state,
        isLoading: true,
        error: null
      };
    case AuthActionTypes.REGISTER_SUCCESS:
      return {
        ...state,
        isLoading: false,
        signed: true,
        user: action.payload,
        error: null
      };
    case AuthActionTypes.REGISTER_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
    
    // Logout cases
    case AuthActionTypes.LOGOUT_REQUEST:
      return {
        ...state,
        isLoading: true
      };
    case AuthActionTypes.LOGOUT_SUCCESS:
      return {
        ...state,
        isLoading: false,
        signed: false,
        user: null
      };
    case AuthActionTypes.LOGOUT_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
    
    // Check auth
    case AuthActionTypes.CHECK_AUTH:
      return {
        ...state,
        signed: action.payload
      };
    
    default:
      return state;
  }
};

export default authReducer;