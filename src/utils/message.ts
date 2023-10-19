import { ElNotification } from 'element-plus'

type MessageType = 'success' | 'error'

export function Message(title: string, message: string, type: MessageType = 'success') {
  if (type === 'success') ElNotification.closeAll()
  let duration = 1000
  switch (type) {
    case 'success':
      duration *= 5
      break
    case 'error':
      console.warn(message)
      duration *= 30
      break
  }
  ElNotification({
    title,
    message,
    type,
    duration,
    showClose: true
  })
}
