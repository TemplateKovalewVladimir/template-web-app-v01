import { FilterNumberType, FilterStringType } from '.'

export const COLUMN_MIN_WIDTH = 50
export const COLUMN_AUTO_WIDTH = -1

export const FILTER_TYPE_LABEL: Record<FilterStringType | FilterNumberType, string> = {
  contains: 'Содержит',
  notcontains: 'Не содержит',
  eq: 'Равно',
  ne: 'Не равно',
  gt: 'Больше',
  lt: 'Меньше',
  ge: 'Больше или равно',
  le: 'Меньше или равно',
  null: 'Пусто',
  notnull: 'Не пусто'
}
