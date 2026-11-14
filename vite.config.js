import { defineConfig } from 'vite';

export default defineConfig({
    root: 'frontend',

    server: {
        port: 5500,

        proxy: {
            '/auto-site': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            },

            '/manual-site': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            }
        }
    }
});