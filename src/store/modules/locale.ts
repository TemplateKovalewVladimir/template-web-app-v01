import { defineStore } from 'pinia'
import { store } from '../index'
import ru from 'element-plus/es/locale/lang/ru'
import { useStorage } from '@/hooks/web/useStorage'
import { LocaleDropdownType } from '@/layout/components/LocaleDropdown'

const { getStorage, setStorage } = useStorage()

const elLocaleMap = {
  ru: ru
}
interface LocaleState {
  currentLocale: LocaleDropdownType
  localeMap: LocaleDropdownType[]
}

export const useLocaleStore = defineStore('locales', {
  state: (): LocaleState => {
    return {
      currentLocale: {
        lang: getStorage('lang') || 'ru',
        elLocale: elLocaleMap[getStorage('lang') || 'ru']
      },
      // 多语言
      localeMap: [
        {
          lang: 'ru',
          name: 'Русский'
        }
      ]
    }
  },
  getters: {
    getCurrentLocale(): LocaleDropdownType {
      return this.currentLocale
    },
    getLocaleMap(): LocaleDropdownType[] {
      return this.localeMap
    }
  },
  actions: {
    setCurrentLocale(localeMap: LocaleDropdownType) {
      // this.locale = Object.assign(this.locale, localeMap)
      this.currentLocale.lang = localeMap?.lang
      this.currentLocale.elLocale = elLocaleMap[localeMap?.lang]
      setStorage('lang', localeMap?.lang)
    }
  }
})

export const useLocaleStoreWithOut = () => {
  return useLocaleStore(store)
}
