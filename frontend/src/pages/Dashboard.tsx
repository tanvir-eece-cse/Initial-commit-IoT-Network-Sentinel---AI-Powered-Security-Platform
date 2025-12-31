import { motion } from 'framer-motion'
import {
  DeviceTabletIcon,
  ExclamationTriangleIcon,
  ShieldCheckIcon,
  SignalIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
} from 'recharts'

// Demo data
const statsData = {
  totalDevices: 156,
  onlineDevices: 142,
  offlineDevices: 10,
  suspiciousDevices: 4,
  totalAnomalies: 23,
  unresolvedAnomalies: 8,
  criticalAlerts: 2,
  highAlerts: 5,
  mediumAlerts: 8,
  lowAlerts: 12,
  networkHealthScore: 94.5,
}

const trafficData = [
  { time: '00:00', bytes: 2400000 },
  { time: '04:00', bytes: 1398000 },
  { time: '08:00', bytes: 9800000 },
  { time: '12:00', bytes: 3908000 },
  { time: '16:00', bytes: 4800000 },
  { time: '20:00', bytes: 3800000 },
  { time: '24:00', bytes: 4300000 },
]

const anomalyData = [
  { time: '00:00', count: 1 },
  { time: '04:00', count: 0 },
  { time: '08:00', count: 3 },
  { time: '12:00', count: 2 },
  { time: '16:00', count: 4 },
  { time: '20:00', count: 1 },
  { time: '24:00', count: 2 },
]

const riskDistribution = [
  { name: 'Low', value: 120, color: '#3B82F6' },
  { name: 'Medium', value: 25, color: '#F59E0B' },
  { name: 'High', value: 8, color: '#F97316' },
  { name: 'Critical', value: 3, color: '#EF4444' },
]

const recentAnomalies = [
  { id: 1, type: 'DDoS Attack', severity: 'critical', source: '192.168.1.105', time: '2 min ago' },
  { id: 2, type: 'Port Scan', severity: 'high', source: '10.0.0.45', time: '15 min ago' },
  { id: 3, type: 'Malware', severity: 'high', source: '192.168.1.89', time: '32 min ago' },
  { id: 4, type: 'Protocol Anomaly', severity: 'medium', source: '10.0.0.12', time: '1 hr ago' },
  { id: 5, type: 'Unauthorized Access', severity: 'medium', source: '192.168.1.200', time: '2 hr ago' },
]

const topThreats = [
  { ip: '192.168.1.105', count: 15 },
  { ip: '10.0.0.45', count: 12 },
  { ip: '192.168.1.89', count: 8 },
  { ip: '10.0.0.12', count: 5 },
  { ip: '192.168.1.200', count: 3 },
]

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-slate-400">Monitor your IoT network security in real-time</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-2 px-4 py-2 bg-green-500/20 text-green-400 rounded-lg">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            System Online
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Devices"
          value={statsData.totalDevices}
          subtitle={`${statsData.onlineDevices} online`}
          icon={DeviceTabletIcon}
          trend={{ value: 12, isUp: true }}
          color="blue"
        />
        <StatsCard
          title="Active Anomalies"
          value={statsData.unresolvedAnomalies}
          subtitle={`${statsData.criticalAlerts} critical`}
          icon={ExclamationTriangleIcon}
          trend={{ value: 3, isUp: false }}
          color="red"
        />
        <StatsCard
          title="Network Health"
          value={`${statsData.networkHealthScore}%`}
          subtitle="Excellent"
          icon={ShieldCheckIcon}
          trend={{ value: 2.5, isUp: true }}
          color="green"
        />
        <StatsCard
          title="Total Alerts"
          value={statsData.criticalAlerts + statsData.highAlerts + statsData.mediumAlerts + statsData.lowAlerts}
          subtitle={`${statsData.criticalAlerts + statsData.highAlerts} high priority`}
          icon={SignalIcon}
          trend={{ value: 5, isUp: false }}
          color="yellow"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-white">Network Traffic</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" tickFormatter={(value) => `${(value / 1000000).toFixed(1)}M`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #334155' }}
                  labelStyle={{ color: '#F8FAFC' }}
                  formatter={(value: number) => [`${(value / 1000000).toFixed(2)} MB`, 'Traffic']}
                />
                <Line
                  type="monotone"
                  dataKey="bytes"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Anomalies Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-white">Anomalies Detected</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={anomalyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #334155' }}
                  labelStyle={{ color: '#F8FAFC' }}
                />
                <Bar dataKey="count" fill="#EF4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-white">Risk Distribution</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {riskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #334155' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-4">
              {riskDistribution.map((item) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-sm text-slate-400">{item.name}</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Recent Anomalies */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card lg:col-span-2"
        >
          <div className="card-header flex justify-between items-center">
            <h3 className="text-lg font-semibold text-white">Recent Anomalies</h3>
            <a href="/anomalies" className="text-sm text-blue-400 hover:text-blue-300">
              View all →
            </a>
          </div>
          <div className="overflow-x-auto">
            <table className="table">
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Source IP</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {recentAnomalies.map((anomaly) => (
                  <tr key={anomaly.id}>
                    <td className="font-medium text-white">{anomaly.type}</td>
                    <td>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium severity-${anomaly.severity}`}>
                        {anomaly.severity}
                      </span>
                    </td>
                    <td className="font-mono text-sm">{anomaly.source}</td>
                    <td className="text-slate-400">{anomaly.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

function StatsCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  color,
}: {
  title: string
  value: string | number
  subtitle: string
  icon: React.ComponentType<{ className?: string }>
  trend: { value: number; isUp: boolean }
  color: 'blue' | 'red' | 'green' | 'yellow'
}) {
  const colorClasses = {
    blue: 'bg-blue-500/20 text-blue-400',
    red: 'bg-red-500/20 text-red-400',
    green: 'bg-green-500/20 text-green-400',
    yellow: 'bg-yellow-500/20 text-yellow-400',
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="card p-6"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400">{title}</p>
          <p className="text-3xl font-bold text-white mt-1">{value}</p>
          <p className="text-sm text-slate-500 mt-1">{subtitle}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
      <div className="flex items-center gap-1 mt-4">
        {trend.isUp ? (
          <ArrowTrendingUpIcon className="w-4 h-4 text-green-400" />
        ) : (
          <ArrowTrendingDownIcon className="w-4 h-4 text-red-400" />
        )}
        <span className={trend.isUp ? 'text-green-400' : 'text-red-400'}>
          {trend.value}%
        </span>
        <span className="text-slate-500 text-sm">vs last week</span>
      </div>
    </motion.div>
  )
}
