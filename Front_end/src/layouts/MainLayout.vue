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
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { toast } from '../utils/toast'
import { getUser, clearAuth } from '../utils/auth'
import { logout as apiLogout } from '../api/auth'
import { getUnreadCount } from '../api/logs'
import brandImg from '../img/name.png'

const router = useRouter()
const route = useRoute()

const user = ref(getUser())
const unreadCount = ref(0)

const tabs = [
  { key: 'assets', label: '资产表', path: '/dashboard' },
  { key: 'overview', label: '总览', path: '/overview' },
  { key: 'message', label: '日志', path: '/messages' },
]

const currentPath = computed(() => route.path)

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
  filter: drop-shadow(0 2px 6px rgba(138, 115, 85, 0.25));
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
  color: var(--gold-deep, #8a7355);
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
  margin-left: auto;
}
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
  transition: transform 0.2s ease, background-color 0.2s ease;
}
.user-avatar svg {
  fill: #2f2f33;
  transition: fill 0.2s ease;
}
.user-avatar:hover {
  transform: scale(1.06);
}
.user-avatar:hover svg {
  fill: var(--gold-deep, #8a7355);
}
.user-avatar:focus-visible {
  background: rgba(138, 115, 85, 0.12);
}

/* ===================== 主区域 ===================== */
.main {
  background: var(--bg-page);
  padding: 20px 24px;
  overflow-y: auto;
}
</style>
