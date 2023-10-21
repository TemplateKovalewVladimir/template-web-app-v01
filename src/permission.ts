import router from './router'
import { useTitle } from '@/hooks/web/useTitle'
import { useNProgress } from '@/hooks/web/useNProgress'
import { usePermissionStore } from '@/store/modules/permission'
import { usePageLoading } from '@/hooks/web/usePageLoading'
import { useUserStore } from '@/store/modules/user'
import { getCurrentUser } from '@/api/user'
import { RouteRecordRaw } from 'vue-router'

const { start, done } = useNProgress()

const { loadStart, loadDone } = usePageLoading()

const whiteList = ['/login']

router.beforeEach(async (to, _from, next) => {
  start()
  loadStart()

  // Белый лист
  if (whiteList.includes(to.path)) {
    next()
    return
  }

  // Инициализировать store нужно внутри beforeEach
  // см https://pinia.vuejs.org/core-concepts/outside-component-usage.html#Single-Page-Applications
  const userStore = useUserStore()
  const permissionStore = usePermissionStore()

  // Запрос информации о пользователе
  if (userStore.userInfo == null) {
    try {
      const { data: userInfo } = await getCurrentUser()
      userStore.userInfo = userInfo
    } catch {
      next(`/login?redirect=${to.path}`)
      return
    }
  }

  // Добавляю Route
  if (!permissionStore.isAddRouters) {
    permissionStore.generateRoutes()
    permissionStore.getAddRouters.forEach((route) => {
      router.addRoute(route as unknown as RouteRecordRaw) // 动态添加可访问路由表
    })
    permissionStore.setIsAddRouters(true)

    next({ ...to, replace: true })
    return
  }

  next()
})

router.afterEach((to) => {
  useTitle(to?.meta?.title as string)
  done() // 结束Progress
  loadDone()
})
