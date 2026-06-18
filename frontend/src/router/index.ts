import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Query', component: () => import('@/pages/Query.vue') },
  { path: '/guide', name: 'Guide', component: () => import('@/pages/Guide.vue') },
  { path: '/report', name: 'Report', component: () => import('@/pages/Report.vue') },
  { path: '/about', name: 'About', component: () => import('@/pages/About.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
