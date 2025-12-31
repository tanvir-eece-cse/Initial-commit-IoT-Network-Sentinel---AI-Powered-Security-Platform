import { motion } from 'framer-motion'
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
} from 'recharts'

// Demo data
const trafficData = [
  { time: '00:00', inbound: 1200, outbound: 800 },
  { time: '04:00', inbound: 800, outbound: 600 },
  { time: '08:00', inbound: 2500, outbound: 1800 },
  { time: '12:00', inbound: 3200, outbound: 2400 },
  { time: '16:00', inbound: 2800, outbound: 2100 },
  { time: '20:00', inbound: 1800, outbound: 1200 },
  { time: '24:00', inbound: 1400, outbound: 900 },
]

const protocolData = [
  { name: 'TCP', value: 65, color: '#3B82F6' },
  { name: 'UDP', value: 25, color: '#10B981' },
  { name: 'ICMP', value: 10, color: '#F59E0B' },
]

const networkStats = {
  totalBandwidth: '15.4 Gbps',
  avgLatency: '12 ms',
  packetLoss: '0.02%',
  activeConnections: 1847,
  blockedConnections: 23,
}

export default function Network() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white">Network Overview</h1>
          <p className="text-slate-400">Monitor network traffic and performance metrics</p>
        </div>
        <button className="btn btn-primary">
          Initiate Scan
        </button>
      </div>

      {/* Network Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div className="card p-4 text-center">
          <p className="text-2xl font-bold text-blue-400">{networkStats.totalBandwidth}</p>
          <p className="text-sm text-slate-400">Total Bandwidth</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-2xl font-bold text-green-400">{networkStats.avgLatency}</p>
          <p className="text-sm text-slate-400">Avg Latency</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-2xl font-bold text-yellow-400">{networkStats.packetLoss}</p>
          <p className="text-sm text-slate-400">Packet Loss</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-2xl font-bold text-white">{networkStats.activeConnections}</p>
          <p className="text-sm text-slate-400">Active Connections</p>
        </div>
        <div className="card p-4 text-center">
          <p className="text-2xl font-bold text-red-400">{networkStats.blockedConnections}</p>
          <p className="text-sm text-slate-400">Blocked</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Traffic Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card lg:col-span-2"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-white">Network Traffic</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #334155' }}
                  labelStyle={{ color: '#F8FAFC' }}
                />
                <Line
                  type="monotone"
                  dataKey="inbound"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  name="Inbound (MB/s)"
                />
                <Line
                  type="monotone"
                  dataKey="outbound"
                  stroke="#10B981"
                  strokeWidth={2}
                  name="Outbound (MB/s)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Protocol Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-white">Protocol Distribution</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie
                  data={protocolData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={70}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {protocolData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#1E293B', border: '1px solid #334155' }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center gap-4 mt-4">
              {protocolData.map((item) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-sm text-slate-400">{item.name}: {item.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Network Topology Placeholder */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-white">Network Topology</h3>
        </div>
        <div className="card-body flex items-center justify-center min-h-[300px]">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-500/20 flex items-center justify-center">
              <svg className="w-8 h-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
            <p className="text-slate-400">Network topology visualization</p>
            <p className="text-sm text-slate-500 mt-1">Interactive map showing device connections</p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
