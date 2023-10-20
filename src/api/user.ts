import request, { Response } from '@/api/utils/request'
import { UserSchema } from './generated'

const baseUrl = '/users'

export function getCurrentUser(): Response<UserSchema> {
  return request({
    url: baseUrl + '/current/',
    method: 'get'
  })
}

export function getUser(userId: number): Response<UserSchema> {
  return request({
    url: baseUrl + '/' + userId,
    method: 'get'
  })
}
