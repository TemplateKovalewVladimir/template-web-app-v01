export const formatterDate = (value: string) => {
  if (typeof value !== 'string') return value

  const split = value.split('-')
  if (split.length !== 3) return value

  const [year, month, day] = split
  return `${day}-${month}-${year}`
}

export const fixed3Formatter = (value: number) => {
  if (typeof value !== 'number') return value
  return value.toFixed(3)
}

export const formatterArray = (value: any[]) => {
  return value.join(', ')
}
