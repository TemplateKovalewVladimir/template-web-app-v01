import Vue from '@vitejs/plugin-vue'
import VueJsx from '@vitejs/plugin-vue-jsx'
import path from 'path'
import { defineConfig } from 'vite'
import Checker from 'vite-plugin-checker'

// https://vitejs.dev/config/
export default defineConfig({
  envPrefix: 'APP',
  server: {
    host: '0.0.0.0',
    port: 8550,
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
    Checker({
      vueTsc: true,
      eslint: {
        useFlatConfig: true,
        lintCommand: 'eslint "./**"'
      }
    })
  ],
  resolve: {
    alias: [{ find: '@', replacement: path.resolve(__dirname, './src') }]
  }
})
