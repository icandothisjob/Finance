<template>
  <div class="messages-page">
    <!-- 顶部工具条 -->
    <div class="msg-toolbar">
      <div class="toolbar-left">
        <div
          class="scope-switch"
          role="tablist"
          ref="scopeSwitchRef"
          :style="scopeIndicatorStyle"
        >
          <button
            type="button"
            role="tab"
            ref="scopeBtnAllRef"
            :aria-selected="scope === 'all'"
            class="scope-btn"
            :class="{ active: scope === 'all' }"
            @click="onScopeChange('all')"
          >全部日志</button>
          <button
            type="button"
            role="tab"
            ref="scopeBtnMineRef"
            :aria-selected="scope === 'mine'"
            class="scope-btn"
            :class="{ active: scope === 'mine' }"
            @click="onScopeChange('mine')"
          >仅我的</button>
          <span class="scope-indicator" aria-hidden="true"></span>
        </div>

        <div
          class="filter-chips"
          ref="chipsContainerRef"
          :style="chipIndicatorStyle"
        >
          <span class="chip-indicator" aria-hidden="true"></span>
          <span
            v-for="opt in actionOptions"
            :key="opt.value || 'all'"
            class="chip"
            :class="{ active: actionFilter === opt.value }"
            :data-value="opt.value || 'all'"
            @click="onActionChange(opt.value)"
          >{{ opt.label }}</span>
        </div>
      </div>

      <div class="toolbar-right">
        <div class="form-control" :class="{ 'is-filled': !!keyword }">
          <input
            type="text"
            required
            v-model="keyword"
            @keyup.enter="reload(true)"
          />
          <label aria-hidden="true">
            <span
              v-for="(ch, i) in keywordLabel"
              :key="i"
              :style="{ transitionDelay: `${i * 50}ms` }"
            >{{ ch }}</span>
          </label>
        </div>
        <el-tooltip content="查询" placement="top">
          <button
            type="button"
            class="svg-icon-btn search-btn"
            @click="reload(true)"
            aria-label="查询"
          >
            <svg viewBox="0 0 1024 1024" width="21" height="21" aria-hidden="true">
              <path d="M469.333333 0c259.2 0 469.333333 210.133333 469.333334 469.333333 0 114.218667-40.832 218.922667-108.629334 300.330667l161.664 161.706667a42.666667 42.666667 0 1 1-60.373333 60.330666l-161.706667-161.706666A467.413333 467.413333 0 0 1 469.333333 938.666667c-259.2 0-469.333333-210.133333-469.333333-469.333334s210.133333-469.333333 469.333333-469.333333z m0 85.333333a384 384 0 1 0 0 768 384 384 0 0 0 0-768z"/>
              <path d="M469.333333 170.666667c102.528 0 195.669333 57.088 250.026667 148.906666a42.666667 42.666667 0 1 1-73.386667 43.52c-39.552-66.773333-105.344-107.093333-176.64-107.093333a42.666667 42.666667 0 0 1 0-85.333333z"/>
              <path d="M725.333333 469.333333m-42.666666 0a42.666667 42.666667 0 1 0 85.333333 0 42.666667 42.666667 0 1 0-85.333333 0Z"/>
            </svg>
          </button>
        </el-tooltip>

        <el-tooltip content="重置" placement="top">
          <button
            type="button"
            class="svg-icon-btn reset-btn"
            @click="onReset"
            aria-label="重置"
          >
            <svg viewBox="0 0 1024 1024" width="24" height="24" aria-hidden="true">
              <path d="M377.856 856.576l-19.456 71.68c23.04 8.704 46.08 14.848 70.656 19.456l20.992-71.68c-25.088-4.096-49.152-10.752-72.192-19.456z m318.976-714.752V363.52h74.24v-115.712c68.096 67.072 111.104 160.256 111.104 263.68 0 204.8-165.376 370.176-370.176 370.176V955.904c244.736 0 443.904-199.168 443.904-443.904 0-113.664-43.52-217.6-114.688-295.936h77.312V141.824H696.832z m-101.376-65.536l-20.992 71.68c24.576 4.096 48.64 10.752 71.68 19.456l19.456-71.68c-23.04-8.704-46.08-14.848-70.144-19.456z m-83.456-8.192c-244.736 0-443.904 199.168-443.904 443.904 0 113.664 43.008 217.6 113.152 295.936h-76.288v74.24H326.656V660.48h-74.24v115.712c-68.096-67.072-111.104-160.256-111.104-263.68 0-204.8 165.376-370.176 370.176-370.176v-74.24z"/>
            </svg>
          </button>
        </el-tooltip>
        <button
          type="button"
          class="btn-secondary"
          :disabled="unread === 0"
          @click="onMarkAllRead"
        >
          全部已读
          <span v-if="unread > 0" class="unread-pill">{{ unread > 99 ? '99+' : unread }}</span>
        </button>
      </div>
    </div>

    <!-- 时间线 -->
    <div
      class="msg-timeline"
      :class="{ empty: !loading && items.length === 0, 'first-load': playToken <= 1 }"
      :key="`timeline-${playToken}`"
    >
      <template v-if="items.length > 0">
        <div
          v-for="group in grouped"
          :key="group.date"
          class="day-group"
        >
          <div class="day-label">
            <span class="day-line"></span>
            <span class="day-text">{{ group.label }}</span>
            <span class="day-line"></span>
          </div>
          <div
            v-for="row in group.items"
            :key="row.id"
            class="msg-card"
            :class="[
              `act-${row.action.split('.')[0]}`,
              `act-${row.action.replace(/\./g, '-')}`,
              { unread: !row.is_read },
            ]"
            @click="onCardClick(row)"
          >
            <div class="msg-icon">
              <img
                v-if="actionImage(row.action)"
                :src="actionImage(row.action)"
                :alt="actionLabel(row.action)"
                class="msg-icon-img"
              />
              <span v-else v-html="actionIcon(row.action)"></span>
            </div>
            <div class="msg-body">
              <div class="msg-head">
                <span class="actor">{{ row.actor || '系统' }}</span>
                <span class="action-tag" :class="`tag-${row.action.replace('.', '-')}`">
                  {{ actionLabel(row.action) }}
                </span>
                <span class="meta-time">{{ fmtTime(row.created_at) }}</span>
              </div>
              <div class="msg-foot">
                <div class="msg-summary">{{ row.summary }}</div>
                <div v-if="row.ip" class="meta-ip">
                  <svg viewBox="0 0 24 24" width="11" height="11" aria-hidden="true">
                    <path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/>
                  </svg>
                  {{ row.ip }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- 空状态 -->
      <div v-else-if="!loading" class="empty-state">
        <svg viewBox="0 0 1024 1024" width="64" height="64" aria-hidden="true">
          <path
            fill="#d4b89a"
            d="M512 64a448 448 0 1 0 0 896 448 448 0 0 0 0-896zm0 832a384 384 0 1 1 0-768 384 384 0 0 1 0 768zm-32-256h64v64h-64v-64zm0-320h64v256h-64V320z"
          />
        </svg>
        <div class="empty-title">暂无日志</div>
        <div class="empty-sub">所有的资产新增、修改、删除等操作都会同步记录在这里</div>
      </div>

      <!-- 骨架/Loading -->
      <div v-if="loading && items.length === 0" class="loading">加载中…</div>
    </div>

    <!-- 分页 -->
    <div v-if="total > pageSize" class="msg-pager">
      <el-pagination
        v-model:current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, jumper, total"
        background
        @current-change="reload(false)"
      />
    </div>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailOpen"
      :show-close="true"
      width="560px"
      align-center
      append-to-body
      class="log-detail-dialog"
      destroy-on-close
    >
      <template #header>
        <div class="dlg-header" v-if="detailRow">
          <div class="dlg-icon">
            <img
              v-if="actionImage(detailRow.action)"
              :src="actionImage(detailRow.action)"
              :alt="actionLabel(detailRow.action)"
            />
            <span v-else v-html="actionIcon(detailRow.action)"></span>
          </div>
          <div class="dlg-title-wrap">
            <div class="dlg-title-line">
              <span class="dlg-actor">{{ detailRow.actor || '系统' }}</span>
              <span
                class="action-tag"
                :class="`tag-${detailRow.action.replace('.', '-')}`"
              >{{ actionLabel(detailRow.action) }}</span>
            </div>
            <div class="dlg-summary">{{ detailRow.summary }}</div>
          </div>
        </div>
      </template>

      <div v-if="detailRow" class="dlg-body">
        <div class="dlg-meta-row">
          <div class="dlg-meta-item">
            <span class="dlg-meta-label">时间</span>
            <span class="dlg-meta-value">{{ fmtFullTime(detailRow.created_at) }}</span>
          </div>
          <div v-if="detailRow.ip" class="dlg-meta-item">
            <span class="dlg-meta-label">来源 IP</span>
            <span class="dlg-meta-value mono">{{ detailRow.ip }}</span>
          </div>
          <div v-if="detailRow.target_label" class="dlg-meta-item">
            <span class="dlg-meta-label">对象</span>
            <span class="dlg-meta-value mono">{{ detailRow.target_label }}</span>
          </div>
        </div>

        <template v-if="detailRow.changes && detailRow.changes.length > 0">
          <div class="dlg-section-title">
            字段变更
            <span class="dlg-section-count">{{ detailRow.changes.length }}</span>
          </div>
          <div class="dlg-changes">
            <div
              v-for="(c, i) in detailRow.changes"
              :key="i"
              class="dlg-change-row"
            >
              <div class="dlg-change-label">{{ c.label }}</div>
              <div class="dlg-change-flow">
                <span class="dlg-ch-before">{{ c.before ?? '空' }}</span>
                <svg viewBox="0 0 24 24" width="14" height="14" class="dlg-ch-arrow" aria-hidden="true">
                  <path fill="currentColor" d="M16.01 11H4v2h12.01v3L20 12l-3.99-4z"/>
                </svg>
                <span class="dlg-ch-after">{{ c.after ?? '空' }}</span>
              </div>
            </div>
          </div>
        </template>

        <div v-else class="dlg-empty">该操作没有字段级变更记录</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { listLogs, markLogsRead } from '../api/logs'
import { toast } from '../utils/toast'

import imgAssetCreate from '../img/新增资产.png'
import imgAssetUpdate from '../img/修改资产.png'
import imgAssetDelete from '../img/删除资产.png'
import imgAssetImport from '../img/批量上传.png'
import imgQrRegen from '../img/二维码刷新.png'
import imgFileUpload from '../img/上传文件.png'
import imgFileDelete from '../img/删除文件.png'
import imgLogin from '../img/登入.png'
import imgLogout from '../img/登出.png'

const ACTION_IMAGE_MAP = {
  'asset.create': imgAssetCreate,
  'asset.update': imgAssetUpdate,
  'asset.delete': imgAssetDelete,
  'asset.import': imgAssetImport,
  'asset.qr.regen': imgQrRegen,
  'file.upload': imgFileUpload,
  'file.delete': imgFileDelete,
  login: imgLogin,
  logout: imgLogout,
}

function actionImage(a) {
  return ACTION_IMAGE_MAP[a] || ''
}

const scope = ref('all')
const actionFilter = ref('')
const keyword = ref('')
const keywordLabel = computed(() => Array.from('Keyword'))
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const unread = ref(0)
const items = ref([])
const loading = ref(false)

const actionOptions = [
  { value: '', label: '全部类型' },
  { value: 'asset.create', label: '新增资产' },
  { value: 'asset.update', label: '修改资产' },
  { value: 'asset.delete', label: '删除资产' },
  { value: 'asset.import', label: '批量导入' },
  { value: 'asset.qr.regen', label: '二维码刷新' },
  { value: 'file.upload', label: '上传附件' },
  { value: 'file.delete', label: '删除附件' },
  { value: 'login', label: '登录' },
  { value: 'logout', label: '登出' },
]

const ACTION_LABEL_MAP = Object.fromEntries(
  actionOptions.filter((o) => o.value).map((o) => [o.value, o.label]),
)

/* ===== scope-switch 下划线滑动指示器 ===== */
const scopeSwitchRef = ref(null)
const scopeBtnAllRef = ref(null)
const scopeBtnMineRef = ref(null)
const scopeIndicator = ref({ left: 0, width: 0 })
const scopeIndicatorStyle = computed(() => ({
  '--scope-indicator-left': `${scopeIndicator.value.left}px`,
  '--scope-indicator-width': `${scopeIndicator.value.width}px`,
}))
function updateScopeIndicator() {
  const container = scopeSwitchRef.value
  const target = scope.value === 'all' ? scopeBtnAllRef.value : scopeBtnMineRef.value
  if (!container || !target) return
  const cb = container.getBoundingClientRect()
  const tb = target.getBoundingClientRect()
  scopeIndicator.value = { left: tb.left - cb.left, width: tb.width }
}

/* ===== filter-chips 底色滑动指示器 ===== */
const chipsContainerRef = ref(null)
const chipIndicator = ref({ left: 0, width: 0, opacity: 0 })
const chipIndicatorStyle = computed(() => ({
  '--chip-indicator-left': `${chipIndicator.value.left}px`,
  '--chip-indicator-width': `${chipIndicator.value.width}px`,
  '--chip-indicator-opacity': chipIndicator.value.opacity,
}))
function updateChipIndicator() {
  const container = chipsContainerRef.value
  if (!container) return
  const target = container.querySelector('.chip.active')
  if (!target) {
    chipIndicator.value = { ...chipIndicator.value, opacity: 0 }
    return
  }
  const cb = container.getBoundingClientRect()
  const tb = target.getBoundingClientRect()
  chipIndicator.value = {
    left: tb.left - cb.left,
    width: tb.width,
    opacity: 1,
  }
}

function refreshIndicators() {
  nextTick(() => {
    updateScopeIndicator()
    updateChipIndicator()
  })
}

watch([scope, actionFilter], refreshIndicators)
onMounted(() => {
  refreshIndicators()
  window.addEventListener('resize', refreshIndicators)
})
onUnmounted(() => {
  window.removeEventListener('resize', refreshIndicators)
})

function actionLabel(a) {
  return ACTION_LABEL_MAP[a] || a
}

// 每个动作配一个高识别度的语义化图标（双图层：底色块 + 角标）
const ACTION_ICON_MAP = {
  // 新增资产：纸箱 + 加号角标
  'asset.create':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M21 8.5L12 4 3 8.5v7L12 20l9-4.5v-7zM12 6.18L18.18 9 12 12.06 5.82 9 12 6.18zM5 10.62l6 2.97v6.16l-6-3v-6.13zm14 6.13l-6 3v-6.16l6-2.97v6.13z"/>' +
      '<g transform="translate(15.5 14)">' +
        '<circle cx="4" cy="4" r="4.5" fill="#fff"/>' +
        '<path fill="#2c7a5e" d="M4 1.5v5M1.5 4h5" stroke="#2c7a5e" stroke-width="1.5" stroke-linecap="round"/>' +
      '</g>' +
    '</svg>',
  // 修改资产：纸箱 + 铅笔角标
  'asset.update':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M21 8.5L12 4 3 8.5v7L12 20l9-4.5v-7zM12 6.18L18.18 9 12 12.06 5.82 9 12 6.18zM5 10.62l6 2.97v6.16l-6-3v-6.13zm14 6.13l-6 3v-6.16l6-2.97v6.13z"/>' +
      '<g transform="translate(13.5 12)">' +
        '<circle cx="5" cy="5" r="5.2" fill="#fff"/>' +
        '<path fill="#b08a52" d="M2.2 7l.55-1.65L6.4 1.7a.7.7 0 0 1 .98 0l.92.92a.7.7 0 0 1 0 .98L4.65 7.25 3 7.8a.4.4 0 0 1-.5-.5L2.2 7z"/>' +
      '</g>' +
    '</svg>',
  // 删除资产：纸箱 + 红色叉角标
  'asset.delete':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M21 8.5L12 4 3 8.5v7L12 20l9-4.5v-7zM12 6.18L18.18 9 12 12.06 5.82 9 12 6.18zM5 10.62l6 2.97v6.16l-6-3v-6.13zm14 6.13l-6 3v-6.16l6-2.97v6.13z" opacity="0.55"/>' +
      '<g transform="translate(13.5 12)">' +
        '<circle cx="5" cy="5" r="5.2" fill="#fff"/>' +
        '<path stroke="#c44545" stroke-width="1.6" stroke-linecap="round" d="M3 3l4 4M7 3l-4 4"/>' +
      '</g>' +
    '</svg>',
  // 批量导入：纸箱 + 向下箭头角标（表示从外部一次导入很多）
  'asset.import':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M21 8.5L12 4 3 8.5v7L12 20l9-4.5v-7zM12 6.18L18.18 9 12 12.06 5.82 9 12 6.18zM5 10.62l6 2.97v6.16l-6-3v-6.13zm14 6.13l-6 3v-6.16l6-2.97v6.13z" opacity="0.6"/>' +
      '<g transform="translate(13 11.5)">' +
        '<circle cx="5" cy="5" r="5.2" fill="#fff"/>' +
        '<path fill="none" stroke="#5a8dc5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M5 2v5M2.7 5L5 7.3 7.3 5M2.3 8.3h5.4"/>' +
      '</g>' +
    '</svg>',
  // 二维码刷新：二维码 + 旋转箭头
  'asset.qr.regen':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M3 3h7v7H3V3zm2 2v3h3V5H5zm9-2h7v7h-7V3zm2 2v3h3V5h-3zM3 14h7v7H3v-7zm2 2v3h3v-3H5zm12.5-3.5l1.7 1.7A4 4 0 1 1 14 18v-1.6a2.4 2.4 0 1 0 4-1.8l-1.7 1.7-1.4-1.4 3-3 3 3-1.4 1.4z"/>' +
    '</svg>',
  // 上传附件：云朵向上箭头
  'file.upload':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M19.35 10.04A7.49 7.49 0 0 0 12 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 0 0 0 14a6 6 0 0 0 6 6h13a5 5 0 0 0 .35-9.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/>' +
    '</svg>',
  // 删除附件：文件 + 红色叉
  'file.delete':
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm4 18H6V4h7v5h5v11z"/>' +
      '<path stroke="#c44545" stroke-width="1.8" stroke-linecap="round" fill="none" d="M9 13l5 5M14 13l-5 5"/>' +
    '</svg>',
  // 登录：门 + 向内箭头
  login:
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M11 7L9.6 8.4l2.6 2.6H2v2h10.2l-2.6 2.6L11 17l5-5-5-5z"/>' +
      '<path fill="currentColor" d="M14 3a2 2 0 0 1 2 2v3h-2V5h-2V3h2zm0 18h-2v-2h2v-3h2v3a2 2 0 0 1-2 2zm6-18a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4v-2h4V5h-4V3h4z" opacity="0.55"/>' +
    '</svg>',
  // 登出：门 + 向外箭头
  logout:
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">' +
      '<path fill="currentColor" d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5-5-5z"/>' +
      '<path fill="currentColor" d="M4 5h6V3H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h6v-2H4V5z" opacity="0.55"/>' +
    '</svg>',
}

function actionIcon(a) {
  return (
    ACTION_ICON_MAP[a] ||
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="6" fill="currentColor"/></svg>'
  )
}

function fmtTime(t) {
  if (!t) return ''
  const d = new Date(t)
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)} 分钟前`
  const sameDay =
    d.getFullYear() === now.getFullYear() &&
    d.getMonth() === now.getMonth() &&
    d.getDate() === now.getDate()
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  if (sameDay) return `${hh}:${mm}`
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day} ${hh}:${mm}`
}

