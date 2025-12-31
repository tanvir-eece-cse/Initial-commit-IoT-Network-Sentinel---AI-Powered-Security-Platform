"""
Model Manager Service
Handles loading, caching, and inference for ML models
"""
import os
from typing import Dict, Any, Optional, List
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from app.core.config import settings


class ModelManager:
    """Manages ML models for anomaly detection"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.models_loaded = False
        self.feature_names = [
            "bytes_in", "bytes_out", "packets_in", "packets_out",
            "duration", "protocol_tcp", "protocol_udp", "protocol_icmp",
            "src_port", "dst_port", "packet_size_mean", "packet_size_std",
            "inter_arrival_time_mean", "inter_arrival_time_std",
            "syn_count", "ack_count", "rst_count", "fin_count",
            "unique_dst_ips", "unique_src_ports"
        ]
        
        # Attack type labels
        self.attack_labels = [
            "normal", "ddos_attack", "port_scan", "malware",
            "botnet", "data_exfiltration", "unauthorized_access", "protocol_anomaly"
        ]
    
    def load_models(self) -> None:
        """Load all ML models"""
        try:
            # For demo purposes, create default models if they don't exist
            self._create_default_models()
            self.models_loaded = True
        except Exception as e:
            print(f"Error loading models: {e}")
            self._create_default_models()
            self.models_loaded = True
    
    def _create_default_models(self) -> None:
        """Create and initialize default models"""
        # Isolation Forest for anomaly detection
        self.models["isolation_forest"] = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        # Random Forest for attack classification
        self.models["random_forest"] = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        
        # Standard scaler
        self.scalers["default"] = StandardScaler()
        
        # Fit models with synthetic data for demo
        self._fit_demo_models()
    
    def _fit_demo_models(self) -> None:
        """Fit models with synthetic demo data"""
        np.random.seed(42)
        
        # Generate synthetic normal data
        n_normal = 1000
        normal_data = np.random.randn(n_normal, len(self.feature_names))
        
        # Generate synthetic anomaly data
        n_anomaly = 100
        anomaly_data = np.random.randn(n_anomaly, len(self.feature_names)) * 3 + 5
        
        # Combine data
        X = np.vstack([normal_data, anomaly_data])
        y = np.array([0] * n_normal + [1] * n_anomaly)
        
        # Fit scaler
        self.scalers["default"].fit(X)
        X_scaled = self.scalers["default"].transform(X)
        
        # Fit Isolation Forest
        self.models["isolation_forest"].fit(X_scaled)
        
        # Generate multi-class labels for Random Forest
        y_multiclass = np.random.choice(
            range(len(self.attack_labels)),
            size=len(X),
            p=[0.7] + [0.3 / 7] * 7
        )
        
        # Fit Random Forest
        self.models["random_forest"].fit(X_scaled, y_multiclass)
    
    def preprocess_features(self, features: Dict[str, Any]) -> np.ndarray:
        """Preprocess input features for model inference"""
        # Extract features in correct order
        feature_vector = []
        for name in self.feature_names:
            value = features.get(name, 0.0)
            feature_vector.append(float(value))
        
        # Reshape and scale
        X = np.array(feature_vector).reshape(1, -1)
        X_scaled = self.scalers["default"].transform(X)
        
        return X_scaled
    
    def predict_anomaly(
        self,
        features: Dict[str, Any],
        model_name: str = "isolation_forest"
    ) -> Dict[str, Any]:
        """Predict if the input is anomalous"""
        X = self.preprocess_features(features)
        
        if model_name == "isolation_forest":
            # Isolation Forest prediction
            prediction = self.models["isolation_forest"].predict(X)[0]
            score = self.models["isolation_forest"].score_samples(X)[0]
            
            is_anomaly = prediction == -1
            # Convert score to confidence (0-1 range)
            confidence = 1 / (1 + np.exp(score))  # Sigmoid transformation
            
        else:
            # Random Forest prediction
            prediction = self.models["random_forest"].predict(X)[0]
            probabilities = self.models["random_forest"].predict_proba(X)[0]
            
            is_anomaly = prediction != 0  # 0 is normal
            confidence = max(probabilities)
        
        # Get attack type if anomaly
        if is_anomaly:
            attack_prediction = self.models["random_forest"].predict(X)[0]
            anomaly_type = self.attack_labels[attack_prediction]
        else:
            anomaly_type = "normal"
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(is_anomaly, confidence, anomaly_type)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(is_anomaly, anomaly_type, risk_score)
        
        return {
            "is_anomaly": bool(is_anomaly),
            "anomaly_type": anomaly_type if is_anomaly else None,
            "confidence_score": float(confidence),
            "risk_score": float(risk_score),
            "model_used": model_name,
            "recommendations": recommendations
        }
    
    def predict_batch(
        self,
        samples: List[Dict[str, Any]],
        model_name: str = "isolation_forest"
    ) -> List[Dict[str, Any]]:
        """Batch prediction for multiple samples"""
        results = []
        for sample in samples:
            result = self.predict_anomaly(sample, model_name)
            results.append(result)
        return results
    
    def _calculate_risk_score(
        self,
        is_anomaly: bool,
        confidence: float,
        anomaly_type: str
    ) -> float:
        """Calculate risk score based on prediction"""
        if not is_anomaly:
            return 0.0
        
        # Base risk from confidence
        base_risk = confidence * 0.5
        
        # Severity multiplier based on attack type
        severity_weights = {
            "ddos_attack": 0.9,
            "malware": 0.95,
            "botnet": 0.85,
            "data_exfiltration": 0.9,
            "unauthorized_access": 0.8,
            "port_scan": 0.6,
            "protocol_anomaly": 0.5,
            "normal": 0.0
        }
        
        severity = severity_weights.get(anomaly_type, 0.5)
        risk_score = base_risk + (severity * 0.5)
        
        return min(risk_score, 1.0)
    
    def _generate_recommendations(
        self,
        is_anomaly: bool,
        anomaly_type: str,
        risk_score: float
    ) -> List[str]:
        """Generate security recommendations"""
        if not is_anomaly:
            return ["Continue normal monitoring"]
        
        recommendations = []
        
        # Common recommendations
        recommendations.append("Investigate source IP address")
        recommendations.append("Review recent activity logs")
        
        # Type-specific recommendations
        type_recommendations = {
            "ddos_attack": [
                "Enable DDoS protection rules",
                "Consider rate limiting",
                "Contact upstream provider if severe"
            ],
            "malware": [
                "Isolate affected device immediately",
                "Run malware scan on affected systems",
                "Check for data exfiltration"
            ],
            "botnet": [
                "Block command and control communication",
                "Isolate infected devices",
                "Scan network for other infected hosts"
            ],
            "data_exfiltration": [
                "Block outbound connections immediately",
                "Investigate data access logs",
                "Check for compromised credentials"
            ],
            "unauthorized_access": [
                "Review authentication logs",
                "Check for credential compromise",
                "Enable additional authentication factors"
            ],
            "port_scan": [
                "Review firewall rules",
                "Block scanning source if malicious",
                "Check for open unnecessary ports"
            ],
            "protocol_anomaly": [
                "Investigate protocol violation",
                "Check for misconfigured devices",
                "Update network policies"
            ]
        }
        
        if anomaly_type in type_recommendations:
            recommendations.extend(type_recommendations[anomaly_type])
        
        # High risk additional recommendations
        if risk_score > 0.8:
            recommendations.insert(0, "CRITICAL: Immediate action required")
            recommendations.append("Consider network isolation")
            recommendations.append("Notify security team immediately")
        
        return recommendations
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        if model_name not in self.models:
            return {"error": f"Model {model_name} not found"}
        
        model = self.models[model_name]
        
        info = {
            "name": model_name,
            "type": type(model).__name__,
            "features": self.feature_names,
            "num_features": len(self.feature_names),
        }
        
        if model_name == "isolation_forest":
            info["n_estimators"] = model.n_estimators
            info["contamination"] = model.contamination
        elif model_name == "random_forest":
            info["n_estimators"] = model.n_estimators
            info["max_depth"] = model.max_depth
            info["classes"] = self.attack_labels
        
        return info
    
    def get_all_models(self) -> Dict[str, Any]:
        """Get information about all available models"""
        return {
            "models": list(self.models.keys()),
            "details": {
                name: self.get_model_info(name)
                for name in self.models.keys()
            }
        }
    
    def get_feature_importance(self, model_name: str) -> Dict[str, float]:
        """Get feature importance for tree-based models"""
        if model_name not in self.models:
            return {}
        
        model = self.models[model_name]
        
        if hasattr(model, "feature_importances_"):
            importance = model.feature_importances_
            return {
                name: float(imp)
                for name, imp in zip(self.feature_names, importance)
            }
        
        return {}
