import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      '5424691d992044543de90a6dcf790260.serveo.net',
      'localhost',
      '127.0.0.1'
    ]
  }
})
