import type { App } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { Layout } from '@/utils/routerHelper'

import type { RouteRecordRaw } from 'vue-router'

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
      title: 'Войти',
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
          title: 'Главная',
          icon: 'ant-design:dashboard-filled',
          noCache: true,
          affix: true,
          alwaysShow: true
        }
      },
      {
        path: 'user',
        component: () => import('@/views/Dashboard/UserSettings.vue'),
        name: 'UserSettings',
        meta: {
          title: 'Профиль',
          icon: 'ant-design:setting-outlined',
          noCache: true,
          hidden: true
        }
      }
    ]
  },
  {
    path: '/setting',
    component: Layout,
    name: 'Setting',
    meta: {
      icon: 'ant-design:setting-outlined',
      title: 'Настройки',
      alwaysShow: true
    },
    children: [
      {
        path: 'user',
        component: () => import('@/views/User/UserTable.vue'),
        name: 'UserTable',
        meta: {
          title: 'Пользователи',
          icon: 'ant-design:user-outlined'
        }
      },
      {
        path: 'user/create',
        component: () => import('@/views/User/UserCreate.vue'),
        name: 'UserCreate',
        meta: {
          title: 'Создать пользователя',
          noTagsView: true,
          noCache: true,
          hidden: true,
          canTo: true,
          activeMenu: '/setting/user'
        }
      },
      {
        path: 'user/:userId(\\d+)',
        component: () => import('@/views/User/UserUpdate.vue'),
        name: 'UserUpdate',
        meta: {
          title: 'Редактирования пользователя',
          noTagsView: true,
          noCache: true,
          hidden: true,
          canTo: true,
          activeMenu: '/setting/user'
        }
      },
      {
        path: 'roles',
        component: () => import('@/views/User/UserRoles.vue'),
        name: 'UserRoles',
        meta: {
          title: 'Роли',
          icon: 'ant-design:apartment-outlined'
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
