<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="(v) => $emit('update:modelValue', v)"
    width="440px"
    :close-on-click-modal="false"
    :show-close="true"
    align-center
    append-to-body
    class="asset-qr-dialog"
    @open="onOpen"
  >
    <template #header>
      <div class="qr-header">
        <div class="qr-header-icon">
          <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
            <path
              fill="currentColor"
              d="M3 11h8V3H3v8zm2-6h4v4H5V5zm8-2v8h8V3h-8zm6 6h-4V5h4v4zM3 21h8v-8H3v8zm2-6h4v4H5v-4zm13-2h3v3h-3zm-5 0h3v3h-3zm5 5h3v3h-3zm-5 0h3v3h-3z"
            />
          </svg>
        </div>
        <div class="qr-header-text">
          <div class="qr-header-title">资产二维码</div>
          <div class="qr-header-sub">{{ asset?.asset_code || '—' }}</div>
        </div>

        <!-- 模式切换：底色块滑动 segmented control -->
        <div
          class="qr-mode-switch"
          role="tablist"
          :data-pending="pendingMode"
        >
          <span class="qr-mode-indicator" @transitionend.self="onIndicatorEnd"></span>
          <button
            type="button"
            class="qr-mode-btn"
            :class="{ active: pendingMode === 'plain' }"
            role="tab"
            :aria-selected="pendingMode === 'plain'"
            @click="onSwitchMode('plain')"
          >纯二维码</button>
          <button
            type="button"
            class="qr-mode-btn"
            :class="{ active: pendingMode === 'label' }"
            role="tab"
            :aria-selected="pendingMode === 'label'"
            @click="onSwitchMode('label')"
          >标签卡</button>
        </div>
      </div>
    </template>

    <div v-loading="loading" class="qr-wrap" :class="`mode-${mode}`">
      <!-- 中间图：纯二维码 / 标签卡预览，相同容器内切换 -->
      <div class="qr-img-box">
        <Transition name="qr-img-fade" mode="out-in">
          <img
            v-if="currentImage"
            :key="mode"
            :src="currentImage"
            :alt="mode === 'label' ? '标签卡预览' : '二维码'"
            :class="['qr-img', mode === 'label' ? 'is-label' : 'is-plain']"
          />
          <div v-else-if="loadError" key="error" class="qr-error">
            <div class="qr-error-title">二维码加载失败</div>
            <div class="qr-error-detail" :title="loadError">{{ loadError }}</div>
            <button type="button" class="qr-error-retry" @click="loadImage">
              重新加载
            </button>
          </div>
          <div v-else key="placeholder" class="qr-placeholder">加载中…</div>
        </Transition>
      </div>

      <div class="qr-info">
        <div class="row">
          <span class="label">编号</span>
          <span class="value mono">{{ asset?.asset_code || '—' }}</span>
        </div>
        <div class="row">
          <span class="label">扫码后跳转</span>
          <div class="value link-row">
            <a
              v-if="qrInfo?.qr_url"
              :href="qrInfo.qr_url"
              target="_blank"
              class="qr-link"
              :title="qrInfo.qr_url"
            >{{ qrInfo.qr_url }}</a>
            <span v-else>—</span>
            <button
              v-if="qrInfo?.qr_url"
              type="button"
              class="copy-btn"
              :class="{ copied: copied }"
              :title="copied ? '已复制' : '复制链接'"
              @click="onCopy"
            >
              <svg v-if="!copied" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
                <path fill="currentColor" d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
                <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 离屏 canvas 用于生成标签卡预览/下载 -->
      <canvas ref="canvasRef" class="hidden-canvas" aria-hidden="true"></canvas>
    </div>

    <template #footer>
      <div class="qr-footer">
        <el-button class="btn-ghost" @click="onDownload" :disabled="!imgSrc">
          <el-icon><Download /></el-icon>
          {{ mode === 'label' ? '下载标签卡' : '下载二维码' }}
        </el-button>
        <el-popconfirm
          title="刷新后旧二维码立即失效，确定刷新？"
          :icon="null"
          :hide-icon="true"
          popper-class="confirm-inline-popconfirm"
          @confirm="onRegenerate"
        >
          <template #reference>
            <el-button class="btn-warning" :loading="regenLoading">
              <el-icon><Refresh /></el-icon>刷新二维码
            </el-button>
          </template>
        </el-popconfirm>
        <el-button class="btn-primary" @click="$emit('update:modelValue', false)">
          关 闭
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { toast } from '../utils/toast'
import { Download, Refresh } from '@element-plus/icons-vue'
import request from '../api/request'
import { getAssetQrInfo, regenerateAssetToken } from '../api/assets'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  asset: { type: Object, default: null },
})
defineEmits(['update:modelValue'])

