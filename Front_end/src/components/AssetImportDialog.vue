<template>
  <el-dialog
    v-model="visible"
    width="80vw"
    :close-on-click-modal="false"
    append-to-body
    class="asset-import-dialog"
    align-center
    @closed="onClosed"
  >
    <div class="import-steps-bar">
      <div
        v-for="(s, i) in STEPS"
        :key="s.key"
        class="import-step"
        :class="{
          'is-current': stepIndex === i,
          'is-done': stepIndex > i,
          'is-todo': stepIndex < i,
        }"
      >
        <span class="import-step-num">
          <svg
            :viewBox="STEP_ICONS[i].viewBox"
            width="16"
            height="16"
            aria-hidden="true"
          >
            <path
              v-for="(d, k) in STEP_ICONS[i].paths"
              :key="k"
              fill="currentColor"
              :d="d"
            />
          </svg>
        </span>
        <span class="import-step-label">{{ s.title }}</span>
      </div>
    </div>

    <!-- ============ Step 1: 上传 ============ -->
    <div v-if="step === 'upload'" class="step-body">
      <el-upload
        class="upload-dropzone"
        drag
        :auto-upload="false"
        :show-file-list="false"
        accept=".xlsx,.csv"
        :on-change="onPickFile"
      >
        <div class="dropzone-inner">
          <div class="dropzone-icon">
            <svg viewBox="40 140 944 740" width="124" height="98" aria-hidden="true">
              <path
                fill="currentColor"
                d="M881.664 455.68c-20.48-17.408-28.672-34.816-32.768-61.44-12.288-91.136-64.512-154.624-148.48-186.368-88.064-33.792-174.08-24.576-247.808 37.888-15.36 14.336-30.72 21.504-49.152 23.552A189.44 189.44 0 0 0 256 198.656h-0.288a191.2 191.2 0 0 0-191.2 191.2v0.288c0 47.104 16.384 89.088 44.032 122.88-31.744 53.248-37.888 115.712-16.384 178.176 30.72 89.088 109.568 144.384 208.896 144.384h443.392c92.16-1.024 172.032-56.32 202.752-142.336 30.72-84.992 6.144-179.2-65.536-237.568zM87.04 390.144C87.04 296.96 162.816 222.208 256 222.208c52.224 0 99.328 23.552 130.048 61.44 7.168 9.216 13.312 18.432 19.456 29.696 7.168 15.36 13.312 32.768 16.384 50.176 1.024 9.216 2.048 17.408 2.048 26.624A168.032 168.032 0 0 1 256 558.08c-29.696 0-58.368-7.168-81.92-20.48a184.8 184.8 0 0 1-28.896-20.672l0.224 0.192a179.2 179.2 0 0 1-19.264-19.232l-0.192-0.224a169.504 169.504 0 0 1-38.912-107.488v-0.032z m833.536 285.696c-23.552 77.824-93.184 129.024-177.152 129.024H299.008c-86.016 0-156.672-51.2-180.224-130.048-15.36-49.152-10.24-97.28 12.288-139.264 9.216 8.192 20.48 15.36 31.744 22.528-15.36 28.672-18.432 62.464-9.216 98.304 17.408 67.584 72.704 109.568 148.48 109.568h432.128c77.824 0 136.192-41.984 152.576-110.592 17.408-67.584-14.336-132.096-82.944-168.96-9.216-6.144-19.456-20.48-19.456-30.72 2.048-91.136-38.912-159.744-113.664-186.368-83.968-28.672-158.72-2.048-214.016 77.824-3.072 4.096-6.144 8.192-11.264 13.312h-1.024a193.28 193.28 0 0 0-18.944-59.456l0.512 1.088c11.264-2.048 20.48-8.192 31.744-19.456 65.536-66.56 147.456-78.848 231.424-47.104 80.896 31.744 128 94.208 132.096 183.296 0 23.552 9.216 36.864 27.648 50.176 68.608 47.104 96.256 129.024 71.68 206.848zM266.24 459.776c-23.552 2.048-44.032-7.168-60.416-26.624l25.6-25.6H153.6V486.4c8.192-9.216 16.384-16.384 24.576-25.6 16.384 18.432 34.816 30.72 58.368 35.84a109.344 109.344 0 0 0 68.32-5.376l-0.736 0.256c35.84-16.384 57.344-44.032 65.536-83.968h-39.936c-8.192 30.72-34.816 51.2-63.488 52.224z m-9.216-139.264a68.16 68.16 0 0 1 60.288 28.48l0.128 0.192c-7.168 7.168-15.36 15.36-24.576 23.552h76.8v-76.8c-8.192 8.192-16.384 15.36-24.576 23.552-34.816-36.864-76.8-49.152-124.928-29.696-36.864 14.336-58.368 43.008-66.56 82.944h39.936a71.104 71.104 0 0 1 63.264-52.224h0.224z"
              />
            </svg>
          </div>
          <div class="dropzone-title">点击或拖拽 Excel / CSV 文件到此处</div>
          <div class="dropzone-sub">
            支持 .xlsx / .csv，单文件不超过 50 MB（旧版 .xls 请先另存为 .xlsx）
          </div>
          <div v-if="parsing" class="parsing-tip">
            <el-icon class="is-loading"><Loading /></el-icon>
            正在解析并请求大模型识别字段映射 …
          </div>
        </div>
      </el-upload>
    </div>

    <!-- ============ Step 2: 列映射 ============ -->
    <div v-else-if="step === 'mapping'" class="step-body mapping-body">
      <!-- 表头行识别信息条 -->
      <div class="header-row-bar">
        <div class="hr-left">
          <span class="hr-label">表头行：</span>
          <span class="hr-row">第 <b>{{ headerRow }}</b> 行</span>

          <span class="hr-sep" aria-hidden="true" />

          <span class="hr-cols">共识别到 <b>{{ headers.length }}</b> 个列</span>
          <span v-if="parseRes.llm_used" class="ai-badge is-ai">
            <svg viewBox="0 0 24 24" class="ai-badge-icon" aria-hidden="true">
              <path
                fill="currentColor"
                d="M12 3l1.3 3.7L17 8l-3.7 1.3L12 13l-1.3-3.7L7 8l3.7-1.3L12 3zm6 10l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9.9-2.1z"
              />
            </svg>
            AI 智能扫描
          </span>
          <span v-else class="ai-badge is-rule">
            <svg viewBox="0 0 24 24" class="ai-badge-icon" aria-hidden="true">
              <path
                fill="currentColor"
                d="M13 2L4 14h6l-1 8 10-13h-7l1-7z"
              />
            </svg>
            规则兜底映射
          </span>
        </div>
        <div class="hr-right">
          <span class="hr-tip muted">未匹配的列将被忽略，不会进入数据库</span>
          <el-button
            size="small"
            link
            class="hr-switch-btn"
            @click="headerPickerVisible = !headerPickerVisible"
          >
            {{ headerPickerVisible ? '收起' : '识别错了？切换表头行' }}
          </el-button>
        </div>
      </div>

      <!-- 表头行选择器：展示顶部预览供用户点选 -->
      <div v-if="headerPickerVisible && topRowsPreview.length" class="header-picker">
        <div class="hp-tip">
          下方是文件顶部 {{ topRowsPreview.length }} 行的预览，<b>点击行号</b>把该行设为表头：
        </div>
        <div class="hp-table-wrap">
          <table class="hp-table">
            <tbody>
              <tr
                v-for="(row, idx) in topRowsPreview"
                :key="idx"
                :class="{ 'is-current': idx + 1 === headerRow }"
                @click="onPickHeaderRow(idx + 1)"
              >
                <td class="hp-rownum">
                  第 {{ idx + 1 }} 行
                  <span v-if="idx + 1 === headerRow" class="hp-cur">当前</span>
                </td>
                <td
                  v-for="(cell, j) in row.slice(0, 12)"
                  :key="j"
                  :title="cell || ''"
                  class="hp-cell"
                >{{ cell ?? '' }}</td>
                <td v-if="row.length > 12" class="hp-more">… 还有 {{ row.length - 12 }} 列</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <el-table :data="mappingTable" size="small" class="mapping-table">
        <el-table-column prop="original" label="Excel 原列名" min-width="200">
          <template #default="{ row }">
            <span class="mono">{{ row.original }}</span>
          </template>
        </el-table-column>
        <el-table-column label="样本数据" min-width="280">
          <template #default="{ row }">
            <span class="sample-text">{{ row.sample || '—' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="映射到系统字段" width="280">
          <template #default="{ row }">
            <el-select
              v-model="mapping[row.original]"
              clearable
              placeholder="不导入此列"
              size="small"
              style="width: 100%"
            >
              <el-option
                v-for="f in fieldDict"
                :key="f.key"
                :label="f.label"
                :value="f.key"
              />
            </el-select>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- ============ Step 3: 数据预览 ============ -->
    <div v-else-if="step === 'preview'" class="step-body preview-body">
      <div class="preview-notice">
        资产编号将由平台按
        <b>「机构 - 大类 - 年份 - 流水」</b>
        规则自动生成，Excel 里的编号会被忽略，无需手工填写
      </div>

      <div class="step-summary preview-summary">
        <span>共 <b>{{ rows.length }}</b> 行</span>
        <span class="ok">可入库 <b>{{ selectableCount }}</b></span>
        <span class="warn">含警告 <b>{{ parseRes.warning_count }}</b></span>
        <span class="err">含错误 <b>{{ parseRes.error_count }}</b></span>
        <span class="selected">已勾选 <b>{{ selectedRows.length }}</b></span>
        <el-button
          type="primary"
          size="small"
          plain
          :loading="aiFilling"
          :disabled="errorRows.length === 0 && warningRows.length === 0"
          class="ai-fill-btn"
          @click="onAiFill"
        >
          <span v-if="!aiFilling" class="ai-fill-icon-wrap" aria-hidden="true">
            <svg class="ai-fill-icon" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M12 3l1.4 4 4 1.4-4 1.4L12 13.8 10.6 9.8l-4-1.4 4-1.4L12 3zm6 11l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2z"
              />
            </svg>
          </span>
          AI 一键补全{{ errorRows.length || warningRows.length
            ? `（${errorRows.length || warningRows.length} 行）`
            : '' }}
        </el-button>
        <span class="muted">绿色行可入库，黄色行有警告（可入库），红色行需先修复；点击右侧校验标签可直接修正</span>
      </div>

      <el-table
        :data="rows"
        border
        size="small"
        class="preview-table"
        height="calc(70vh - 240px)"
        :row-class-name="rowClass"
        @selection-change="onSelectionChange"
        ref="previewTableRef"
      >
        <el-table-column type="selection" width="44" :selectable="isRowSelectable" />
        <el-table-column label="#" width="56" align="center">
          <template #default="{ row }">
            <span class="row-index">{{ row.row_index }}</span>
          </template>
        </el-table-column>
        <el-table-column
          v-for="f in previewColumns"
          :key="f.key"
          :label="f.label"
          :min-width="columnWidth(f.key)"
        >
          <template #default="{ row, $index }">
            <el-input
              v-if="editing.idx === $index && editing.field === f.key"
              v-model="editing.value"
              size="small"
              autofocus
              @blur="commitEdit"
              @keyup.enter="commitEdit"
              @keyup.esc="cancelEdit"
            />
            <span
              v-else
              class="cell-display"
              :class="{
                'is-empty': isEmpty(row.data[f.key]),
                'is-locked': aiFilling,
              }"
              :title="aiFilling
                ? 'AI 补全进行中，暂不可手动编辑'
                : formatCell(row.data[f.key])"
              @dblclick="aiFilling
                ? null
                : startEdit($index, f.key, row.data[f.key])"
            >
              {{ formatCell(row.data[f.key]) || '—' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="校验" width="240">
          <template #default="{ row, $index }">
            <div v-if="!row.issues.length" class="issue-ok">通过</div>
            <div v-else class="issue-list">
              <el-tooltip
                v-for="(it, i) in row.issues"
                :key="i"
                :content="aiFilling
                  ? 'AI 补全进行中，暂不可手动修正'
                  : `${it.message}（点击修正）`"
                placement="top"
              >
                <el-tag
                  :type="it.level === 'error' ? 'danger' : 'warning'"
                  size="small"
                  effect="light"
                  class="issue-tag"
                  :class="aiFilling ? 'is-locked' : 'clickable'"
                  @click="aiFilling ? null : openFixDialog($index, it)"
                >
                  {{ fieldLabel(it.field) || '整行' }}
                </el-tag>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- ============ Step 4: 结果 ============ -->
    <div v-else-if="step === 'result'" class="step-body result-body">
      <!-- 中心庆祝区 -->
      <div
        class="result-celebrate"
        :class="commitRes.failed === 0 ? 'is-success' : 'is-warning'"
      >
        <!-- 烟花层 -->
        <div v-if="confettiList.length" class="confetti-layer" aria-hidden="true">
          <span
            v-for="(c, i) in confettiList"
            :key="i"
            class="confetti"
            :style="c"
          />
        </div>

        <!-- 大图标 + 光圈 -->
        <div class="result-big-icon">
          <span class="ring ring-1" />
          <span class="ring ring-2" />
          <span class="ring ring-3" />
          <svg
            v-if="commitRes.failed === 0"
            viewBox="0 0 120 120"
            class="big-icon-svg"
            aria-hidden="true"
          >
            <circle cx="60" cy="60" r="56" fill="currentColor" opacity="0.12" />
            <circle cx="60" cy="60" r="46" fill="currentColor" />
            <path
              class="big-check"
              d="M38 62l16 16 30-34"
              stroke="#ffffff"
              stroke-width="7"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"
            />
          </svg>
          <svg
            v-else
            viewBox="0 0 120 120"
            class="big-icon-svg"
            aria-hidden="true"
          >
            <circle cx="60" cy="60" r="56" fill="currentColor" opacity="0.12" />
            <circle cx="60" cy="60" r="46" fill="currentColor" />
            <path
              d="M60 32v36"
              stroke="#ffffff"
              stroke-width="7"
              stroke-linecap="round"
            />
            <circle cx="60" cy="86" r="4.5" fill="#ffffff" />
          </svg>
        </div>

        <!-- 大标题 + 副标题 -->
        <div class="result-big-title">
          {{ commitRes.failed === 0 ? '导入完成' : '部分导入失败' }}
        </div>
        <div class="result-big-sub">
          成功 <b class="ok">{{ commitRes.success }}</b> 个，失败
          <b :class="commitRes.failed > 0 ? 'err' : 'zero'">{{ commitRes.failed }}</b> 个
        </div>
      </div>

      <!-- 失败明细 -->
      <div v-if="commitRes.failures.length" class="failures-block">
        <div class="failures-title">
          <span class="fail-dot" />失败明细
        </div>
        <el-table
          :data="commitRes.failures"
          size="small"
          max-height="240"
          class="failures-table"
        >
          <el-table-column type="index" label="#" width="50" />
          <el-table-column prop="asset_code" label="资产编号" width="220" />
          <el-table-column prop="error" label="错误信息" />
        </el-table>
      </div>
    </div>

    <template v-if="step !== 'upload'" #footer>
      <div class="dialog-footer">
        <el-button v-if="step !== 'result'" @click="goBack">
          上一步
        </el-button>
        <el-button
          v-if="step === 'mapping'"
          type="primary"
          @click="goPreview"
        >下一步</el-button>
        <el-button
          v-if="step === 'preview'"
          type="primary"
          :loading="committing"
          :disabled="selectedRows.length === 0"
          @click="onCommit"
        >开始导入（{{ selectedRows.length }} 条）</el-button>
        <el-button
          v-if="step === 'result'"
          type="primary"
          @click="visible = false"
        >完成</el-button>
      </div>
    </template>
  </el-dialog>

  <!-- ============ 单字段修复弹窗 ============ -->
  <el-dialog
    v-model="fixDialog.visible"
    width="440px"
    append-to-body
    align-center
    :close-on-click-modal="false"
    class="fix-field-dialog"
  >
    <template #header>
      <div class="fix-header">
        <span class="fix-title">修正字段</span>
        <span class="fix-sub">{{ fieldLabel(fixDialog.field) }}</span>
      </div>
    </template>

    <div v-if="fixDialog.issueMsg" class="fix-issue">
      <span class="fix-issue-tag">问题</span>
      <span>{{ fixDialog.issueMsg }}</span>
    </div>

    <div class="fix-body">
      <!-- 资产大类下拉 -->
      <el-select
        v-if="fixDialog.field === 'asset_class'"
        v-model="fixDialog.value"
        placeholder="请选择资产大类"
        style="width: 100%"
        @keyup.enter="commitFix"
      >
        <el-option
          v-for="c in assetClasses"
          :key="c.code"
          :label="`${c.code} - ${c.name}`"
          :value="c.code"
        />
      </el-select>

      <!-- 状态下拉 -->
      <el-select
        v-else-if="fixDialog.field === 'status'"
        v-model="fixDialog.value"
        placeholder="请选择状态"
        style="width: 100%"
        @keyup.enter="commitFix"
      >
        <el-option
          v-for="s in STATUS_OPTIONS"
          :key="s"
          :label="s"
          :value="s"
        />
      </el-select>

      <!-- 日期选择 -->
      <el-date-picker
        v-else-if="DATE_FIELDS.has(fixDialog.field)"
        v-model="fixDialog.value"
        type="date"
        value-format="YYYY-MM-DD"
        placeholder="选择日期"
        style="width: 100%"
      />

      <!-- 数字输入 -->
      <el-input-number
        v-else-if="NUMBER_FIELDS.has(fixDialog.field)"
        v-model="fixDialog.value"
        :min="0"
        :precision="2"
        :step="100"
        :controls="false"
        style="width: 100%"
        @keyup.enter="commitFix"
      />

      <!-- 兜底：普通文本 -->
      <el-input
        v-else
        v-model="fixDialog.value"
        :placeholder="`请输入${fieldLabel(fixDialog.field)}`"
        autofocus
        @keyup.enter="commitFix"
      />
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="fixDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="commitFix">保存</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { toast } from '../utils/toast'
import {
  parseImportExcel,
  commitImport,
  aiFillImport,
  listAssetClasses,
} from '../api/assets'

// 系统字段中文标签（issue 弹窗里给用户看的）
const FIELD_LABELS = {
  asset_code: '资产编号',
  asset_class: '资产大类',
  category: '资产分类',
  brand: '品牌',
  model: '型号',
  serial_number: '序列号 / SN',
  specification: '规格配置',
  purchase_date: '购置日期',
  supplier: '供应商',
  price: '采购金额',
  warranty_until: '保修到期日期',
  location: '存放位置',
  owner: '使用人 / 责任人',
  department: '所属部门',
  status: '状态',
  remark: '备注',
}
const STATUS_OPTIONS = ['在用', '闲置', '维修', '报废']
const DATE_FIELDS = new Set(['purchase_date', 'warranty_until'])
const NUMBER_FIELDS = new Set(['price'])

const STEPS = [
  { key: 'upload', title: '上传文件' },
  { key: 'mapping', title: '列映射' },
  { key: 'preview', title: '数据预览' },
  { key: 'result', title: '导入结果' },
]

const STEP_ICONS = [
  {
    viewBox: '0 0 1024 1024',
    paths: [
      'M543.6 825.3H131.3c-28 0-50.7-22.8-50.8-50.7V141c0-29.9 24.3-54.3 54.3-54.3H261c25.1 0 46.6 17.9 51.2 42.6l20.9 111.9c11.7 62.6 66.4 108 130 108h385.6c29.9 0 54.2 24.3 54.2 54.3v72.4c0 22.2 18 40.3 40.3 40.3 22.2 0 40.3-18 40.3-40.3v-72.4c0-74.3-60.5-134.8-134.8-134.8H463.3c-24.9 0-46.3-17.8-50.9-42.3l-20.9-111.9C379.8 51.8 324.9 6.2 261 6.2H134.8C60.5 6.2 0 66.7 0 141v633.6C0 847 58.9 905.8 131.3 905.9h412.3c22.2 0 40.3-18 40.3-40.3 0-22.3-18-40.3-40.3-40.3z',
      'M570.4 140.4h322.1c22.2 0 40.3-18 40.3-40.3s-18-40.3-40.3-40.3H570.4c-22.2 0-40.3 18-40.3 40.3s18 40.3 40.3 40.3zM1014.6 717.6l-124-124C877.7 580.7 861 574 844 573.4c-0.9-0.1-1.7-0.1-2.6-0.1-0.9 0-1.7 0-2.6 0.1-16.9 0.6-33.7 7.4-46.7 20.3L668.3 717.6c-12.6 12.6-12.6 33 0 45.6 12.6 12.6 33 12.6 45.6 0l95.4-95.4v317.9c0 17.8 14.4 32.2 32.2 32.2s32.2-14.4 32.2-32.2v-318l95.4 95.4c6.3 6.3 14.5 9.4 22.8 9.4 8.2 0 16.5-3.1 22.8-9.4 12.4-12.6 12.4-33-0.1-45.5z',
    ],
  },
  {
    viewBox: '0 0 1024 1024',
    paths: [
      'M256 479.8h512.1V416l-64-128h-64l64 128H256zM768.1 544H256v63.8l64.1 128h64l-64-128h448z',
      'M384.1 831.6H192V192h192.1v63.1h64V128H128v767.6h320.1V767.8h-64zM576.1 128v128h64v-64h192.1v639.6H640.1v-63.8h-64v127.8h320.1V128z',
    ],
  },
  {
    viewBox: '0 0 1024 1024',
    paths: [
      'M868.430463 524.197618c4.999024-7.298574 4.999024-17.396602 0-24.695177C784.846788 378.426089 663.270533 302.041008 527.796993 302.041008s-257.049795 76.385081-340.733451 197.561413c-4.999024 7.298574-4.999024 17.396602 0 24.695177C270.747198 645.473931 392.323452 721.859012 527.796993 721.859012c135.47354-0.09998 257.049795-76.585042 340.63347-197.661394z m-83.083773 1.599687c-71.286077 82.983792-162.668229 129.474712-257.649678 129.474712S341.333411 608.781097 270.047335 525.797305c-6.698692-7.798477-6.698692-20.096075 0-27.894552 71.286077-82.983792 162.668229-129.474712 257.649677-129.474712s186.363601 46.49092 257.649678 129.474712c6.798672 7.798477 6.798672 20.096075 0 27.894552zM527.796993 402.521383c-60.388205 0-109.378637 49.090412-109.378637 109.378637 0 60.288225 49.090412 109.378637 109.378637 109.378637 60.388205 0 109.378637-49.090412 109.378637-109.378637 0-60.388205-48.990432-109.378637-109.378637-109.378637z m0 154.769771c-25.095099 0-45.391135-20.396016-45.391135-45.391134 0-25.095099 20.396016-45.391135 45.391135-45.391135s45.391135 20.396016 45.391134 45.391135-20.396016 45.391135-45.391134 45.391134zM32.09381 335.234525c17.696544 0 31.993751-14.297208 31.993751-31.993752V190.862722h0.599883l0.09998-97.780902c1.699668-16.196837 15.097051-29.094318 31.793791-29.094318h221.056824c17.696544 0 31.993751-14.297208 31.993752-31.993751s-14.297208-31.993751-31.993752-31.993751H64.787424C29.094396 0 0.100059 28.994337 0.100059 64.687366V303.240773c0 17.696544 14.297208 31.993751 31.993751 31.993752zM959.212732 0H706.462097c-17.696544 0-31.993751 14.297208-31.993751 31.993751s14.297208 31.993751 31.993751 31.993751h221.056825c16.696739 0 29.994142 12.897481 31.79379 29.094318l0.099981 97.780902h0.599883v112.378051c0 17.696544 14.297208 31.993751 31.993751 31.993752s31.993751-14.297208 31.993751-31.993752V64.687366C1023.900098 28.894357 994.905761 0 959.212732 0z m-641.674673 959.812537H96.481234c-16.696739 0-29.994142-12.897481-31.79379-29.094318l-0.099981-97.780902h-0.599882V720.559266c0-17.696544-14.297208-31.993751-31.993752-31.993751s-31.993751 14.297208-31.993751 31.993751v238.553407c0 35.693029 28.994337 64.687366 64.687366 64.687366h252.750635c17.696544 0 31.993751-14.297208 31.993751-31.993751 0.09998-17.696544-14.197227-31.993751-31.893771-31.993751z m674.368287-271.247022c-17.696544 0-31.993751 14.297208-31.993751 31.993751v112.378051h-0.599883l-0.09998 97.780902c-1.699668 16.196837-15.097051 29.094318-31.79379 29.094318h-220.956845c-17.696544 0-31.993751 14.297208-31.993751 31.993751s14.297208 31.993751 31.993751 31.993751H959.212732c35.693029 0 64.687366-28.994337 64.687366-64.687366V720.559266c0-17.696544-14.297208-31.993751-31.993752-31.993751z',
    ],
  },
  {
    viewBox: '0 0 1024 1024',
    paths: [
      'M135.63636347 500.34090869v309.19090957c0 43.52727305 35.30454521 78.83181826 78.83181827 78.83181827h595.06363652a78.83181826 78.83181826 0 0 0 78.83181826-78.83181827V214.46818174A78.83181826 78.83181826 0 0 0 809.53181826 135.63636347h-284.27727305a32.72727305 32.72727305 0 0 1 0-65.45454521h284.27727305A144.28636348 144.28636348 0 0 1 953.81818174 214.46818174v595.06363652a144.28636348 144.28636348 0 0 1-144.28636348 144.28636348H214.46818174A144.28636348 144.28636348 0 0 1 70.18181826 809.53181826v-309.19090957a32.72727305 32.72727305 0 1 1 65.45454522 0z',
      'M101.15 176.50454521l15.13636347 0.81818174a423.9 423.9 0 0 1 396.24545479 358.56818174 32.72727305 32.72727305 0 0 0 64.67727305-9.98181738A489.35454521 489.35454521 0 0 0 119.84545479 111.95l-15.17727305-0.81818174A32.72727305 32.72727305 0 0 0 101.15 176.54545479z',
      'M542.96818174 525.54090869l-139.90909043-76.45909043a32.72727305 32.72727305 0 0 0-31.37727305 57.43636348l149.89090869 81.94090957a53.18181826 53.18181826 0 0 0 70.15909131-17.79545479l93.68181827-144.81818173a32.72727305 32.72727305 0 0 0-54.98181827-35.59090958l-87.46363652 135.28636348z',
    ],
  },
]

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue', 'imported'])

const visible = ref(props.modelValue)
watch(
  () => props.modelValue,
  (v) => {
    visible.value = v
    if (v) resetAll()
  },
)
watch(visible, (v) => emit('update:modelValue', v))

const step = ref('upload')
const stepIndex = computed(() => {
  return { upload: 0, mapping: 1, preview: 2, result: 3 }[step.value] ?? 0
})

const parsing = ref(false)
const committing = ref(false)
const parseRes = reactive({
  llm_used: false,
  warning_count: 0,
  error_count: 0,
  header_auto_detected: true,
})
const headers = ref([])
const mapping = ref({})
const originalMapping = ref({})
const rows = ref([])
const fieldDict = ref([])
const commitRes = reactive({ success: 0, failed: 0, failures: [] })
const currentFile = ref(null)
const headerRow = ref(1)

// 烟花粒子（仅在 result 步骤且无失败时生成一次）
const confettiList = ref([])
const CONFETTI_COLORS = [
  '#ff6b6b',
  '#ffd166',
  '#06d6a0',
  '#118ab2',
  '#ef476f',
  '#f4a340',
  '#c084ff',
  '#ffe066',
  '#34c77b',
]
function generateConfetti() {
  const total = 36
  const list = []
  for (let i = 0; i < total; i++) {
    const angle = (i / total) * 360 + (Math.random() * 24 - 12)
    const distance = 160 + Math.random() * 140
    const rad = (angle * Math.PI) / 180
    const tx = Math.cos(rad) * distance
    const ty = Math.sin(rad) * distance + distance * 0.35
    const rot = Math.random() * 720 - 360
    const delay = Math.random() * 0.22
    const duration = 1.4 + Math.random() * 0.8
    const isCircle = Math.random() > 0.55
    const w = isCircle ? 7 : 6 + Math.random() * 4
    const h = isCircle ? 7 : 10 + Math.random() * 6
    list.push({
      '--tx': `${tx}px`,
      '--ty': `${ty}px`,
      '--rot': `${rot}deg`,
      'animation-delay': `${delay}s`,
      'animation-duration': `${duration}s`,
      background: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
      'border-radius': isCircle ? '50%' : '2px',
      width: `${w}px`,
      height: `${h}px`,
    })
  }
  return list
}
watch(step, (v) => {
  if (v === 'result' && commitRes.failed === 0 && commitRes.success > 0) {
    confettiList.value = generateConfetti()
  } else {
    confettiList.value = []
  }
})
const topRowsPreview = ref([])
const headerPickerVisible = ref(false)

const previewTableRef = ref()
const selectedRows = ref([])

// AI 一键补全状态
const aiFilling = ref(false)
const assetClasses = ref([])

// 单字段修复弹窗
const fixDialog = reactive({
  visible: false,
  rowIdx: -1,
  field: '',
  value: null,
  issueMsg: '',
})

const mappingTable = computed(() => {
  if (!headers.value.length) return []
  const firstRow = rows.value[0]
  return headers.value.map((h) => ({
    original: h,
    sample: firstRow ? formatCell(pickRaw(firstRow, h)) : '',
  }))
})

const previewColumns = computed(() => {
  const used = new Set(Object.values(mapping.value).filter(Boolean))
  // asset_code 一律由平台自动生成，预览时不显示也不允许编辑
  return fieldDict.value.filter(
    (f) => used.has(f.key) && f.key !== 'asset_code',
  )
})

const errorRows = computed(() =>
  rows.value.filter((r) => r.issues?.some((i) => i.level === 'error')),
)
const warningRows = computed(() =>
  rows.value.filter(
    (r) =>
      !r.issues?.some((i) => i.level === 'error') &&
      r.issues?.some((i) => i.level === 'warning'),
  ),
)

const selectableCount = computed(() =>
  rows.value.filter(isRowSelectable).length,
)

function pickRaw(row, originalCol) {
  // 预览时我们只保留映射后的 data，原列样本只在 mapping 阶段有用，
  // 这里仅用于映射阶段显示样本，找到对应已映射的字段值即可。
  const target = mapping.value[originalCol]
  if (target) return row.data[target]
  return undefined
}

function resetAll() {
  step.value = 'upload'
  parsing.value = false
  committing.value = false
  aiFilling.value = false
  headers.value = []
  mapping.value = {}
  originalMapping.value = {}
  rows.value = []
  fieldDict.value = []
  selectedRows.value = []
  currentFile.value = null
  headerRow.value = 1
  topRowsPreview.value = []
  headerPickerVisible.value = false
  Object.assign(parseRes, {
    llm_used: false,
    warning_count: 0,
    error_count: 0,
    header_auto_detected: true,
  })
  Object.assign(commitRes, { success: 0, failed: 0, failures: [] })
  editing.idx = -1
  editing.field = ''
  editing.value = ''
  Object.assign(fixDialog, {
    visible: false,
    rowIdx: -1,
    field: '',
    value: null,
    issueMsg: '',
  })
}

async function onPickFile(uploadFile) {
  const raw = uploadFile.raw
  if (!raw) return
  parsing.value = true
  currentFile.value = raw
  try {
    const res = await parseImportExcel(raw)
    applyParseResult(res)
    if (!rows.value.length) {
      toast.warning('没有解析到任何数据行')
      return
    }
    toast.success(
      res.llm_used
        ? `已用百炼模型识别 ${headers.value.length} 列`
        : `已用规则映射识别 ${headers.value.length} 列`,
    )
    // 顺手把资产大类字典拉下来，留给修复弹窗用
    if (!assetClasses.value.length) {
      try {
        assetClasses.value = await listAssetClasses()
      } catch (e) {
        // 拉不到也不致命，下拉退化为空
      }
    }
    step.value = 'mapping'
  } catch (e) {
    // request.js 内已有错误提示
  } finally {
    parsing.value = false
  }
}

function applyParseResult(res) {
  headers.value = res.headers || []
  mapping.value = { ...(res.mapping || {}) }
  originalMapping.value = { ...(res.mapping || {}) }
  rows.value = (res.rows || []).map((r) => ({
    ...r,
    data: { ...(r.data || {}) },
  }))
  fieldDict.value = res.field_dict || []
  parseRes.llm_used = !!res.llm_used
  parseRes.warning_count = res.warning_count || 0
  parseRes.error_count = res.error_count || 0
  parseRes.header_auto_detected = res.header_auto_detected !== false
  headerRow.value = res.header_row || 1
  topRowsPreview.value = Array.isArray(res.top_rows_preview)
    ? res.top_rows_preview
    : []
}

async function onPickHeaderRow(rowIdx) {
  if (!currentFile.value) return
  if (rowIdx === headerRow.value) {
    headerPickerVisible.value = false
    return
  }
  parsing.value = true
  try {
    // 切换表头后映射重新走 LLM/规则识别，不带 mapping
    const res = await parseImportExcel(currentFile.value, null, rowIdx)
    applyParseResult(res)
    toast.success(`已将第 ${rowIdx} 行设为表头并重新识别`)
    headerPickerVisible.value = false
  } finally {
    parsing.value = false
  }
}

function mappingChanged() {
  const a = mapping.value
  const b = originalMapping.value
  const keys = new Set([...Object.keys(a), ...Object.keys(b)])
  for (const k of keys) {
    if ((a[k] || null) !== (b[k] || null)) return true
  }
  return false
}

function goBack() {
  if (step.value === 'mapping') step.value = 'upload'
  else if (step.value === 'preview') step.value = 'mapping'
}

async function goPreview() {
  // 如果用户改过映射，重新调一次后端按新映射规范化数据
  if (mappingChanged() && currentFile.value) {
    parsing.value = true
    try {
      const res = await parseImportExcel(
        currentFile.value,
        mapping.value,
        headerRow.value,
      )
      applyParseResult(res)
      toast.success('已按新映射重新规范化数据')
    } catch (e) {
      // request.js 内已有错误提示
      parsing.value = false
      return
    } finally {
      parsing.value = false
    }
  }
  step.value = 'preview'
  nextTick(() => {
    if (previewTableRef.value) {
      rows.value.forEach((row) => {
        if (isRowSelectable(row)) {
          previewTableRef.value.toggleRowSelection(row, true)
        }
      })
    }
  })
}

function isRowSelectable(row) {
  return !row.issues.some((i) => i.level === 'error')
}

function rowClass({ row }) {
  if (row.issues.some((i) => i.level === 'error')) return 'row-error'
  if (row.issues.some((i) => i.level === 'warning')) return 'row-warning'
  return 'row-ok'
}

function onSelectionChange(rows) {
  selectedRows.value = rows
}

function isEmpty(v) {
  return v === null || v === undefined || v === ''
}

function formatCell(v) {
  if (v === null || v === undefined) return ''
  if (typeof v === 'number') {
    // 价格可能是浮点数，保留 2 位；其他原样
    if (!Number.isInteger(v)) return v.toFixed(2)
    return String(v)
  }
  if (typeof v === 'string' && v.includes('T')) {
    // ISO datetime → 截到日期
    const m = v.match(/^(\d{4}-\d{2}-\d{2})/)
    if (m) return m[1]
  }
  return String(v)
}

function columnWidth(key) {
  const widths = {
    asset_code: 200,
    asset_class: 80,
    category: 120,
    brand: 100,
    model: 160,
    serial_number: 140,
    specification: 200,
    purchase_date: 130,
    supplier: 140,
    price: 110,
    warranty_until: 130,
    location: 120,
    owner: 100,
    department: 120,
    status: 90,
    remark: 200,
  }
  return widths[key] || 140
}

// ============ 单元格双击编辑 ============
const editing = reactive({ idx: -1, field: '', value: '' })

function startEdit(idx, field, val) {
  editing.idx = idx
  editing.field = field
  editing.value = val == null ? '' : String(val)
}

function commitEdit() {
  if (editing.idx < 0) return
  const row = rows.value[editing.idx]
  if (!row) return
  let val = editing.value
  // 简单类型转换
  if (editing.field === 'price') {
    const n = parseFloat(val)
    val = Number.isFinite(n) ? n : null
  } else if (val === '') {
    val = null
  }
  row.data[editing.field] = val
  // 清掉对应字段的 error/warning（用户已经手工改过了）
  row.issues = row.issues.filter((i) => i.field !== editing.field)
  cancelEdit()
}

function cancelEdit() {
  editing.idx = -1
  editing.field = ''
  editing.value = ''
}

// ============ 单字段修复弹窗 ============
function fieldLabel(key) {
  return FIELD_LABELS[key] || key
}

function openFixDialog(rowIdx, issue) {
  const row = rows.value[rowIdx]
  if (!row || !issue?.field) return
  fixDialog.rowIdx = rowIdx
  fixDialog.field = issue.field
  fixDialog.issueMsg = issue.message || ''
  const cur = row.data[issue.field]
  if (cur === null || cur === undefined) {
    fixDialog.value = ''
  } else if (NUMBER_FIELDS.has(issue.field)) {
    fixDialog.value = Number(cur)
  } else if (DATE_FIELDS.has(issue.field) && typeof cur === 'string') {
    const m = cur.match(/^(\d{4}-\d{2}-\d{2})/)
    fixDialog.value = m ? m[1] : cur
  } else {
    fixDialog.value = String(cur)
  }
  fixDialog.visible = true
}

function commitFix() {
  const row = rows.value[fixDialog.rowIdx]
  if (!row) {
    fixDialog.visible = false
    return
  }
  const field = fixDialog.field
  let val = fixDialog.value

  if (val === '' || val == null) {
    val = null
  } else if (NUMBER_FIELDS.has(field)) {
    const n = parseFloat(val)
    val = Number.isFinite(n) ? n : null
  } else if (DATE_FIELDS.has(field)) {
    // el-date-picker 给的是 'YYYY-MM-DD'，统一拼成 ISO
    if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val)) {
      val = `${val}T00:00:00`
    }
  } else if (typeof val === 'string') {
    val = val.trim() || null
  }

  row.data[field] = val
  // 把对应字段的所有 issue 都清掉
  row.issues = row.issues.filter((i) => i.field !== field)
  fixDialog.visible = false

  if (val !== null) {
    toast.success(`已修正「${fieldLabel(field)}」`)
  }
}

// ============ AI 一键补全 ============
async function onAiFill() {
  // 优先补错误行；没有错误时再尝试警告行；都没有就跳过
  let targets = errorRows.value
  if (!targets.length) targets = warningRows.value
  if (!targets.length) {
    toast.info('当前没有需要补全的行')
    return
  }
  aiFilling.value = true
  try {
    const payload = targets.map((r) => ({
      row_index: r.row_index,
      data: { ...r.data },
    }))
    const res = await aiFillImport(payload, true)
    const updated = res?.rows || []
    if (!updated.length) {
      toast.warning('AI 没有返回任何补全结果')
      return
    }
    // 用 row_index 回填到 rows
    const byIdx = new Map(updated.map((u) => [u.row_index, u]))
    rows.value = rows.value.map((r) => {
      const u = byIdx.get(r.row_index)
      if (!u) return r
      return { ...r, data: { ...(u.data || {}) }, issues: u.issues || [] }
    })
    parseRes.error_count = res.error_count ?? parseRes.error_count
    parseRes.warning_count = res.warning_count ?? parseRes.warning_count

    // 重新勾选可入库行
    await nextTick()
    if (previewTableRef.value) {
      previewTableRef.value.clearSelection()
      rows.value.forEach((row) => {
        if (isRowSelectable(row)) {
          previewTableRef.value.toggleRowSelection(row, true)
        }
      })
    }
    toast.success(
      `AI 补全完成：参考 ${res.used_samples || 0} 条前置资产，` +
        `处理 ${updated.length} 行`,
    )
  } catch (e) {
    // request.js 已有错误提示
  } finally {
    aiFilling.value = false
  }
}

// ============ 提交 ============
async function onCommit() {
  if (!selectedRows.value.length) {
    toast.warning('请至少勾选一行')
    return
  }
  committing.value = true
  try {
    const payloadRows = selectedRows.value.map((r) => {
      const d = { ...r.data }
      // asset_code 一律由后端按平台规则生成，前端不带过去（即使 Excel 里有也忽略）
      delete d.asset_code
      Object.keys(d).forEach((k) => {
        if (d[k] === '') d[k] = null
      })
      return d
    })
    const res = await commitImport(payloadRows)
    commitRes.success = res.success
    commitRes.failed = res.failed
    commitRes.failures = res.failures || []
    step.value = 'result'
    if (res.success > 0) emit('imported')
    if (res.failed === 0) {
      toast.success(`已成功导入 ${res.success} 条`)
    } else if (res.success === 0) {
      toast.error(`全部 ${res.failed} 条均导入失败`)
    } else {
      toast.warning(`成功 ${res.success} 条，失败 ${res.failed} 条`)
    }
  } finally {
    committing.value = false
  }
}

function onClosed() {
  resetAll()
}
</script>

<style scoped>
.import-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.import-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--theme-text-strong, #5a4730);
  letter-spacing: 1px;
}
.import-sub {
  font-size: 12px;
  color: var(--theme-text-muted, #b9a78a);
}

/* 弹窗主体样式见底部全局 style 块（避开 scoped + append-to-body 的匹配问题） */

.import-steps-bar {
  display: flex;
  align-items: stretch;
  gap: 4px;
  margin: 48px auto 22px;
  padding: 0;
  width: 70%;
  list-style: none;
}

.import-step {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 14px 20px 14px 30px;
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.2px;
  line-height: 1;
  white-space: nowrap;
  background: var(--theme-surface-muted, #f4ecdd);
  color: var(--theme-text-muted, #b6a482);
  clip-path: polygon(
    0 0,
    calc(100% - 16px) 0,
    100% 50%,
    calc(100% - 16px) 100%,
    0 100%,
    16px 50%
  );
  transition: background 0.32s ease, color 0.32s ease, box-shadow 0.32s ease,
    transform 0.32s ease;
}

.import-step:first-child {
  padding-left: 20px;
  clip-path: polygon(
    0 0,
    calc(100% - 16px) 0,
    100% 50%,
    calc(100% - 16px) 100%,
    0 100%
  );
}

.import-step:last-child {
  padding-right: 20px;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 16px 50%);
}

.import-step.is-current {
  background: linear-gradient(135deg, var(--theme-primary, #c5a47e) 0%, var(--theme-primary-deep, #8a7355) 100%);
  color: #fff;
  box-shadow: 0 6px 16px -10px rgba(var(--theme-primary-deep-rgb), 0.55);
  animation: step-current-glow 2.4s ease-in-out infinite;
}

.import-step.is-done {
  background: linear-gradient(135deg, var(--theme-primary-light-5, #e6cfa9) 0%, var(--theme-primary, #c5a47e) 100%);
  color: #fff;
}

.import-step.is-todo {
  background: var(--theme-surface-muted, #f4ecdd);
  color: var(--theme-text-muted, #b6a482);
}

/* ===== 进度条动效 ===== */
.import-step > * {
  position: relative;
  z-index: 2;
}

/* 当前步骤：阴影呼吸 */
@keyframes step-current-glow {
  0%,
  100% {
    box-shadow: 0 4px 14px -10px rgba(var(--theme-primary-deep-rgb), 0.5);
  }
  50% {
    box-shadow:
      0 8px 22px -6px rgba(var(--theme-primary-deep-rgb), 0.85),
      0 0 0 3px rgba(var(--theme-primary-rgb), 0.18);
  }
}

/* 当前步骤：图标脉冲 */
.import-step.is-current .import-step-num {
  animation: step-icon-pulse 1.8s ease-in-out infinite;
}
@keyframes step-icon-pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* 当前步骤：入场弹动（切换时播放一次） */
.import-step.is-current .import-step-label {
  animation: step-label-in 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
@keyframes step-label-in {
  from {
    transform: translateY(4px);
    opacity: 0.4;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 已完成步骤：流光扫过（5s 一轮） */
.import-step.is-done::before {
  content: '';
  position: absolute;
  top: 0;
  left: -45%;
  width: 38%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.42) 50%,
    transparent 100%
  );
  transform: skewX(-22deg);
  pointer-events: none;
  z-index: 1;
  animation: step-sheen 5s ease-in-out infinite;
}
@keyframes step-sheen {
  0%,
  55% {
    left: -45%;
  }
  82%,
  100% {
    left: 115%;
  }
}

.import-step-num {
  flex: 0 0 24px;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: inherit;
  transition: color 0.32s ease;
}

.import-step.is-todo .import-step-num {
  color: var(--theme-text-muted, #b6a482);
}

.import-step-num svg {
  display: block;
  width: 20px;
  height: 20px;
}
.import-step-num svg path {
  fill: currentColor;
}

.import-step-label {
  position: relative;
  top: 0;
}

.step-body {
  padding: 4px 0 8px;
  min-height: 320px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* ===== Step 1 ===== */
.upload-dropzone {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.upload-dropzone :deep(.el-upload) {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.upload-dropzone :deep(.el-upload-dragger) {
  width: 100%;
  flex: 1;
  min-height: 0;
  border: 1.5px dashed var(--theme-primary-light-3, #d4b89a);
  border-radius: 12px;
  background: var(--theme-surface-subtle, #fffdf8);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}
.upload-dropzone :deep(.el-upload-dragger:hover) {
  border-color: var(--theme-primary-deep, #8a7355);
  background: var(--theme-surface-hover, #fff9ec);
}
.dropzone-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 24px;
}

/* ===== 上传图标：静态展示，无触摸动画 ===== */
.dropzone-icon {
  color: var(--theme-primary, #c5a47e);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 168px;
  height: 168px;
  border-radius: 50%;
  background: radial-gradient(
    circle at 50% 50%,
    rgba(var(--theme-primary-rgb), 0.22) 0%,
    rgba(var(--theme-primary-rgb), 0.02) 70%
  );
}
.dropzone-icon svg {
  display: block;
}
.dropzone-inner {
  gap: 14px;
  padding: 32px;
}

.dropzone-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--theme-text-strong, #5a4730);
}
.dropzone-sub {
  font-size: 12.5px;
  color: var(--theme-text-muted, #a89c84);
}
.parsing-tip {
  margin-top: 14px;
  color: var(--theme-primary-deep, #8a7355);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
.tip-box {
  margin-top: 18px;
  padding: 14px 18px;
  background: var(--theme-surface, #faf4e9);
  border: 1px solid var(--theme-border, #ecdfc9);
  border-radius: 10px;
  color: var(--theme-text-hover, #6e5a40);
  font-size: 13px;
}
.tip-title {
  font-weight: 700;
  margin-bottom: 6px;
  color: var(--theme-text-strong, #5a4730);
}
.tip-box ul {
  margin: 0;
  padding-left: 18px;
  line-height: 1.8;
}
.tip-box em {
  font-style: normal;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
}

/* ===== Step 2: 表头行识别 ===== */
.header-row-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: var(--theme-surface, #faf4e9);
  border: 1px solid var(--theme-border, #ecdfc9);
  border-radius: 8px;
}
.hr-left {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 13.5px;
  color: var(--theme-text-hover, #6e5a40);
}
.hr-label {
  color: var(--theme-primary-deep, #8a7355);
}
.hr-row b {
  color: var(--theme-text-strong, #5a4730);
  margin: 0 2px;
}
.hr-sep {
  display: inline-block;
  width: 1px;
  height: 14px;
  background: #e0cfae;
  margin: 0 2px;
}
.hr-cols b {
  color: var(--theme-text-strong, #5a4730);
  margin: 0 2px;
}
.hr-right {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.hr-tip {
  font-size: 12.5px;
  color: var(--theme-text-muted, #b9a78a);
  white-space: nowrap;
}
.hr-switch-btn {
  color: var(--theme-primary-deep, #8a7355) !important;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-thickness: 1px;
  text-decoration-color: var(--theme-primary, #c5a47e);
}
.hr-switch-btn:hover {
  color: var(--theme-text-strong, #5a4730) !important;
  text-decoration-color: var(--theme-primary-deep, #8a7355);
}
.hr-switch-btn :deep(span) {
  text-decoration: inherit;
}
.header-picker {
  margin-bottom: 12px;
  padding: 12px 14px;
  background: var(--theme-surface-subtle, #fffdf8);
  border: 1px dashed var(--theme-primary-light-3, #d4b89a);
  border-radius: 8px;
}
.hp-tip {
  margin-bottom: 8px;
  color: var(--theme-text-hover, #6e5a40);
  font-size: 13px;
}
.hp-tip b {
  color: var(--theme-text-strong, #5a4730);
}
.hp-table-wrap {
  max-height: 240px;
  overflow: auto;
}
.hp-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}
.hp-table tr {
  cursor: pointer;
  transition: background 0.12s ease;
}
.hp-table tr:hover {
  background: var(--theme-surface-strong, #fff4dc);
}
.hp-table tr.is-current {
  background: var(--theme-surface-strong, #fff4dc);
}
.hp-table tr.is-current .hp-rownum {
  color: var(--theme-text-strong, #5a4730);
  font-weight: 700;
}
.hp-table td {
  padding: 6px 8px;
  border-bottom: 1px solid var(--theme-table-line, #f3ece0);
  color: #1a1a1a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
}
.hp-rownum {
  width: 90px;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  white-space: nowrap;
}
.hp-cur {
  margin-left: 6px;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 8px;
  background: var(--theme-primary, #c5a47e);
  color: #fff;
}
.hp-cell {
  color: #4a4a4a;
}
.hp-more {
  color: var(--theme-text-muted, #b9a78a);
  font-style: italic;
  white-space: nowrap;
}

/* ===== Step 2: 列映射表 ===== */
.preview-summary {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 12px;
  color: var(--theme-text-hover, #6e5a40);
  font-size: 13.5px;
}
.muted {
  color: var(--theme-text-muted, #b9a78a);
  font-size: 12.5px;
}
/* ===== AI 徽章：AI 智能映射 / 规则兜底映射 ===== */
.ai-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 24px;
  padding: 0 11px 0 9px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.3px;
  line-height: 1;
  user-select: none;
  overflow: hidden;
  isolation: isolate;
  white-space: nowrap;
}
.ai-badge-icon {
  width: 13px;
  height: 13px;
  flex-shrink: 0;
}
.ai-badge.is-ai {
  color: var(--theme-text-strong, #5a4730);
  background: linear-gradient(135deg, #f4e6c8 0%, #e6cf9d 100%);
  border: 1px solid #d4b88c;
  box-shadow: 0 1px 2px rgba(138, 109, 60, 0.12);
}
.ai-badge.is-ai .ai-badge-icon {
  color: #b08a4f;
}
.ai-badge.is-rule {
  color: #b66a14;
  background: linear-gradient(135deg, #fff3df 0%, #ffe6c2 100%);
  border: 1px solid #f1cf95;
}
.mapping-table {
  background: transparent;
}
.mapping-table :deep(.el-table__inner-wrapper::before),
.mapping-table :deep(.el-table__border-left-patch) {
  display: none !important;
}
.mapping-table :deep(.el-table),
.mapping-table :deep(.el-table__inner-wrapper),
.mapping-table :deep(.el-table tr),
.mapping-table :deep(.el-table th.el-table__cell),
.mapping-table :deep(.el-table td.el-table__cell) {
  background-color: transparent !important;
}
.mapping-table :deep(thead th) {
  background-color: transparent !important;
  color: var(--theme-primary-deep, #8a7355) !important;
  font-weight: 700;
  font-size: 14.5px;
  letter-spacing: 0.3px;
  padding-top: 4px !important;
  padding-bottom: 4px !important;
  border-bottom: 1px solid var(--theme-border, #ecdfc9) !important;
}
.mapping-table :deep(thead th .cell) {
  font-size: 14.5px;
  line-height: 1.4;
}
.mapping-table :deep(td.el-table__cell) {
  border-bottom: 1px solid #f3ead8 !important;
}
.mapping-table :deep(.el-table__row:hover > td.el-table__cell) {
  background-color: #fbf6ec !important;
}
.mono {
  font-family: 'Consolas', 'Menlo', 'Courier New', monospace;
  color: #1a1a1a;
}
.sample-text {
  color: var(--theme-text-hover, #6e5a40);
}

/* ===== Step 3 ===== */
.preview-body {
  display: flex;
  flex-direction: column;
}
.preview-summary .ok b { color: #34c77b; }
.preview-summary .warn b { color: #f4a340; }
.preview-summary .err b { color: #ef665b; }
.preview-summary .selected b { color: var(--theme-primary-deep, #8a7355); }
.preview-table {
  border-radius: 0;
}
.preview-table :deep(thead th) {
  background-color: var(--theme-surface, #faf4e9) !important;
  color: var(--theme-primary-deep, #8a7355) !important;
}
/* 去掉左右外边框（保留顶部/底部/水平/内部竖向分隔线） */
.preview-table :deep(.el-table),
.preview-table :deep(.el-table__inner-wrapper),
.preview-table :deep(.el-table--border) {
  border-left: none !important;
  border-right: none !important;
  box-shadow: none !important;
}
.preview-table :deep(.el-table--border::after),
.preview-table :deep(.el-table--border::before),
.preview-table :deep(.el-table__border-left-patch) {
  display: none !important;
}
.preview-table :deep(.el-table tr > th.el-table__cell:first-child),
.preview-table :deep(.el-table tr > td.el-table__cell:first-child) {
  border-left: none !important;
}
.preview-table :deep(.el-table tr > th.el-table__cell:last-child),
.preview-table :deep(.el-table tr > td.el-table__cell:last-child) {
  border-right: none !important;
}
.preview-table :deep(.row-error) {
  background: #fdebec !important;
}
.preview-table :deep(.row-warning) {
  background: var(--theme-surface-hover, #fff7e6) !important;
}
.preview-table :deep(.row-ok) {
  background: #ffffff;
}
.row-index {
  color: var(--theme-text-muted, #b9a78a);
  font-size: 12px;
}
.cell-display {
  display: inline-block;
  width: 100%;
  cursor: text;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.cell-display.is-empty {
  color: var(--theme-placeholder, #c9bba0);
}
.issue-ok {
  color: #34c77b;
  font-size: 12px;
}
.issue-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.issue-tag {
  cursor: help;
}
.issue-tag.clickable {
  cursor: pointer;
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}
.issue-tag.clickable:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

/* 预览顶部提示条 */
.preview-notice {
  margin-bottom: 10px;
  padding: 9px 14px;
  border-radius: 8px;
  background: var(--theme-surface-strong, #fff4dc);
  border: 1px solid #f0d99a;
  color: var(--theme-text-hover, #6e5a40);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.preview-notice b {
  color: var(--theme-text-strong, #5a4730);
  margin: 0 2px;
}

/* AI 一键补全按钮 */
.ai-fill-btn {
  margin-left: auto;
}
.ai-fill-btn :deep(.el-icon) {
  color: var(--theme-primary, #c5a47e);
}
.ai-fill-icon-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  margin-right: 4px;
}
.ai-fill-icon {
  width: 16px;
  height: 16px;
  color: var(--theme-primary, #c5a47e);
  transition: color 0.22s ease;
}
.ai-fill-btn:hover:not(.is-disabled) .ai-fill-icon,
.ai-fill-btn:focus-visible:not(.is-disabled) .ai-fill-icon {
  color: #ffffff;
}

/* AI 补全进行中：锁定手动编辑视觉 */
.cell-display.is-locked {
  cursor: not-allowed;
  opacity: 0.55;
  user-select: none;
}
.issue-tag.is-locked {
  cursor: not-allowed;
  opacity: 0.55;
  filter: grayscale(0.2);
}

/* ===== Step 4: 导入结果 ===== */
.result-body {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 8px 0 4px;
}

/* 中心庆祝区 */
.result-celebrate {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 90px 24px 32px;
  min-height: 360px;
  overflow: visible;
}
.result-celebrate.is-success {
  color: #1f9d57;
}
.result-celebrate.is-warning {
  color: #d18b22;
}

/* 大图标 + 光圈 */
.result-big-icon {
  position: relative;
  width: 132px;
  height: 132px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  animation: result-icon-pop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.big-icon-svg {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 8px 18px rgba(31, 157, 87, 0.25));
}
.result-celebrate.is-warning .big-icon-svg {
  filter: drop-shadow(0 8px 18px rgba(209, 139, 34, 0.28));
}
.big-check {
  stroke-dasharray: 80;
  stroke-dashoffset: 80;
  animation: check-draw 0.55s 0.35s ease-out forwards;
}
.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px solid currentColor;
  opacity: 0;
  pointer-events: none;
  z-index: 1;
}
.ring-1 {
  animation: ring-pulse 1.8s ease-out 0.15s 1 both;
}
.ring-2 {
  animation: ring-pulse 1.8s ease-out 0.45s 1 both;
}
.ring-3 {
  animation: ring-pulse 1.8s ease-out 0.75s 1 both;
}

@keyframes result-icon-pop {
  0% {
    transform: scale(0.4);
    opacity: 0;
  }
  60% {
    transform: scale(1.08);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
@keyframes check-draw {
  to {
    stroke-dashoffset: 0;
  }
}
@keyframes ring-pulse {
  0% {
    transform: scale(0.85);
    opacity: 0.55;
  }
  100% {
    transform: scale(1.85);
    opacity: 0;
  }
}

/* 大标题 + 副标题 */
.result-big-title {
  margin-top: 26px;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: 1.5px;
  color: var(--theme-text-strong, #5a4730);
  animation: result-text-up 0.45s 0.2s ease-out both;
}
.result-celebrate.is-success .result-big-title {
  color: #1d8a4f;
}
.result-celebrate.is-warning .result-big-title {
  color: #c47a14;
}
.result-big-sub {
  margin-top: 10px;
  font-size: 14px;
  color: var(--theme-primary-deep, #8a7355);
  letter-spacing: 0.3px;
  animation: result-text-up 0.45s 0.3s ease-out both;
}
.result-big-sub b {
  font-weight: 800;
  margin: 0 3px;
  font-size: 15px;
}
.result-big-sub .ok {
  color: #1d8a4f;
}
.result-big-sub .err {
  color: #d65349;
}
.result-big-sub .zero {
  color: var(--theme-text-muted, #b9a78a);
}

@keyframes result-text-up {
  from {
    transform: translateY(8px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 烟花层 */
.confetti-layer {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  pointer-events: none;
  z-index: 3;
}
.confetti {
  position: absolute;
  top: 0;
  left: 0;
  transform: translate(-50%, -50%);
  opacity: 0;
  animation-name: confetti-burst;
  animation-timing-function: cubic-bezier(0.22, 0.68, 0.32, 1);
  animation-fill-mode: forwards;
}
@keyframes confetti-burst {
  0% {
    transform: translate(-50%, -50%) rotate(0deg) scale(0.6);
    opacity: 0;
  }
  12% {
    opacity: 1;
  }
  100% {
    transform:
      translate(
        calc(-50% + var(--tx)),
        calc(-50% + var(--ty))
      )
      rotate(var(--rot))
      scale(1);
    opacity: 0;
  }
}

/* 失败明细 */
.failures-block {
  margin-top: 4px;
}
.failures-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  color: var(--theme-text-strong, #5a4730);
  margin-bottom: 10px;
  font-size: 14px;
}
.fail-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef665b;
}
.failures-table :deep(thead th) {
  background-color: var(--theme-surface, #faf4e9) !important;
  color: var(--theme-primary-deep, #8a7355) !important;
}
.failures-table :deep(.el-table),
.failures-table :deep(.el-table__inner-wrapper) {
  border-left: none !important;
  border-right: none !important;
  box-shadow: none !important;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ===== 单字段修复弹窗 ===== */
.fix-field-dialog :deep(.el-dialog) {
  border-radius: 12px;
}
.fix-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.fix-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--theme-text-strong, #5a4730);
}
.fix-sub {
  font-size: 13px;
  color: var(--theme-primary, #c5a47e);
}
.fix-issue {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 14px;
  padding: 8px 10px;
  background: var(--theme-surface-hover, #fff7e6);
  border: 1px solid #f0d99a;
  border-radius: 6px;
  color: var(--theme-text-hover, #6e5a40);
  font-size: 12.5px;
  line-height: 1.5;
}
.fix-issue-tag {
  flex: 0 0 auto;
  background: var(--theme-primary, #c5a47e);
  color: #fff;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 600;
}
.fix-body {
  padding: 4px 0;
}
</style>

<!-- 弹窗本体样式必须用非 scoped 全局 style：
     class="asset-import-dialog" 直接挂在 .el-dialog 自己身上，
     且组件 append-to-body 后会脱离当前组件的 data-v 作用域 -->
<style>
.el-dialog.asset-import-dialog {
  border-radius: 14px !important;
  overflow: hidden !important;
  /* 锁定 16:9 横向比例：宽度受 78vw 与 (max-height * 16/9) 双重约束 */
  width: min(78vw, calc(80vh * 16 / 9)) !important;
  min-width: 1080px !important;
  max-width: 1500px !important;
  height: min(calc(78vw * 9 / 16), 80vh) !important;
  min-height: 520px !important;
  max-height: 88vh !important;
  display: flex !important;
  flex-direction: column !important;
  padding: 0 !important;
}
.el-dialog.asset-import-dialog > .el-dialog__header {
  padding: 0 !important;
  margin: 0 !important;
}
.el-dialog.asset-import-dialog > .el-dialog__body {
  flex: 1 1 auto !important;
  min-height: 0 !important;
  padding: 12px 28px 16px !important;
  display: flex !important;
  flex-direction: column !important;
  overflow-y: auto;
}
.el-dialog.asset-import-dialog > .el-dialog__footer {
  flex: 0 0 auto;
  padding: 8px 24px 16px !important;
}
</style>
