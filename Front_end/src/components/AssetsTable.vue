<template>
  <div class="assets-table">
    <div class="filter-bar">
      <form class="filter-row" @submit.prevent="onSearch" autocomplete="off">
        <!-- 左侧：新增 / Excel 导入 -->
        <div class="actions-left">
          <el-tooltip content="新增资产" placement="top">
            <button
              type="button"
              class="svg-icon-btn add-btn"
              @click="openCreate"
              aria-label="新增资产"
            >
              <svg viewBox="0 0 1024 1024" width="22" height="22" aria-hidden="true">
                <path d="M469.332942 469.332942V298.751751a42.623964 42.623964 0 1 1 85.333262 0V469.332942h170.581192a42.623964 42.623964 0 1 1 0 85.333262H554.666204v170.581192a42.623964 42.623964 0 1 1-85.333262 0V554.666204H298.751751a42.623964 42.623964 0 1 1 0-85.333262H469.332942z m477.866269 312.533073a42.666631 42.666631 0 0 1-72.533273-45.055962A424.959646 424.959646 0 0 0 938.665884 511.999573c0-235.647804-191.018507-426.666311-426.666311-426.666311S85.333262 276.35177 85.333262 511.999573s191.018507 426.666311 426.666311 426.666311a424.447646 424.447646 0 0 0 225.578479-64.426613 42.666631 42.666631 0 0 1 45.183962 72.405273A509.780909 509.780909 0 0 1 511.999573 1023.999147C229.247809 1023.999147 0 794.751338 0 511.999573S229.247809 0 511.999573 0s511.999573 229.247809 511.999574 511.999573a510.719574 510.719574 0 0 1-76.799936 269.866442z"/>
              </svg>
            </button>
          </el-tooltip>
          <el-tooltip content="Excel 智能导入" placement="top">
            <button
              type="button"
              class="svg-icon-btn import-btn"
              @click="openImport"
              aria-label="Excel 智能导入"
            >
              <svg viewBox="100 60 824 800" width="22" height="22" aria-hidden="true">
                <path d="M840.871012 682.73478H609.004445c-19.482868 0-36.629203-17.107413-36.629204-36.670558 0-19.643421 17.147551-36.7557 36.629204-36.7557h231.866567c19.563145 0 36.629203 17.111062 36.629203 36.7557 0 19.561929-17.066059 36.670558-36.629203 36.670558z"/>
                <path d="M744.340928 562.81747l-109.812199 110.17466c-9.822927 7.325841-19.563145 9.784005-26.808709 9.784005v-0.041355c-9.822927 0-19.565577-2.415593-24.478257-9.781572-14.650465-14.65533-14.650465-36.750834 0-51.406165l109.817064-110.094383c14.650465-14.73439 36.629203-14.73439 51.282101 0 14.651681 14.612759 14.651681 36.669342 0 51.36481z"/>
                <path d="M744.742311 783.048807c-7.323408 4.951602-17.066059 9.784005-26.888986 9.784005-9.658725 0-19.485301-2.374239-24.314055-9.784005l-109.893692-110.055461c-14.652898-14.694252-14.652898-36.711912 0-51.445087 14.65533-14.612759 36.629203-14.612759 51.204257 0l109.893692 110.135738c14.650465 14.731958 14.650465 36.750834-0.001216 51.36481z"/>
                <path d="M857.939503 531.057159c-1.448626 0.440305-3.057806 0-4.027206-1.250367-12.880733-16.986998-42.107468-54.785076-56.997546-69.799219-19.969393-20.328204-47.179484-31.821126-75.601021-31.821126a105.885947 105.885947 0 0 0-75.675217 31.821126l-109.836525 110.257369c-14.652898 14.652898-24.433254 34.256181-29.283901 53.819326-2.478842 7.324624-2.478842 14.652898-2.478842 21.979954 0 7.325841 0 14.611543 2.478842 22.020093 4.850648 19.563145 14.631004 39.12629 29.283901 53.818109l107.419716 110.135738c21.978738 22.020093 46.374286 31.801665 75.677649 31.801665 28.419105-0.121631 55.551352-11.553737 75.596156-31.801665 16.667109-14.812234 44.523061-52.131086 57.081471-69.357698a3.421483 3.421483 0 0 1 3.945713-1.247935c1.448626 0.442737 2.415593 1.811087 2.415593 3.381345 0 55.794614-45.487596 101.481685-101.200717 101.481685H339.26074c-55.65109 0-101.220178-45.687071-101.220179-101.481685V277.614453c0-55.852997 45.569089-101.481685 101.220179-101.481685h419.893639c55.629196 0 101.198285 45.627472 101.198285 101.481685v250.060146c0 1.488765-0.966967 2.896036-2.413161 3.38256z"/>
                <path d="M297.777239 132.444096c-56.114504 0-102.487574 46.514162-102.487574 102.80868v518.839317c0 7.406117 0 14.69182 2.454515 24.474608C166.003331 761.499426 146.499785 729.619917 146.499785 692.94571V196.068104c0-53.842435 43.916122-97.880189 97.616249-97.880189h424.706582c29.22187 0 56.114504 14.69182 73.180563 34.256181H297.777239z"/>
              </svg>
            </button>
          </el-tooltip>
        </div>

        <!-- 右侧：关键词输入框 + 查询 + 重置 -->
        <div class="actions-right">
          <div class="form-control" :class="{ 'is-filled': !!query.keyword }">
            <input
              type="text"
              required
              v-model="query.keyword"
              @keyup.enter="onSearch"
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
              @click="onSearch"
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
        </div>
      </form>
    </div>

    <el-card shadow="never" class="table-card">
      <div class="table-band">
      <el-table
        :data="list"
        v-loading="loading"
        size="small"
        class="gold-table"
        :header-cell-class-name="() => 'gold-header-cell'"
      >
        <el-table-column prop="asset_code" label="资产编号" width="200" fixed="left" />
        <el-table-column prop="asset_class" label="大类" width="80">
          <template #default="{ row }">
            <span class="class-badge" :data-class="row.asset_class">
              <span class="class-badge__dot"></span>
              <span class="class-badge__text">{{ row.asset_class }}</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="110" />
        <el-table-column prop="brand" label="品牌" width="90" />
        <el-table-column prop="model" label="型号" min-width="140" show-overflow-tooltip />
        <el-table-column prop="serial_number" label="SN" width="130" show-overflow-tooltip />
        <el-table-column prop="specification" label="规格" min-width="180" show-overflow-tooltip />
        <el-table-column label="购置日期" width="110">
          <template #default="{ row }">{{ fmtDate(row.purchase_date) }}</template>
        </el-table-column>
        <el-table-column prop="supplier" label="供应商" width="120" show-overflow-tooltip />
        <el-table-column prop="price" label="金额" width="100" align="left">
          <template #default="{ row }">
            {{ row.price != null ? `¥ ${Number(row.price).toFixed(2)}` : '—' }}
          </template>
        </el-table-column>
        <el-table-column label="保修至" width="110">
          <template #default="{ row }">{{ fmtDate(row.warranty_until) }}</template>
        </el-table-column>
        <el-table-column prop="location" label="存放位置" width="110" show-overflow-tooltip />
        <el-table-column prop="owner" label="使用人" width="90">
          <template #default="{ row }">{{ row.owner || '—' }}</template>
        </el-table-column>
        <el-table-column prop="department" label="部门" width="100">
          <template #default="{ row }">{{ row.department || '—' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="statusTag(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right" align="center">
          <template #default="{ row }">
            <div class="row-actions">
              <el-tooltip content="编辑" placement="top">
                <button
                  type="button"
                  class="svg-icon-btn edit"
                  @click="openEdit(row)"
                  aria-label="编辑"
                >
                  <svg viewBox="0 0 1024 1024" width="18" height="18" aria-hidden="true">
                    <path d="M882.553 207.403l-66.652-66.652L894.352 62.3s67.244-1.399 67.244 65.845l-79.043 79.258z m-727.882 34.214v627.609H782.28V443.348l89.658-89.658v515.536c0 49.518-40.14 89.658-89.658 89.658H154.671c-49.518 0-89.658-40.14-89.658-89.658V241.617c0-49.518 40.14-89.658 89.658-89.658h515.536l-89.658 89.658H154.671zM378.817 645.08v-67.244l33.622-33.622 67.199 67.199-33.578 33.667h-67.243z m458.965-392.789L502.021 588.967 434.853 521.8l336.219-336.219 66.71 66.71z"/>
                  </svg>
                </button>
              </el-tooltip>
              <el-tooltip content="二维码" placement="top">
                <button
                  type="button"
                  class="svg-icon-btn qr"
                  @click="openQr(row)"
                  aria-label="二维码"
                >
                  <svg viewBox="0 0 1024 1024" width="28" height="28" aria-hidden="true">
                    <path d="M597.333333 597.333333h85.333334v-85.333333h85.333333v128h-85.333333v42.666667h-85.333334v-42.666667h-85.333333v-128h85.333333v85.333333z m-384-85.333333h256v256H213.333333v-256z m85.333334 85.333333v85.333334h85.333333v-85.333334H298.666667zM213.333333 213.333333h256v256H213.333333V213.333333z m85.333334 85.333334v85.333333h85.333333V298.666667H298.666667z m213.333333-85.333334h256v256h-256V213.333333z m85.333333 85.333334v85.333333h85.333334V298.666667h-85.333334z m85.333334 384h85.333333v85.333333h-85.333333v-85.333333z m-170.666667 0h85.333333v85.333333h-85.333333v-85.333333z"/>
                  </svg>
                </button>
              </el-tooltip>
              <el-popconfirm
                title="确定删除该资产？"
                :icon="null"
                :hide-icon="true"
                popper-class="confirm-inline-popconfirm"
                @confirm="onDelete(row)"
              >
                <template #reference>
                  <button
                    type="button"
                    class="svg-icon-btn del del-color"
                    aria-label="删除"
                  >
                    <svg viewBox="0 0 1024 1024" width="20" height="20" aria-hidden="true">
                      <path d="M862.6176 172.1344H633.856c-4.4032-58.7776-53.4528-105.1136-113.3568-105.1136h-16.9984c-59.904 0-108.9536 46.336-113.3568 105.1136H161.3824c-20.0704 0-36.3008 16.2816-36.3008 36.3008s16.2816 36.3008 36.3008 36.3008h701.2352a36.3008 36.3008 0 0 0 0-72.6016zM686.6944 950.3744H337.3056c-98.2528 0-177.92-79.6672-177.92-177.92V316.3136c0-14.9504 12.1344-27.0848 27.0848-27.0848h651.0592c14.9504 0 27.0848 12.1344 27.0848 27.0848v456.1408c0 98.2528-79.616 177.92-177.92 177.92z" fill="#F7264E"/>
                      <path d="M678.6048 917.3504h-346.112c-83.3024 0-150.8352-67.5328-150.8352-150.8352V329.3184c0-10.5984 8.6016-19.2 19.2-19.2h609.3312c10.5984 0 19.2 8.6016 19.2 19.2v437.1968c0.0512 83.3024-67.4816 150.8352-150.784 150.8352z" fill="#F92B5C"/>
                      <path d="M642.0992 882.8416H350.8224c-83.3024 0-150.8352-67.5328-150.8352-150.8352V344.9856c0-9.9328 8.0896-18.0224 18.0224-18.0224h556.9024c9.9328 0 18.0224 8.0896 18.0224 18.0224v386.9696c0 83.3536-67.5328 150.8864-150.8352 150.8864z" fill="#FC4C66"/>
                      <path d="M615.1168 857.5488h-251.392c-83.3024 0-150.8352-67.5328-150.8352-150.8352v-348.672c0-9.5232 7.68-17.2032 17.2032-17.2032h518.656c9.5232 0 17.2032 7.68 17.2032 17.2032v348.672c0 83.3024-67.5328 150.8352-150.8352 150.8352z" fill="#FF5F7E"/>
                      <path d="M859.8528 182.8864h-260.352c-3.1744-42.24-38.4-75.52-81.408-75.52h-12.1856c-43.008 0-78.2336 33.28-81.408 75.52H164.1472c-14.3872 0-26.0608 11.6736-26.0608 26.112 0 14.3872 11.6736 26.112 26.0608 26.112h695.7568c14.3872 0 26.0608-11.6736 26.0608-26.112 0-14.3872-11.6736-26.112-26.112-26.112z" fill="#FC4C66"/>
                      <path d="M845.2608 193.8432h-279.04a50.5344 50.5344 0 0 0-50.432-46.7456h-7.5776c-26.6752 0-48.4864 20.6336-50.432 46.7456h-279.04a16.1792 16.1792 0 0 0 0 32.3584h666.5216a16.1792 16.1792 0 0 0 0-32.3584z" fill="#FF5F7E"/>
                      <path d="M336.9984 519.168c-37.4784 0-67.9424 30.464-67.9424 67.9424v166.3488c0 37.4784 30.464 67.9424 67.9424 67.9424 37.4784 0 67.9424-30.464 67.9424-67.9424v-166.3488c0-37.4272-30.5152-67.9424-67.9424-67.9424zM684.6976 519.168c-37.4784 0-67.9424 30.464-67.9424 67.9424v166.3488c0 37.4784 30.464 67.9424 67.9424 67.9424 37.4784 0 67.9424-30.464 67.9424-67.9424v-166.3488c-0.0512-37.4272-30.5152-67.9424-67.9424-67.9424zM510.8224 412.1088c-37.4784 0-67.9424 30.464-67.9424 67.9424v273.408c0 37.4784 30.464 67.9424 67.9424 67.9424 37.4784 0 67.9424-30.464 67.9424-67.9424v-273.408c0-37.4784-30.464-67.9424-67.9424-67.9424z" fill="#F92B5C"/>
                      <path d="M336.9984 800.3072c-25.856 0-46.848-20.992-46.848-46.848v-166.3488c0-25.856 20.992-46.848 46.848-46.848 25.856 0 46.848 20.992 46.848 46.848v166.3488c0 25.856-20.992 46.848-46.848 46.848zM684.6976 800.3072c-25.856 0-46.848-20.992-46.848-46.848v-166.3488c0-25.856 20.992-46.848 46.848-46.848 25.856 0 46.848 20.992 46.848 46.848v166.3488c0 25.856-20.992 46.848-46.848 46.848zM510.8224 800.3072c-25.856 0-46.848-20.992-46.848-46.848v-273.408c0-25.856 20.992-46.848 46.848-46.848 25.856 0 46.848 20.992 46.848 46.848v273.408c0 25.856-20.9408 46.848-46.848 46.848z" fill="var(--theme-surface-muted, #f9f1e8)"/>
                      <path d="M336.9984 786.2272a32.768 32.768 0 0 1-32.768-32.768v-166.3488a32.768 32.768 0 1 1 65.536 0v166.3488a32.768 32.768 0 0 1-32.768 32.768zM684.6976 786.2272a32.768 32.768 0 0 1-32.768-32.768v-166.3488a32.768 32.768 0 1 1 65.536 0v166.3488c0 18.0736-14.6944 32.768-32.768 32.768zM510.8224 786.2272a32.768 32.768 0 0 1-32.768-32.768v-273.408a32.768 32.768 0 1 1 65.536 0v273.408c0.0512 18.0736-14.6432 32.768-32.768 32.768z" fill="#FFFFFF"/>
                    </svg>
                  </button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      </div>

      <el-pagination
        style="margin-top: 12px; justify-content: flex-end; display: flex"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        v-model:current-page="query.page"
        v-model:page-size="query.page_size"
        :page-sizes="[10, 20, 50, 100]"
        @current-change="loadList"
        @size-change="loadList"
      />
    </el-card>

    <AssetQrDialog v-model="qrVisible" :asset="qrAsset" />

    <AssetImportDialog
      v-model="importVisible"
      @imported="onImported"
    />

    <el-dialog
      v-model="dialogVisible"
      width="75vw"
      :show-close="true"
      :close-on-click-modal="false"
      append-to-body
      class="asset-edit-dialog"
      align-center
    >
      <template #header>
        <div class="dialog-header"></div>
      </template>


      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="left"
        class="asset-form"
      >
        <!-- 分组：基础信息 -->
        <div class="form-section">
          <div class="section-title">
            <span class="section-icon">
              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                <path d="M618.666667 288a32 32 0 0 1 0 64H320a32 32 0 0 1 0-64h298.666667zM704 480a32 32 0 0 1 0 64H320a32 32 0 0 1 0-64h384zM533.333333 672a32 32 0 0 1 0 64H320a32 32 0 0 1 0-64h213.333333z" fill="currentColor"/>
                <path d="M768 85.333333a128 128 0 0 1 128 128v597.333334a128 128 0 0 1-128 128H256a128 128 0 0 1-128-128V213.333333a128 128 0 0 1 128-128h512z m0 64H256a64 64 0 0 0-64 64v597.333334a64 64 0 0 0 64 64h512a64 64 0 0 0 64-64V213.333333a64 64 0 0 0-64-64z" fill="currentColor"/>
              </svg>
            </span>
            基础信息
          </div>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="资产大类" prop="asset_class">
                <el-select
                  v-model="form.asset_class"
                  placeholder="请选择"
                  style="width: 100%"
                  :disabled="editing"
                  @change="onClassChange"
                >
                  <el-option
                    v-for="c in assetClasses"
                    :key="c.code"
                    :label="`${c.code} - ${c.name}`"
                    :value="c.code"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="9">
              <el-form-item label="资产编号" prop="asset_code">
                <el-input
                  v-model="form.asset_code"
                  :placeholder="editing ? '' : (form.asset_class ? '生成中…' : '请先选择资产大类')"
                  disabled
                  class="asset-code-input"
                >
                  <template v-if="!editing && genLoading" #suffix>
                    <el-icon class="is-loading"><Loading /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="分类" prop="category">
                <el-input v-model="form.category" placeholder="如 笔记本" />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="品牌">
                <el-input v-model="form.brand" placeholder="如 联想" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 分组：规格信息 -->
        <div class="form-section">
          <div class="section-title">
            <span class="section-icon">
              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                <path d="M468.906667 57.941333a68.394667 68.394667 0 0 1 86.165333 0l399.936 322.624c30.058667 24.234667 35.136 68.693333 11.328 99.328a69.269333 69.269333 0 0 1-37.802667 24.768l-3.712 0.810667 0.021334 361.514667c0 59.370667-44.48 108.48-102.528 113.877333l-4.736 0.362667-4.949334 0.106666H211.370667c-59.84 0-109.056-47.808-112.106667-109.312l-0.106667-5.034666-0.021333-361.514667-2.453333-0.490667c-29.696-6.848-52.16-33.088-53.909334-64.96L42.666667 436.010667c0-21.610667 9.685333-42.026667 26.325333-55.466667z m46.72 50.026667a5.76 5.76 0 0 0-7.253334 0L108.864 431.146667a6.058667 6.058667 0 0 0-2.218667 4.693333c0 3.328 2.624 6.016 5.866667 6.016h18.816c17.536-0.021333 31.744 14.506667 31.744 32.405333v392.533334l0.064 3.392C164.437333 896.533333 185.792 917.333333 211.712 917.333333h599.765333l3.328-0.085333c25.770667-1.322667 46.101333-23.146667 46.101334-49.621333V474.282667c0-17.92 14.208-32.426667 31.744-32.426667h18.816c1.792 0 3.477333-0.832 4.608-2.261333a6.101333 6.101333 0 0 0-0.96-8.426667z m138.133333 564.693333a32 32 0 0 1-3.754667 45.098667C610.858667 750.890667 568.106667 768 522.666667 768c-45.44 0-88.192-17.109333-127.36-50.24a32 32 0 1 1 41.386666-48.853333C464.704 692.650667 493.056 704 522.666667 704c29.589333 0 57.941333-11.349333 85.973333-35.093333a32 32 0 0 1 45.12 3.754666z" fill="currentColor"/>
              </svg>
            </span>
            规格信息
          </div>
          <el-row :gutter="20">
            <el-col :span="7">
              <el-form-item label="型号">
                <el-input v-model="form.model" placeholder="如 ThinkPad T14s" />
              </el-form-item>
            </el-col>
            <el-col :span="7">
              <el-form-item label="SN">
                <el-input v-model="form.serial_number" placeholder="序列号 / SN" />
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label="规格">
                <el-input v-model="form.specification" placeholder="如 R7-7840U/16GB/512GB" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 分组：财务与时间 -->
        <div class="form-section">
          <div class="section-title">
            <span class="section-icon">
              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                <path d="M753.770667 74.666667a162.453333 162.453333 0 0 1 162.453333 162.453333v553.194667a32 32 0 1 1-64 0V237.12A98.453333 98.453333 0 0 0 753.770667 138.666667H270.229333a98.453333 98.453333 0 0 0-98.453333 98.453333v553.194667a32 32 0 0 1-64 0V237.12A162.453333 162.453333 0 0 1 270.229333 74.666667h483.541334z" fill="currentColor"/>
                <path d="M970.794667 724.352a32 32 0 0 1 21.077333 60.416l-466.474667 162.773333a32 32 0 0 1-20.992 0.042667l-472.170666-162.773333a32 32 0 0 1 20.864-60.501334l461.674666 159.146667 456.021334-159.104zM618.773333 243.648a32 32 0 1 1 45.333334 45.184l-152.426667 152.917333-152.768-152.896a32 32 0 0 1 45.269333-45.226666l107.456 107.52 107.136-107.498667z" fill="currentColor"/>
                <path d="M683.797333 396.416a32 32 0 1 1 0 64h-343.68a32 32 0 1 1 0-64h343.68zM683.797333 526.634667a32 32 0 1 1 0 64h-343.68a32 32 0 1 1 0-64h343.68z" fill="currentColor"/>
                <path d="M511.253333 353.834667a32 32 0 0 1 32.704 31.274666l7.957334 357.162667a32 32 0 0 1-63.978667 1.429333l-7.978667-357.162666a32 32 0 0 1 31.296-32.704z" fill="currentColor"/>
              </svg>
            </span>
            财务与时间
          </div>
          <el-row :gutter="20">
            <el-col :span="7">
              <el-form-item label="供应商">
                <el-input v-model="form.supplier" placeholder="如 联想官网" />
              </el-form-item>
            </el-col>
            <el-col :span="5">
              <el-form-item label="金额">
                <el-input
                  v-model.number="form.price"
                  type="number"
                  :min="0"
                  step="0.01"
                  placeholder="0.00"
                  class="price-input"
                >
                  <template #prefix>
                    <span class="price-prefix">¥</span>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="购置日期">
                <el-date-picker
                  v-model="form.purchase_date"
                  type="date"
                  value-format="YYYY-MM-DDTHH:mm:ss"
                  style="width: 100%"
                  placeholder="请选择"
                />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="保修至">
                <el-date-picker
                  v-model="form.warranty_until"
                  type="date"
                  value-format="YYYY-MM-DDTHH:mm:ss"
                  style="width: 100%"
                  placeholder="请选择"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 分组：归属与状态 -->
        <div class="form-section">
          <div class="section-title">
            <span class="section-icon">
              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                <path d="M792.896 117.333333a156.437333 156.437333 0 0 1 156.437333 156.437334 32 32 0 0 1-64 0A92.437333 92.437333 0 0 0 792.896 181.333333H231.978667A93.312 93.312 0 0 0 138.666667 274.645333v496.042667a93.312 93.312 0 0 0 93.312 93.312h560.917333a92.437333 92.437333 0 0 0 92.437333-92.437333 32 32 0 1 1 64 0 156.437333 156.437333 0 0 1-156.437333 156.437333H231.978667A157.312 157.312 0 0 1 74.666667 770.688V274.645333A157.312 157.312 0 0 1 231.978667 117.333333h560.917333z" fill="currentColor"/>
                <path d="M456.682667 345.621333a32 32 0 1 1 48.256 42.026667l-117.333334 134.656 116.992 129.813333a32 32 0 0 1-0.042666 42.88l-2.304 2.325334a32 32 0 0 1-45.205334-2.346667l-135.936-150.890667a32 32 0 0 1-0.341333-42.453333l135.914667-156.010667z" fill="currentColor"/>
                <path d="M917.333333 488.106667a32 32 0 0 1 0 64H356.096a32 32 0 0 1 0-64H917.333333z" fill="currentColor"/>
              </svg>
            </span>
            归属与状态
          </div>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="存放位置">
                <el-input v-model="form.location" placeholder="如 库房" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="状态">
                <el-select
                  v-model="form.status"
                  style="width: 100%"
                  class="status-select"
                  :class="`status-select-${statusKey(form.status)}`"
                >
                  <template #prefix>
                    <i class="status-dot" :class="`dot-${statusKey(form.status)}`"></i>
                  </template>
                  <el-option label="在用" value="在用">
                    <i class="status-dot dot-active"></i><span>在用</span>
                  </el-option>
                  <el-option label="闲置" value="闲置">
                    <i class="status-dot dot-idle"></i><span>闲置</span>
                  </el-option>
                  <el-option label="维修" value="维修">
                    <i class="status-dot dot-repair"></i><span>维修</span>
                  </el-option>
                  <el-option label="报废" value="报废">
                    <i class="status-dot dot-scrap"></i><span>报废</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="使用人">
                <el-input v-model="form.owner" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="部门">
                <el-input v-model="form.department" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <!-- 分组：备注 -->
        <div class="form-section">
          <div class="section-title">
            <span class="section-icon">
              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                <path d="M512 74.666667C259.242667 74.666667 53.333333 269.888 53.333333 512l0.106667 9.685333c2.005333 87.146667 30.826667 170.666667 83.029333 241.493334l4.650667 6.165333-28.010667 97.578667c-9.813333 34.133333 9.941333 69.76 44.074667 79.573333l4.757333 0.682667c20.778667 2.986667 22.250667 2.389333 44.544-6.464l82.56-46.464-4.437333-2.346667C353.749333 929.6 431.658667 949.333333 512 949.333333c252.757333 0 458.666667-195.221333 458.666667-437.333333S764.757333 74.666667 512 74.666667z m0 64c218.602667 0 394.666667 167.786667 394.666667 373.333333S730.602667 885.333333 512 885.333333c-70.122667 0-137.429333-17.28-196.736-49.621333l-26.752-14.592-113.408 63.829333a0.32 0.32 0 0 1-0.490667-0.384l36.970667-128.746666-18.218667-23.509334-5.397333-7.125333C142.208 663.104 117.333333 589.354667 117.333333 512c0-205.546667 176.064-373.333333 394.666667-373.333333z" fill="currentColor"/>
                <path d="M694.314667 419.072a32 32 0 0 1 43.221333 47.210667l-196.736 180.096a117.333333 117.333333 0 0 1-161.344-2.730667l-83.093333-81.429333a32 32 0 1 1 44.8-45.717334l83.093333 81.429334a53.333333 53.333333 0 0 0 73.344 1.237333l196.714667-180.096z" fill="currentColor"/>
              </svg>
            </span>
            备注
          </div>
          <el-row :gutter="24">
            <el-col :span="14">
              <el-form-item label-width="0" class="remark-form-item">
                <el-input
                  v-model="form.remark"
                  type="textarea"
                  resize="none"
                  maxlength="500"
                  show-word-limit
                  placeholder="补充说明信息（可选）"
                  class="remark-textarea"
                />
              </el-form-item>
            </el-col>
            <el-col :span="10">
              <el-form-item label-width="0">
                <!-- 整面板就是一个虚线上传区；可拖拽 / 点击空白处上传 -->
                <el-upload
                  class="files-upload"
                  :class="{ 'has-files': displayFiles.length > 0 }"
                  drag
                  :auto-upload="false"
                  :show-file-list="false"
                  multiple
                  :disabled="uploading"
                  :on-change="onPickFile"
                >
                  <!-- 空状态 -->
                  <div class="files-empty" v-if="!displayFiles.length">
                    <div class="files-empty-title">点击上传附件</div>
                    <div class="files-empty-sub">
                      支持拖拽 · 单文件最大 {{ MAX_FILE_MB }} MB
                    </div>
                  </div>

                  <!-- 已有文件：列表 + 底部"添加更多" 提示 -->
                  <div class="files-stage" v-else @click.stop>
                    <div class="files-list">
                      <div
                        v-for="f in displayFiles"
                        :key="f.id"
                        class="file-item"
                        :class="{ 'is-pending': f._pending }"
                      >
                        <div class="file-icon" :style="{ background: fileColor(f.filename) }">
                          {{ fileExt(f.filename) }}
                        </div>
                        <div class="file-meta">
                          <a
                            v-if="!f._pending"
                            class="file-name"
                            :href="f.file_url"
                            target="_blank"
                            :title="f.filename"
                          >{{ f.filename }}</a>
                          <span v-else class="file-name as-text" :title="f.filename">
                            {{ f.filename }}
                            <span class="pending-tag">待上传</span>
                          </span>
                          <div class="file-sub">
                            <span>{{ humanSize(f.size) }}</span>
                            <span class="dot-sep" v-if="!f._pending">·</span>
                            <span v-if="!f._pending">{{ fmtDate(f.created_at) }}</span>
                          </div>
                        </div>
                        <div class="file-actions">
                          <el-tooltip v-if="!f._pending" content="下载" placement="top">
                            <a class="file-action" :href="f.file_url" :download="f.filename" target="_blank" aria-label="下载" @click.stop>
                              <svg viewBox="0 0 1024 1024" width="16" height="16" aria-hidden="true">
                                <path d="M512 64a32 32 0 0 1 32 32v517.4l140.7-140.7a32 32 0 1 1 45.3 45.3L534.6 726a32 32 0 0 1-45.2 0L294 530.6a32 32 0 1 1 45.2-45.2L480 626V96a32 32 0 0 1 32-32z m352 768a32 32 0 0 1 0 64H160a32 32 0 0 1 0-64h704z" fill="currentColor"/>
                              </svg>
                            </a>
                          </el-tooltip>
                          <el-popconfirm
                            :title="f._pending ? '确定移除该文件？' : '确定删除该附件？'"
                            :icon="null"
                            :hide-icon="true"
                            popper-class="confirm-inline-popconfirm"
                            @confirm="onRemoveFile(f)"
                          >
                            <template #reference>
                              <button type="button" class="file-action file-del" aria-label="删除附件" @click.stop>
                                <svg viewBox="0 0 1024 1024" width="14" height="14" aria-hidden="true">
                                  <path d="m812.16 183.467 28.49 28.49L548.49 504.116 840.65 796.276l-28.49 28.49L520.117 532.49 227.957 824.65l-28.49-28.49 292.16-292.16L199.467 211.957l28.49-28.49L520.117 475.51 812.16 183.467z" fill="currentColor"/>
                                </svg>
                              </button>
                            </template>
                          </el-popconfirm>
                        </div>
                      </div>
                    </div>
                    <!-- 添加更多：转发点击到 el-upload 的根，触发文件选择 -->
                    <div
                      class="files-add-more"
                      @click="triggerUploadPick"
                    >
                      <span class="plus">＋</span>
                      <span>添加更多文件</span>
                    </div>
                  </div>
                </el-upload>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button class="btn-ghost" @click="dialogVisible = false">取消</el-button>
          <el-button class="btn-primary-gold" :loading="saving" @click="onSubmit">
            {{ editing ? '保存修改' : '确定新增' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import { toast } from '../utils/toast'
import {
  listAssets,
  createAsset,
  updateAsset,
  deleteAsset,
  listAssetClasses,
  previewNextCode,
  listAssetFiles,
  uploadAssetFile,
  deleteAssetFile,
} from '../api/assets'
import AssetQrDialog from './AssetQrDialog.vue'
import AssetImportDialog from './AssetImportDialog.vue'
const emit = defineEmits(['change'])

const list = ref([])
const total = ref(0)
const loading = ref(false)
const assetClasses = ref([])

const query = reactive({
  page: 1,
  page_size: 10,
  keyword: '',
  status: '',
  category: '',
  asset_class: '',
})

const keywordLabel = computed(() => Array.from('Keyword'))

function fmtDate(v) {
  if (!v) return '—'
  return String(v).slice(0, 10)
}

async function loadClasses() {
  try {
    assetClasses.value = await listAssetClasses()
  } catch {
    /* 错误已提示 */
  }
}

async function loadList() {
  loading.value = true
  try {
    const params = { ...query }
    Object.keys(params).forEach((k) => {
      if (params[k] === '' || params[k] == null) delete params[k]
    })
    const res = await listAssets(params)
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function onSearch() {
  query.page = 1
  loadList()
}

function onReset() {
  query.keyword = ''
  query.status = ''
  query.category = ''
  query.asset_class = ''
  query.page = 1
  loadList()
}

function statusTag(status) {
  return (
    {
      在用: 'success',
      闲置: 'info',
      维修: 'warning',
      报废: 'danger',
    }[status] || ''
  )
}

function statusKey(status) {
  return (
    {
      在用: 'active',
      闲置: 'idle',
      维修: 'repair',
      报废: 'scrap',
    }[status] || 'active'
  )
}

const dialogVisible = ref(false)
const editing = ref(null)
const formRef = ref()
const saving = ref(false)
const genLoading = ref(false)
const fileList = ref([])         // 编辑模式：服务端已存的、当前还在的附件
const pendingFiles = ref([])     // 待上传（新增/编辑都用）：{ tempId, raw, filename, size, created_at }
const pendingDeletes = ref([])   // 编辑模式下被用户点 X 但尚未保存的已有附件：{ id, filename }
const uploading = ref(false)

const MAX_FILE_MB = 50

// 视图层统一展示：先展示「待上传」（新加的浮在最上面），再展示已存在的真实附件
const displayFiles = computed(() => {
  const pending = pendingFiles.value.map((f) => ({
    id: f.tempId,
    filename: f.filename,
    size: f.size,
    created_at: f.created_at,
    file_url: '',
    _pending: true,
  }))
  return editing.value ? [...pending, ...fileList.value] : pending
})

function humanSize(bytes) {
  if (!bytes && bytes !== 0) return '—'
  const units = ['B', 'KB', 'MB', 'GB']
  let v = Number(bytes)
  let i = 0
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024
    i++
  }
  return `${v.toFixed(v >= 10 || i === 0 ? 0 : 1)} ${units[i]}`
}

function fileExt(name) {
  const m = String(name || '').match(/\.([a-zA-Z0-9]+)$/)
  return (m ? m[1] : 'FILE').toUpperCase().slice(0, 4)
}

function fileColor(name) {
  const ext = fileExt(name)
  const map = {
    PDF: '#e25d5d',
    DOC: '#3a82f6', DOCX: '#3a82f6',
    XLS: '#1d8f4e', XLSX: '#1d8f4e', CSV: '#1d8f4e',
    PPT: '#e07a1d', PPTX: '#e07a1d',
    PNG: '#7c5cf0', JPG: '#7c5cf0', JPEG: '#7c5cf0', GIF: '#7c5cf0', WEBP: '#7c5cf0',
    ZIP: 'var(--theme-primary-deep, #8a7355)', RAR: 'var(--theme-primary-deep, #8a7355)', '7Z': 'var(--theme-primary-deep, #8a7355)',
    TXT: '#6b7280', LOG: '#6b7280',
  }
  return map[ext] || 'var(--theme-primary-deep, #8a7355)'
}

async function loadFiles() {
  if (!editing.value) {
    fileList.value = []
    return
  }
  try {
    fileList.value = await listAssetFiles(editing.value.id)
  } catch {
    /* 错误已提示 */
  }
}

async function onPickFile(uploadFile) {
  const raw = uploadFile.raw
  if (!raw) return
  if (raw.size > MAX_FILE_MB * 1024 * 1024) {
    toast.error(`文件过大，单文件最大 ${MAX_FILE_MB} MB`)
    return
  }
  // 新增 / 编辑模式都一律暂存到内存，等点击「保存修改 / 确定新增」后再统一上传到 COS
  pendingFiles.value.unshift({
    tempId: `tmp-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    raw,
    filename: raw.name,
    size: raw.size,
    created_at: new Date().toISOString(),
  })
  toast.success(`已选择：${raw.name}（保存后自动上传）`)
}

async function onRemoveFile(f) {
  // 待上传的暂存文件：直接从内存移除（还没传到 COS）
  if (f._pending) {
    pendingFiles.value = pendingFiles.value.filter((x) => x.tempId !== f.id)
    toast.success('已移除')
    return
  }
  // 已存在的真实附件：编辑模式下只标记待删除，等点击保存才真正调 COS 删除
  if (editing.value) {
    pendingDeletes.value.push({ id: f.id, filename: f.filename })
    fileList.value = fileList.value.filter((x) => x.id !== f.id)
    toast.info(`已标记删除：${f.filename}（保存后生效）`)
    return
  }
  // 兜底（理论上不会进到这个分支）
  await deleteAssetFile(editing.value.id, f.id)
  fileList.value = fileList.value.filter((x) => x.id !== f.id)
  toast.success('附件已删除')
}

function triggerUploadPick(e) {
  if (uploading.value) return
  // 找到 el-upload 内置的隐藏 file input 并触发点击，弹出系统文件选择框
  const input = e?.currentTarget
    ?.closest('.files-upload')
    ?.querySelector('input.el-upload__input')
  input?.click()
}

function emptyForm() {
  return {
    asset_code: '',
    asset_class: '',
    category: '',
    brand: '',
    model: '',
    serial_number: '',
    specification: '',
    purchase_date: '',
    supplier: '',
    price: 0,
    warranty_until: '',
    location: '',
    owner: '',
    department: '',
    status: '在用',
    remark: '',
  }
}

const form = reactive(emptyForm())

const rules = {
  asset_class: [{ required: true, message: '请选择资产大类', trigger: [] }],
  category: [{ required: true, message: '请输入资产分类', trigger: [] }],
}

function resetForm() {
  Object.assign(form, emptyForm())
}

function openCreate() {
  editing.value = null
  resetForm()
  fileList.value = []
  pendingFiles.value = []
  pendingDeletes.value = []
  dialogVisible.value = true
  nextTick(() => formRef.value?.clearValidate())
}

function openEdit(row) {
  editing.value = row
  fileList.value = []
  pendingFiles.value = []
  pendingDeletes.value = []
  loadFiles()
  Object.assign(form, {
    asset_code: row.asset_code,
    asset_class: row.asset_class || '',
    category: row.category || '',
    brand: row.brand || '',
    model: row.model || '',
    serial_number: row.serial_number || '',
    specification: row.specification || '',
    purchase_date: row.purchase_date || '',
    supplier: row.supplier || '',
    price: row.price ?? 0,
    warranty_until: row.warranty_until || '',
    location: row.location || '',
    owner: row.owner || '',
    department: row.department || '',
    status: row.status || '在用',
    remark: row.remark || '',
  })
  dialogVisible.value = true
  nextTick(() => formRef.value?.clearValidate())
}

function onClassChange() {
  if (editing.value) return
  // 大类清空 → 编号也清空；否则自动重新生成
  if (!form.asset_class) {
    form.asset_code = ''
    return
  }
  regenerateCode()
}

// 自动预览下一个编号；失败 / 没大类时静默不打扰用户
async function regenerateCode() {
  if (editing.value || !form.asset_class) return
  genLoading.value = true
  try {
    const params = { asset_class: form.asset_class }
    if (form.purchase_date) {
      const y = new Date(form.purchase_date).getFullYear()
      if (!Number.isNaN(y)) params.year = y
    }
    const res = await previewNextCode(params)
    form.asset_code = res.code
  } catch {
    /* 错误已由 request.js 提示 */
  } finally {
    genLoading.value = false
  }
}

// 购置日期变化时，新增模式下重新生成一次（年份段会跟着变）
watch(
  () => form.purchase_date,
  () => {
    if (!editing.value && form.asset_class) {
      regenerateCode()
    }
  },
)

async function onSubmit() {
  await formRef.value?.validate()
  saving.value = true
  try {
    const payload = { ...form }
    if (!payload.purchase_date) payload.purchase_date = null
    if (!payload.warranty_until) payload.warranty_until = null
    if (!payload.asset_code) payload.asset_code = null
    if (editing.value) {
      const { asset_code, ...rest } = payload
      await updateAsset(editing.value.id, rest)
      await syncAttachments(editing.value.id, '更新成功')
    } else {
      const created = await createAsset(payload)
      await syncAttachments(created.id, `新增成功，编号：${created.asset_code}`)
    }
    dialogVisible.value = false
    loadList()
    emit('change')
  } finally {
    saving.value = false
  }
}

/**
 * 把当前 pendingFiles（待上传）/ pendingDeletes（待删除）一次性同步到 COS，
 * 调用方传入 assetId 以及主操作（创建 / 更新）的成功文案，组合成一条 toast。
 */
async function syncAttachments(assetId, mainOkMsg) {
  const dels = pendingDeletes.value
  const ups = pendingFiles.value

  let delOk = 0
  let delFail = 0
  let upOk = 0
  let upFail = 0

  for (const d of dels) {
    try {
      await deleteAssetFile(assetId, d.id)
      delOk++
    } catch {
      delFail++
    }
  }
  for (const f of ups) {
    try {
      await uploadAssetFile(assetId, f.raw)
      upOk++
    } catch {
      upFail++
    }
  }

  pendingDeletes.value = []
  pendingFiles.value = []

  const parts = [mainOkMsg]
  if (upOk) parts.push(`上传 ${upOk} 个附件`)
  if (delOk) parts.push(`删除 ${delOk} 个附件`)

  const hasFail = upFail || delFail
  if (!hasFail) {
    toast.success(parts.join('，'))
    return
  }

  if (upFail) parts.push(`${upFail} 个附件上传失败`)
  if (delFail) parts.push(`${delFail} 个附件删除失败`)
  if (upOk + delOk === 0) {
    toast.error(parts.join('，'))
  } else {
    toast.warning(parts.join('，'))
  }
}

async function onDelete(row) {
  await deleteAsset(row.id)
  toast.success('删除成功')
  loadList()
  emit('change')
}

const qrVisible = ref(false)
const qrAsset = ref(null)
function openQr(row) {
  qrAsset.value = row
  qrVisible.value = true
}

const importVisible = ref(false)
function openImport() {
  importVisible.value = true
}
function onImported() {
  loadList()
  emit('change')
}

defineExpose({ loadList })

onMounted(() => {
  loadClasses()
  loadList()
})
</script>

<style scoped>
/* ===================== 页面入场动画 ===================== */
.assets-table {
  animation: page-fade-in 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.assets-table .filter-bar {
  animation: section-rise 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: 0.06s;
}
.assets-table .table-card {
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

/* 表格紧贴筛选栏 */
.table-card {
  --asset-table-band-y: 16px;
  margin-top: 0;
  background: transparent;
  border: none;
  border-radius: 0 !important;
  box-shadow: none;
  isolation: isolate;
  overflow: visible !important;
  position: relative;
}
.table-band {
  position: relative;
  isolation: isolate;
}
.table-band::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 0;
  background: var(--bg-page, #fafaf8);
  pointer-events: none;
}
.table-band :deep(.gold-table) {
  position: relative;
  z-index: 1;
}
.table-card :deep(.el-card__body) {
  padding: var(--asset-table-band-y) 18px !important;
  background: transparent;
}

/* ===================== 大类徽标：印章式描边轮廓 ===================== */
.class-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 38px;
  height: 24px;
  padding: 0 8px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: #b08a52;
  background: transparent;
  border: 1.5px solid #c9a063;
  border-radius: 3px;
  position: relative;
  transition: background 0.22s ease, color 0.22s ease, box-shadow 0.22s ease,
    transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
  text-transform: uppercase;
  font-family: 'Georgia', 'Times New Roman', serif;
}
.class-badge::before,
.class-badge::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 4px;
  height: 1.5px;
  background: #c9a063;
  transform: translateY(-50%);
}
.class-badge::before { left: -5px; }
.class-badge::after { right: -5px; }
.class-badge:hover {
  background: #c9a063;
  color: #fff;
  box-shadow: 0 2px 8px rgba(var(--theme-primary-rgb), 0.35);
  transform: translateY(-1px);
}
.class-badge__dot { display: none; }
.class-badge__text {
  line-height: 1;
  display: inline-block;
}

/* 不同大类配色 */
.class-badge[data-class="IT"] {
  color: #4a8bd6;
  border-color: #4a8bd6;
}
.class-badge[data-class="IT"]::before,
.class-badge[data-class="IT"]::after { background: #4a8bd6; }
.class-badge[data-class="IT"]:hover {
  background: #4a8bd6;
  color: #fff;
  box-shadow: 0 2px 8px rgba(74, 139, 214, 0.35);
}

.class-badge[data-class="OA"] {
  color: #4ea886;
  border-color: #4ea886;
}
.class-badge[data-class="OA"]::before,
.class-badge[data-class="OA"]::after { background: #4ea886; }
.class-badge[data-class="OA"]:hover {
  background: #4ea886;
  color: #fff;
  box-shadow: 0 2px 8px rgba(78, 168, 134, 0.35);
}

.class-badge[data-class="FA"] {
  color: #d68a4a;
  border-color: #d68a4a;
}
.class-badge[data-class="FA"]::before,
.class-badge[data-class="FA"]::after { background: #d68a4a; }
.class-badge[data-class="FA"]:hover {
  background: #d68a4a;
  color: #fff;
  box-shadow: 0 2px 8px rgba(214, 138, 74, 0.35);
}

.class-badge[data-class="VE"] {
  color: #9466b8;
  border-color: #9466b8;
}
.class-badge[data-class="VE"]::before,
.class-badge[data-class="VE"]::after { background: #9466b8; }
.class-badge[data-class="VE"]:hover {
  background: #9466b8;
  color: #fff;
  box-shadow: 0 2px 8px rgba(148, 102, 184, 0.35);
}

/* ===================== 筛选栏：上移、左右两组、底边对齐 ===================== */
.filter-bar {
  display: flex;
  margin: -12px 0 8px;
  padding: 0;
}
.filter-row {
  display: flex;
  width: 100%;
  align-items: flex-end;        /* 关键：所有子元素底部对齐 */
  justify-content: space-between;
  gap: 14px;
  padding: 0 6px;
}
.actions-left,
.actions-right {
  display: inline-flex;
  align-items: flex-end;
  gap: 14px;
}
.actions-left {
  margin-left: 12px;
}
.actions-left .svg-icon-btn {
  transform: translateY(2px);
}
/* 让左侧两个图标按钮的下边沿与 keyword 输入框底部金线齐平 */
.actions-left .svg-icon-btn,
.actions-right .svg-icon-btn {
  padding-bottom: 6px;          /* 与 .form-control input 的底部 padding 对齐 */
}

/* ===================== 金色浮动 label 输入框 ===================== */
.form-control {
  position: relative;
  margin: 0;
  width: 200px;
}
.form-control input {
  background-color: transparent;
  border: 0;
  border-bottom: 2px solid var(--theme-input-border, #e0d2b8);
  display: block;
  width: 100%;
  padding: 14px 0 6px;
  font-size: 15px;
  color: var(--theme-primary-deep, #8a7355);
  font-family: inherit;
  transition: border-bottom-color 0.25s ease;
}
.form-control input:focus,
.form-control input:valid,
.form-control.is-filled input {
  outline: 0;
  border-bottom-color: var(--theme-primary, #c5a47e);
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
  color: var(--theme-text-muted, #b9a78a);
  letter-spacing: 1px;
  transition: 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
.form-control input:focus + label span,
.form-control input:valid + label span,
.form-control.is-filled label span {
  color: var(--theme-primary-deep, #8a7355);
  transform: translateY(-18px);
  font-size: 11px;
  font-weight: 600;
}

/* ===================== 金色表头表格 ===================== */
.gold-table {
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid var(--theme-border, #ecdfc9);
  border-left: 0;
  border-right: 0;
}

/* 表头：白底 + 金色文字（不要用透明，避免固定列表头与普通列表头重叠透出） */
.gold-table :deep(.gold-header-cell),
.gold-table :deep(.el-table__fixed-header-wrapper th.gold-header-cell),
.gold-table :deep(.el-table__fixed-right .gold-header-cell),
.gold-table :deep(.el-table__fixed .gold-header-cell) {
  background-color: #ffffff !important;
  color: var(--theme-primary-deep, #8a7355) !important;
  font-weight: 600;
  font-size: 16px;
  letter-spacing: 1.3px;
  height: 60px;
  border-bottom: 2px solid var(--theme-primary-light-3, #d4b89a) !important;
  border-right: none !important;
}
.gold-table :deep(.gold-header-cell .cell) {
  color: var(--theme-primary-deep, #8a7355) !important;
  font-size: 17px;
  letter-spacing: 1.5px;
  font-weight: 700;
}
/* 表头整行背景同样保持白色，覆盖 Element Plus 默认浅灰 */
.gold-table :deep(.el-table__header-wrapper thead tr) {
  background-color: #ffffff !important;
}
/* 排序图标改为金色 */
.gold-table :deep(.gold-header-cell .caret-wrapper .sort-caret.ascending) {
  border-bottom-color: var(--theme-primary-deep, #8a7355);
}
.gold-table :deep(.gold-header-cell .caret-wrapper .sort-caret.descending) {
  border-top-color: var(--theme-primary-deep, #8a7355);
}

/* 单元格：去除竖向边框，加大行高拉开行距 */
.gold-table :deep(.el-table__row td) {
  border-bottom: 1px solid var(--theme-table-line, #f3ece0) !important;
  border-right: none !important;
  padding: 14px 0 !important;
  font-size: 13.5px;
}
/* 悬停高亮（柔和米色） */
.gold-table :deep(.el-table__body tr:hover > td.el-table__cell) {
  background-color: var(--theme-surface, #faf4e9) !important;
}

/* ===================== 图标按钮（使用内联 SVG） ===================== */
.row-actions {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
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
  outline: 1px dashed rgba(var(--theme-primary-deep-rgb), 0.5);
  outline-offset: 2px;
}

/* 编辑：金棕色 */
.svg-icon-btn.edit svg { fill: var(--theme-primary-deep, #8a7355); }
.svg-icon-btn.edit:hover svg { fill: var(--theme-text-hover, #6e5a40); }

/* 二维码：深灰/黑，相对其他图标下移一点 */
.svg-icon-btn.qr svg { fill: #333; }
.svg-icon-btn.qr:hover svg { fill: #000; }
.svg-icon-btn.qr { transform: translateY(1px); }
/* 黑夜模式下：二维码图标改为白色 */
html.dark .svg-icon-btn.qr svg { fill: #ffffff; }
html.dark .svg-icon-btn.qr:hover svg { fill: #f0f0f0; }

/* 删除：彩色 SVG 内置颜色，按钮本身仅做缩放反馈 */
.svg-icon-btn.del svg { fill: initial; }
.svg-icon-btn.del:hover svg {
  filter: brightness(1.05) saturate(1.1);
}

/* 查询 / 重置 / 新增资产 / Excel 导入：无背景，金棕色 */
.svg-icon-btn.search-btn,
.svg-icon-btn.reset-btn,
.svg-icon-btn.add-btn,
.svg-icon-btn.import-btn {
  padding: 6px;
}
.svg-icon-btn.search-btn svg,
.svg-icon-btn.reset-btn svg,
.svg-icon-btn.add-btn svg,
.svg-icon-btn.import-btn svg { fill: var(--theme-primary-deep, #8a7355); }
.svg-icon-btn.search-btn:hover svg,
.svg-icon-btn.reset-btn:hover svg,
.svg-icon-btn.add-btn:hover svg,
.svg-icon-btn.import-btn:hover svg { fill: var(--theme-text-hover, #6e5a40); }
.svg-icon-btn.import-btn svg {
  transform: translateY(-1px);
  transition: transform 0.38s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: import-btn-breath 3.6s ease-in-out infinite;
  will-change: transform;
}
.svg-icon-btn.import-btn:hover svg {
  transform: translateY(-1px) scale(1.18) translateX(2px);
  animation: none;
}
.svg-icon-btn.import-btn:active svg {
  transform: translateY(-1px) scale(0.92);
  transition-duration: 0.1s;
  animation: none;
}
@keyframes import-btn-breath {
  0%, 100% { transform: translateY(-1px) translateX(0); }
  50%       { transform: translateY(-1px) translateX(1.5px); }
}
.svg-icon-btn.reset-btn svg { transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1); }
.svg-icon-btn.reset-btn:hover svg { transform: rotate(-180deg); }
.svg-icon-btn.add-btn svg { transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }
.svg-icon-btn.add-btn:hover svg { transform: rotate(90deg); }
.svg-icon-btn.search-btn:hover svg { animation: search-bounce 0.5s ease; }
@keyframes search-bounce {
  0%, 100% { transform: translateY(0); }
  40%      { transform: translateY(-3px) scale(1.05); }
  70%      { transform: translateY(0) scale(0.98); }
}

/* ===================== 编辑/新增资产弹窗 UI 美化 ===================== */
/* 16:9 电脑屏幕比例：宽度 75vw（最小 1100px、最大 1500px），高度按内容自适应 */
.asset-edit-dialog :deep(.el-dialog) {
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 24px 60px rgba(60, 45, 25, 0.18), 0 4px 12px rgba(60, 45, 25, 0.08);
  border: 1px solid #efe4d0;
  background: #ffffff;
  min-width: 1100px;
  max-width: 1500px;
  height: clamp(560px, calc(75vw * 9 / 16), 780px);
  max-height: 90vh;
  margin: 0 !important;
  display: flex;
  flex-direction: column;
}
.asset-edit-dialog :deep(.el-dialog__header) {
  margin: 0;
  padding: 0;
  background: #ffffff;
  border-bottom: none;
  height: 0;
}
.asset-edit-dialog .dialog-header {
  display: none;
}
.asset-edit-dialog :deep(.el-dialog__headerbtn) {
  top: 14px;
  right: 14px;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  z-index: 2;
  transition: background-color 0.2s ease;
}
.asset-edit-dialog :deep(.el-dialog__headerbtn:hover) {
  background-color: rgba(var(--theme-primary-deep-rgb), 0.08);
}
.asset-edit-dialog :deep(.el-dialog__close) {
  font-size: 18px;
  color: #999;
}
.asset-edit-dialog :deep(.el-dialog__body) {
  padding: 24px 36px 10px;
  flex: 1;
  min-height: 0;
  overflow-y: auto;
}
.asset-edit-dialog :deep(.el-dialog__footer) {
  padding: 16px 36px 22px;
  border-top: 1px solid var(--theme-table-line, #f3ece0);
  background: #ffffff;
  flex-shrink: 0;
}

/* ===== 顶部资产摘要（无底色） ===== */
/* ===== 表单分组（放大版 + 高密度） ===== */
.asset-edit-dialog .asset-form .form-section {
  margin-bottom: 14px;
}
.asset-edit-dialog .asset-form .form-section:last-child {
  margin-bottom: 0;
}
/* form-item：label 在左、输入框在右，间距固定，单行不换行 */
.asset-edit-dialog :deep(.el-form-item) {
  margin-bottom: 14px;
  display: flex;
  flex-wrap: nowrap;            /* 整个 form-item 内不换行 */
  align-items: center;
}
/* label：宽度严格按文字内容自适应（覆盖 EP 注入的 inline width） */
.asset-edit-dialog :deep(.el-form-item__label) {
  flex: 0 0 auto;               /* 不伸缩，按内容宽度 */
  width: max-content !important;
  max-width: max-content !important;
  min-width: 0 !important;
  height: 38px;
  line-height: 38px;
  margin: 0 10px 0 0 !important; /* label 与输入框的固定间距：10px */
  padding: 0 !important;
  text-align: left;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  font-size: 13.5px;
  letter-spacing: 0.3px;
  white-space: nowrap;
  overflow: visible;
  float: none;
}
/* 必填星号 */
.asset-edit-dialog :deep(.el-form-item.is-required > .el-form-item__label::before) {
  margin-right: 4px;
  color: var(--theme-primary, #c5a47e);
}
/* 内容区：占满 label 之外的剩余空间 */
.asset-edit-dialog :deep(.el-form-item__content) {
  flex: 1 1 auto;
  min-width: 0;                 /* 关键：让内容区可被 flex 收缩，而不是撑出列宽 */
  line-height: normal;
  margin-left: 0 !important;
}
/* 输入框尺寸 */
.asset-edit-dialog :deep(.el-input__wrapper),
.asset-edit-dialog :deep(.el-textarea__inner) {
  min-height: 38px;
}
.asset-edit-dialog :deep(.el-input__inner) {
  height: 36px;
  line-height: 36px;
  font-size: 14px;
}
.asset-edit-dialog :deep(.el-input__inner)::placeholder,
.asset-edit-dialog :deep(.el-textarea__inner)::placeholder {
  color: var(--theme-placeholder, #c9bba0);
}
/* 备注 textarea 这种多行控件，label 顶部对齐 */
.asset-edit-dialog :deep(.el-form-item:has(.el-textarea)) {
  align-items: flex-start;
}
.asset-edit-dialog :deep(.el-form-item:has(.el-textarea) > .el-form-item__label) {
  height: 38px;
  line-height: 38px;
}

.asset-edit-dialog .section-title {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--theme-text-strong, #5a4730);
  margin: 0 0 14px;
  letter-spacing: 1px;
}
.asset-edit-dialog .section-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  color: var(--theme-text-strong, #5a4730);
}
.asset-edit-dialog .section-icon svg {
  width: 20px;
  height: 20px;
  overflow: visible;
}
.asset-edit-dialog .section-icon svg path {
  stroke: currentColor;
  stroke-width: 32;
  stroke-linejoin: round;
  stroke-linecap: round;
  paint-order: stroke fill;
}

/* ===== 输入框统一观感（圆角 + 金色边框） ===== */
.asset-edit-dialog :deep(.el-input__wrapper),
.asset-edit-dialog :deep(.el-textarea__inner) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px var(--theme-input-border, #e6d9bf) inset;
  transition: box-shadow 0.2s ease;
  background: #ffffff;
}
.asset-edit-dialog :deep(.el-input__inner) {
  color: #1a1a1a;
  font-size: 13px;
}
.asset-edit-dialog :deep(.el-input__wrapper:hover),
.asset-edit-dialog :deep(.el-textarea__inner:hover) {
  box-shadow: 0 0 0 1px var(--theme-primary-light-3, #d4b89a) inset;
}
.asset-edit-dialog :deep(.el-input__wrapper.is-focus),
.asset-edit-dialog :deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 1.5px var(--theme-primary-deep, #8a7355) inset !important;
}
.asset-edit-dialog :deep(.el-input.is-disabled .el-input__wrapper) {
  background-color: var(--theme-surface-muted, #f8f3e9);
  box-shadow: 0 0 0 1px var(--theme-border, #ecdfc9) inset;
}
.asset-edit-dialog :deep(.el-input.is-disabled .el-input__inner) {
  color: var(--theme-primary-deep, #8a7355);
  -webkit-text-fill-color: var(--theme-primary-deep, #8a7355);
}
.asset-edit-dialog :deep(.el-input-group__append) {
  background-color: var(--theme-surface, #faf4e9);
  color: var(--theme-primary-deep, #8a7355);
  border-radius: 0 8px 8px 0;
  box-shadow: 0 0 0 1px var(--theme-input-border, #e6d9bf) inset;
}
.asset-edit-dialog :deep(.el-input-group__append .el-button) {
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 500;
  border: none;
  background: transparent;
}

/* 金额输入框 ¥ 前缀 */
.asset-edit-dialog .price-input :deep(.el-input__wrapper) {
  padding-left: 0;
}
.asset-edit-dialog .price-prefix {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 100%;
  background: var(--theme-surface, #faf4e9);
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  border-right: 1px solid var(--theme-input-border, #e6d9bf);
  margin-right: 10px;
}
/* 隐藏 number 输入框的上下箭头 */
.asset-edit-dialog .price-input :deep(input[type='number']) {
  -moz-appearance: textfield;
  appearance: textfield;
}
.asset-edit-dialog .price-input :deep(input[type='number']::-webkit-outer-spin-button),
.asset-edit-dialog .price-input :deep(input[type='number']::-webkit-inner-spin-button) {
  -webkit-appearance: none;
  appearance: none;
  margin: 0;
}

/* 状态下拉选择器 - 带圆点 */
.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2c9b5a;
  margin-right: 6px;
  flex-shrink: 0;
}
.status-dot.dot-active { background: #2c9b5a; }
.status-dot.dot-idle { background: #909399; }
.status-dot.dot-repair { background: #e6a23c; }
.status-dot.dot-scrap { background: #f56c6c; }

.asset-edit-dialog :deep(.el-select .el-input__prefix) {
  display: flex;
  align-items: center;
  padding-left: 4px;
}

/* 日期选择器图标颜色 */
.asset-edit-dialog :deep(.el-input__prefix-inner > .el-icon) {
  color: var(--theme-primary-deep, #8a7355);
}

/* textarea 字符计数样式 */
.asset-edit-dialog :deep(.el-textarea .el-input__count) {
  background: transparent;
  color: var(--theme-text-muted, #b9a78a);
  font-size: 12px;
}

/* ===== 底部按钮 ===== */
.asset-edit-dialog .dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.asset-edit-dialog .btn-ghost {
  min-width: 96px;
  height: 40px;
  padding: 0 24px;
  border-radius: 8px;
  border: 2px solid var(--theme-primary-deep, #8a7355);
  background: transparent;
  color: var(--theme-primary-deep, #8a7355);
  font-weight: 600;
  letter-spacing: 2px;
  transition: all 0.2s ease;
}
.asset-edit-dialog .btn-ghost:hover {
  background: rgba(var(--theme-primary-deep-rgb), 0.1);
  border-color: var(--theme-text-hover, #6e5a40);
  color: var(--theme-text-hover, #6e5a40);
}
.asset-edit-dialog .btn-primary-gold {
  min-width: 120px;
  height: 40px;
  padding: 0 28px;
  border-radius: 8px;
  border: none;
  color: #ffffff;
  font-weight: 600;
  letter-spacing: 2px;
  background: linear-gradient(135deg, var(--theme-primary, #c5a47e) 0%, var(--theme-primary-deep, #8a7355) 100%);
  box-shadow: none;
  transition: transform 0.15s ease, filter 0.2s ease;
}
.asset-edit-dialog .btn-primary-gold:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
}
.asset-edit-dialog .btn-primary-gold:active {
  transform: translateY(0);
}

/* ===================== 附件上传面板（虚线 dropzone） ===================== */
/* 整面板就是 el-upload 的拖拽区，固定高度内部滚动 */
.files-upload {
  width: 100%;
  display: block;
}
.files-upload :deep(.el-upload),
.files-upload :deep(.el-upload-dragger) {
  width: 100%;
  display: block;
}
.files-upload :deep(.el-upload-dragger) {
  height: 160px;                    /* ★ 固定高度，与左侧备注 textarea 对齐 */
  padding: 0;
  border: 1.5px dashed var(--theme-primary-light-3, #d4b89a);
  border-radius: 12px;
  background: var(--theme-surface-subtle, #fffdf8);
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  cursor: pointer;
}

/* 备注 textarea：固定高度，与右侧附件框对齐 */
.remark-form-item :deep(.el-textarea),
.remark-form-item :deep(.el-textarea__inner) {
  height: 160px !important;
}
.remark-form-item :deep(.el-textarea__inner) {
  resize: none;
}
.files-upload :deep(.el-upload-dragger:hover) {
  border-color: var(--theme-primary-deep, #8a7355);
  background: var(--theme-surface-hover, #fff9ec);
}
.files-upload :deep(.el-upload-dragger.is-dragover) {
  border-color: var(--theme-primary-deep, #8a7355);
  background: var(--theme-surface-strong, #fff4dc);
  box-shadow: 0 0 0 4px rgba(var(--theme-primary-deep-rgb), 0.08) inset;
}
/* 已有文件时：默认状态用实线浅金色框，避免和列表内容争夺视觉焦点 */
.files-upload.has-files :deep(.el-upload-dragger) {
  border-style: solid;
  border-color: var(--theme-border, #ecdfc9);
  cursor: default;                  /* 列表区不再整体可点 */
}
.files-upload.has-files :deep(.el-upload-dragger:hover) {
  border-color: var(--theme-border, #ecdfc9);
  background: var(--theme-surface-subtle, #fffdf8);
}
/* 禁用态（新建模式） */
.files-upload.is-disabled :deep(.el-upload-dragger) {
  border-color: var(--theme-border, #ecdfc9);
  background: var(--theme-surface-muted, #faf6ec);
  cursor: not-allowed;
}
.files-upload.is-disabled :deep(.el-upload-dragger:hover) {
  border-color: var(--theme-border, #ecdfc9);
  background: var(--theme-surface-muted, #faf6ec);
}

/* ===== 空状态：居中大图标 + 主标题 + 副标题 ===== */
.files-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--theme-text-muted, #b9a78a);
  text-align: center;
  padding: 16px;
}
.files-empty svg {
  color: var(--theme-primary, #c5a47e);
  margin-bottom: 4px;
}
.files-empty-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--theme-primary-deep, #8a7355);
  letter-spacing: 0.5px;
}
.files-empty-sub {
  font-size: 12px;
  color: var(--theme-text-muted, #b9a78a);
}

/* ===== 已有文件时的列表区 ===== */
.files-stage {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  text-align: left;
  cursor: default;
}
.files-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px 6px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  scrollbar-width: thin;
  scrollbar-color: var(--theme-primary-light-3, #d4b89a) transparent;
}
.files-list::-webkit-scrollbar {
  width: 6px;
}
.files-list::-webkit-scrollbar-thumb {
  background: var(--theme-primary-light-3, #d4b89a);
  border-radius: 3px;
}
.files-list::-webkit-scrollbar-thumb:hover {
  background: var(--theme-primary-dark-2, #b89770);
}
.files-list::-webkit-scrollbar-track {
  background: transparent;
}

/* ===== 底部"添加更多文件" 按钮（保留虚线感觉，与上方文件列表区分） ===== */
.files-add-more {
  flex-shrink: 0;
  margin: 0 8px 8px;
  padding: 6px;
  border: 1px dashed var(--theme-primary-light-3, #d4b89a);
  border-radius: 8px;
  background: transparent;
  color: var(--theme-primary-deep, #8a7355);
  font-size: 12.5px;
  font-weight: 500;
  letter-spacing: 0.3px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.18s ease;
}
.files-add-more:hover {
  border-color: var(--theme-primary-deep, #8a7355);
  background: var(--theme-surface-hover, #fff7e6);
  color: var(--theme-text-strong, #5a4730);
}
.files-add-more .plus {
  font-size: 14px;
  font-weight: 700;
  line-height: 1;
}

.file-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  border-radius: 6px;
  transition: background-color 0.15s ease;
}
.file-item:hover {
  background: var(--theme-surface, #faf4e9);
}
.file-icon {
  flex-shrink: 0;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.3px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}
.file-meta {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.file-name {
  font-size: 12.5px;
  color: #1a1a1a;
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
  line-height: 1.4;
}
.file-name:hover {
  color: var(--theme-primary-deep, #8a7355);
  text-decoration: underline;
}
.file-name.as-text {
  color: #6b5e48;
  cursor: default;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.file-name.as-text:hover {
  color: #6b5e48;
  text-decoration: none;
}
.pending-tag {
  display: inline-flex;
  align-items: center;
  height: 16px;
  padding: 0 6px;
  border-radius: 8px;
  background: var(--theme-surface-strong, #fff4dc);
  color: var(--theme-primary-deep, #b8893a);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
}
.file-item.is-pending {
  background: #fffaf0;
}
.file-item.is-pending:hover {
  background: var(--theme-surface-strong, #fff4dc);
}
.file-sub {
  font-size: 11px;
  color: var(--theme-text-muted, #a89c84);
  display: inline-flex;
  align-items: center;
  gap: 5px;
  line-height: 1.3;
}
.file-sub .dot-sep {
  color: var(--theme-border-strong, #d4c8ad);
}

/* 操作按钮组：默认半隐藏，悬停 file-item 时显示 */
.file-actions {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  opacity: 0;
  transition: opacity 0.15s ease;
}
.file-item:hover .file-actions {
  opacity: 1;
}
.file-action {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  border: none;
  background: transparent;
  color: var(--theme-primary-deep, #8a7355);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.15s ease;
}
.file-action:hover {
  background: var(--theme-surface-strong, #f0e3c8);
  color: var(--theme-text-strong, #5a4730);
}
.file-action.file-del:hover {
  background: #fdebec;
  color: #f56c6c;
}
.file-action svg {
  display: block;
}

.files-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--theme-text-muted, #b9a78a);
  font-size: 12px;
  text-align: center;
  padding: 20px;
}
.files-empty svg {
  color: var(--theme-primary-light-3, #d4b89a);
}
</style>

<style>
/* ===== 通用确认弹窗（删除资产 / 删除附件 / 移除文件 等单行确认） ===== */
/* 同时保留 .delete-asset-popconfirm 作为历史别名，避免破坏外部引用 */
.confirm-inline-popconfirm.el-popper,
.delete-asset-popconfirm.el-popper {
  min-width: auto !important;
  width: auto !important;
  max-width: none !important;
  padding: 14px 16px !important;
  border-radius: 10px !important;
  border: 1px solid rgba(var(--theme-primary-rgb), 0.6) !important;
  box-shadow: 0 12px 32px rgba(94, 74, 46, 0.22),
    0 2px 8px rgba(94, 74, 46, 0.08) !important;
}
.confirm-inline-popconfirm .el-popconfirm__main,
.delete-asset-popconfirm .el-popconfirm__main {
  align-items: center;
  white-space: nowrap;
  padding-left: 0 !important;
  margin-bottom: 10px;
}
.confirm-inline-popconfirm .el-popconfirm__icon,
.confirm-inline-popconfirm .el-popconfirm__main > .el-icon,
.delete-asset-popconfirm .el-popconfirm__icon,
.delete-asset-popconfirm .el-popconfirm__main > .el-icon {
  display: none !important;
}
.confirm-inline-popconfirm .el-popconfirm__main .el-popconfirm__icon + *,
.delete-asset-popconfirm .el-popconfirm__main .el-popconfirm__icon + * {
  margin-left: 0 !important;
}
.confirm-inline-popconfirm .el-popconfirm__action,
.delete-asset-popconfirm .el-popconfirm__action {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.confirm-inline-popconfirm .el-popper__arrow::before,
.delete-asset-popconfirm .el-popper__arrow::before {
  border-color: rgba(var(--theme-primary-rgb), 0.6) !important;
}

/* ===================== 编辑/新增资产弹窗 进入/退出动效 ===================== */
/* 弹窗本体：自定义入场，从下方放大淡入 */
.asset-edit-dialog {
  animation: asset-dialog-pop-in 0.36s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes asset-dialog-pop-in {
  from {
    opacity: 0;
    transform: translate3d(0, 18px, 0) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translate3d(0, 0, 0) scale(1);
  }
}
/* 蒙层淡入更平滑 */
.el-overlay:has(.asset-edit-dialog) {
  animation: asset-dialog-overlay-in 0.28s ease both;
}
@keyframes asset-dialog-overlay-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
</style>
