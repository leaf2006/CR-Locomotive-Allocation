<template>
  <n-data-table
    :columns="columns"
    :data="data"
    :bordered="false"
    :single-line="false"
    :pagination="{ pageSize: 50 }"
    :row-key="(row: TrainItem) => row.id"
    :expanded-row-keys="expandedKeys"
    @update:expanded-row-keys="onExpandedKeysChange"
    striped
  />
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import { NDataTable, NButton, NImage } from 'naive-ui'
import type { DataTableColumns, DataTableRowKey } from 'naive-ui'
import type { TrainItem } from '@/types'

const props = defineProps<{
  data: TrainItem[]
}>()

const emit = defineEmits<{
  (e: 'clickModel', model: string): void
  (e: 'clickAllocation', allocation: string): void
}>()

const expandedKeys = ref<DataTableRowKey[]>([])

function onExpandedKeysChange(keys: DataTableRowKey[]) {
  expandedKeys.value = keys
}

function formatPhotoDate(date: string | null): string {
  if (!date || date.length < 6) return '-'
  const year = date.substring(0, 4)
  const month = date.substring(4, 6)
  return `${year}年${month}月`
}

const columns: DataTableColumns<TrainItem> = [
  {
    type: 'expand',
    expandable: () => true,
    renderExpand: (row: TrainItem) => {
      return h('div', { style: 'padding: 16px 0; line-height: 2;' }, [
        h('div', {}, [
          h('strong', {}, '备注：'),
          h('span', {}, row.note || '无备注'),
        ]),
        row.photoAuthor
          ? h('div', {}, [h('strong', {}, '拍摄者：'), h('span', {}, row.photoAuthor)])
          : null,
        row.photoDate
          ? h('div', {}, [h('strong', {}, '拍摄日期：'), h('span', {}, formatPhotoDate(row.photoDate))])
          : null,
        row.photoUrl
          ? h('div', { style: 'margin-top: 8px;' }, [
              h('strong', {}, '照片：'),
              h('br'),
              h(NImage, {
                src: row.photoUrl,
                width: 300,
                lazy: true,
                style: 'margin-top: 8px; border-radius: 4px;',
              }),
            ])
          : h('div', {}, [h('strong', {}, '照片：'), h('span', { style: 'opacity: 0.5;' }, '暂无图片')]),
      ])
    },
  },
  {
    title: '编号',
    key: 'id',
    width: 160,
    ellipsis: { tooltip: true },
  },
  {
    title: '车型',
    key: 'model',
    width: 120,
    render(row) {
      return h(
        NButton,
        {
          text: true,
          type: 'primary',
          onClick: () => emit('clickModel', row.model),
        },
        { default: () => row.model }
      )
    },
  },
  {
    title: '配属',
    key: 'allocation',
    width: 180,
    ellipsis: { tooltip: true },
    render(row) {
      if (!row.allocation) return h('span', { style: 'opacity: 0.5;' }, '-')
      return h(
        NButton,
        {
          text: true,
          type: 'primary',
          onClick: () => emit('clickAllocation', row.allocation!),
        },
        { default: () => row.allocation }
      )
    },
  },
  {
    title: '生产厂家',
    key: 'manufacturer',
    width: 160,
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', {}, row.manufacturer || '-')
    },
  },
]
</script>
