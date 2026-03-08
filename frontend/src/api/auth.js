import api from './axios'

export const login = (data) => api.post('/login', data)
export const logoutUser = () => api.post('/logout')
