import VirtTable from '../VirtTable.vue'
import { COLUMN_AUTO_WIDTH } from './constants'

export type TypeVirtTable = InstanceType<typeof VirtTable> | null

// prop = isRequired('prop'),
// type = isRequired('type'),
// label = isRequired('label'),
// width = undefined,
// overflow = true,
// visible = true,
// fixed = false,
// align = 'left',
// headerAlign = 'left',
// formatter = null,
// menu = true,
// sort = '',
// filters = [],
// printNoWrap = false,
// unique = undefined,

export type onLoadDataType = (current: number, size: number, sort?: IColumnSort) => Promise<any[]>

export type SortType = 'ASC' | 'DESC' | null
type ColumnType = 'string' | 'number' | 'date'

export interface IColumnSort {
  prop: string
  sort: SortType
}

export interface IColumn {
  prop: string
  type: ColumnType

  label: string
  visible?: boolean
  width?: number
  showOverflowTooltip?: boolean

  sort?: SortType
}

export class Column implements IColumn {
  prop: string
  type: ColumnType

  label: string
  visible: boolean
  width: number
  showOverflowTooltip: boolean

  sort: SortType

  constructor(column: IColumn) {
    this.prop = column.prop
    this.type = column.type

    this.label = column.label
    this.visible = column.visible || true
    this.width = column.width || COLUMN_AUTO_WIDTH
    this.showOverflowTooltip = column.showOverflowTooltip || true

    this.sort = column.sort || null
  }
}

export class Columns extends Array<Column> {
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
}
