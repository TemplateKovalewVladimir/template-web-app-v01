import { useRoute } from 'vue-router'

import { UserRole } from '@/api/generated/models/UserRole'
import { useUserStore } from '@/store/modules/user'

const DEFAULT_ROUTE = 'DEFAULT_ROUTE'
const DEFAULT_ROLE: UserRole = UserRole.RO

export const useCan = () => {
  const route = useRoute()
  const userStore = useUserStore()

  const roles =
    userStore.userInfo?.roles.frontend ??
    ({ DEFAULT_ROUTE: DEFAULT_ROLE } as Record<string, UserRole>)
  const routeName = (route.name as string) ?? DEFAULT_ROUTE

  const currentRole: UserRole = roles[routeName]

  const can = (): boolean => {
    if (currentRole === UserRole.RO) return false
    if (currentRole === UserRole.RW) return true
    return false
  }
  const isCan = can()

  return { isCan }

  // import { ComponentInternalInstance, DirectiveBinding, VNode } from 'vue'
  // import { Directive } from 'vue'
  // interface VNoneWithCtx extends VNode {
  //   ctx?: ComponentInternalInstance
  // }
  // /**
  //  * НЕ ИСПОЛЬЗУЙ В TEMPLATE SLOT VirtTable!!!
  //  */
  //   let countUpdate = 0
  // const disabledElement = (vnode: VNoneWithCtx) => {
  //   if (vnode.ctx) {
  //     const nameComponent = vnode.ctx.type.name

  //     if (nameComponent === 'ElForm') vnode.ctx.props.disabled = !isCan
  //     if (nameComponent === 'ElButton') vnode.ctx.props.disabled = !isCan
  //     if (nameComponent === 'ElInput') vnode.ctx.props.disabled = !isCan
  //   }
  // }

  // const vCan: Directive<HTMLElement, string> = {
  //   created: (_el: HTMLElement, _binding: DirectiveBinding<string>, vnode: VNoneWithCtx) => {
  //     disabledElement(vnode)
  //   },
  //   updated: (_el: HTMLElement, _binding: DirectiveBinding<string>, vnode: VNoneWithCtx) => {
  //     countUpdate++
  //     if (countUpdate > 100) console.warn('vCan - Слишком много раз обновилось!!', vnode)

  //     disabledElement(vnode)
  //   }
  // }
}
