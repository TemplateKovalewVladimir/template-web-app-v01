import router from './router'
// import { useAppStoreWithOut } from '@/store/modules/app'
// import { useStorage } from '@/hooks/web/useStorage'
// import type { RouteRecordRaw } from 'vue-router'
import { useTitle } from '@/hooks/web/useTitle'
import { useNProgress } from '@/hooks/web/useNProgress'
// import { usePermissionStoreWithOut } from '@/store/modules/permission'
import { usePageLoading } from '@/hooks/web/usePageLoading'
import { useUserStore } from '@/store/modules/user'
import { getCurrentUser } from '@/api/user'

// const permissionStore = usePermissionStoreWithOut()

// const appStore = useAppStoreWithOut()

// const { getStorage } = useStorage()

const { start, done } = useNProgress()

const { loadStart, loadDone } = usePageLoading()

const whiteList = ['/login']

router.beforeEach(async (to, _from, next) => {
  start()
  loadStart()

  // Инициализировать store нужно внутри beforeEach
  // см https://pinia.vuejs.org/core-concepts/outside-component-usage.html#Single-Page-Applications
  const userStore = useUserStore()

  // Белый лист
  if (whiteList.includes(to.path)) {
    next()
    return
  }

  // Запрос информации о пользователе
  if (userStore.userInfo == null) {
    try {
      const { data: userInfo } = await getCurrentUser()
      userStore.userInfo = userInfo
    } catch {
      next('/login')
      return
    }
  }

  next()

  // // 开发者可根据实际情况进行修改
  // const roleRouters = getStorage('roleRouters') || []

  // // 是否使用动态路由
  // if (appStore.getDynamicRouter) {
  //   appStore.serverDynamicRouter
  //     ? await permissionStore.generateRoutes('server', roleRouters as AppCustomRouteRecordRaw[])
  //     : await permissionStore.generateRoutes('frontEnd', roleRouters as string[])
  // } else {
  //   await permissionStore.generateRoutes('static')
  // }

  // // permissionStore.getAddRouters.forEach((route) => {
  // //   router.addRoute(route as unknown as RouteRecordRaw) // 动态添加可访问路由表
  // // })
  // // const redirectPath = from.query.redirect || to.path
  // // const redirect = decodeURIComponent(redirectPath as string)
  // // const nextData = to.path === redirect ? { ...to, replace: true } : { path: redirect }
  // permissionStore.setIsAddRouters(true)

  // next()
  // //   }
  // // } else {
  // //   if (whiteList.indexOf(to.path) !== -1) {
  // //     next()
  // //   } else {
  // //     next(`/login?redirect=${to.path}`) // 否则全部重定向到登录页
  // //   }
  // // }
})

router.afterEach((to) => {
  useTitle(to?.meta?.title as string)
  done() // 结束Progress
  loadDone()
})