function dayLabel(t) {
  const d = new Date(t)
  const now = new Date()
  const startOf = (x) => new Date(x.getFullYear(), x.getMonth(), x.getDate()).getTime()
  const diffDay = Math.round((startOf(now) - startOf(d)) / 86400000)
  if (diffDay === 0) return '今天'
  if (diffDay === 1) return '昨天'
  if (diffDay < 7) return `${diffDay} 天前`
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day}`
}

const grouped = computed(() => {
  const out = []
  const map = new Map()
  for (const it of items.value) {
    const d = new Date(it.created_at)
    const key = `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`
    if (!map.has(key)) {
      map.set(key, { date: key, label: dayLabel(it.created_at), items: [] })
      out.push(map.get(key))
    }
    map.get(key).items.push(it)
  }
  return out
})

const playToken = ref(0)

async function reload(reset = false) {
  if (reset) page.value = 1
  loading.value = true
  try {
    const data = await listLogs({
      page: page.value,
      page_size: pageSize.value,
      scope: scope.value,
      action: actionFilter.value || undefined,
      keyword: keyword.value || undefined,
    })
    items.value = data.items || []
    total.value = data.total || 0
    unread.value = data.unread || 0
    playToken.value++
  } finally {
    loading.value = false
  }
}

function onScopeChange(v) {
  if (scope.value === v) return
  scope.value = v
  reload(true)
}

function onActionChange(v) {
  if (actionFilter.value === v) return
  actionFilter.value = v
  reload(true)
}

function clearKeyword() {
  keyword.value = ''
  reload(true)
}

function onReset() {
  keyword.value = ''
  actionFilter.value = ''
  scope.value = 'all'
  reload(true)
}

async function onMarkOne(row) {
  if (row.is_read) return
  try {
    const res = await markLogsRead([row.id])
    row.is_read = true
    unread.value = res?.unread ?? Math.max(unread.value - 1, 0)
    window.dispatchEvent(new CustomEvent('messages:unread', { detail: unread.value }))
  } catch {
    /* 已由拦截器提示 */
  }
}

const detailOpen = ref(false)
const detailRow = ref(null)

function onCardClick(row) {
  detailRow.value = row
  detailOpen.value = true
  if (!row.is_read) {
    onMarkOne(row)
  }
}

function fmtFullTime(t) {
  if (!t) return ''
  const d = new Date(t)
  const pad = (n) => String(n).padStart(2, '0')
  return (
    `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` +
    `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
  )
}

