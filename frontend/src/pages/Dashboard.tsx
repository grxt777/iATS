import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import './Dashboard.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface KPICardProps {
  title: string;
  value: string | number;
  icon: string;
  change?: string;
  color: string;
}

const KPICard: React.FC<KPICardProps> = ({ title, value, icon, change, color }) => (
  <div className={`kpi-card ${color}`}>
    <div className="kpi-header">
      <span className="kpi-icon">{icon}</span>
      {change && <span className="kpi-change">{change}</span>}
    </div>
    <div className="kpi-value">{value}</div>
    <div className="kpi-title">{title}</div>
  </div>
);

const Dashboard: React.FC = () => {
  const { data: healthData, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => axios.get(`${API_URL}/health`).then(res => res.data),
  });

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>AI Smart Logistics Platform Overview</p>
      </div>
      
      {isLoading ? (
        <div className="loading">Loading...</div>
      ) : (
        <>
          <div className="kpi-grid">
            <KPICard
              title="Active Orders"
              value="247"
              icon=""
              change="+12% vs last week"
              color="blue"
            />
            <KPICard
              title="Available Vehicles"
              value="89"
              icon="🚛"
              change="+5 new"
              color="green"
            />
            <KPICard
              title="AI Matches Today"
              value="156"
              icon="🤖"
              change="94% accuracy"
              color="purple"
            />
            <KPICard
              title="Safety Checks"
              value="42"
              icon="🛡️"
              change="3 warnings"
              color="orange"
            />
            <KPICard
              title="Empty Trips Prevented"
              value="38"
              icon="📉"
              change="-30% vs last month"
              color="red"
            />
            <KPICard
              title="Fuel Saved"
              value="2.4M UZS"
              icon="⛽"
              change="-18% consumption"
              color="teal"
            />
          </div>
          
          <div className="dashboard-grid">
            <div className="dashboard-card">
              <h3>Recent Orders</h3>
              <div className="orders-list">
                <div className="order-item">
                  <span className="order-id">#1247</span>
                  <span className="order-route">Tashkent → Samarkand</span>
                  <span className="order-status matched">Matched</span>
                </div>
                <div className="order-item">
                  <span className="order-id">#1246</span>
                  <span className="order-route">Bukhara → Navoi</span>
                  <span className="order-status pending">Pending</span>
                </div>
                <div className="order-item">
                  <span className="order-id">#1245</span>
                  <span className="order-route">Fergana → Tashkent</span>
                  <span className="order-status transit">In Transit</span>
                </div>
              </div>
            </div>
            
            <div className="dashboard-card">
              <h3>AI Insights</h3>
              <div className="insights-list">
                <div className="insight-item warning">
                  <span className="insight-icon">⚠️</span>
                  <div>
                    <strong>Permit Deficit Alert</strong>
                    <p>China route permits running low - apply now</p>
                  </div>
                </div>
                <div className="insight-item success">
                  <span className="insight-icon">✅</span>
                  <div>
                    <strong>Safety Check Passed</strong>
                    <p>Order #1247 apples cargo - phytosanitary valid</p>
                  </div>
                </div>
                <div className="insight-item info">
                  <span className="insight-icon">💡</span>
                  <div>
                    <strong>Return Load Found</strong>
                    <p>Vehicle #34 has return cargo Samarkand → Tashkent</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="dashboard-footer">
            <p>System Status: <span className="status-ok">● Online</span></p>
            <p>API Version: {healthData?.version || '1.0.0'}</p>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
