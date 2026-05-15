<template>
  <el-container class="layout">
    <el-header class="header">
      <!-- 左侧：品牌图片（点击刷新整个页面） -->
      <div class="header-left">
        <img
          :src="brandImg"
          alt="DAIL TECH"
          class="brand-img"
          role="button"
          tabindex="0"
          title="刷新页面"
          @click="reloadPage"
          @keydown.enter.prevent="reloadPage"
          @keydown.space.prevent="reloadPage"
        />
      </div>

      <!-- 中间：导航 tabs（视觉上绝对居中，不受左右宽度影响） -->
      <nav class="header-center" aria-label="主导航">
        <a
          v-for="tab in tabs"
          :key="tab.key"
          href="javascript:void(0)"
          class="nav-tab"
          :class="{ active: isActive(tab) }"
          @click="onTabClick(tab)"
        >
          <span class="nav-tab-text">{{ tab.label }}</span>
          <span
            v-if="tab.key === 'message' && unreadCount > 0"
            class="nav-badge"
          >{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
        </a>
      </nav>

      <!-- 右侧：用户头像下拉，贴到页面最右侧 -->
      <div class="header-right">
        <button
          type="button"
          class="mode-switch"
          :title="currentMode === 'dark' ? '切换到白天模式' : '切换到黑夜模式'"
          :aria-label="currentMode === 'dark' ? '切换到白天模式' : '切换到黑夜模式'"
          @click="onModeToggle"
        >
          <!-- 太阳（射线版）：dark 模式下展示，点击切回 light -->
          <svg
            v-if="currentMode === 'dark'"
            class="mode-icon mode-icon-sun"
            viewBox="0 0 1024 1024"
            width="24"
            height="24"
            aria-hidden="true"
          >
            <path d="M839.646 874.664h-655.18c-18.75 0-33.888-15.137-33.888-33.888v-655.18c0-18.751 15.137-33.888 33.889-33.888h655.18c18.75 0 33.888 15.137 33.888 33.888v655.18c0 18.638-15.25 33.888-33.889 33.888zM573.96 231.911c-207.399-42.7-387.008 136.91-344.308 344.308C252.582 687.373 339.79 774.58 450.944 797.51c207.398 42.7 387.008-136.91 344.308-344.308-22.931-111.041-110.25-198.36-221.292-221.292zM999.26 536.004L536.004 999.261c-13.216 13.217-34.679 13.217-47.895 0L24.739 536.004c-13.217-13.216-13.217-34.679 0-47.895l463.257-463.37c13.216-13.217 34.679-13.217 47.895 0l463.37 463.257c13.217 13.33 13.217 34.792 0 48.008z m-690.31-227.618C197.345 419.992 196.1 600.28 305.223 713.468c113.301 117.593 303.077 117.593 416.378 0 109.121-113.188 107.879-293.476-3.728-405.082-112.849-112.962-295.96-112.962-408.922 0zM535.44 287.15c-145.495-15.588-267.155 105.959-251.567 251.566 11.297 105.62 95.453 189.777 201.073 201.186C630.44 755.489 752.1 633.942 736.512 488.334 725.216 382.602 641.059 298.558 535.44 287.15z" fill="currentColor"/>
          </svg>
          <!-- 月亮：light 模式下展示，点击切到 dark -->
          <svg
            v-else
            class="mode-icon mode-icon-moon"
            viewBox="0 0 1024 1024"
            width="24"
            height="24"
            aria-hidden="true"
          >
            <path d="M803.925 139.349a17.067 17.067 0 0 0-32.17 0l-18.39 51.968a17.067 17.067 0 0 1-10.41 10.368l-51.926 18.39a17.067 17.067 0 0 0 0 32.17l51.926 18.39a17.067 17.067 0 0 1 10.41 10.41l18.347 51.926a17.067 17.067 0 0 0 32.213 0l18.39-51.926a17.067 17.067 0 0 1 10.367-10.41l51.968-18.347a17.067 17.067 0 0 0 0-32.213l-51.968-18.39a17.067 17.067 0 0 1-10.368-10.367l-18.39-51.968zM603.648 308.907a11.776 11.776 0 0 1 22.187 0l10.197 28.629c1.152 3.37 3.84 5.973 7.168 7.168l28.587 10.154a11.776 11.776 0 0 1 0 22.187l-28.587 10.197a11.776 11.776 0 0 0-7.168 7.168l-10.154 28.587a11.776 11.776 0 0 1-22.23 0l-10.154-28.587a11.776 11.776 0 0 0-7.168-7.168l-28.587-10.154a11.776 11.776 0 0 1 0-22.187l28.587-10.197a11.776 11.776 0 0 0 7.168-7.168l10.154-28.587zM715.52 436.096a7.851 7.851 0 0 1 14.806 0l6.784 19.072c.768 2.261 2.56 4.01 4.778 4.821l19.072 6.742a7.851 7.851 0 0 1 0 14.805l-19.072 6.784a7.893 7.893 0 0 0-4.778 4.778l-6.784 19.072a7.851 7.851 0 0 1-14.806 0l-6.74-19.072a7.893 7.893 0 0 0-4.78-4.778l-19.114-6.784a7.851 7.851 0 0 1 0-14.805l19.114-6.742a7.893 7.893 0 0 0 4.78-4.821l6.74-19.072z" fill="currentColor"/>
            <path d="M475.093 198.4a32.427 32.427 0 0 1-2.858 36.395 251.136 251.136 0 0 0-55.467 157.482c0 141.397 118.187 257.579 265.942 257.579 40.618 0 78.976-8.79 113.28-24.448a32.427 32.427 0 0 1 43.648 41.514C786.09 801.323 652.245 896 496.128 896 293.76 896 128 736.256 128 537.301c0-180.992 137.216-329.557 314.325-354.901a32.427 32.427 0 0 1 32.768 16.042z" fill="currentColor"/>
          </svg>
        </button>
        <el-dropdown @command="onThemeCommand" trigger="click" popper-class="theme-dropdown-popper">
          <button
            type="button"
            class="theme-switch"
            :title="`主题色：${currentThemeConfig.label}`"
            aria-label="切换主题色"
          >
            <span
              class="theme-switch-dot"
              :style="{ backgroundColor: currentThemeConfig.color }"
            ></span>
            <svg viewBox="0 0 1024 1024" width="22" height="22" aria-hidden="true">
              <path d="M512 85.333333C276.352 85.333333 85.333333 276.352 85.333333 512s191.018667 426.666667 426.666667 426.666667h71.111111c58.88 0 106.666667-47.786667 106.666667-106.666667 0-27.306667-10.24-52.224-27.093334-71.111111h62.648889c117.76 0 213.333333-95.573333 213.333334-213.333333C938.666667 294.4 747.648 85.333333 512 85.333333zM256 533.333333a64 64 0 1 1 0-128 64 64 0 0 1 0 128z m128-170.666666a64 64 0 1 1 0-128 64 64 0 0 1 0 128z m256 0a64 64 0 1 1 0-128 64 64 0 0 1 0 128z m128 170.666666a64 64 0 1 1 0-128 64 64 0 0 1 0 128z"/>
            </svg>
          </button>
          <template #dropdown>
            <el-dropdown-menu class="theme-dropdown-menu">
              <el-dropdown-item
                v-for="theme in themes"
                :key="theme.key"
                :command="theme.key"
                :title="theme.label"
                :class="['theme-menu-item', { 'is-current-theme': theme.key === currentTheme }]"
              >
                <span
                  class="theme-menu-dot"
                  :style="{ backgroundColor: theme.color }"
                ></span>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown @command="onCommand" trigger="click">
          <span
            class="user-avatar"
            role="button"
            tabindex="0"
            :title="user?.nickname || user?.username || '未登录'"
          >
            <svg viewBox="0 0 1024 1024" width="34" height="34" aria-hidden="true">
              <path d="M513.536 628.6336c101.6832 0 280.8832 38.7072 310.8864 193.7408 77.5168-77.5168 124.928-185.9584 124.928-305.0496 0-241.152-194.6624-435.8144-435.8144-435.8144S77.7216 277.0944 77.7216 517.2224c0 119.0912 47.4112 227.6352 124.928 306.0736 30.0032-154.9312 209.2032-194.6624 310.8864-194.6624z m0-439.7056c112.3328 0 204.3904 91.0336 204.3904 204.3904 0 112.3328-91.0336 204.3904-204.3904 204.3904a203.776 203.776 0 0 1-204.3904-204.3904c0.1024-112.4352 92.0576-204.3904 204.3904-204.3904z"/>
              <path d="M515.4816 1006.8992c-65.8432 0-129.8432-12.9024-189.952-38.4-58.1632-24.576-110.2848-59.8016-155.136-104.5504A485.56032 485.56032 0 0 1 65.8432 708.8128c-25.6-60.2112-38.5024-124.1088-38.5024-189.952 0-65.8432 12.9024-129.8432 38.4-189.952 24.576-58.1632 59.8016-110.2848 104.5504-155.136 44.8512-44.8512 96.9728-79.9744 155.136-104.5504C385.6384 43.6224 449.536 30.72 515.4816 30.72c65.8432 0 129.8432 12.9024 189.952 38.4 58.1632 24.576 110.2848 59.8016 155.136 104.5504 44.8512 44.8512 79.9744 96.9728 104.5504 155.136C990.6176 389.0176 1003.52 452.9152 1003.52 518.8608c0 65.8432-12.9024 129.8432-38.4 189.952-24.576 58.1632-59.8016 110.2848-104.5504 155.136a485.56032 485.56032 0 0 1-155.136 104.5504 484.39296 484.39296 0 0 1-189.952 38.4z m0-936.8576c-60.6208 0-119.3984 11.8784-174.6944 35.2256a447.76448 447.76448 0 0 0-142.6432 96.1536A444.42624 444.42624 0 0 0 101.9904 344.064a446.70976 446.70976 0 0 0-35.2256 174.6944c0 60.6208 11.8784 119.3984 35.2256 174.6944 22.6304 53.4528 54.9888 101.4784 96.1536 142.6432 41.1648 41.2672 89.1904 73.6256 142.6432 96.1536 55.296 23.3472 114.0736 35.2256 174.6944 35.2256 60.6208 0 119.3984-11.8784 174.6944-35.2256 53.4528-22.6304 101.4784-54.9888 142.6432-96.1536 41.2672-41.1648 73.6256-89.1904 96.1536-142.6432 23.3472-55.296 35.2256-114.0736 35.2256-174.6944 0-60.6208-11.8784-119.3984-35.2256-174.6944a447.76448 447.76448 0 0 0-96.1536-142.6432 444.42624 444.42624 0 0 0-142.6432-96.1536 447.44704 447.44704 0 0 0-174.6944-35.2256z"/>
            </svg>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item disabled>
                {{ user?.nickname || user?.username || '未登录' }}
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>
                <el-icon><SwitchButton /></el-icon>退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>

    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { toast } from '../utils/toast'
import { getUser, clearAuth } from '../utils/auth'
import { logout as apiLogout } from '../api/auth'
import { getUnreadCount } from '../api/logs'
import { getStoredTheme, saveTheme, themes, getStoredMode, toggleMode } from '../utils/theme'
import brandImgLight from '../img/name.png'
import brandImgDark from '../img/name_white.png'

const router = useRouter()
const route = useRoute()

const user = ref(getUser())
const unreadCount = ref(0)
const currentTheme = ref(getStoredTheme())
const currentMode = ref(getStoredMode())

const tabs = [
  { key: 'assets', label: '资产表', path: '/dashboard' },
  { key: 'overview', label: '总览', path: '/overview' },
  { key: 'message', label: '日志', path: '/messages' },
]

const currentPath = computed(() => route.path)
const currentThemeConfig = computed(() => (
  themes.find((theme) => theme.key === currentTheme.value) || themes[0]
))
const brandImg = computed(() => (
  currentMode.value === 'dark' ? brandImgDark : brandImgLight
))

function isActive(tab) {
  if (tab.key === 'assets') {
    return currentPath.value === '/dashboard' || currentPath.value === '/' || currentPath.value.startsWith('/assets')
  }
  return currentPath.value.startsWith(tab.path)
}

function onTabClick(tab) {
  if (tab.key === 'overview') {
    toast.info('总览页面开发中')
    return
  }
  if (route.path !== tab.path) {
    router.push(tab.path)
  }
}

function reloadPage() {
  window.location.reload()
}

function onThemeCommand(theme) {
  currentTheme.value = saveTheme(theme)
}

let modeToggleLock = false

async function onModeToggle(e) {
  if (modeToggleLock) return
  modeToggleLock = true

  const btn = e.currentTarget
  const rect = btn.getBoundingClientRect()
  const x = rect.left + rect.width / 2
  const y = rect.top + rect.height / 2

  const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

  if (!document.startViewTransition || reducedMotion) {
    currentMode.value = toggleMode(currentMode.value)
    modeToggleLock = false
    return
  }

  const transition = document.startViewTransition(async () => {
    currentMode.value = toggleMode(currentMode.value)
    await nextTick()
  })

  try {
    await transition.ready

    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y),
    )

    document.documentElement.animate(
      {
        clipPath: [
          `circle(0px at ${x}px ${y}px)`,
          `circle(${endRadius}px at ${x}px ${y}px)`,
        ],
      },
      {
        duration: 580,
        easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
        pseudoElement: '::view-transition-new(root)',
      },
    )

    await transition.finished
  } catch {
    /* transition was skipped */
  } finally {
    modeToggleLock = false
  }
}

