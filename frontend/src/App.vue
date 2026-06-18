<template>
  <n-config-provider :theme="currentTheme" :theme-overrides="themeOverrides">
    <n-layout>
      <HeaderNav />
      <n-layout-content content-style="padding: 24px; max-width: 1400px; margin: 0 auto;">
        <router-view />
      </n-layout-content>
      <n-layout-footer bordered class="footer-bar">
        <p class="footer-disclaimer">本网站所有数据来源于第三方渠道，仅供参考、学习交流使用，不确保数据的完全真实性</p>
        <p class="footer-copyright">Copyright © Leaf developer 2026</p>
      </n-layout-footer>
    </n-layout>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, provide, watch } from 'vue'
import { NConfigProvider, NLayout, NLayoutContent, NLayoutFooter, darkTheme } from 'naive-ui'
import type { GlobalThemeOverrides } from 'naive-ui'
import HeaderNav from './components/HeaderNav.vue'

const isDark = ref(false)
provide('isDark', isDark)

const currentTheme = computed(() => isDark.value ? darkTheme : null)

const themeOverrides = computed<GlobalThemeOverrides>(() => ({
  common: {
    primaryColor: '#18a058',
    ...(isDark.value ? {} : {}),
  },
}))

// 同步 body 背景色
watch(isDark, (val) => {
  document.body.style.background = val ? '#1e1e1e' : '#f5f5f5'
  document.body.style.color = val ? '#ddd' : '#333'
  document.body.classList.toggle('dark', val)
}, { immediate: true })
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f5f5;
  color: #333;
  transition: background 0.3s, color 0.3s;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.n-layout {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.n-layout-content {
  flex: 1;
}

.footer-bar {
  text-align: center;
  padding: 20px 16px;
}

.footer-disclaimer {
  font-size: 12px;
  color: #999;
  margin-bottom: 6px;
}

.footer-copyright {
  font-size: 13px;
  color: #666;
}

body.dark .footer-disclaimer {
  color: #777;
}

body.dark .footer-copyright {
  color: #aaa;
}
</style>
