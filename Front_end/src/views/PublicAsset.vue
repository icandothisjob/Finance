<template>
  <div class="page">
    <!-- 顶部装饰光带 -->
    <div class="bg-glow" aria-hidden="true"></div>

    <div class="card">
      <!-- 品牌 -->
      <div class="brand-bar">
        <img :src="logoImg" alt="LOGO" class="brand-logo" />
        <div class="brand-text">
          <div class="brand-title">德工智能资产管理平台</div>
          <div class="brand-sub">Asset Public View</div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="state-box">
        <div class="spinner" aria-hidden="true"></div>
        <div class="state-text">正在加载资产信息…</div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="state-box error">
        <svg viewBox="0 0 24 24" width="40" height="40" aria-hidden="true">
          <path
            fill="#c44545"
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"
          />
        </svg>
        <div class="state-text">{{ error }}</div>
        <div class="state-hint">请联系资产管理员核对二维码或链接。</div>
      </div>

      <!-- Asset Info -->
      <div v-else-if="asset" class="asset">
        <!-- 状态条 -->
        <div class="banner">
          <div class="banner-left">
            <div class="asset-code mono">{{ asset.asset_code }}</div>
            <div class="asset-title">
              {{ assetTitle }}
            </div>
          </div>
        </div>

        <!-- 分组：基础信息 -->
        <div class="section">
          <div class="section-head">
            <span class="section-name">基础信息</span>
          </div>
          <div class="info-grid">
            <div class="info-item" v-for="item in baseItems" :key="item.label">
              <div class="ii-label">{{ item.label }}</div>
              <div class="ii-value" :class="{ mono: item.mono }">
                {{ item.value || '—' }}
              </div>
            </div>
          </div>
        </div>

        <!-- 分组：规格与位置 -->
        <div
          class="section"
          v-if="asset.specification || asset.location"
        >
          <div class="section-head">
            <span class="section-name">规格与位置</span>
          </div>
          <div class="info-grid">
            <div class="info-item" v-if="asset.specification">
              <div class="ii-label">规格</div>
              <div class="ii-value">{{ asset.specification }}</div>
            </div>
            <div class="info-item" v-if="asset.location">
              <div class="ii-label">存放位置</div>
              <div class="ii-value">{{ asset.location }}</div>
            </div>
          </div>
        </div>

        <!-- 分组：购置与使用 -->
        <div class="section">
          <div class="section-head">
            <span class="section-name">购置与使用</span>
          </div>
          <div class="info-grid">
            <div
              class="info-item"
              v-for="item in usageItems"
              :key="item.label"
            >
              <div class="ii-label">{{ item.label }}</div>
              <div class="ii-value" :class="{ mono: item.mono }">{{ item.value || '—' }}</div>
            </div>
          </div>
        </div>

        <!-- 底部提示 -->
        <div class="tip-bar">
          <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
          </svg>
          <span>本页面为只读视图，如需变更请联系资产管理员。</span>
        </div>
      </div>
    </div>

    <div class="footer">
      Asset Management &copy; {{ new Date().getFullYear() }}
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getPublicAsset } from '../api/assets'
import logoImg from '../img/logo.png'

const route = useRoute()
const loading = ref(true)
const error = ref('')
const asset = ref(null)

const assetTitle = computed(() => {
  const a = asset.value
  if (!a) return ''
  const name = [a.brand, a.model].filter(Boolean).join(' ')
  if (a.category && name) return `${a.category} · ${name}`
  return name || a.category || '资产'
})

const baseItems = computed(() => {
  const a = asset.value
  if (!a) return []
  return [
    { label: '资产分类', value: a.category },
    { label: '品牌', value: a.brand },
    { label: '型号', value: a.model },
    { label: '序列号 SN', value: a.serial_number, mono: true },
  ]
})

