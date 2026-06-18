import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  base: '/CR-Locomotive-Allocation/',
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
})