async function refreshUnread() {
  try {
    const data = await getUnreadCount()
    unreadCount.value = data?.unread ?? 0
  } catch {
    /* 静默失败：未登录或网络问题 */
  }
}

let pollTimer = null
onMounted(() => {
  refreshUnread()
  pollTimer = setInterval(refreshUnread, 30000)
  window.addEventListener('messages:unread', onUnreadEvent)
})
onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
  window.removeEventListener('messages:unread', onUnreadEvent)
})

function onUnreadEvent(e) {
  if (typeof e.detail === 'number') {
    unreadCount.value = e.detail
  }
}

async function onCommand(cmd) {
  if (cmd === 'logout') {
    try {
      await ElMessageBox.confirm('确定退出登录？', '提示', {
        confirmButtonText: '退出',
        cancelButtonText: '取消',
        type: 'warning',
      })
      try {
        await apiLogout()
      } catch {
        /* 已由拦截器或网络层处理；继续清理本地状态 */
      }
      clearAuth()
      toast.success('已退出登录')
      router.replace('/login')
    } catch {
      /* 用户取消 */
    }
  }
}
</script>

<style scoped>
.layout {
  height: 100vh;
}

/* ===================== 顶部：透明导航栏 ===================== */
.header {
  position: relative;
  background: transparent !important;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 80px !important;
  box-shadow: none;
}