function fmtDate(v) {
  if (!v) return ''
  const d = new Date(v)
  if (Number.isNaN(d.getTime())) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

function fmtPrice(v) {
  if (v == null || v === '') return ''
  const n = Number(v)
  if (Number.isNaN(n)) return ''
  return `¥ ${n.toFixed(2)}`
}

const usageItems = computed(() => {
  const a = asset.value
  if (!a) return []
  return [
    { label: '购置日期', value: fmtDate(a.purchase_date), mono: true },
    { label: '金额', value: fmtPrice(a.price), mono: true },
    { label: '使用人', value: a.owner },
    { label: '部门', value: a.department },
  ]
})

function statusClass(status) {
  return (
    {
      在用: 'status-active',
      闲置: 'status-idle',
      维修: 'status-repair',
      报废: 'status-scrap',
    }[status] || 'status-default'
  )
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    asset.value = await getPublicAsset(route.params.token)
  } catch (e) {
    error.value =
      e?.response?.data?.detail || '资产不存在或链接已失效'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.page {
  position: relative;
  min-height: 100vh;
  min-height: 100dvh; /* 移动浏览器地址栏伸缩时更稳 */
  padding: 32px 16px 60px;
  padding-top: max(32px, env(safe-area-inset-top));
  padding-bottom: max(60px, calc(env(safe-area-inset-bottom) + 40px));
  padding-left: max(16px, env(safe-area-inset-left));
  padding-right: max(16px, env(safe-area-inset-right));
  display: flex;
  flex-direction: column;
  align-items: center;
  background: transparent;
  font-family: 'HarmonyOS Sans SC', 'Noto Sans SC', 'PingFang SC',
    'Microsoft YaHei UI', 'Microsoft YaHei', -apple-system,
    BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
  color: #2f2f33;
  -webkit-font-smoothing: antialiased;
}
.bg-glow {
  display: none;
}

.card {
  position: relative;
  width: 100%;
  max-width: 520px;
  background: #fff;
  border-radius: 18px;
  border: 1px solid rgba(var(--theme-primary-rgb), 0.18);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 1) inset,
    0 18px 50px rgba(94, 74, 46, 0.18);
  padding: 22px 22px 18px;
}

/* ===================== 品牌条 ===================== */
.brand-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.brand-logo {
  height: 40px;
  width: auto;
  max-width: 160px;
  object-fit: contain;
  user-select: none;
  -webkit-user-drag: none;
}
.brand-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.brand-title {
  font-size: 16px;
  font-weight: 700;
  color: #2f2f33;
  letter-spacing: 1px;
}
.brand-sub {
  font-size: 11px;
  color: var(--theme-text-muted, #b9a78a);
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* ===================== Loading / Error ===================== */
.state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 48px 16px;
  color: var(--theme-primary-deep, #8a7355);
  text-align: center;
}
.state-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--theme-text-hover, #5e4a2e);
}
.state-hint {
  font-size: 12.5px;
  color: var(--theme-text-muted, #b9a78a);
}
.state-box.error .state-text {
  color: #c44545;
}
.spinner {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 3px solid rgba(var(--theme-primary-rgb), 0.25);
  border-top-color: #c9a063;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===================== 横幅：编号 + 名称 + 大类 + 状态 ===================== */
.banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #fbf3e3 0%, #f5e6c8 100%);
  border: 1px solid rgba(var(--theme-primary-rgb), 0.3);
  border-radius: 12px;
  margin-bottom: 18px;
}
.banner-left {
  min-width: 0;
  flex: 1;
}
.asset-code {
  font-size: 13px;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}
.asset-title {
  font-size: 16px;
  font-weight: 700;
  color: #2f2f33;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.banner-right {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

/* 大类徽标（与 AssetsTable 同款的精简版） */
.class-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 22px;
  padding: 0 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
  color: #b08a52;
  background: #fff;
  border: 1.5px solid #c9a063;
  border-radius: 4px;
  font-family: 'Georgia', 'Times New Roman', serif;
}
.class-badge[data-class="IT"]  { color: #1f5fa8; border-color: #4a8bd6; }
.class-badge[data-class="OA"]  { color: #2c7a5e; border-color: #4ea886; }
.class-badge[data-class="FA"]  { color: #8a4b1f; border-color: #d68a4a; }
.class-badge[data-class="VE"]  { color: #6b3a8a; border-color: #9466b8; }

/* 状态 pill */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px 3px 8px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 999px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.08);
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 3px currentColor;
  opacity: 1;
  transform: scale(1);
}
.status-dot {
  background: #999;
  box-shadow: 0 0 0 3px rgba(153, 153, 153, 0.18);
}
.status-active { color: #2c7a5e; border-color: rgba(44, 122, 94, 0.3); }
.status-active .status-dot { background: #2c7a5e; box-shadow: 0 0 0 3px rgba(44,122,94,0.18); }
.status-idle   { color: #1f5fa8; border-color: rgba(31, 95, 168, 0.3); }
.status-idle   .status-dot { background: #1f5fa8; box-shadow: 0 0 0 3px rgba(31,95,168,0.18); }
.status-repair { color: #b08a52; border-color: rgba(176, 138, 82, 0.3); }
.status-repair .status-dot { background: #b08a52; box-shadow: 0 0 0 3px rgba(176,138,82,0.18); }
.status-scrap  { color: #c44545; border-color: rgba(196, 69, 69, 0.3); }
.status-scrap  .status-dot { background: #c44545; box-shadow: 0 0 0 3px rgba(196,69,69,0.18); }

/* ===================== 信息分组 ===================== */
.section {
  margin-top: 14px;
}
.section-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}
.section-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--theme-text-hover, #5e4a2e);
  letter-spacing: 1px;
}
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 16px;
  padding: 0;
  background: transparent;
  border-radius: 0;
  border: none;
}
.info-item.full {
  grid-column: 1 / -1;
}
.ii-label {
  font-size: 11.5px;
  color: var(--theme-primary-deep, #8a7355);
  margin-bottom: 2px;
  letter-spacing: 0.5px;
}
.ii-value {
  font-size: 13.5px;
  color: #2f2f33;
  font-weight: 500;
  word-break: break-all;
  line-height: 1.4;
}
.ii-value.mono {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 12.5px;
  letter-spacing: 0.3px;
}

/* ===================== 底部提示 + 页脚 ===================== */
.tip-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 18px;
  padding: 8px 10px;
  font-size: 11.5px;
  color: var(--theme-text-muted, #b9a78a);
  border-top: 1px dashed rgba(var(--theme-primary-rgb), 0.3);
  padding-top: 12px;
}
.tip-bar svg { color: #c9a063; }

.footer {
  margin-top: 18px;
  color: var(--theme-text-muted, #b9a78a);
  font-size: 11.5px;
  letter-spacing: 1px;
}

/* ===================== 平板：< 768px ===================== */
@media (max-width: 767px) {
  .page {
    padding: 20px 12px 40px;
    padding-top: max(20px, env(safe-area-inset-top));
    padding-bottom: max(40px, calc(env(safe-area-inset-bottom) + 24px));
  }
  .card {
    padding: 18px 16px 14px;
    border-radius: 14px;
    box-shadow:
      0 1px 0 rgba(255, 255, 255, 1) inset,
      0 8px 28px rgba(94, 74, 46, 0.12);
  }
  .brand-bar {
    gap: 10px;
    padding-bottom: 12px;
    margin-bottom: 14px;
  }
  .brand-logo { height: 36px; width: auto; max-width: 140px; }
  .brand-title { font-size: 15px; letter-spacing: 0.5px; }
  .brand-sub { font-size: 10.5px; letter-spacing: 1.5px; }

  .banner {
    padding: 12px 14px;
    margin-bottom: 14px;
    border-radius: 10px;
  }
  .asset-code { font-size: 12px; }
  .asset-title { font-size: 15px; }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 8px 0;
    padding: 10px 12px;
  }
  .info-item {
    padding: 6px 0;
    border-bottom: 1px dashed rgba(var(--theme-primary-rgb), 0.18);
  }
  .info-item:last-child {
    border-bottom: 0;
    padding-bottom: 0;
  }
  .info-item:first-child {
    padding-top: 0;
  }
  .ii-label { font-size: 11px; }
  .ii-value { font-size: 14px; }

  .state-box { padding: 36px 12px; }
  .state-text { font-size: 13.5px; }
  .tip-bar {
    margin-top: 14px;
    padding-top: 10px;
    font-size: 11px;
  }
}

/* ===================== 手机：< 480px ===================== */
@media (max-width: 479px) {
  .page { padding: 16px 10px 36px; }
  .card { padding: 16px 14px 12px; border-radius: 12px; }
  .brand-bar { gap: 10px; }
  .brand-logo { height: 32px; width: auto; max-width: 120px; }
  .brand-title { font-size: 14px; }
  .brand-sub { font-size: 10px; }
  .banner { padding: 10px 12px; }
  .asset-title { font-size: 14px; -webkit-line-clamp: 3; }
  .ii-value { font-size: 13.5px; }
  .ii-value.mono { font-size: 12px; }
  .footer { font-size: 11px; margin-top: 14px; }
}

/* ===================== 极小屏 / 横屏 ===================== */
@media (max-width: 360px) {
  .brand-title { font-size: 13px; letter-spacing: 0; }
  .asset-title { font-size: 13.5px; }
  .ii-value { font-size: 13px; }
}

/* 横屏（视口高度较小）减小垂直留白 */
@media (max-height: 480px) and (orientation: landscape) {
  .page { padding-top: 10px; padding-bottom: 20px; }
  .brand-bar { margin-bottom: 10px; padding-bottom: 10px; }
  .banner { margin-bottom: 10px; }
  .section { margin-top: 10px; }
}

/* 高分辨率：图标边缘锐化 */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 2dppx) {
  .brand-logo {
    image-rendering: -webkit-optimize-contrast;
  }
}
</style>
