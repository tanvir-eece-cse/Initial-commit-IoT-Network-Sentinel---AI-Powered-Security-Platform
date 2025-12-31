import { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { useAuthStore } from '../store/authStore'

export default function Settings() {
  const { user, updateUser } = useAuthStore()
  const [profile, setProfile] = useState({
    fullName: user?.full_name || '',
    email: user?.email || '',
  })
  const [passwords, setPasswords] = useState({
    current: '',
    new: '',
    confirm: '',
  })
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    critical: true,
    high: true,
    medium: false,
    low: false,
  })

  const handleProfileSave = () => {
    updateUser({ full_name: profile.fullName })
    toast.success('Profile updated successfully')
  }

  const handlePasswordChange = () => {
    if (passwords.new !== passwords.confirm) {
      toast.error('Passwords do not match')
      return
    }
    if (passwords.new.length < 8) {
      toast.error('Password must be at least 8 characters')
      return
    }
    toast.success('Password changed successfully')
    setPasswords({ current: '', new: '', confirm: '' })
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-slate-400">Manage your account and preferences</p>
      </div>

      {/* Profile Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-white">Profile Settings</h3>
        </div>
        <div className="card-body space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={profile.fullName}
              onChange={(e) => setProfile({ ...profile, fullName: e.target.value })}
              className="input"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Email
            </label>
            <input
              type="email"
              value={profile.email}
              onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              className="input"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Role
            </label>
            <input
              type="text"
              value={user?.role || 'User'}
              disabled
              className="input bg-slate-700/50 cursor-not-allowed"
            />
          </div>
          <div className="pt-4">
            <button onClick={handleProfileSave} className="btn btn-primary">
              Save Changes
            </button>
          </div>
        </div>
      </motion.div>

      {/* Password Change */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-white">Change Password</h3>
        </div>
        <div className="card-body space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Current Password
            </label>
            <input
              type="password"
              value={passwords.current}
              onChange={(e) => setPasswords({ ...passwords, current: e.target.value })}
              className="input"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              New Password
            </label>
            <input
              type="password"
              value={passwords.new}
              onChange={(e) => setPasswords({ ...passwords, new: e.target.value })}
              className="input"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Confirm New Password
            </label>
            <input
              type="password"
              value={passwords.confirm}
              onChange={(e) => setPasswords({ ...passwords, confirm: e.target.value })}
              className="input"
            />
          </div>
          <div className="pt-4">
            <button onClick={handlePasswordChange} className="btn btn-primary">
              Change Password
            </button>
          </div>
        </div>
      </motion.div>

      {/* Notification Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-white">Notification Preferences</h3>
        </div>
        <div className="card-body space-y-4">
          <div className="flex items-center justify-between py-2">
            <div>
              <p className="font-medium text-white">Email Notifications</p>
              <p className="text-sm text-slate-400">Receive alerts via email</p>
            </div>
            <Toggle
              enabled={notifications.email}
              onChange={(val) => setNotifications({ ...notifications, email: val })}
            />
          </div>
          <div className="flex items-center justify-between py-2">
            <div>
              <p className="font-medium text-white">Push Notifications</p>
              <p className="text-sm text-slate-400">Browser push notifications</p>
            </div>
            <Toggle
              enabled={notifications.push}
              onChange={(val) => setNotifications({ ...notifications, push: val })}
            />
          </div>
          <hr className="border-slate-700" />
          <p className="text-sm font-medium text-slate-400 uppercase">Alert Severity</p>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-slate-300">Critical Alerts</span>
              <Toggle
                enabled={notifications.critical}
                onChange={(val) => setNotifications({ ...notifications, critical: val })}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-300">High Priority Alerts</span>
              <Toggle
                enabled={notifications.high}
                onChange={(val) => setNotifications({ ...notifications, high: val })}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-300">Medium Priority Alerts</span>
              <Toggle
                enabled={notifications.medium}
                onChange={(val) => setNotifications({ ...notifications, medium: val })}
              />
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-300">Low Priority Alerts</span>
              <Toggle
                enabled={notifications.low}
                onChange={(val) => setNotifications({ ...notifications, low: val })}
              />
            </div>
          </div>
        </div>
      </motion.div>

      {/* About */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-white">About</h3>
        </div>
        <div className="card-body">
          <div className="space-y-2 text-sm">
            <p className="text-slate-400">
              <span className="text-slate-300">Version:</span> 1.0.0
            </p>
            <p className="text-slate-400">
              <span className="text-slate-300">Author:</span> Md. Tanvir Hossain
            </p>
            <p className="text-slate-400">
              <span className="text-slate-300">GitHub:</span>{' '}
              <a
                href="https://github.com/tanvir-eece-cse"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300"
              >
                github.com/tanvir-eece-cse
              </a>
            </p>
            <p className="text-slate-400">
              <span className="text-slate-300">LinkedIn:</span>{' '}
              <a
                href="https://www.linkedin.com/in/tanvir-eece/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300"
              >
                linkedin.com/in/tanvir-eece
              </a>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

function Toggle({
  enabled,
  onChange,
}: {
  enabled: boolean
  onChange: (val: boolean) => void
}) {
  return (
    <button
      onClick={() => onChange(!enabled)}
      className={`
        relative inline-flex h-6 w-11 items-center rounded-full transition-colors
        ${enabled ? 'bg-blue-600' : 'bg-slate-600'}
      `}
    >
      <span
        className={`
          inline-block h-4 w-4 transform rounded-full bg-white transition-transform
          ${enabled ? 'translate-x-6' : 'translate-x-1'}
        `}
      />
    </button>
  )
}
