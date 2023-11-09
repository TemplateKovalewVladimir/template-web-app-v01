import { cloneDeep } from 'lodash-es'
import { defineStore } from 'pinia'

import { asyncRouterMap, constantRouterMap } from '@/router'
import { flatMultiLevelRoutes } from '@/utils/routerHelper'

import { useUserStore } from './user'

export interface PermissionState {
  routers: AppRouteRecordRaw[]
  addRouters: AppRouteRecordRaw[]
  isAddRouters: boolean
  menuTabRouters: AppRouteRecordRaw[]
}

export function deleteRoutes(
  routes: AppRouteRecordRaw[],
  whiteListRouter: string[]
): AppRouteRecordRaw[] {
  const result: AppRouteRecordRaw[] = []

  for (const route of routes) {
    if (whiteListRouter.includes(route.name)) {
      if (route.children === undefined) {
        result.push(cloneDeep(route))
      } else {
        const children = deleteRoutes(route.children, whiteListRouter)
        const cloneRoute = cloneDeep({ ...route, children: [] as AppRouteRecordRaw[] })
        cloneRoute.children = children
        result.push(cloneRoute)
      }
    }
  }
  return result
}

export const usePermissionStore = defineStore('permission', {
  state: (): PermissionState => ({
    routers: [],
    addRouters: [],
    isAddRouters: false,
    menuTabRouters: []
  }),
  getters: {
    getRouters(): AppRouteRecordRaw[] {
      return this.routers
    },
    getAddRouters(): AppRouteRecordRaw[] {
      return flatMultiLevelRoutes(cloneDeep(this.addRouters))
    },
    getIsAddRouters(): boolean {
      return this.isAddRouters
    },
    getMenuTabRouters(): AppRouteRecordRaw[] {
      return this.menuTabRouters
    }
  },
  actions: {
    generateRoutes() {
      const userStore = useUserStore()
      let routerMap: AppRouteRecordRaw[] = []

      const userRoles = Object.keys(userStore.userInfo?.roles.frontend || {})
      routerMap = deleteRoutes(asyncRouterMap, userRoles)

      // Динамическая маршрутизация, в конце необходимо поставить 404
      this.addRouters = routerMap.concat([
        {
          path: '/:path(.*)*',
          redirect: '/404',
          name: '404Page',
          meta: {
            hidden: true,
            breadcrumb: false
          }
        }
      ])
      // Рендеринг всех маршрутов меню
      this.routers = cloneDeep(constantRouterMap).concat(routerMap)
    },
    setIsAddRouters(state: boolean): void {
      this.isAddRouters = state
    },
    setMenuTabRouters(routers: AppRouteRecordRaw[]): void {
      this.menuTabRouters = routers
    }
  }
})
