import type { Metadata } from "next";
import { QueryProvider } from "@/lib/query-provider";
import "./globals.css";

export const metadata: Metadata = {
  title: "OptiFerre | Mira en minutos cuánta plata tienes muerta en bodega",
  description:
    "Sube tu Excel y descubre qué productos están quietos, cuáles se van a acabar y cuánto deberías comprar. Para ferreterías, materiales y depósitos.",
  metadataBase: new URL("https://optiferre.app")
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="gradient-bg min-h-screen">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
