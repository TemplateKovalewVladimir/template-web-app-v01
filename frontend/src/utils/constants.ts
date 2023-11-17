const toolHeader = '50px'
const tagsView = '35px'
const appViewPadding = '2 * 20px'
const contentWrapPadding = '2 * 20px'
const contentWrapHeader = '55px'
const contentWrapHeaderButton = '62px'
const contentWrapBorder = '3px'
const tableHeightWrappedInContentWrapInHeader = `calc(100vh - ${toolHeader} - ${tagsView} - ${appViewPadding} - ${contentWrapPadding} - ${contentWrapHeader} - ${contentWrapBorder})`
const tableHeightWrappedInContentWrapInHeaderButton = `calc(100vh - ${toolHeader} - ${tagsView} - ${appViewPadding} - ${contentWrapPadding} - ${contentWrapHeaderButton} - ${contentWrapBorder})`

export { tableHeightWrappedInContentWrapInHeader, tableHeightWrappedInContentWrapInHeaderButton }
