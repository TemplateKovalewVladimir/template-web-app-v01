import type { App } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { Layout } from '@/utils/routerHelper'

import type { RouteRecordRaw } from 'vue-router'

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/test/01',
    name: 'Root',
    meta: {
      hidden: true
    }
  },
  {
    path: '/redirect',
    component: Layout,
    name: 'Redirect',
    children: [
      {
        path: '/redirect/:path(.*)',
        name: 'Redirect',
        component: () => import('@/components/Redirect/Redirect.vue'),
        meta: {}
      }
    ],
    meta: {
      hidden: true,
      noTagsView: true
    }
  },

  {
    path: '/test',
    component: Layout,
    redirect: '/test/01',
    name: 'Test',
    meta: {
      title: 'Test',
      icon: 'ant-design:dashboard-filled',
      alwaysShow: true
    },
    children: [
      {
        path: '01',
        component: () => import('@/views/Test/TestView01.vue'),
        name: 'TestView01',
        meta: {
          title: 'Test01',
          icon: 'ant-design:dashboard-filled'
        }
      },
      {
        path: '02',
        component: () => import('@/views/Test/TestView02.vue'),
        name: 'TestView02',
        meta: {
          title: 'Test02',
          icon: 'ant-design:dashboard-filled'
        }
      },
      {
        path: '03',
        component: () => import('@/views/Test/TestView03.vue'),
        name: 'TestView03',
        meta: {
          title: 'Test03',
          icon: 'ant-design:dashboard-filled'
        }
      }
    ]
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = []

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
