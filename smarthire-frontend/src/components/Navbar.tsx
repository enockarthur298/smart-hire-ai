// components/Navbar.tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { name: 'Dashboard', href: '/' },
  { name: 'Interview Schedule', href: '/interview' },
  { name: 'Interview Chat', href: '/chat' },
  { name: 'Offer Letters', href: '/offer-letter' },
]

export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="bg-blue-700 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        <h1 className="text-xl font-bold">SmartHireAI</h1>
        <ul className="flex space-x-6">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={`hover:text-yellow-300 transition ${
                  pathname === item.href ? 'underline text-yellow-300' : ''
                }`}
              >
                {item.name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  )
}