async function onMarkAllRead() {
  try {
    const res = await markLogsRead(null)
    items.value.forEach((it) => (it.is_read = true))
    unread.value = res?.unread ?? 0
    window.dispatchEvent(new CustomEvent('messages:unread', { detail: unread.value }))
    toast.success('已全部标记为已读')
  } catch {
    /* 已由拦截器提示 */
  }
}

let pollTimer = null
onMounted(() => {
  reload(true)
  pollTimer = setInterval(() => {
    if (!loading.value) reload(false)
  }, 30000)
})
onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

watch(scope, () => {
  // already handled by onScopeChange
})
</script>

<style scoped>
.messages-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-family: 'HarmonyOS Sans SC', 'Noto Sans SC', 'PingFang SC',
    'Microsoft YaHei UI', 'Microsoft YaHei', -apple-system,
    BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
  letter-spacing: 0.3px;
  -webkit-font-smoothing: antialiased;
  color: #2f2f33;
  animation: page-fade-in 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.messages-page .msg-toolbar {
  animation: section-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: 0.06s;
}
.messages-page .msg-timeline.first-load {
  animation: section-rise 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: 0.16s;
}
@keyframes page-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes section-rise {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ===================== 工具条（扁平、无卡片） ===================== */
.msg-toolbar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 18px;
  padding: 4px 4px 14px;
  background: transparent;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  margin-bottom: 4px;
}
.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  flex-wrap: wrap;
}
/* 让左侧 scope/chips 与右侧输入框底线大致齐平 */
.scope-switch,
.filter-chips {
  align-self: center;
  margin-bottom: 6px;
}
.toolbar-right .btn-secondary,
.toolbar-right .btn-icon {
  margin-bottom: 6px;
}

