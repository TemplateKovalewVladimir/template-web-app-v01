import Vue from '@vitejs/plugin-vue'
import VueJsx from '@vitejs/plugin-vue-jsx'
import { defineConfig } from 'vite'
import path from 'path'
import UnoCSS from 'unocss/vite'
import Checker from 'vite-plugin-checker'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 5000,
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
    VueJsx(),
    UnoCSS(),
    Checker({
      vueTsc: true,
      eslint: {
        lintCommand: 'eslint "./**"'
      }
    })
  ],
  resolve: {
    alias: [{ find: '@', replacement: path.resolve(__dirname, './src') }]
  }
})
