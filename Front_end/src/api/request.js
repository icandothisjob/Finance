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
    const data = error?.response?.data
    let detail = data?.detail
    // 后端 500 但没有 detail（多半是 ASGI/代理层错误）时，把 status + URL 显式带上
    if (!detail) {
      if (status) {
        const url = error?.config?.url || ''
        detail = `服务器错误 ${status}（${url}）${error.message ? ' - ' + error.message : ''}`
      } else {
        detail = error.message || '请求失败'
      }
    }
    const msg = typeof detail === 'string' ? detail : JSON.stringify(detail)

    if (status === 401) {
      clearAuth()
      toast.error('登录已过期，请重新登录')
      const current = window.location.pathname + window.location.search
      if (!current.startsWith('/login')) {
        const redirect = encodeURIComponent(current)
        window.location.href = `/login?redirect=${redirect}`
      }
    } else {
      toast.error(msg, { duration: 8000 })
    }
    return Promise.reject(error)
  },
)

export default request
