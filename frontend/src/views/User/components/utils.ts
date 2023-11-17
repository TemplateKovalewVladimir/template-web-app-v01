import { UserRoleBackend, UserRolesSchemaBackend } from '@/api/generated'

enum UserRoleFrontend {
  NONE = 'NONE'
}

type UserRoleType = UserRoleBackend | UserRoleFrontend

export interface RoleType {
  name: string
  title?: string
  role: UserRoleType
  children?: RoleType[]
}

export function convertToRoleType(
  routes: AppRouteRecordRaw[],
  userRoles: UserRolesSchemaBackend
): RoleType[] {
  const result: RoleType[] = []
  for (const route of routes) {
    const convertedRoute: RoleType = {
      name: route.name,
      title: route.meta.title,
      role: userRoles.frontend.hasOwnProperty(route.name)
        ? userRoles.frontend[route.name]
        : UserRoleFrontend.NONE,
      children:
        route?.children !== undefined ? convertToRoleType(route.children, userRoles) : undefined
    }
    result.push(convertedRoute)
  }
  return result
}

function _convertToUserRolesSchema(roles: RoleType[]): Record<string, UserRoleBackend> {
  let userRole = {}
  for (const role of roles) {
    if (role.role !== UserRoleFrontend.NONE) {
      userRole[role.name] = role.role
    }
    if (role.children) {
      const childrenRole = _convertToUserRolesSchema(role.children)
      if (Object.keys(childrenRole).length !== 0) childrenRole[role.name] = UserRoleBackend.RO
      if (childrenRole) userRole = { ...userRole, ...childrenRole }
    }
  }
  return userRole
}

export function convertToUserRolesSchema(roles: RoleType[]): UserRolesSchemaBackend {
  return { frontend: _convertToUserRolesSchema(roles) }
}
