<template>
  <n-card>
    <n-space vertical :size="16">
      <n-space :size="12" align="center" wrap>
        <!-- 车型 -->
        <n-select
          v-model:value="query.model"
          :options="modelOptions"
          placeholder="输入搜索或选择车型"
          filterable
          clearable
          style="width: 200px;"
          @clear="clearModel"
        />
        <!-- 车号 -->
        <n-input
          v-model:value="query.number"
          placeholder="车号，如 0001"
          clearable
          style="width: 160px;"
          @clear="clearNumber"
        />
        <!-- 生产厂家 -->
        <n-select
          v-model:value="query.manufacturer"
          :options="manufacturerOptions"
          placeholder="输入搜索或选择厂家"
          filterable
          clearable
          style="width: 200px;"
          @clear="clearManufacturer"
        />
        <!-- 配属 -->
        <n-select
          v-model:value="query.allocation"
          :options="allocationOptions"
          placeholder="输入搜索或选择配属"
          filterable
          clearable
          style="width: 200px;"
          @clear="clearAllocation"
        />
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