/* 左：品牌图片，整体再向右内缩一点 */
.header-left {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  margin-left: 24px;
}
.brand-img {
  height: 42px;
  width: auto;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
  cursor: pointer;
  transform-origin: left center;
  transition: transform 0.25s ease, filter 0.25s ease;
}
.brand-img:hover {
  transform: scale(1.08);
  filter: drop-shadow(0 2px 6px rgba(var(--theme-primary-deep-rgb), 0.25));
}
.brand-img:active {
  transform: scale(1.04);
}

/* 中：tabs 绝对定位居中，不受两侧宽度变化影响 */
.header-center {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: inline-flex;
  align-items: center;
  gap: 14px;
  font-family: 'Noto Serif SC', 'Source Han Serif SC', 'Songti SC', 'STSong', 'SimSun', serif;
}
.nav-tab {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 84px;
  height: 36px;
  font-size: 17px;
  letter-spacing: 3px;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0 12px;
  cursor: pointer;
  transition: color 0.25s ease, font-size 0.25s ease, font-weight 0.25s ease;
}
.nav-tab:hover {
  color: var(--theme-primary-deep, #8a7355);
}
.nav-tab.active {
  color: var(--text-primary, #2f2f33);
  font-size: 20px;
  font-weight: 700;
}
.nav-tab-text {
  display: inline-block;
}
.nav-badge {
  position: absolute;
  top: 2px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  background: #ef665b;
  color: #fff;
  font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0;
  line-height: 18px;
  border-radius: 9px;
  text-align: center;
  box-shadow: 0 0 0 2px var(--bg-page, #f5efe2);
  animation: badge-pop 0.3s ease;
}
@keyframes badge-pop {
  0% { transform: scale(0.4); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

/* 右：用户区域，自动贴到页面最右侧 */
.header-right {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  gap: 14px;
  margin-left: auto;
}
.mode-switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
  transition: transform 0.2s ease, background-color 0.2s ease;
}
.mode-switch .mode-icon {
  width: 38px;
  height: 38px;
  display: block;
  transform: translateX(10px);
}
.mode-switch:hover {
  transform: scale(1.1) rotate(-8deg);
}
.mode-switch:active {
  transform: scale(0.94);
  transition-duration: 0.1s;
}
.mode-switch:focus-visible {
  background: rgba(var(--theme-primary-deep-rgb), 0.12);
}
/* 月亮：黑色，相对默认位置再向左偏一点 */
.mode-switch .mode-icon-moon {
  color: #1a1a1a;
  transform: translateX(4px);
}
/* 太阳：白色，不加底色光晕 */
.mode-switch .mode-icon-sun {
  width: 30px;
  height: 30px;
  color: #ffffff;
  transform: translate(2px, 0px);
}
.theme-switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  padding: 0;
  color: var(--text-primary, #2f2f33);
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  outline: none;
  transition: transform 0.2s ease, background-color 0.2s ease, color 0.2s ease;
}
.theme-switch svg {
  width: 30px;
  height: 30px;
  display: block;
  fill: currentColor;
  transition: fill 0.2s ease;
}
.theme-switch:hover {
  color: var(--theme-primary-deep, #8a7355);
  transform: scale(1.1);
}
.theme-switch:focus-visible {
  background: rgba(var(--theme-primary-deep-rgb), 0.12);
}
.theme-switch-dot {
  position: absolute;
  right: 7px;
  bottom: 7px;
  width: 12px;
  height: 12px;
  border: 2px solid var(--bg-page, #f5efe2);
  border-radius: 50%;
}
/* 主题色下拉项色块的精细样式集中在 styles/main.css 的
   .theme-dropdown-popper 下，因为 el-dropdown 的弹层会 teleport 到 body，
   作用域 :deep() 无法命中。 */
.user-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  cursor: pointer;
  outline: none;
  background: transparent;
  border: none;
  border-radius: 50%;
  color: var(--text-primary);
  transition: transform 0.2s ease, background-color 0.2s ease, color 0.2s ease;
}
.user-avatar svg {
  fill: currentColor;
  transition: fill 0.2s ease;
}
.user-avatar:hover {
  transform: scale(1.06);
}
.user-avatar:hover svg {
  fill: var(--theme-primary-deep, #8a7355);
}
.user-avatar:focus-visible {
  background: rgba(var(--theme-primary-deep-rgb), 0.12);
}

/* ===================== 主区域 ===================== */
.main {
  background: var(--bg-page);
  padding: 20px 24px;
  overflow-y: auto;
}
</style>
