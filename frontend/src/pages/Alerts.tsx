import { useState } from 'react'
import { motion } from 'framer-motion'
import { BellIcon, CheckIcon } from '@heroicons/react/24/outline'

// Demo data
const alertsData = [
  { id: 1, title: 'Critical DDoS Attack', message: 'High volume traffic detected from 192.168.1.105', severity: 'critical', is_acknowledged: false, created_at: '2024-12-31T10:30:00Z' },
  { id: 2, title: 'Port Scan Detected', message: 'Sequential port scanning from 10.0.0.45', severity: 'high', is_acknowledged: false, created_at: '2024-12-31T10:15:00Z' },
  { id: 3, title: 'Malware Communication', message: 'Device 192.168.1.89 attempting to contact known C2 server', severity: 'high', is_acknowledged: false, created_at: '2024-12-31T09:45:00Z' },
  { id: 4, title: 'Unusual Protocol', message: 'Non-standard protocol usage detected on port 8443', severity: 'medium', is_acknowledged: true, created_at: '2024-12-31T09:00:00Z' },
  { id: 5, title: 'Failed Login Attempts', message: 'Multiple failed authentication attempts on smart lock', severity: 'medium', is_acknowledged: true, created_at: '2024-12-31T08:30:00Z' },
  { id: 6, title: 'Bandwidth Spike', message: 'Unusual bandwidth consumption from industrial sensor', severity: 'low', is_acknowledged: false, created_at: '2024-12-31T08:00:00Z' },
]

const severityColors: Record<string, string> = {
  critical: 'border-l-red-600 bg-red-500/10',
  high: 'border-l-orange-500 bg-orange-500/10',
  medium: 'border-l-yellow-500 bg-yellow-500/10',
  low: 'border-l-blue-500 bg-blue-500/10',
}

export default function Alerts() {
  const [alerts, setAlerts] = useState(alertsData)
  const [filter, setFilter] = useState<'all' | 'unacknowledged'>('all')

  const filteredAlerts = filter === 'all' 
    ? alerts 
    : alerts.filter(a => !a.is_acknowledged)

  const acknowledgeAlert = (id: number) => {
    setAlerts(alerts.map(a => 
      a.id === id ? { ...a, is_acknowledged: true } : a
    ))
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleString()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Alerts</h1>
          <p className="text-slate-400">Security alerts and notifications</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
          >
            All ({alerts.length})
          </button>
          <button
            onClick={() => setFilter('unacknowledged')}
            className={`btn ${filter === 'unacknowledged' ? 'btn-primary' : 'btn-secondary'}`}
          >
            Unacknowledged ({alerts.filter(a => !a.is_acknowledged).length})
          </button>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-3">
        {filteredAlerts.map((alert, index) => (
          <motion.div
            key={alert.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className={`card border-l-4 ${severityColors[alert.severity]} ${
              alert.is_acknowledged ? 'opacity-60' : ''
            }`}
          >
            <div className="p-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-start gap-3">
                  <div className={`p-2 rounded-lg ${
                    alert.severity === 'critical' ? 'bg-red-500/20 text-red-400' :
                    alert.severity === 'high' ? 'bg-orange-500/20 text-orange-400' :
                    alert.severity === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>
                    <BellIcon className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-semibold text-white">{alert.title}</h3>
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                        alert.severity === 'critical' ? 'bg-red-600 text-white' :
                        alert.severity === 'high' ? 'bg-orange-500 text-white' :
                        alert.severity === 'medium' ? 'bg-yellow-500 text-black' :
                        'bg-blue-500 text-white'
                      }`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      {alert.is_acknowledged && (
                        <span className="flex items-center gap-1 text-green-400 text-xs">
                          <CheckIcon className="w-3 h-3" />
                          Acknowledged
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-slate-400 mb-2">{alert.message}</p>
                    <p className="text-xs text-slate-500">{formatDate(alert.created_at)}</p>
                  </div>
                </div>
                {!alert.is_acknowledged && (
                  <button
                    onClick={() => acknowledgeAlert(alert.id)}
                    className="btn btn-secondary text-sm flex items-center gap-1"
                  >
                    <CheckIcon className="w-4 h-4" />
                    Acknowledge
                  </button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {filteredAlerts.length === 0 && (
        <div className="text-center py-12">
          <BellIcon className="w-12 h-12 mx-auto text-slate-600 mb-4" />
          <p className="text-slate-400">No alerts to display</p>
        </div>
      )}
    </div>
  )
}
