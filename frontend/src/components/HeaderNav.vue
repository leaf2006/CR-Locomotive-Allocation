<template>
  <n-layout-header bordered class="header-layout">
    <div class="header-title" @click="$router.push('/')">
      轨上名录
    </div>
    <n-space align="center" class="header-nav">
      <n-button :type="currentRoute === '/' ? 'primary' : 'default'" quaternary @click="$router.push('/')" size="small">
        查询
      </n-button>
      <n-button :type="currentRoute === '/guide' ? 'primary' : 'default'" quaternary @click="$router.push('/guide')" size="small">
        使用指南
      </n-button>
      <n-button :type="currentRoute === '/report' ? 'primary' : 'default'" quaternary @click="$router.push('/report')" size="small">
        数据有误？
      </n-button>
      <n-button :type="currentRoute === '/about' ? 'primary' : 'default'" quaternary @click="$router.push('/about')" size="small">
        关于
      </n-button>
      <n-button quaternary circle size="small" @click="toggleDark" :style="{ padding: '6px' }">
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
.header-layout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  gap: 8px;
  flex-wrap: wrap;
  background: #fff;
  transition: background 0.3s;
}

body.dark .header-layout {
  background: #1e1e1e;
}

.header-title {
  font-size: 20px;
  font-weight: bold;
  color: #18a058;
  cursor: pointer;
  white-space: nowrap;
}

.header-nav {
  flex-shrink: 0;
}

.theme-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.theme-icon :deep(svg) {
  width: 20px;
  height: 20px;
}

@media (max-width: 800px) {
  .header-layout {
    padding: 8px 12px;
    justify-content: center;
  }

  .header-title {
    font-size: 18px;
    width: 100%;
    text-align: center;
  }

  .header-nav {
    justify-content: center;
  }
}
</style>
