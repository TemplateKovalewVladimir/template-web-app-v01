import VirtTable from '../VirtTable.vue'
import { COLUMN_AUTO_WIDTH } from './constants'

type VirtTableType = InstanceType<typeof VirtTable> | null

type onLoadDataType = (params: IOnLoadDataParams) => Promise<any[]>
type formatterType = ((value: any) => string) | null

type AlignType = 'left' | 'right'
type ColumnType = 'string' | 'number' | 'date' | 'string[]' | 'number[]'
type SortType = 'ASC' | 'DESC' | null
type FilterLogicalOperator = 'and' | 'or'
type FilterContains = 'contains' | 'notcontains'
type FilterEquals = 'eq' | 'ne'
type FilterCompare = 'gt' | 'lt'
type FilterCompareEquals = 'ge' | 'le'
type FilterEmpty = 'null' | 'notnull'
type FilterStringType = FilterContains | FilterEquals | FilterEmpty
type FilterNumberType = FilterEquals | FilterCompare | FilterCompareEquals | FilterEmpty
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
  operator: FilterLogicalOperator
  filters: FilterType[]
}

interface IColumn {
  prop: string
  type: ColumnType

  label: string
  width?: number
  align?: AlignType
  visible?: boolean
  showOverflowTooltip?: boolean

  formatter?: formatterType

  sort?: SortType
  operator?: FilterLogicalOperator
  filters?: FilterType[]
}

class Column implements IColumn {
  prop: string
  type: ColumnType

  label: string
  width: number
  align: AlignType
  visible: boolean
  showOverflowTooltip: boolean

  formatter: formatterType

  sort: SortType
  operator: FilterLogicalOperator
  filters: FilterType[]

  constructor(column: IColumn) {
    this.prop = column.prop
    this.type = column.type

    this.label = column.label
    this.width = column.width || COLUMN_AUTO_WIDTH
    this.align = column.align || 'left'
    this.visible = column.visible || true
    this.showOverflowTooltip = column.showOverflowTooltip || true

    this.formatter = column.formatter || null

    this.sort = column.sort || null
    this.operator = 'or'
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
        filters.push({
          prop: column.prop,
          type: column.type,
          operator: column.operator,
          filters: column.filters
        })

    return filters.length ? filters : undefined
  }
  resetFilters(): void {
    this.forEach((v) => (v.filters = []))
  }
}

export type {
  ColumnType,
  FilterLogicalOperator,
  FilterNumberType,
  FilterStringType,
  FilterType,
  IColumn,
  IColumnSort,
  IFilterNumber,
  IFilterString,
  onLoadDataType,
  SortType,
  VirtTableType
}

export { Column, Columns }
