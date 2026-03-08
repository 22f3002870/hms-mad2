import axios from 'axios'
import store from '../store'

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  
})


// Attach token if present
api.interceptors.request.use(config => {
  const token = store.state.auth.token
  if (token) {
    config.headers.Authorization = token
  }
  return config
})

export default api
