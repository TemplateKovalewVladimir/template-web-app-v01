import { HTTPBasicCredentialsBackend, TokenSchemaBackend } from '@/api/generated'
import request, { Response } from '@/api/utils/request'

const baseUrl = '/login'

export function getTokenBasic(creds: HTTPBasicCredentialsBackend): Response<TokenSchemaBackend> {
  return request({
    url: baseUrl + '/token/basic/',
    method: 'post',
    data: creds
  })
}

export function getTokenSSO(): Response<TokenSchemaBackend> {
  return request({
    url: baseUrl + '/token/sso/',
    method: 'get',
    withCredentials: true
  })
}
