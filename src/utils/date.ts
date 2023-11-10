const dateFormatterMonth = new Intl.DateTimeFormat('ru-RU', { month: 'long' })

const getCapitalizedMonth = (month: number): string => {
  const now = new Date()
  const currentYear = now.getFullYear()

  const date = new Date(currentYear, month - 1, 1)
  const textMonth = dateFormatterMonth.format(date)
  const capitalizedTextMonth = textMonth.charAt(0).toUpperCase() + textMonth.slice(1)

  return capitalizedTextMonth
}

const dateToBackendFormat = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

const dateBackendToFrontendFormat = (date: string) => {
  if (typeof date !== 'string') return date

  const split = date.split('-')
  if (split.length !== 3) return date

  const [year, month, day] = split
  return `${day}-${month}-${year}`
}

export { dateBackendToFrontendFormat, dateToBackendFormat, getCapitalizedMonth }
