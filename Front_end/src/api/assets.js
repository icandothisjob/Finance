import request from './request'

export function listAssets(params) {
  return request.get('/api/assets', { params })
}

export function getAsset(id) {
  return request.get(`/api/assets/${id}`)
}

export function createAsset(data) {
  return request.post('/api/assets', data)
}

export function updateAsset(id, data) {
  return request.put(`/api/assets/${id}`, data)
}

export function deleteAsset(id) {
  return request.delete(`/api/assets/${id}`)
}

export function listAssetClasses() {
  return request.get('/api/assets/dict/classes')
}

export function previewNextCode(params) {
  return request.get('/api/assets/next-code', { params })
}

export function getAssetQrInfo(id) {
  return request.get(`/api/assets/${id}/qrcode-info`)
}

export function regenerateAssetToken(id) {
  return request.post(`/api/assets/${id}/regenerate-token`)
}

export function getPublicAsset(token) {
  return request.get(`/api/public/assets/${token}`)
}

export function listAssetFiles(assetId) {
  return request.get(`/api/assets/${assetId}/files`)
}

export function uploadAssetFile(assetId, file, onProgress) {
  const fd = new FormData()
  fd.append('file', file)
  return request.post(`/api/assets/${assetId}/files`, fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 5 * 60 * 1000,
    onUploadProgress: (e) => {
      if (onProgress && e.total) {
        onProgress(Math.round((e.loaded / e.total) * 100))
      }
    },
  })
}

export function deleteAssetFile(assetId, fileId) {
  return request.delete(`/api/assets/${assetId}/files/${fileId}`)
}

