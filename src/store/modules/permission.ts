import { defineStore } from 'pinia'
import { asyncRouterMap, constantRouterMap } from '@/router'
import { flatMultiLevelRoutes } from '@/utils/routerHelper'
import { cloneDeep } from 'lodash-es'

export interface PermissionState {
  routers: AppRouteRecordRaw[]
  addRouters: AppRouteRecordRaw[]
  isAddRouters: boolean
  menuTabRouters: AppRouteRecordRaw[]
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
      let routerMap: AppRouteRecordRaw[] = []

      routerMap = cloneDeep(asyncRouterMap)

      // 动态路由，404一定要放到最后面
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
      // 渲染菜单的所有路由
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
