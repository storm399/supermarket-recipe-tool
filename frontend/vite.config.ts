import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: process.env.VITE_API_URL || "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: true,
    port: 4173,
    // Render servert de preview onder onrender.com; Vite blokkeert
    // vreemde hostnames standaard (DNS-rebinding-bescherming).
    allowedHosts: [".onrender.com", "localhost"],
  },
});
