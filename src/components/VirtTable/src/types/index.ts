import VirtTable from '../VirtTable.vue'
import { COLUMN_AUTO_WIDTH } from './constants'

type VirtTableType = InstanceType<typeof VirtTable> | null

type onLoadDataType = (params: IOnLoadDataParams) => Promise<any[]>

type ColumnType = 'string' | 'number' | 'date'
type SortType = 'ASC' | 'DESC' | null
type FilterContains = 'contains' | 'notcontains'
type FilterEquals = 'eq' | 'ne'
type FilterEmpty = 'null' | 'notnull'
type FilterStringType = FilterContains | FilterEquals | FilterEmpty
type FilterNumberType = FilterEquals | FilterEmpty
type FilterType = IFilterString | IFilterNumber

interface IOnLoadDataParams {
  page: number
  size: number
  sort?: IColumnSort
  filters?: IFilters[]
}

interface IColumnSort {
  prop: string
  sort: SortType
}

interface IFilterString {
  type: FilterStringType
  value: string
}

interface IFilterNumber {
  type: FilterNumberType
  value: number
}

interface IFilters {
  prop: string
  type: ColumnType
  filters: FilterType[]
}

interface IColumn {
  prop: string
  type: ColumnType

  label: string
  visible?: boolean
  width?: number
  showOverflowTooltip?: boolean

  sort?: SortType
  filters?: FilterType[]
}

class Column implements IColumn {
  prop: string
  type: ColumnType

  label: string
  visible: boolean
  width: number
  showOverflowTooltip: boolean

  sort: SortType
  filters: FilterType[]

  constructor(column: IColumn) {
    this.prop = column.prop
    this.type = column.type

    this.label = column.label
    this.visible = column.visible || true
    this.width = column.width || COLUMN_AUTO_WIDTH
    this.showOverflowTooltip = column.showOverflowTooltip || true

    this.sort = column.sort || null
    this.filters = column.filters || []
  }
}

class Columns extends Array<Column> {
  constructor(...columns: IColumn[]) {
    super(...columns.map((v) => new Column(v)))
  }

  visibleAll(): void {
    this.forEach((v) => (v.visible = true))
  }

  resetSort(): void {
    this.forEach((v) => (v.sort = null))
  }
  getSort(): IColumnSort | undefined {
    const column = this.find((v) => v.sort !== null)
    if (column) return { prop: column.prop, sort: column.sort }
  }

  getFilters(): IFilters[] | undefined {
    const filters: IFilters[] = []

    for (const column of this)
      if (column.filters.length > 0)
        filters.push({ prop: column.prop, type: column.type, filters: column.filters })

    return filters.length ? filters : undefined
  }
  resetFilters(): void {
    this.forEach((v) => (v.filters = []))
  }
}

export type {
  VirtTableType,
  onLoadDataType,
  IColumn,
  IColumnSort,
  SortType,
  IFilterString,
  IFilterNumber,
  FilterStringType,
  FilterNumberType,
  FilterType
}

export { Column, Columns }