const loading = ref(false)
const regenLoading = ref(false)
const qrInfo = ref(null)
const imgSrc = ref('')
const labelPreviewSrc = ref('')
const copied = ref(false)
const mode = ref('plain') // 'plain' | 'label'
const pendingMode = ref('plain') // 仅用于切换按钮底色滑动动画的高亮
const canvasRef = ref(null)
const loadError = ref('')

const currentImage = computed(() =>
  mode.value === 'label' ? labelPreviewSrc.value : imgSrc.value,
)

function onSwitchMode(next) {
  if (next === pendingMode.value) return
  pendingMode.value = next
  // 弹窗宽度不变，直接切换内容；按钮底色滑动同步进行
  mode.value = next
  if (next === 'label' && !labelPreviewSrc.value) {
    renderLabelPreview()
  }
}
function onIndicatorEnd() {
  // 兼容旧模板的事件占位，无需逻辑
}

// 标签卡右侧字段：分类 + 型号 + 序列号
const labelItems = computed(() => {
  const a = props.asset
  if (!a) return []
  return [
    { label: '分类', value: a.category },
    { label: '型号', value: a.model },
    { label: '序列号', value: a.serial_number, mono: true },
  ]
})

async function onOpen() {
  if (!props.asset) return
  loading.value = true
  loadError.value = ''
  try {
    qrInfo.value = await getAssetQrInfo(props.asset.id)
  } catch (e) {
    console.error('[AssetQrDialog] 获取二维码信息失败:', e)
    loading.value = false
    return
  }
  try {
    await loadImage()
  } finally {
    loading.value = false
  }
}

async function loadImage() {
  if (imgSrc.value) {
    URL.revokeObjectURL(imgSrc.value)
  }
  imgSrc.value = ''
  labelPreviewSrc.value = ''
  loadError.value = ''
  if (!props.asset) return
  const url = `/api/assets/${props.asset.id}/qrcode.png?ts=${Date.now()}`
  try {
    // 走统一 axios 实例：自动带 token、统一 401 跳转、统一 toast 错误
    const blob = await request.get(url, {
      responseType: 'blob',
      timeout: 20000,
    })
    if (!(blob instanceof Blob)) {
      throw new Error('返回数据格式异常')
    }
    if (blob.size === 0) {
      throw new Error('二维码图片为空（0 字节）')
    }
    if (blob.type && !blob.type.startsWith('image/')) {
      // 后端可能返回了 JSON 错误体（被转成 blob）
      const text = await blob.text().catch(() => '')
      throw new Error(text || `非图片响应：${blob.type}`)
    }
    imgSrc.value = URL.createObjectURL(blob)
    if (mode.value === 'label') {
      renderLabelPreview()
    }
  } catch (e) {
    const status = e?.response?.status
    const detail =
      (typeof e?.response?.data === 'string' && e.response.data) ||
      e?.response?.data?.detail ||
      e?.message ||
      '未知错误'
    const msg = status ? `HTTP ${status}：${detail}` : String(detail)
    loadError.value = msg
    console.error('[AssetQrDialog] 二维码加载失败:', {
      url,
      status,
      error: e,
    })
  }
}

function onDownload() {
  if (!imgSrc.value) return
  if (mode.value === 'plain') {
    downloadPlain()
  } else {
    downloadLabel()
  }
}

