import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { FlatCompat } from '@eslint/eslintrc'
import js from '@eslint/js'
import simpleImportSort from 'eslint-plugin-simple-import-sort'
import parser from 'vue-eslint-parser'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all
})

export default [
  {
    ignores: [
      'node_modules/*',
      'dist*',
      'README.md',
      '**/Dockerfile',
      '**/nginx.conf',
      'public/*',
      'index.html',
      'src/assets/*',
      '**/*.bak',
      '**/*.less',
      '**/*.css',
      '**/*.json'
    ]
  },
  ...compat.extends(
    'plugin:vue/vue3-recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier',
    'plugin:prettier/recommended'
  ),
  {
    plugins: {
      'simple-import-sort': simpleImportSort
    },

    languageOptions: {
      parser: parser,
      ecmaVersion: 2020,

      sourceType: 'module',

      parserOptions: {
        parser: '@typescript-eslint/parser',
        jsxPragma: 'React',

        ecmaFeatures: {
          jsx: true
        }
      }
    },

    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      'simple-import-sort/imports': 'error',
      'simple-import-sort/exports': 'error'
    }
  }
]
