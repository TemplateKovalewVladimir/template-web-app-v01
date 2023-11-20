import Vue from '@vitejs/plugin-vue'
import VueJsx from '@vitejs/plugin-vue-jsx'
import path from 'path'
import UnoCSS from 'unocss/vite'
import { defineConfig } from 'vite'
import Checker from 'vite-plugin-checker'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'

// https://vitejs.dev/config/
export default defineConfig({
  envPrefix: 'APP',
  server: {
    host: '0.0.0.0',
    port: 8100,
    strictPort: true
  },
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[hash:16].js`,
        chunkFileNames: `assets/[hash:16].js`,
        assetFileNames: `assets/[hash:16].[ext]`
      }
    }
  },
  plugins: [
    Vue({
      script: {
        defineModel: true
      }
    }),
    createSvgIconsPlugin({
      iconDirs: [path.resolve(__dirname, 'src/assets/svgs')],
      symbolId: 'icon-[dir]/[name]'
    }),
    VueJsx(),
    UnoCSS(),
    Checker({
      vueTsc: true,
      eslint: {
        lintCommand: 'eslint "./**"'
      }
    })
  ],
  css: {
    preprocessorOptions: {
      less: {
        additionalData: '@import "./src/styles/variables.module.less";',
        javascriptEnabled: true
      }
    }
  },
  resolve: {
    alias: [{ find: '@', replacement: path.resolve(__dirname, './src') }]
  }
})
