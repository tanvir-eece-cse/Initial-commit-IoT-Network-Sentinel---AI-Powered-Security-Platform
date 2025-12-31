// User types
export interface User {
  id: string
  email: string
  full_name: string
  role: 'admin' | 'analyst' | 'viewer'
  is_active: boolean
  created_at: string
}

// Device types
export interface Device {
  id: string
  name: string
  device_type: DeviceType
  ip_address: string
  mac_address: string
  status: DeviceStatus
  firmware_version: string
  last_seen: string
  risk_score: number
  location?: string
  manufacturer?: string
  created_at: string
  updated_at: string
}

export type DeviceType = 
  | 'sensor'
  | 'camera'
  | 'thermostat'
  | 'smart_plug'
  | 'gateway'
  | 'router'
  | 'other'

export type DeviceStatus = 'online' | 'offline' | 'unknown'

// Anomaly types
export interface Anomaly {
  id: string
  device_id: string
  device_name?: string
  anomaly_type: AnomalyType
  severity: Severity
  confidence: number
  description: string
  source_ip: string
  destination_ip: string
  source_port?: number
  destination_port?: number
  protocol?: string
  status: AnomalyStatus
  detected_at: string
  resolved_at?: string
  notes?: string
}

export type AnomalyType =
  | 'port_scan'
  | 'ddos_attack'
  | 'data_exfiltration'
  | 'unauthorized_access'
  | 'malware_activity'
  | 'protocol_anomaly'
  | 'traffic_spike'
  | 'unusual_behavior'
  | 'other'

export type Severity = 'critical' | 'high' | 'medium' | 'low'

export type AnomalyStatus = 'new' | 'investigating' | 'resolved' | 'false_positive'

// Alert types
export interface Alert {
  id: string
  anomaly_id?: string
  device_id?: string
  title: string
  message: string
  severity: Severity
  type: AlertType
  status: AlertStatus
  created_at: string
  acknowledged_at?: string
  acknowledged_by?: string
}

export type AlertType = 'anomaly' | 'system' | 'maintenance' | 'security'
export type AlertStatus = 'active' | 'acknowledged' | 'resolved'

// Network types
export interface NetworkStats {
  total_packets: number
  total_bytes: number
  protocols: Record<string, number>
  top_talkers: TopTalker[]
  traffic_by_hour: TrafficData[]
}

export interface TopTalker {
  ip: string
  bytes_sent: number
  bytes_received: number
  device_name?: string
}

export interface TrafficData {
  timestamp: string
  bytes: number
  packets: number
  inbound?: number
  outbound?: number
}

// Dashboard types
export interface DashboardStats {
  total_devices: number
  online_devices: number
  offline_devices: number
  total_anomalies_today: number
  critical_anomalies: number
  high_anomalies: number
  medium_anomalies: number
  low_anomalies: number
  network_health_score: number
  total_traffic_today: string
}

// ML Prediction types
export interface PredictionRequest {
  features: Record<string, number | string>
}

export interface PredictionResponse {
  prediction: 'normal' | 'anomaly'
  confidence: number
  anomaly_type?: AnomalyType
  risk_score: number
  recommended_action?: string
}

export interface BatchPredictionRequest {
  samples: PredictionRequest[]
}

export interface BatchPredictionResponse {
  predictions: PredictionResponse[]
  processing_time_ms: number
}

// API Response types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pages: number
}

export interface ApiError {
  detail: string
  status_code?: number
}

// Auth types
export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
}

// Filter types
export interface DeviceFilters {
  status?: DeviceStatus
  device_type?: DeviceType
  search?: string
}

export interface AnomalyFilters {
  severity?: Severity
  status?: AnomalyStatus
  device_id?: string
  date_from?: string
  date_to?: string
}

export interface AlertFilters {
  severity?: Severity
  status?: AlertStatus
  type?: AlertType
}

// WebSocket message types
export interface WSMessage {
  type: 'anomaly' | 'alert' | 'device_status' | 'metrics'
  data: unknown
  timestamp: string
}

export interface WSAnomalyMessage extends WSMessage {
  type: 'anomaly'
  data: Anomaly
}

export interface WSAlertMessage extends WSMessage {
  type: 'alert'
  data: Alert
}

export interface WSDeviceStatusMessage extends WSMessage {
  type: 'device_status'
  data: {
    device_id: string
    status: DeviceStatus
  }
}

// Chart data types
export interface ChartDataPoint {
  name: string
  value: number
  [key: string]: string | number
}

export interface TimeSeriesDataPoint {
  timestamp: string
  value: number
  label?: string
}
