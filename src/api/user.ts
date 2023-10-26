import request, { Response } from '@/api/utils/request'
import { UserCreateSchemaBackend, UserSchemaBackend, UserUpdateSchemaBackend } from './generated'

const baseUrl = '/users'

export function getCurrentUser(): Response<UserSchemaBackend> {
  return request({
    url: baseUrl + '/current/',
    method: 'get'
  })
}

export function getUser(userId: number): Response<UserSchemaBackend> {
  return request({
    url: baseUrl + '/' + userId,
    method: 'get'
  })
}

export function getUsers(): Response<UserSchemaBackend[]> {
  return request({
    url: baseUrl + '/',
    method: 'get'
  })
}

export function createUser(user: UserCreateSchemaBackend): Response<UserSchemaBackend> {
  return request({
    url: baseUrl + '/',
    method: 'post',
    data: user
  })
}

export function updateUser(
  userId: number,
  user: UserUpdateSchemaBackend
): Response<UserSchemaBackend> {
  return request({
    url: baseUrl + '/' + userId,
    method: 'put',
    data: user
  })
}

export function deleteUser(userId: number): Response<UserSchemaBackend> {
  return request({
    url: baseUrl + '/' + userId,
    method: 'delete'
  })
}
