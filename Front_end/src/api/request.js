import axios from 'axios'
import { toast } from '../utils/toast'
import { getToken, clearAuth } from '../utils/auth'

const request = axios.create({
  baseURL: '/',
  timeout: 15000,
})

request.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail || error.message || '请求失败'
    const msg = typeof detail === 'string' ? detail : '请求失败'

    if (status === 401) {
      clearAuth()
      toast.error('登录已过期，请重新登录')
      const current = window.location.pathname + window.location.search
      if (!current.startsWith('/login')) {
        const redirect = encodeURIComponent(current)
        window.location.href = `/login?redirect=${redirect}`
      }
    } else {
      toast.error(msg)
    }
    return Promise.reject(error)
  },
)

export default request
