import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ShieldCheckIcon, EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline'
import toast from 'react-hot-toast'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../services/api'

export default function Login() {
  const [isLogin, setIsLogin] = useState(true)
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    fullName: '',
  })
  
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (isLogin) {
        // Login
        const tokenData = await authApi.login(formData.email, formData.password)
        const userData = await authApi.getCurrentUser()
        
        login(userData, tokenData.access_token, tokenData.refresh_token)
        toast.success('Welcome back!')
        navigate('/')
      } else {
        // Register
        await authApi.register({
          email: formData.email,
          username: formData.username,
          password: formData.password,
          full_name: formData.fullName,
        })
        
        toast.success('Account created! Please login.')
        setIsLogin(true)
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  // Demo login handler
  const handleDemoLogin = () => {
    // For demo purposes, create a mock user
    const mockUser = {
      id: 1,
      email: 'demo@sentinel.io',
      username: 'demo_user',
      full_name: 'Demo User',
      role: 'admin',
      is_superuser: true,
    }
    
    login(mockUser, 'demo-token', 'demo-refresh-token')
    toast.success('Logged in with demo account!')
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-600/20 mb-4">
            <ShieldCheckIcon className="w-10 h-10 text-blue-500" />
          </div>
          <h1 className="text-3xl font-bold text-white">IoT Network Sentinel</h1>
          <p className="text-slate-400 mt-2">AI-Powered Network Security Platform</p>
        </div>

        {/* Form Card */}
        <div className="card">
          <div className="card-body">
            {/* Toggle */}
            <div className="flex rounded-lg bg-slate-700 p-1 mb-6">
              <button
                onClick={() => setIsLogin(true)}
                className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${
                  isLogin ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                Login
              </button>
              <button
                onClick={() => setIsLogin(false)}
                className={`flex-1 py-2 text-sm font-medium rounded-md transition-colors ${
                  !isLogin ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                Register
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {!isLogin && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      value={formData.fullName}
                      onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                      className="input"
                      placeholder="Enter your full name"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Username
                    </label>
                    <input
                      type="text"
                      value={formData.username}
                      onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                      className="input"
                      placeholder="Choose a username"
                      required={!isLogin}
                    />
                  </div>
                </>
              )}

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Email
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="input"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="input pr-10"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="w-5 h-5" />
                    ) : (
                      <EyeIcon className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="btn btn-primary w-full"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                        fill="none"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    Processing...
                  </span>
                ) : isLogin ? (
                  'Login'
                ) : (
                  'Create Account'
                )}
              </button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-700" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="bg-slate-800 px-4 text-slate-400">or</span>
              </div>
            </div>

            {/* Demo Login */}
            <button
              onClick={handleDemoLogin}
              className="btn btn-secondary w-full"
            >
              Try Demo Account
            </button>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-slate-500 mt-6">
          Built by{' '}
          <a
            href="https://github.com/tanvir-eece-cse"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:text-blue-300"
          >
            Md. Tanvir Hossain
          </a>
        </p>
      </motion.div>
    </div>
  )
}