/* 左侧 scope 改为下划线式 segmented tabs，下划线在按钮之间平移 */
.scope-switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 22px;
  padding: 0;
  background: transparent;
  margin-right: 4px;
}
.scope-btn {
  appearance: none;
  border: 0;
  background: transparent;
  height: 28px;
  padding: 0;
  font-size: 14px;
  font-weight: 600;
  color: #b9a78a;
  cursor: pointer;
  position: relative;
  letter-spacing: 0.5px;
  transition: color 0.25s ease;
}
.scope-btn:hover {
  color: #8a7355;
}
.scope-btn.active {
  color: #2f2f33;
}
/* 滑动下划线 */
.scope-indicator {
  position: absolute;
  bottom: -6px;
  left: 0;
  height: 2px;
  background: #c9a063;
  border-radius: 2px;
  pointer-events: none;
  transform: translateX(var(--scope-indicator-left, 0));
  width: var(--scope-indicator-width, 0);
  transition: transform 0.34s cubic-bezier(0.22, 1, 0.36, 1),
    width 0.34s cubic-bezier(0.22, 1, 0.36, 1);
}

/* 一道竖向分隔线，强化 scope 与 chips 的层级 */
.toolbar-left::before {
  content: none;
}
.scope-switch + .filter-chips {
  position: relative;
  padding-left: 14px;
}
.scope-switch + .filter-chips::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 14px;
  background: rgba(201, 160, 99, 0.35);
}

