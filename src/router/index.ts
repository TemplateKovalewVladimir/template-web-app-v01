import type { App } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { Layout } from '@/utils/routerHelper'

import type { RouteRecordRaw } from 'vue-router'

import { useI18n } from '@/hooks/web/useI18n'

const { t } = useI18n()

export const constantRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
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
    path: '/login',
    component: () => import('@/views/Login/Login.vue'),
    name: 'Login',
    meta: {
      hidden: true,
      title: t('router.login'),
      noTagsView: true
    }
  },
  {
    path: '/404',
    component: () => import('@/views/Error/404.vue'),
    name: 'NoFind',
    meta: {
      hidden: true,
      title: '404',
      noTagsView: true
    }
  }
]

export const asyncRouterMap: AppRouteRecordRaw[] = [
  {
    path: '/dashboard',
    component: Layout,
    name: 'Dashboard',
    meta: {},
    children: [
      {
        path: '',
        component: () => import('@/views/Dashboard/MainPage.vue'),
        name: 'MainPage',
        meta: {
          title: t('router.dashboard'),
          icon: 'ant-design:dashboard-filled',
          noCache: true,
          affix: true,
          alwaysShow: true
        }
      }
    ]
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

const router = createRouter({
  history: createWebHistory(),
  strict: true,
  routes: constantRouterMap as RouteRecordRaw[],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export const setupRouter = (app: App<Element>) => {
  app.use(router)
}

export const resetRouter = (): void => {
  const resetWhiteNameList = ['Redirect', 'Login', 'NoFind', 'Root']
  router.getRoutes().forEach((route) => {
    const { name } = route
    if (name && !resetWhiteNameList.includes(name as string)) {
      router.hasRoute(name) && router.removeRoute(name)
    }
  })
}

export default router
