import { dateBackendToFrontendFormat } from './date'

export const formatterDate = (value: string) => {
  return dateBackendToFrontendFormat(value)
}

export const fixed3Formatter = (value: number) => {
  if (typeof value !== 'number') return value
  return value.toFixed(3)
}

export const formatterArray = (value: any[]) => {
  return value.join(', ')
}
