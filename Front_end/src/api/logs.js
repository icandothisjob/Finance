import request from './request'

export function listLogs(params) {
  return request.get('/api/logs', { params })
}

export function getUnreadCount() {
  return request.get('/api/logs/unread-count')
}

export function markLogsRead(ids) {
  return request.post('/api/logs/mark-read', { ids: ids ?? null })
}
