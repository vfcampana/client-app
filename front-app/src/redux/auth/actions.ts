// src/redux/auth/auth.actions.ts

import AuthActionTypes from './action.types';

// Action creators simples (não são thunks)
export const loginRequest = () => ({
  type: AuthActionTypes.LOGIN_REQUEST
});

export const loginSuccess = (user: any) => ({
  type: AuthActionTypes.LOGIN_SUCCESS,
  payload: user
});

export const loginFailure = (error: string) => ({
  type: AuthActionTypes.LOGIN_FAILURE,
  payload: error
});

export const registerRequest = () => ({
  type: AuthActionTypes.REGISTER_REQUEST
});

export const registerSuccess = (user: any) => ({
  type: AuthActionTypes.REGISTER_SUCCESS,
  payload: user
});

export const registerFailure = (error: string) => ({
  type: AuthActionTypes.REGISTER_FAILURE,
  payload: error
});

export const logoutRequest = () => ({
  type: AuthActionTypes.LOGOUT_REQUEST
});

export const logoutSuccess = () => ({
  type: AuthActionTypes.LOGOUT_SUCCESS
});

export const logoutFailure = (error: string) => ({
  type: AuthActionTypes.LOGOUT_FAILURE,
  payload: error
});

export const setAuthStatus = (isAuthenticated: boolean) => ({
  type: AuthActionTypes.CHECK_AUTH,
  payload: isAuthenticated
});