.filter-chips {
  position: relative;
  display: inline-flex;
  flex-wrap: wrap;
  gap: 4px;
  isolation: isolate;
}
/* 滑动底色块 */
.chip-indicator {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  background: rgba(201, 160, 99, 0.18);
  border-radius: 6px;
  pointer-events: none;
  z-index: 0;
  opacity: var(--chip-indicator-opacity, 0);
  transform: translateX(var(--chip-indicator-left, 0));
  width: var(--chip-indicator-width, 0);
  transition: transform 0.34s cubic-bezier(0.22, 1, 0.36, 1),
    width 0.34s cubic-bezier(0.22, 1, 0.36, 1),
    opacity 0.2s ease;
}
.chip {
  position: relative;
  z-index: 1;
  font-size: 12px;
  color: #8a7355;
  background: transparent;
  border: 0;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  user-select: none;
  transition: color 0.22s ease,
    transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.chip:hover:not(.active) {
  color: #5e4a2e;
}
.chip:active {
  transform: scale(0.94);
}
.chip.active {
  color: #5e4a2e;
  font-weight: 600;
}

/* 金色浮动 label 输入框（与资产表保持一致） */
.form-control {
  position: relative;
  margin: 0;
  width: 220px;
}
.form-control input {
  background-color: transparent;
  border: 0;
  border-bottom: 2px solid #e0d2b8;
  display: block;
  width: 100%;
  padding: 14px 0 6px;
  font-size: 15px;
  color: var(--gold-deep, #8a7355);
  font-family: inherit;
  transition: border-bottom-color 0.25s ease;
}
.form-control input:focus,
.form-control input:valid,
.form-control.is-filled input {
  outline: 0;
  border-bottom-color: var(--gold, #c5a47e);
}
.form-control label {
  position: absolute;
  top: 14px;
  left: 0;
  pointer-events: none;
  display: flex;
}
.form-control label span {
  display: inline-block;
  font-size: 15px;
  min-width: 5px;
  color: #b9a78a;
  letter-spacing: 1px;
  transition: 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.form-control input:focus + label span,
.form-control input:valid + label span,
.form-control.is-filled label span {
  color: var(--gold-deep, #8a7355);
  transform: translateY(-18px);
  font-size: 11px;
  font-weight: 600;
}

/* "全部已读" 改为文字按钮（无边框） */
.btn-secondary {
  appearance: none;
  border: 0;
  background: transparent;
  color: #8a7355;
  height: 30px;
  padding: 0 6px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s ease, background-color 0.22s ease,
    transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.btn-secondary:hover:not(:disabled) {
  color: #5e4a2e;
  background: rgba(201, 160, 99, 0.1);
  transform: translateY(-1px);
}
.btn-secondary:active:not(:disabled) {
  transform: scale(0.96);
  transition-duration: 0.1s;
}
.btn-secondary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.unread-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  padding: 0;
  background: #ef665b;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  line-height: 1;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 刷新按钮：纯图标，悬浮才出现底色 */
.btn-icon {
  appearance: none;
  border: 0;
  background: transparent;
  color: #8a7355;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.18s ease;
}
.btn-icon:hover:not(:disabled) {
  background: rgba(201, 160, 99, 0.12);
  color: #5e4a2e;
}
.btn-icon .spinning {
  animation: spin 0.9s linear infinite;
}

/* ===================== 资产表同款图标按钮（查询 / 重置） ===================== */
.svg-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  outline: none;
  transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), filter 0.18s ease;
  line-height: 0;
}
.svg-icon-btn svg {
  display: block;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), fill 0.18s ease;
}
.svg-icon-btn:hover {
  transform: scale(1.18);
}
.svg-icon-btn:active {
  transform: scale(0.92);
  transition-duration: 0.1s;
}
.svg-icon-btn:focus-visible {
  outline: 1px dashed rgba(138, 115, 85, 0.5);
  outline-offset: 2px;
}
.svg-icon-btn.search-btn,
.svg-icon-btn.reset-btn {
  padding: 6px;
}
.svg-icon-btn.search-btn svg,
.svg-icon-btn.reset-btn svg { fill: #8a7355; }
.svg-icon-btn.search-btn:hover svg,
.svg-icon-btn.reset-btn:hover svg { fill: #6e5a40; }
.svg-icon-btn.reset-btn svg { transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1); }
.svg-icon-btn.reset-btn:hover svg { transform: rotate(-180deg); }
.svg-icon-btn.search-btn:hover svg { animation: search-bounce 0.5s ease; }
@keyframes search-bounce {
  0%, 100% { transform: translateY(0); }
  40%      { transform: translateY(-3px) scale(1.05); }
  70%      { transform: translateY(0) scale(0.98); }
}
/* 让图标按钮的下沿与输入框底部金线对齐 */
.toolbar-right .svg-icon-btn {
  padding-bottom: 6px;
  margin-bottom: 0;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ===================== 时间线 ===================== */
.msg-timeline {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
}
.day-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.day-label {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 2px 4px 2px;
  animation: day-label-in 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes day-label-in {
  from { opacity: 0; transform: translateY(-4px); }
  to   { opacity: 1; transform: translateY(0); }
}
.day-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(
    to right,
    transparent,
    rgba(201, 160, 99, 0.35),
    transparent
  );
}
.day-text {
  font-size: 12px;
  color: #8a7355;
  letter-spacing: 1px;
  font-weight: 600;
}

.msg-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px 8px 14px;
  background: #fff;
  border: 2px solid rgba(201, 160, 99, 0.45);
  border-radius: 10px;
  animation: msg-card-rise 0.42s cubic-bezier(0.22, 1, 0.36, 1) both;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  cursor: pointer;
  overflow: hidden;
}
.msg-card .msg-body {
  padding-bottom: 0;
}

.msg-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(138, 115, 85, 0.15);
  border-color: rgba(201, 160, 99, 0.7);
}
.msg-card:active {
  transform: scale(0.995);
  transition-duration: 0.1s;
}
.msg-card.unread {
  background: #fffbf3;
  border-style: dashed;
  border-color: rgba(201, 160, 99, 0.7);
}
/* 交错入场：限定在前 12 张，避免大列表性能负担 */
.msg-card:nth-child(1)  { animation-delay: 0.02s; }
.msg-card:nth-child(2)  { animation-delay: 0.05s; }
.msg-card:nth-child(3)  { animation-delay: 0.08s; }
.msg-card:nth-child(4)  { animation-delay: 0.11s; }
.msg-card:nth-child(5)  { animation-delay: 0.14s; }
.msg-card:nth-child(6)  { animation-delay: 0.17s; }
.msg-card:nth-child(7)  { animation-delay: 0.20s; }
.msg-card:nth-child(8)  { animation-delay: 0.23s; }
.msg-card:nth-child(9)  { animation-delay: 0.26s; }
.msg-card:nth-child(10) { animation-delay: 0.29s; }
.msg-card:nth-child(11) { animation-delay: 0.32s; }
.msg-card:nth-child(12) { animation-delay: 0.35s; }

@keyframes msg-card-rise {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 卡片左侧图标：直接展示 PNG，无边框无底色 */
.msg-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 0;
  background: transparent;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  color: #b08a52;
}
.msg-icon-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
  display: block;
  user-select: none;
  -webkit-user-drag: none;
}

.msg-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.msg-head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.actor {
  font-weight: 700;
  font-size: 13.5px;
  color: #2f2f33;
}
.action-tag {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  background: #f0e7d3;
  color: #8a7355;
}
.tag-asset-create { background: #e1f3e8; color: #2c7a5e; }
.tag-asset-update { background: #fff3d9; color: #b08a52; }
.tag-asset-delete { background: #fde4e4; color: #c44545; }
.tag-asset-qr-regen { background: #e6f0fb; color: #1f5fa8; }
.tag-file-upload { background: #e6f0fb; color: #1f5fa8; }
.tag-file-delete { background: #fde4e4; color: #c44545; }
.tag-login { background: #f0e7f7; color: #6b3a8a; }
.tag-logout { background: #f0e7f7; color: #6b3a8a; }

.unread-dot {
  width: 7px;
  height: 7px;
  background: #ef665b;
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(239, 102, 91, 0.18);
}
.msg-summary {
  font-size: 13.5px;
  color: #2f2f33;
  line-height: 1.35;
}

.changes {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-top: 2px;
  padding: 5px 10px;
  background: #f9f5ec;
  border-left: 2px solid rgba(201, 160, 99, 0.5);
  border-radius: 0 6px 6px 0;
}
.change-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  flex-wrap: wrap;
}
.ch-field {
  color: #8a7355;
  font-weight: 600;
  min-width: 56px;
}
.ch-before {
  color: #c44545;
  text-decoration: line-through;
  background: rgba(196, 69, 69, 0.08);
  padding: 1px 6px;
  border-radius: 3px;
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.ch-after {
  color: #2c7a5e;
  background: rgba(44, 122, 94, 0.08);
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.ch-arrow {
  color: #b9a78a;
  flex-shrink: 0;
}

.meta-time {
  margin-left: auto;
  font-size: 12px;
  color: #999;
  line-height: 1.2;
}
.msg-foot {
  display: flex;
  align-items: center;
  gap: 12px;
}
.msg-foot .msg-summary {
  flex: 1;
  min-width: 0;
}
.meta-ip {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: #b9a78a;
  letter-spacing: 0.3px;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  line-height: 1.2;
}
.meta-ip svg {
  color: #d4b89a;
}

/* 空 / loading */
.msg-timeline.empty {
  min-height: 320px;
}
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 60px 20px;
  color: #b9a78a;
  text-align: center;
}
.empty-title {
  font-size: 16px;
  color: #8a7355;
  font-weight: 600;
}
.empty-sub {
  font-size: 12.5px;
}
.loading {
  text-align: center;
  color: #b9a78a;
  padding: 40px;
  font-size: 13px;
}

.msg-pager {
  display: flex;
  justify-content: flex-end;
  padding: 8px 4px 4px;
}
</style>

<!-- 弹窗内部样式：因 el-dialog 通过 teleport 渲染到 body，使用非 scoped -->
<style>
.log-detail-dialog .el-dialog {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(201, 160, 99, 0.25);
  box-shadow: 0 20px 60px rgba(94, 74, 46, 0.25);
}
.log-detail-dialog .el-dialog__header {
  padding: 18px 22px 14px;
  margin-right: 0;
  background: linear-gradient(180deg, #fffbf3 0%, #fff 100%);
  border-bottom: 1px solid rgba(201, 160, 99, 0.18);
}
.log-detail-dialog .el-dialog__body {
  padding: 18px 22px 22px;
}
.log-detail-dialog .dlg-header {
  display: flex;
  align-items: center;
  gap: 14px;
}
.log-detail-dialog .dlg-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.log-detail-dialog .dlg-icon img {
  width: 40px;
  height: 40px;
  object-fit: contain;
  display: block;
}
.log-detail-dialog .dlg-title-wrap {
  flex: 1;
  min-width: 0;
}
.log-detail-dialog .dlg-title-line {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 4px;
}
.log-detail-dialog .dlg-actor {
  font-size: 15px;
  font-weight: 700;
  color: #2f2f33;
}
.log-detail-dialog .action-tag {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.5px;
  background: #f0e7d3;
  color: #8a7355;
}
.log-detail-dialog .tag-asset-create { background: #e1f3e8; color: #2c7a5e; }
.log-detail-dialog .tag-asset-update { background: #fff3d9; color: #b08a52; }
.log-detail-dialog .tag-asset-delete { background: #fde4e4; color: #c44545; }
.log-detail-dialog .tag-asset-qr-regen { background: #e6f0fb; color: #1f5fa8; }
.log-detail-dialog .tag-file-upload { background: #e6f0fb; color: #1f5fa8; }
.log-detail-dialog .tag-file-delete { background: #fde4e4; color: #c44545; }
.log-detail-dialog .tag-login { background: #f0e7f7; color: #6b3a8a; }
.log-detail-dialog .tag-logout { background: #f0e7f7; color: #6b3a8a; }
.log-detail-dialog .dlg-summary {
  font-size: 14px;
  color: #555;
  line-height: 1.5;
}

.log-detail-dialog .dlg-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
  padding: 10px 14px;
  background: #faf6ec;
  border-radius: 8px;
  margin-bottom: 16px;
}
.log-detail-dialog .dlg-meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
.log-detail-dialog .dlg-meta-label {
  color: #8a7355;
  font-weight: 600;
}
.log-detail-dialog .dlg-meta-value {
  color: #2f2f33;
}
.log-detail-dialog .dlg-meta-value.mono {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 12.5px;
}

.log-detail-dialog .dlg-section-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #5e4a2e;
  margin-bottom: 10px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(201, 160, 99, 0.25);
  width: 100%;
}
.log-detail-dialog .dlg-section-count {
  background: #c9a063;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 999px;
  min-width: 18px;
  text-align: center;
}

.log-detail-dialog .dlg-changes {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 380px;
  overflow-y: auto;
}
.log-detail-dialog .dlg-change-row {
  display: grid;
  grid-template-columns: 80px 1fr;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #fafafa;
  border-radius: 6px;
}
.log-detail-dialog .dlg-change-row:hover {
  background: #f5f0e3;
}
.log-detail-dialog .dlg-change-label {
  font-size: 12.5px;
  color: #8a7355;
  font-weight: 600;
}
.log-detail-dialog .dlg-change-flow {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  font-size: 13px;
}
.log-detail-dialog .dlg-ch-before {
  color: #c44545;
  text-decoration: line-through;
  background: rgba(196, 69, 69, 0.08);
  padding: 2px 8px;
  border-radius: 4px;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.log-detail-dialog .dlg-ch-after {
  color: #2c7a5e;
  background: rgba(44, 122, 94, 0.08);
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.log-detail-dialog .dlg-ch-arrow {
  color: #b9a78a;
  flex-shrink: 0;
}
.log-detail-dialog .dlg-empty {
  padding: 24px;
  text-align: center;
  color: #b9a78a;
  font-size: 13px;
  background: #faf6ec;
  border-radius: 8px;
}

/* ===================== 日志详情弹窗 进入动效 ===================== */
.log-detail-dialog {
  animation: log-dialog-pop-in 0.36s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes log-dialog-pop-in {
  from {
    opacity: 0;
    transform: translate3d(0, 18px, 0) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1);
  }
}
.el-overlay:has(.log-detail-dialog) {
  animation: log-dialog-overlay-in 0.28s ease both;
}
@keyframes log-dialog-overlay-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* 字段变更行：进入时上浮淡入 */
.log-detail-dialog .dlg-change-row {
  animation: change-row-fade 0.32s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.log-detail-dialog .dlg-change-row:nth-child(1) { animation-delay: 0.04s; }
.log-detail-dialog .dlg-change-row:nth-child(2) { animation-delay: 0.08s; }
.log-detail-dialog .dlg-change-row:nth-child(3) { animation-delay: 0.12s; }
.log-detail-dialog .dlg-change-row:nth-child(4) { animation-delay: 0.16s; }
.log-detail-dialog .dlg-change-row:nth-child(5) { animation-delay: 0.20s; }
.log-detail-dialog .dlg-change-row:nth-child(n+6) { animation-delay: 0.24s; }
@keyframes change-row-fade {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
