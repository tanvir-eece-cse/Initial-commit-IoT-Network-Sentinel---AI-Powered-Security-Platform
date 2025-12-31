import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  MagnifyingGlassIcon,
  PlusIcon,
  FunnelIcon,
} from '@heroicons/react/24/outline'

// Demo data
const devicesData = [
  { id: 1, device_id: 'DEV001', name: 'Smart Thermostat', type: 'Sensor', ip: '192.168.1.10', mac: 'AA:BB:CC:DD:EE:01', status: 'online', risk_score: 0.1 },
  { id: 2, device_id: 'DEV002', name: 'Security Camera', type: 'Camera', ip: '192.168.1.11', mac: 'AA:BB:CC:DD:EE:02', status: 'online', risk_score: 0.2 },
  { id: 3, device_id: 'DEV003', name: 'Smart Lock', type: 'Access Control', ip: '192.168.1.12', mac: 'AA:BB:CC:DD:EE:03', status: 'offline', risk_score: 0.0 },
  { id: 4, device_id: 'DEV004', name: 'Industrial Sensor', type: 'Sensor', ip: '192.168.1.13', mac: 'AA:BB:CC:DD:EE:04', status: 'suspicious', risk_score: 0.8 },
  { id: 5, device_id: 'DEV005', name: 'Smart Light', type: 'Actuator', ip: '192.168.1.14', mac: 'AA:BB:CC:DD:EE:05', status: 'online', risk_score: 0.15 },
  { id: 6, device_id: 'DEV006', name: 'Motion Detector', type: 'Sensor', ip: '192.168.1.15', mac: 'AA:BB:CC:DD:EE:06', status: 'online', risk_score: 0.3 },
  { id: 7, device_id: 'DEV007', name: 'HVAC Controller', type: 'Controller', ip: '192.168.1.16', mac: 'AA:BB:CC:DD:EE:07', status: 'online', risk_score: 0.25 },
  { id: 8, device_id: 'DEV008', name: 'Network Switch', type: 'Network', ip: '192.168.1.1', mac: 'AA:BB:CC:DD:EE:08', status: 'online', risk_score: 0.05 },
]

export default function Devices() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('')

  const filteredDevices = devicesData.filter(device => {
    const matchesSearch = device.name.toLowerCase().includes(search.toLowerCase()) ||
                         device.ip.includes(search) ||
                         device.device_id.toLowerCase().includes(search.toLowerCase())
    const matchesStatus = !statusFilter || device.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500'
      case 'offline': return 'bg-gray-500'
      case 'suspicious': return 'bg-red-500'
      default: return 'bg-gray-500'
    }
  }

  const getRiskColor = (score: number) => {
    if (score >= 0.7) return 'text-red-400'
    if (score >= 0.4) return 'text-yellow-400'
    return 'text-green-400'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Devices</h1>
          <p className="text-slate-400">Manage and monitor IoT devices on your network</p>
        </div>
        <button className="btn btn-primary flex items-center gap-2">
          <PlusIcon className="w-5 h-5" />
          Add Device
        </button>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search devices..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-10"
            />
          </div>
          <div className="flex items-center gap-2">
            <FunnelIcon className="w-5 h-5 text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input w-40"
            >
              <option value="">All Status</option>
              <option value="online">Online</option>
              <option value="offline">Offline</option>
              <option value="suspicious">Suspicious</option>
            </select>
          </div>
        </div>
      </div>

      {/* Devices Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredDevices.map((device, index) => (
          <motion.div
            key={device.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="card p-4 hover:border-blue-500/50 transition-colors cursor-pointer"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${getStatusColor(device.status)}`} />
                <span className="text-xs text-slate-400 uppercase">{device.status}</span>
              </div>
              <span className={`text-sm font-mono ${getRiskColor(device.risk_score)}`}>
                Risk: {(device.risk_score * 100).toFixed(0)}%
              </span>
            </div>
            
            <h3 className="text-lg font-semibold text-white mb-1">{device.name}</h3>
            <p className="text-sm text-slate-400 mb-4">{device.type}</p>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-500">Device ID</span>
                <span className="text-slate-300 font-mono">{device.device_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">IP Address</span>
                <span className="text-slate-300 font-mono">{device.ip}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">MAC</span>
                <span className="text-slate-300 font-mono text-xs">{device.mac}</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {filteredDevices.length === 0 && (
        <div className="text-center py-12">
          <p className="text-slate-400">No devices found matching your criteria</p>
        </div>
      )}
    </div>
  )
}
