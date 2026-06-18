<template>
  <n-layout-header bordered :style="{ padding: '12px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: isDark ? '#1e1e1e' : '#fff', transition: 'background 0.3s' }">
    <div style="font-size: 20px; font-weight: bold; color: #18a058; cursor: pointer;" @click="$router.push('/')">
      轨上名录
    </div>
    <n-space align="center">
      <n-button :type="currentRoute === '/' ? 'primary' : 'default'" quaternary @click="$router.push('/')">
        查询
      </n-button>
      <n-button :type="currentRoute === '/guide' ? 'primary' : 'default'" quaternary @click="$router.push('/guide')">
        使用指南
      </n-button>
      <n-button :type="currentRoute === '/report' ? 'primary' : 'default'" quaternary @click="$router.push('/report')">
        数据有误？
      </n-button>
      <n-button :type="currentRoute === '/about' ? 'primary' : 'default'" quaternary @click="$router.push('/about')">
        关于
      </n-button>
      <n-button quaternary circle size="large" @click="toggleDark" :style="{ padding: '6px' }">
        <template #icon>
          <span v-if="isDark" class="theme-icon" v-html="iconLight" />
          <span v-else class="theme-icon" v-html="iconDark" />
        </template>
      </n-button>
    </n-space>
  </n-layout-header>
</template>

<script setup lang="ts">
import { computed, inject, ref, type Ref } from 'vue'
import { useRoute } from 'vue-router'
import { NLayoutHeader, NButton, NSpace } from 'naive-ui'
import iconDark from '@/assets/icons/dark_mode.svg?raw'
import iconLight from '@/assets/icons/light_mode.svg?raw'

const route = useRoute()
const currentRoute = computed(() => route.path)

const isDark = inject<Ref<boolean>>('isDark', () => ref(false), true)
const toggleDark = () => { isDark.value = !isDark.value }
</script>

<style scoped>
.theme-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.theme-icon :deep(svg) {
  width: 20px;
  height: 20px;
}
</style>
