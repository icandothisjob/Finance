export const THEME_STORAGE_KEY = 'asset-platform-theme'
export const MODE_STORAGE_KEY = 'asset-platform-mode'

export const themes = [
  { key: 'gold', label: '金色', color: '#c5a47e' },
  { key: 'blue', label: '蓝色', color: '#4f8fd8' },
  { key: 'green', label: '绿色', color: '#46a76d' },
]

export const modes = ['light', 'dark']

const themeKeys = new Set(themes.map((theme) => theme.key))
const modeSet = new Set(modes)

export function normalizeTheme(theme) {
  return themeKeys.has(theme) ? theme : 'gold'
}

export function normalizeMode(mode) {
  return modeSet.has(mode) ? mode : 'light'
}

export function applyTheme(theme) {
  const nextTheme = normalizeTheme(theme)
  document.documentElement.dataset.theme = nextTheme
  return nextTheme
}

export function applyMode(mode) {
  const nextMode = normalizeMode(mode)
  const root = document.documentElement
  root.dataset.mode = nextMode
  // Element Plus 内置暗色 CSS 变量基于 html.dark 选择器
  if (nextMode === 'dark') {
    root.classList.add('dark')
  } else {
    root.classList.remove('dark')
  }
  return nextMode
}

export function getStoredTheme() {
  try {
    return normalizeTheme(localStorage.getItem(THEME_STORAGE_KEY))
  } catch {
    return 'gold'
  }
}

export function getStoredMode() {
  try {
    const stored = localStorage.getItem(MODE_STORAGE_KEY)
    if (stored) return normalizeMode(stored)
    // 未设置过：跟随系统偏好
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'light'
  } catch {
    return 'light'
  }
}

export function saveTheme(theme) {
  const nextTheme = applyTheme(theme)
  try {
    localStorage.setItem(THEME_STORAGE_KEY, nextTheme)
  } catch {
    /* localStorage can be unavailable in private or restricted contexts. */
  }
  return nextTheme
}

export function saveMode(mode) {
  const nextMode = applyMode(mode)
  try {
    localStorage.setItem(MODE_STORAGE_KEY, nextMode)
  } catch {
    /* ignore */
  }
  return nextMode
}

export function toggleMode(currentMode) {
  return saveMode(currentMode === 'dark' ? 'light' : 'dark')
}

export function initTheme() {
  applyMode(getStoredMode())
  return applyTheme(getStoredTheme())
}
