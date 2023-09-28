import type { App } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import type { RouteRecordRaw } from 'vue-router'

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    name: 'default',
    path: '/',
    component: () => import('@/Default.vue'),
    meta: {}
  },
  {
    name: 'foo',
    path: '/foo',
    component: () => import('@/components/HelloWorld.vue'),
    meta: {}
  },
  {
    name: 'table v1',
    path: '/table/v1',
    component: () => import('@/TableV1Test.vue'),
    meta: {}
  },
  {
    name: 'table v2',
    path: '/table/v2',
    component: () => import('@/TableV2Test.vue'),
    meta: {}
  }
]

const router = createRouter({
  history: createWebHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export default router
