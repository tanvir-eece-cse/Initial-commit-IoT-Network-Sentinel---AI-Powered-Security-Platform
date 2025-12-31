import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  HomeIcon,
  DeviceTabletIcon,
  ExclamationTriangleIcon,
  GlobeAltIcon,
  BellIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline'
import { useAuthStore } from '../store/authStore'

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Devices', href: '/devices', icon: DeviceTabletIcon },
  { name: 'Anomalies', href: '/anomalies', icon: ExclamationTriangleIcon },
  { name: 'Network', href: '/network', icon: GlobeAltIcon },
  { name: 'Alerts', href: '/alerts', icon: BellIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Mobile sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-40 bg-black/50 lg:hidden"
              onClick={() => setSidebarOpen(false)}
            />
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              exit={{ x: -300 }}
              className="fixed inset-y-0 left-0 z-50 w-72 bg-slate-800 lg:hidden"
            >
              <Sidebar currentPath={location.pathname} onLogout={handleLogout} user={user} />
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-72 lg:flex-col">
        <Sidebar currentPath={location.pathname} onLogout={handleLogout} user={user} />
      </div>

      {/* Main content */}
      <div className="lg:pl-72">
        {/* Top bar */}
        <div className="sticky top-0 z-30 flex h-16 items-center gap-x-4 border-b border-slate-700 bg-slate-800/95 backdrop-blur px-4 sm:px-6 lg:px-8">
          <button
            type="button"
            className="lg:hidden -m-2.5 p-2.5 text-slate-400 hover:text-white"
            onClick={() => setSidebarOpen(true)}
          >
            <Bars3Icon className="h-6 w-6" />
          </button>

          <div className="flex flex-1 justify-end gap-x-4">
            {/* Notifications */}
            <button className="relative p-2 text-slate-400 hover:text-white">
              <BellIcon className="h-6 w-6" />
              <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500" />
            </button>

            {/* User info */}
            <div className="flex items-center gap-x-3">
              <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center">
                <span className="text-sm font-medium text-white">
                  {user?.username?.charAt(0).toUpperCase() || 'U'}
                </span>
              </div>
              <div className="hidden sm:block">
                <p className="text-sm font-medium text-white">{user?.full_name || user?.username}</p>
                <p className="text-xs text-slate-400">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  )
}

function Sidebar({
  currentPath,
  onLogout,
  user,
}: {
  currentPath: string
  onLogout: () => void
  user: any
}) {
  return (
    <div className="flex h-full flex-col bg-slate-800 border-r border-slate-700">
      {/* Logo */}
      <div className="flex h-16 items-center gap-x-3 px-6 border-b border-slate-700">
        <ShieldCheckIcon className="h-8 w-8 text-blue-500" />
        <div>
          <h1 className="text-lg font-bold text-white">IoT Sentinel</h1>
          <p className="text-xs text-slate-400">Network Security</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4">
        <ul className="space-y-1">
          {navigation.map((item) => {
            const isActive = currentPath === item.href
            return (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={`
                    flex items-center gap-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors
                    ${isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                    }
                  `}
                >
                  <item.icon className="h-5 w-5" />
                  {item.name}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      {/* User section */}
      <div className="border-t border-slate-700 p-4">
        <div className="flex items-center gap-x-3 px-4 py-3">
          <div className="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center">
            <span className="text-sm font-medium text-white">
              {user?.username?.charAt(0).toUpperCase() || 'U'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">
              {user?.full_name || user?.username}
            </p>
            <p className="text-xs text-slate-400 truncate">{user?.role}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="flex w-full items-center gap-x-3 px-4 py-3 rounded-lg text-sm font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition-colors"
        >
          <ArrowRightOnRectangleIcon className="h-5 w-5" />
          Logout
        </button>
      </div>
    </div>
  )
}
