import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'System Design Reference',
  description: 'Quick reference for system design interviews',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
