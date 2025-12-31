import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try to refresh
      const refreshToken = useAuthStore.getState().refreshToken
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          })
          
          const { access_token, refresh_token } = response.data
          useAuthStore.getState().login(
            useAuthStore.getState().user!,
            access_token,
            refresh_token
          )
          
          // Retry original request
          error.config.headers.Authorization = `Bearer ${access_token}`
          return axios(error.config)
        } catch (refreshError) {
          // Refresh failed, logout
          useAuthStore.getState().logout()
        }
      } else {
        useAuthStore.getState().logout()
      }
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return response.data
  },
  
  register: async (data: { email: string; username: string; password: string; full_name?: string }) => {
    const response = await api.post('/auth/register', data)
    return response.data
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
  
  changePassword: async (currentPassword: string, newPassword: string) => {
    const response = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
    return response.data
  },
}

// Dashboard API
export const dashboardApi = {
  getStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },
  
  getTrafficTimeline: async (hours: number = 24, metric: string = 'bytes') => {
    const response = await api.get(`/dashboard/traffic/timeline?hours=${hours}&metric=${metric}`)
    return response.data
  },
  
  getAnomaliesTimeline: async (hours: number = 24) => {
    const response = await api.get(`/dashboard/anomalies/timeline?hours=${hours}`)
    return response.data
  },
  
  getRecentAnomalies: async (limit: number = 10) => {
    const response = await api.get(`/dashboard/recent-anomalies?limit=${limit}`)
    return response.data
  },
  
  getRecentAlerts: async (limit: number = 10, unacknowledgedOnly: boolean = false) => {
    const response = await api.get(`/dashboard/recent-alerts?limit=${limit}&unacknowledged_only=${unacknowledgedOnly}`)
    return response.data
  },
  
  getRiskDistribution: async () => {
    const response = await api.get('/dashboard/risk-distribution')
    return response.data
  },
  
  getTopThreats: async (limit: number = 5) => {
    const response = await api.get(`/dashboard/top-threats?limit=${limit}`)
    return response.data
  },
}

// Devices API
export const devicesApi = {
  getAll: async (page: number = 1, pageSize: number = 20, status?: string, search?: string) => {
    let url = `/devices?page=${page}&page_size=${pageSize}`
    if (status) url += `&status=${status}`
    if (search) url += `&search=${search}`
    
    const response = await api.get(url)
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await api.get(`/devices/${id}`)
    return response.data
  },
  
  create: async (data: any) => {
    const response = await api.post('/devices', data)
    return response.data
  },
  
  update: async (id: number, data: any) => {
    const response = await api.put(`/devices/${id}`, data)
    return response.data
  },
  
  delete: async (id: number) => {
    await api.delete(`/devices/${id}`)
  },
  
  getStats: async () => {
    const response = await api.get('/devices/stats/summary')
    return response.data
  },
}

// Anomalies API
export const anomaliesApi = {
  getAll: async (params: {
    page?: number
    pageSize?: number
    anomalyType?: string
    severity?: string
    isResolved?: boolean
    startDate?: string
    endDate?: string
  } = {}) => {
    const searchParams = new URLSearchParams()
    if (params.page) searchParams.set('page', String(params.page))
    if (params.pageSize) searchParams.set('page_size', String(params.pageSize))
    if (params.anomalyType) searchParams.set('anomaly_type', params.anomalyType)
    if (params.severity) searchParams.set('severity', params.severity)
    if (params.isResolved !== undefined) searchParams.set('is_resolved', String(params.isResolved))
    if (params.startDate) searchParams.set('start_date', params.startDate)
    if (params.endDate) searchParams.set('end_date', params.endDate)
    
    const response = await api.get(`/anomalies?${searchParams.toString()}`)
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await api.get(`/anomalies/${id}`)
    return response.data
  },
  
  resolve: async (id: number, notes?: string, isFalsePositive: boolean = false) => {
    const response = await api.post(`/anomalies/${id}/resolve?is_false_positive=${isFalsePositive}`, {
      notes,
    })
    return response.data
  },
  
  getStats: async () => {
    const response = await api.get('/anomalies/stats/summary')
    return response.data
  },
}

// Network API
export const networkApi = {
  getTraffic: async (startTime?: string, endTime?: string, interval: string = '1h') => {
    let url = `/network/traffic?interval=${interval}`
    if (startTime) url += `&start_time=${startTime}`
    if (endTime) url += `&end_time=${endTime}`
    
    const response = await api.get(url)
    return response.data
  },
  
  getTrafficSummary: async (hours: number = 24) => {
    const response = await api.get(`/network/traffic/summary?hours=${hours}`)
    return response.data
  },
  
  getTopology: async () => {
    const response = await api.get('/network/topology')
    return response.data
  },
  
  getHealthScore: async () => {
    const response = await api.get('/network/health-score')
    return response.data
  },
  
  getProtocols: async (hours: number = 24) => {
    const response = await api.get(`/network/protocols?hours=${hours}`)
    return response.data
  },
  
  initiateScan: async (scanType: string = 'quick') => {
    const response = await api.post(`/network/scan?scan_type=${scanType}`)
    return response.data
  },
}

// ML API
export const mlApi = {
  predict: async (features: any, modelName: string = 'isolation_forest') => {
    const response = await api.post('/ml/predict', {
      features,
      model_name: modelName,
    })
    return response.data
  },
  
  getModels: async () => {
    const response = await api.get('/ml/models')
    return response.data
  },
  
  getMetrics: async (modelName?: string) => {
    let url = '/ml/metrics'
    if (modelName) url += `?model_name=${modelName}`
    
    const response = await api.get(url)
    return response.data
  },
}

export default api