function downloadPlain() {
  const a = document.createElement('a')
  a.href = imgSrc.value
  a.download = `qr-${props.asset?.asset_code || 'asset'}.png`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

/**
 * 用 Canvas 绘制"标签卡"PNG：左二维码 + 右标准信息。
 * 输出尺寸采用 2x，确保打印清晰。
 * @returns Promise<string> dataURL（PNG）
 */
function renderLabelToCanvas() {
  return new Promise((resolve, reject) => {
    const a = props.asset
    if (!a || !imgSrc.value) {
      reject(new Error('资产或二维码尚未就绪'))
      return
    }

    const PAD_X = 24
    const PAD_Y = 28
    const QR_BOX = 180
    const DIVIDER_GAP = 32
    const RIGHT_W = 360
    const W = PAD_X + QR_BOX + DIVIDER_GAP + RIGHT_W + PAD_X
    const H = PAD_Y + QR_BOX + PAD_Y
    const SCALE = 2
    const canvas = canvasRef.value || document.createElement('canvas')
    canvas.width = W * SCALE
    canvas.height = H * SCALE
    const ctx = canvas.getContext('2d')
    if (!ctx) {
      reject(new Error('Canvas 上下文不可用'))
      return
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0)
    ctx.scale(SCALE, SCALE)
    ctx.imageSmoothingEnabled = false

    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, W, H)

    const qrX = PAD_X
    // 卡片总高减去 QR 高度后居中（实际效果：QR 在卡片纵向略上方稍居中）
    const qrSize = QR_BOX
    const qrY = (H - qrSize) / 2
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      ctx.drawImage(img, qrX, qrY, qrSize, qrSize)

      const divX = qrX + qrSize + DIVIDER_GAP / 2
      ctx.beginPath()
      ctx.moveTo(divX, qrY + 4)
      ctx.lineTo(divX, qrY + qrSize - 4)
      ctx.strokeStyle = 'rgba(0, 0, 0, 0.12)'
      ctx.lineWidth = 1
      ctx.stroke()

      const rightX = divX + DIVIDER_GAP / 2 + 4
      const maxRightWidth = W - rightX - PAD_X
      ctx.textBaseline = 'top'

      const codeLabelSize = 13
      const codeLabelGap = 10
      const codeValueSize = 28
      const headBlockH = codeLabelSize + codeLabelGap + codeValueSize

      const fields = labelItems.value
      const fieldFontSize = 16
      const labelFontSize = 14
      const rowH = 30
      const rowsCount = Math.max(fields.length, 1)
      const fieldsBlockH = rowH * (rowsCount - 1) + fieldFontSize

      const headFieldsGap = 22
      const totalH = headBlockH + headFieldsGap + fieldsBlockH

      const startY = qrY + Math.max(0, (qrSize - totalH) / 2)

      let y = startY
      ctx.fillStyle = 'rgba(0,0,0,0.55)'
      ctx.font = `600 ${codeLabelSize}px "Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif`
      ctx.fillText('资产编号', rightX, y)
      y += codeLabelSize + codeLabelGap

      ctx.fillStyle = '#0f0f12'
      ctx.font = `700 ${codeValueSize}px "SF Mono",Menlo,Consolas,monospace`
      fillTextEllipsis(ctx, a.asset_code || '—', rightX, y, maxRightWidth, codeValueSize)
      y += codeValueSize + headFieldsGap

      const labelColW = 64
      const valueGap = 16
      for (let i = 0; i < fields.length; i++) {
        const f = fields[i]
        const ry = y + rowH * i

        ctx.fillStyle = 'rgba(0,0,0,0.55)'
        ctx.font = `600 ${labelFontSize}px "Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif`
        ctx.fillText(f.label, rightX, ry + 1)

        ctx.fillStyle = '#0f0f12'
        ctx.font = f.mono
          ? `500 ${fieldFontSize}px "SF Mono",Menlo,Consolas,monospace`
          : `500 ${fieldFontSize}px "Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif`
        const valueX = rightX + labelColW + valueGap
        const valueMax = maxRightWidth - labelColW - valueGap - 4
        fillTextEllipsis(ctx, f.value || '—', valueX, ry, valueMax, fieldFontSize)
      }

      resolve(canvas.toDataURL('image/png'))
    }
    img.onerror = () => reject(new Error('二维码图片加载失败'))
    img.src = imgSrc.value
  })
}

async function renderLabelPreview() {
  try {
    labelPreviewSrc.value = await renderLabelToCanvas()
  } catch (e) {
    toast.error(e?.message || '标签卡预览生成失败')
  }
}

