import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue2 from '@vitejs/plugin-vue2'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue2(),
  ],
  resolve: {
    // TODO: this line should be removed once all imports to .vue files include the .vue extension
    //   like `import App from './App';` on "src/main.js"
    extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // https://github.com/vitejs/vite/discussions/4158
      vue: 'vue/dist/vue.esm.js',
    },
  },
});
