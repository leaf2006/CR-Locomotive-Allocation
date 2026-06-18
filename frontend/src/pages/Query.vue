<template>
  <n-spin :show="loading">
    <n-space vertical :size="16">
      <QueryPanel
        :query="query"
        :models="models"
        :manufacturers="manufacturers"
        :allocations="allocations"
        :filtered-count="filteredData.length"
        @clear-model="clearModel"
        @clear-number="clearNumber"
        @clear-manufacturer="clearManufacturer"
        @clear-allocation="clearAllocation"
        @clear-all="clearAll"
      />
      <ResultTable
        v-if="filteredData.length > 0"
        :data="filteredData"
        @click-model="setModel"
        @click-allocation="setAllocation"
      />
      <EmptyState v-else />
    </n-space>
  </n-spin>
</template>

<script setup lang="ts">
import { NSpin, NSpace } from 'naive-ui'
import QueryPanel from '@/components/QueryPanel.vue'
import ResultTable from '@/components/ResultTable.vue'
import EmptyState from '@/components/EmptyState.vue'
import { useData } from '@/composables/useData'
import { useQuery } from '@/composables/useQuery'
import { useFilter } from '@/composables/useFilter'

const { rawData, models, manufacturers, allocations, loading } = useData()
const {
  query,
  clearModel,
  clearNumber,
  clearManufacturer,
  clearAllocation,
  clearAll,
  setModel,
  setAllocation,
} = useQuery()
const { filteredData } = useFilter(rawData, query)
</script>
