/**
 * @param str - строка, которую нужно преобразовать в формат с символом подчеркивания
 * @returns строка с символом подчеркивания
 */
export const humpToUnderline = (str: string): string => {
  return str.replace(/([A-Z])/g, '-$1').toLowerCase()
}

/**
 * Функция setCssVar устанавливает значение CSS-переменной на указанном DOM-элементе.
 * @param prop - Название CSS-переменной.
 * @param val - Значение, которое нужно присвоить CSS-переменной.
 * @param dom - DOM-элемент, на котором нужно установить CSS-переменную. По умолчанию, root-элемент (document.documentElement).
 */
export const setCssVar = (prop, val, dom = document.documentElement) => {
  dom.style.setProperty(prop, val)
}

/**
 * Функция для поиска индекса объекта в массиве
 * @param {Array} ary Массив, в котором ищем
 * @param {Function} fn Функция для проверки
 * @returns {Number} Индекс найденного объекта или -1, если объект не найден
 */
export const findIndex = <T = Recordable>(ary: Array<T>, fn: Fn): number => {
  if (ary.findIndex) {
    return ary.findIndex(fn)
  }
  let index = -1
  ary.some((item: T, i: number, ary: Array<T>) => {
    const ret: T = fn(item, i, ary)
    if (ret) {
      index = i
      return ret
    }
  })
  return index
}

/**
 * Удаляет все пробелы в начале и конце строки.
 *
 * @param str - Исходная строка, которую нужно обрезать.
 * @returns Обрезанная строка без пробелов в начале и конце.
 */
export const trim = (str: string) => {
  return str.replace(/(^\s*)|(\s*$)/g, '')
}
