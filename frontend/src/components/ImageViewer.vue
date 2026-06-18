<template>
  <n-image
    :src="src"
    :width="width"
    :fallback-src="''"
    lazy
    style="border-radius: 4px;"
  >
    <template #placeholder>
      <div style="width: 100%; height: 120px; display: flex; align-items: center; justify-content: center; opacity: 0.5;">
        加载中...
      </div>
    </template>
    <template #error>
      <div style="width: 100%; height: 120px; display: flex; align-items: center; justify-content: center; opacity: 0.5;">
        暂无图片
      </div>
    </template>
  </n-image>
</template>

<script setup lang="ts">
import { NImage } from 'naive-ui'

defineProps<{
  src: string
  width?: number
}>()
</script>
