<template>
  <n-card>
    <n-space vertical :size="16">
      <div class="filter-row">
        <!-- 车型 -->
        <div class="filter-group">
          <div class="filter-label">车型</div>
          <n-select
            v-model:value="query.model"
            :options="modelOptions"
            filterable
            clearable
            @clear="clearModel"
          />
        </div>
        <!-- 车号 -->
        <div class="filter-group">
          <div class="filter-label">车号</div>
          <n-input
            v-model:value="query.number"
            placeholder="0001"
            clearable
            @clear="clearNumber"
          />
        </div>
        <!-- 生产厂家 -->
        <div class="filter-group">
          <div class="filter-label">生产厂家</div>
          <n-select
            v-model:value="query.manufacturer"
            :options="manufacturerOptions"
            filterable
            clearable
            @clear="clearManufacturer"
          />
        </div>
        <!-- 配属 -->
        <div class="filter-group">
          <div class="filter-label">配属</div>
          <n-select
            v-model:value="query.allocation"
            :options="allocationOptions"
            filterable
            clearable
            @clear="clearAllocation"
          />
        </div>
        <!-- 全局清除 -->
        <div class="filter-actions">
          <n-button @click="clearAll" :disabled="!hasAnyQuery">
            清除全部
          </n-button>
        </div>
      </div>
      <div style="opacity: 0.6; font-size: 13px;">
        共 {{ filteredCount }} 条结果
        <template v-if="version">
          &nbsp;&nbsp;版本号：<a
            :href="'./data/raw_result.json'"
            target="_blank"
            rel="noopener noreferrer"
            style="color: inherit; text-decoration: underline; text-underline-offset: 2px;"
          >{{ version }}</a>
        </template>
      </div>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NCard, NSpace, NSelect, NInput, NButton } from 'naive-ui'

const props = defineProps<{
  query: {
    model: string
    number: string
    manufacturer: string
    allocation: string
  }
  models: string[]
  manufacturers: string[]
  allocations: string[]
  filteredCount: number
  version?: string
}>()

const emit = defineEmits<{
  (e: 'clearModel'): void
  (e: 'clearNumber'): void
  (e: 'clearManufacturer'): void
  (e: 'clearAllocation'): void
  (e: 'clearAll'): void
}>()

const modelOptions = computed(() =>
  props.models.map(m => ({ label: m, value: m }))
)
const manufacturerOptions = computed(() =>
  props.manufacturers.map(m => ({ label: m, value: m }))
)
const allocationOptions = computed(() =>
  props.allocations.map(a => ({ label: a, value: a }))
)

const hasAnyQuery = computed(() =>
  props.query.model || props.query.number || props.query.manufacturer || props.query.allocation
)

function clearModel() { emit('clearModel') }
function clearNumber() { emit('clearNumber') }
function clearManufacturer() { emit('clearManufacturer') }
function clearAllocation() { emit('clearAllocation') }
function clearAll() { emit('clearAll') }
</script>

<style scoped>
/* ---------- 搜索字段行（flex-wrap） ----------
   宽度足够时所有搜索项 + 清除按钮在一行内显示，
   空间不足时自动换行，杜绝横向溢出。 */
.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-end;
}

/* ---------- 单个搜索框组 ---------- */
.filter-group {
  flex: 1 1 160px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

/* n-select / n-input 填满所在列宽 */
.filter-group :deep(.n-select),
.filter-group :deep(.n-input) {
  width: 100%;
}

.filter-label {
  font-size: 13px;
  color: #666;
  text-align: left;
  white-space: nowrap;
}

/* ---------- 清除按钮不伸缩 ---------- */
.filter-actions {
  flex: 0 0 auto;
}
</style>
