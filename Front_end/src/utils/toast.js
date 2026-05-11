/**
 * 统一的轻量级 toast 提示。
 * UI 风格：圆角胶囊条 + 左侧图标 + 标题 + 右侧关闭按钮，从屏幕右上角进入。
 *
 * 用法：
 *   import { toast } from '@/utils/toast'
 *   toast.success('保存成功')
 *   toast.error('操作失败')
 *   toast.warning('请先选择资产大类')
 *   toast.info('提示文本', { duration: 5000 })
 */

const TYPES = {
  success: {
    bg: '#34C77B',
    icon:
      '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="#fff" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>',
  },
  error: {
    bg: '#EF665B',
    icon:
      '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="#fff" d="M13 13h-2V7h2v6zm0 4h-2v-2h2v2zm-1-15C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/></svg>',
  },
  warning: {
    bg: '#F4A340',
    icon:
      '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="#fff" d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
  },
  info: {
    bg: '#8A7355',
    icon:
      '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="#fff" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>',
  },
}

const CLOSE_ICON =
  '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 20 20"><path fill="#fff" d="m15.83 5.34-1.17-1.17-4.66 4.66-4.66-4.66-1.17 1.17 4.66 4.66-4.66 4.66 1.17 1.17 4.66-4.66 4.66 4.66 1.17-1.17-4.66-4.66z"/></svg>'

let containerEl = null
const STYLE_ID = '__app_toast_style__'

function ensureStyle() {
  if (document.getElementById(STYLE_ID)) return
  const style = document.createElement('style')
  style.id = STYLE_ID
  style.textContent = `
    .app-toast-container {
      position: fixed;
      top: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .app-toast {
      pointer-events: auto;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
        Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      min-width: 280px;
      max-width: 420px;
      padding: 12px 14px;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: flex-start;
      border-radius: 10px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18),
                  0 0 5px -3px rgba(17, 17, 17, 0.6);
      color: #fff;
      transform: translateX(120%);
      opacity: 0;
      transition: transform 0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
                  opacity 0.25s ease;
    }
    .app-toast.is-show {
      transform: translateX(0);
      opacity: 1;
    }
    .app-toast.is-hide {
      transform: translateX(120%);
      opacity: 0;
    }
    .app-toast__icon {
      width: 20px;
      height: 20px;
      flex-shrink: 0;
      transform: translateY(-1px);
      margin-right: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .app-toast__icon svg { display: block; }
    .app-toast__title {
      flex: 1;
      font-weight: 500;
      font-size: 14px;
      line-height: 1.45;
      color: #fff;
      word-break: break-word;
    }
    .app-toast__close {
      width: 22px;
      height: 22px;
      flex-shrink: 0;
      cursor: pointer;
      margin-left: 10px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background-color 0.15s ease;
      opacity: 0.85;
    }
    .app-toast__close:hover {
      background: rgba(255, 255, 255, 0.18);
      opacity: 1;
    }
  `
  document.head.appendChild(style)
}

function ensureContainer() {
  ensureStyle()
  if (containerEl && document.body.contains(containerEl)) return containerEl
  containerEl = document.createElement('div')
  containerEl.className = 'app-toast-container'
  document.body.appendChild(containerEl)
  return containerEl
}

function show(type, message, options = {}) {
  const cfg = TYPES[type] || TYPES.info
  const duration = options.duration ?? 3000
  const container = ensureContainer()

  const el = document.createElement('div')
  el.className = 'app-toast'
  el.style.background = cfg.bg
  el.innerHTML = `
    <div class="app-toast__icon">${cfg.icon}</div>
    <div class="app-toast__title">${escapeHtml(String(message ?? ''))}</div>
    <div class="app-toast__close" role="button" aria-label="关闭">${CLOSE_ICON}</div>
  `
  container.appendChild(el)

  requestAnimationFrame(() => {
    el.classList.add('is-show')
  })

  let timer = null
  const close = () => {
    if (timer) {
      clearTimeout(timer)
      timer = null
    }
    el.classList.remove('is-show')
    el.classList.add('is-hide')
    el.addEventListener(
      'transitionend',
      () => {
        el.remove()
      },
      { once: true },
    )
  }

  el.querySelector('.app-toast__close')?.addEventListener('click', close)

  if (duration > 0) {
    timer = setTimeout(close, duration)
  }

  return { close }
}

function escapeHtml(s) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

export const toast = {
  success: (msg, opts) => show('success', msg, opts),
  error: (msg, opts) => show('error', msg, opts),
  warning: (msg, opts) => show('warning', msg, opts),
  info: (msg, opts) => show('info', msg, opts),
}

export default toast
