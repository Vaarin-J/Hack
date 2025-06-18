import './globals.css'
import type { ReactNode } from 'react'

export const metadata = {
  title: 'Kalshi Optimizer',
  description: 'Live Kalshi AI betting assistant',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}