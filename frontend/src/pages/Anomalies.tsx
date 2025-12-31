import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline'

// Demo data
const anomaliesData = [
  { id: 1, type: 'ddos_attack', severity: 'critical', title: 'DDoS Attack Detected', source_ip: '192.168.1.105', dest_ip: '192.168.1.1', confidence: 0.95, is_resolved: false, detected_at: '2024-12-31T10:30:00Z' },
  { id: 2, type: 'port_scan', severity: 'high', title: 'Port Scanning Activity', source_ip: '10.0.0.45', dest_ip: '192.168.1.0/24', confidence: 0.88, is_resolved: false, detected_at: '2024-12-31T10:15:00Z' },
  { id: 3, type: 'malware', severity: 'high', title: 'Malware Communication', source_ip: '192.168.1.89', dest_ip: '203.0.113.50', confidence: 0.92, is_resolved: false, detected_at: '2024-12-31T09:45:00Z' },
  { id: 4, type: 'protocol_anomaly', severity: 'medium', title: 'Unusual Protocol Usage', source_ip: '10.0.0.12', dest_ip: '192.168.1.1', confidence: 0.75, is_resolved: true, detected_at: '2024-12-31T09:00:00Z' },
  { id: 5, type: 'unauthorized_access', severity: 'medium', title: 'Failed Login Attempts', source_ip: '192.168.1.200', dest_ip: '192.168.1.10', confidence: 0.82, is_resolved: true, detected_at: '2024-12-31T08:30:00Z' },
  { id: 6, type: 'data_exfiltration', severity: 'high', title: 'Large Data Transfer', source_ip: '192.168.1.50', dest_ip: '198.51.100.25', confidence: 0.78, is_resolved: false, detected_at: '2024-12-31T08:00:00Z' },
  { id: 7, type: 'botnet', severity: 'critical', title: 'Botnet Activity', source_ip: '192.168.1.75', dest_ip: '203.0.113.100', confidence: 0.91, is_resolved: true, detected_at: '2024-12-30T22:00:00Z' },
]

const severityColors: Record<string, string> = {
  critical: 'bg-red-600 text-white',
  high: 'bg-orange-500 text-white',
  medium: 'bg-yellow-500 text-black',
  low: 'bg-blue-500 text-white',
}

const typeLabels: Record<string, string> = {
  ddos_attack: 'DDoS Attack',
  port_scan: 'Port Scan',
  malware: 'Malware',
  botnet: 'Botnet',
  data_exfiltration: 'Data Exfiltration',
  unauthorized_access: 'Unauthorized Access',
  protocol_anomaly: 'Protocol Anomaly',
}

export default function Anomalies() {
  const [search, setSearch] = useState('')
  const [severityFilter, setSeverityFilter] = useState('')
  const [resolvedFilter, setResolvedFilter] = useState<string>('')

  const filteredAnomalies = anomaliesData.filter(anomaly => {
    const matchesSearch = anomaly.title.toLowerCase().includes(search.toLowerCase()) ||
                         anomaly.source_ip.includes(search)
    const matchesSeverity = !severityFilter || anomaly.severity === severityFilter
    const matchesResolved = resolvedFilter === '' || 
                           (resolvedFilter === 'resolved' && anomaly.is_resolved) ||
                           (resolvedFilter === 'unresolved' && !anomaly.is_resolved)
    return matchesSearch && matchesSeverity && matchesResolved
  })

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return date.toLocaleString()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Anomalies</h1>
        <p className="text-slate-400">View and manage detected network anomalies</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="card p-4 text-center">
          <p className="text-3xl font-bold text-white">{anomaliesData.length}</p>
          <p className="text-sm text-slate-400">Total</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-3xl font-bold text-red-400">
            {anomaliesData.filter(a => a.severity === 'critical').length}
          </p>
          <p className="text-sm text-slate-400">Critical</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-3xl font-bold text-yellow-400">
            {anomaliesData.filter(a => !a.is_resolved).length}
          </p>
          <p className="text-sm text-slate-400">Unresolved</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-3xl font-bold text-green-400">
            {anomaliesData.filter(a => a.is_resolved).length}
          </p>
          <p className="text-sm text-slate-400">Resolved</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search anomalies..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-10"
            />
          </div>
          <div className="flex items-center gap-2">
            <FunnelIcon className="w-5 h-5 text-slate-400" />
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              className="input w-36"
            >
              <option value="">All Severity</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
            <select
              value={resolvedFilter}
              onChange={(e) => setResolvedFilter(e.target.value)}
              className="input w-36"
            >
              <option value="">All Status</option>
              <option value="resolved">Resolved</option>
              <option value="unresolved">Unresolved</option>
            </select>
          </div>
        </div>
      </div>

      {/* Anomalies List */}
      <div className="space-y-4">
        {filteredAnomalies.map((anomaly, index) => (
          <motion.div
            key={anomaly.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.05 }}
            className="card p-4 hover:border-blue-500/50 transition-colors"
          >
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${severityColors[anomaly.severity]}`}>
                    {anomaly.severity.toUpperCase()}
                  </span>
                  <span className="text-sm text-slate-400">
                    {typeLabels[anomaly.type] || anomaly.type}
                  </span>
                  {anomaly.is_resolved ? (
                    <span className="flex items-center gap-1 text-green-400 text-sm">
                      <CheckCircleIcon className="w-4 h-4" />
                      Resolved
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-red-400 text-sm">
                      <XCircleIcon className="w-4 h-4" />
                      Active
                    </span>
                  )}
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">{anomaly.title}</h3>
                <div className="flex flex-wrap gap-4 text-sm">
                  <span className="text-slate-400">
                    Source: <span className="font-mono text-slate-300">{anomaly.source_ip}</span>
                  </span>
                  <span className="text-slate-400">
                    Destination: <span className="font-mono text-slate-300">{anomaly.dest_ip}</span>
                  </span>
                  <span className="text-slate-400">
                    Confidence: <span className="text-blue-400">{(anomaly.confidence * 100).toFixed(0)}%</span>
                  </span>
                  <span className="text-slate-400">
                    Detected: <span className="text-slate-300">{formatDate(anomaly.detected_at)}</span>
                  </span>
                </div>
              </div>
              <div className="flex gap-2">
                <button className="btn btn-secondary text-sm">View Details</button>
                {!anomaly.is_resolved && (
                  <button className="btn btn-primary text-sm">Resolve</button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {filteredAnomalies.length === 0 && (
        <div className="text-center py-12">
          <p className="text-slate-400">No anomalies found matching your criteria</p>
        </div>
      )}
    </div>
  )
}
