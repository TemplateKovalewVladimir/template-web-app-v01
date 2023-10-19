import request, { Response } from '@/api/utils/request'
import { HTTPBasicCredentials, TokenSchema } from '@/api/generated'

const baseUrl = '/login'

export function getTokenBasic(creds: HTTPBasicCredentials): Response<TokenSchema> {
  return request({
    url: baseUrl + '/token/basic/',
    method: 'post',
    data: creds
  })
}

export function getTokenSSO(): Response<TokenSchema> {
  return request({
    url: baseUrl + '/token/sso/',
    method: 'get',
    withCredentials: true
  })
}