async function downloadLabel() {
  try {
    const url = await renderLabelToCanvas()
    const link = document.createElement('a')
    link.href = url
    link.download = `label-${props.asset?.asset_code || 'asset'}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (e) {
    toast.error(e?.message || '标签卡导出失败')
  }
}

function fillTextEllipsis(ctx, text, x, y, maxWidth, fontSize) {
  const ellipsis = '…'
  let str = String(text ?? '')
  if (ctx.measureText(str).width <= maxWidth) {
    ctx.fillText(str, x, y)
    return
  }
  while (str.length > 0 && ctx.measureText(str + ellipsis).width > maxWidth) {
    str = str.slice(0, -1)
  }
  ctx.fillText(str + ellipsis, x, y)
  // eslint-disable-next-line no-unused-vars
  const _ = fontSize
}

async function onRegenerate() {
  if (!props.asset) return
  regenLoading.value = true
  loadError.value = ''
  try {
    qrInfo.value = await regenerateAssetToken(props.asset.id)
    await loadImage()
    if (!loadError.value) {
      toast.success('已刷新，旧二维码立即失效')
    }
  } catch (e) {
    console.error('[AssetQrDialog] 刷新二维码失败:', e)
  } finally {
    regenLoading.value = false
  }
}

async function onCopy() {
  const url = qrInfo.value?.qr_url
  if (!url) return
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(url)
    } else {
      const ta = document.createElement('textarea')
      ta.value = url
      ta.style.position = 'fixed'
      ta.style.opacity = '0'
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
    }
    copied.value = true
    toast.success('链接已复制')
    setTimeout(() => (copied.value = false), 1500)
  } catch {
    toast.error('复制失败')
  }
}

watch(
  () => props.modelValue,
  (v) => {
    if (!v) {
      if (imgSrc.value) {
        URL.revokeObjectURL(imgSrc.value)
      }
      imgSrc.value = ''
      labelPreviewSrc.value = ''
      qrInfo.value = null
      copied.value = false
      mode.value = 'plain'
      pendingMode.value = 'plain'
      loadError.value = ''
    }
  },
)
</script>

<style scoped>
.qr-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
  padding: 4px 0 0;
}
.hidden-canvas {
  position: absolute;
  left: -9999px;
  top: -9999px;
  pointer-events: none;
}

/* ====== 中间图片容器（纯二维码 / 标签卡预览） ====== */
.qr-img-box {
  position: relative;
  width: 100%;
  min-height: 240px;
  padding: 8px 0;
  background: transparent;
  border: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: min-height 0.28s ease;
}
.qr-img {
  display: block;
  max-width: 100%;
  height: auto;
  image-rendering: pixelated;
}
.qr-img.is-plain {
  width: 240px;
  height: 240px;
}
.qr-img.is-label {
  width: 100%;
  max-width: 100%;
  height: auto;
  image-rendering: auto;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(94, 74, 46, 0.08);
}
.qr-placeholder {
  color: var(--theme-text-muted, #b9a78a);
  font-size: 12px;
}
.qr-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  max-width: 320px;
  padding: 14px 16px;
  text-align: center;
}
.qr-error-title {
  color: #c0413a;
  font-size: 14px;
  font-weight: 600;
}
.qr-error-detail {
  color: var(--theme-primary-deep, #8a7355);
  font-size: 12px;
  line-height: 1.5;
  word-break: break-all;
  max-height: 96px;
  overflow: auto;
}
.qr-error-retry {
  appearance: none;
  border: 1px solid rgba(var(--theme-primary-rgb), 0.45);
  background: #fff;
  color: #6b5d44;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s ease;
}
.qr-error-retry:hover {
  background: #faf3e3;
  border-color: #c9a063;
  color: var(--theme-text-hover, #5e4a2e);
}
.qr-info {
  width: 100%;
  font-size: 13px;
  color: var(--text-primary, #2f2f33);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.label {
  width: 78px;
  flex-shrink: 0;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  padding-top: 2px;
}
.value {
  flex: 1;
  min-width: 0;
  color: var(--text-primary, #2f2f33);
  word-break: break-all;
}
.value.mono {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 12.5px;
  color: var(--theme-text-hover, #5e4a2e);
}

.link-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0;
  min-width: 0;
  background: transparent;
  border: 0;
}
.qr-link {
  flex: 1;
  min-width: 0;
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #b08a52;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 12px;
  text-decoration: none;
  transition: color 0.15s ease;
}
.qr-link:hover {
  color: #8a6e3f;
  text-decoration: underline;
}
.copy-btn {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  background: transparent;
  color: var(--theme-primary-deep, #8a7355);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.18s ease;
}
.copy-btn:hover {
  background: rgba(var(--theme-primary-rgb), 0.15);
  color: var(--theme-text-hover, #5e4a2e);
}
.copy-btn.copied {
  color: #2c7a5e;
}

/* 图片切换过渡：纯二维码 <-> 标签卡预览 */
.qr-img-fade-enter-active,
.qr-img-fade-leave-active {
  transition: opacity 0.26s cubic-bezier(0.22, 1, 0.36, 1),
    transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
.qr-img-fade-enter-from {
  opacity: 0;
  transform: scale(0.96);
}
.qr-img-fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>

<!-- 弹窗本体（teleport 到 body，需要非 scoped 才能命中） -->
<style>
.asset-qr-dialog .el-dialog {
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid rgba(var(--theme-primary-rgb), 0.25);
  box-shadow: 0 20px 60px rgba(94, 74, 46, 0.25);
}
.asset-qr-dialog .el-dialog__header {
  padding: 16px 20px 14px;
  margin-right: 0;
  background: linear-gradient(180deg, var(--theme-surface-subtle, #fffbf3) 0%, #fff 100%);
  border-bottom: 0;
}
.asset-qr-dialog .el-dialog__body {
  padding: 18px 20px 8px;
}
.asset-qr-dialog .el-dialog__footer {
  padding: 14px 20px 18px;
  border-top: 1px solid rgba(var(--theme-primary-rgb), 0.12);
}

.asset-qr-dialog .qr-header {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.asset-qr-dialog .qr-header-icon {
  width: 36px;
  height: 36px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fbf3e3 0%, #f5e6c8 100%);
  border: 1px solid rgba(var(--theme-primary-rgb), 0.35);
  border-radius: 8px;
  color: #b08a52;
}
.asset-qr-dialog .qr-header-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.asset-qr-dialog .qr-header-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary, #2f2f33);
  line-height: 1.2;
}
.asset-qr-dialog .qr-header-sub {
  margin-top: 2px;
  font-size: 12px;
  color: var(--theme-primary-deep, #8a7355);
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  letter-spacing: 0.3px;
}

/* 模式切换：segmented control，金色底色块滑动 */
.asset-qr-dialog .qr-mode-switch {
  position: relative;
  margin-left: auto;
  display: inline-flex;
  gap: 0;
  background: transparent;
  padding: 0;
  isolation: isolate;
  min-width: 144px;
}
.asset-qr-dialog .qr-mode-indicator {
  position: absolute;
  top: 0;
  bottom: 0;
  width: calc(50% );
  background: rgba(var(--theme-primary-rgb), 0.22);
  border-radius: 6px;
  z-index: 0;
  transition: left 0.34s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.2s ease;
  pointer-events: none;
}
.asset-qr-dialog .qr-mode-switch[data-pending="plain"] .qr-mode-indicator {
  left: 0;
}
.asset-qr-dialog .qr-mode-switch[data-pending="label"] .qr-mode-indicator {
  left: 50%;
}
.asset-qr-dialog .qr-mode-btn {
  position: relative;
  z-index: 1;
  appearance: none;
  border: 0;
  font-size: 12px;
  color: var(--theme-primary-deep, #8a7355);
  background: transparent;
  padding: 4px 14px;
  border-radius: 6px;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s ease;
  flex: 1 1 0%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  min-width: 0;
}
.asset-qr-dialog .qr-mode-btn:hover:not(.active) {
  color: var(--theme-text-hover, #5e4a2e);
}
.asset-qr-dialog .qr-mode-btn.active {
  color: var(--theme-text-hover, #5e4a2e);
  font-weight: 600;
}

.asset-qr-dialog .qr-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
}
.asset-qr-dialog .qr-footer .el-button {
  height: 34px;
  padding: 0 14px;
  border-radius: 6px;
  font-weight: 600;
}
.asset-qr-dialog .btn-ghost {
  background: #fff;
  color: #6b5d44;
  border: 1px solid rgba(var(--theme-primary-rgb), 0.45);
}
.asset-qr-dialog .btn-ghost:not(:disabled):hover {
  background: #faf3e3;
  border-color: #c9a063;
  color: var(--theme-text-hover, #5e4a2e);
}
.asset-qr-dialog .btn-warning {
  background: #c9a063;
  color: #fff;
  border: 1px solid #c9a063;
}
.asset-qr-dialog .btn-warning:hover {
  background: #b88f54;
  border-color: #b88f54;
  color: #fff;
}
.asset-qr-dialog .btn-primary {
  background: var(--theme-primary-deep, #8a7355);
  color: #fff;
  border: 1px solid var(--theme-primary-deep, #8a7355);
}
.asset-qr-dialog .btn-primary:hover {
  background: var(--theme-text-hover, #6e5a40);
  border-color: var(--theme-text-hover, #6e5a40);
  color: #fff;
}

/* 标签卡模式下窄屏：右侧字段更紧凑 */
@media (max-width: 720px) {
  .asset-qr-dialog .qr-mode-switch {
    margin-left: 0;
    width: 100%;
    justify-content: center;
  }
  .asset-qr-dialog .qr-label-card {
    flex-direction: column;
    align-items: center;
  }
  .asset-qr-dialog .qr-label-card .lc-info {
    border-left: 0;
    border-top: 1px solid rgba(var(--theme-primary-rgb), 0.3);
    padding: 12px 0 0;
    margin-top: 8px;
    width: 100%;
  }
}

/* 刷新二维码确认气泡现已统一为 AssetsTable.vue 中定义的 .confirm-inline-popconfirm */
</style>
