<template>
  <n-card>
    <n-space vertical :size="16">
      <n-space :size="16" align="end" wrap>
        <!-- 车型 -->
        <div class="filter-group">
          <div class="filter-label">车型</div>
          <n-select
            v-model:value="query.model"
            :options="modelOptions"
            filterable
            clearable
            style="width: 200px;"
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
            style="width: 160px;"
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
            style="width: 200px;"
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
            style="width: 200px;"
            @clear="clearAllocation"
          />
        </div>
        <!-- 全局清除 -->
        <n-button @click="clearAll" :disabled="!hasAnyQuery">
          清除全部
        </n-button>
      </n-space>
      <div style="opacity: 0.6; font-size: 13px;">
        共 {{ filteredCount }} 条结果
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
.filter-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-label {
  font-size: 13px;
  color: #666;
  text-align: left;
}
</style>
