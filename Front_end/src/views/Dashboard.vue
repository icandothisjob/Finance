<template>
  <div class="dashboard">
    <AssetsTable />
  </div>
</template>

<script setup>
import AssetsTable from '../components/AssetsTable.vue'
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'HarmonyOS Sans SC', 'Noto Sans SC', 'PingFang SC',
    'Microsoft YaHei UI', 'Microsoft YaHei', -apple-system,
    BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
  letter-spacing: 0.3px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.dashboard :deep(.el-table),
.dashboard :deep(.el-input__inner),
.dashboard :deep(.el-input__wrapper),
.dashboard :deep(.el-select__wrapper),
.dashboard :deep(.el-button),
.dashboard :deep(.el-form-item__label) {
  font-family: inherit;
}
</style>
