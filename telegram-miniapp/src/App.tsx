import React, { useEffect, useState } from 'react';
import WebApp from '@twa-dev/sdk';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface Order {
  id: number;
  cargo_name: string;
  cargo_type: string;
  weight_kg: number;
  pickup_address: string;
  delivery_address: string;
  budget_uzs: number;
  urgency_score: number;
}

function App() {
  const [user, setUser] = useState<any>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize Telegram WebApp
    WebApp.ready();
    WebApp.expand();
    
    const tgUser = WebApp.initDataUnsafe?.user;
    if (tgUser) {
      setUser({
        id: tgUser.id,
        username: tgUser.username,
        first_name: tgUser.first_name,
        last_name: tgUser.last_name
      });
    }

    // Load available orders
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/v1/orders?status=pending&limit=10`);
      setOrders(response.data || []);
    } catch (error) {
      console.error('Failed to load orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const acceptOrder = async (order: Order) => {
    try {
      WebApp.showConfirm(`Accept order #${order.id}?\n${order.pickup_address} → ${order.delivery_address}`, async (accepted) => {
        if (accepted) {
          await axios.put(`${API_URL}/api/v1/orders/${order.id}`, {
            status: 'matched',
            matched_vehicle_id: 1 // Driver's vehicle
          });
          
          WebApp.showAlert('Order accepted! Check your route.');
          WebApp.openTelegramLink('https://t.me/AILogisticsBot');
        }
      });
    } catch (error) {
      WebApp.showAlert('Failed to accept order');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '1rem',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '1rem',
        marginBottom: '1rem',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', color: '#1a1a2e' }}>
          🚛 AI Logistics
        </h1>
        <p style={{ margin: '0.5rem 0 0', color: '#666' }}>
          Welcome, {user?.first_name || 'Driver'}!
        </p>
      </div>

      {/* Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '0.5rem',
        marginBottom: '1rem'
      }}>
        <StatCard icon="" value="12" label="Completed" />
        <StatCard icon="" value="2.4M" label="Earned UZS" />
        <StatCard icon="⭐" value="4.9" label="Rating" />
      </div>

      {/* Orders */}
      <div style={{
        background: 'white',
        borderRadius: '16px',
        padding: '1rem',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ margin: '0 0 1rem', fontSize: '1.25rem', color: '#1a1a2e' }}>
          Available Orders
        </h2>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            Loading orders...
          </div>
        ) : orders.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            No orders available
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {orders.map(order => (
              <OrderCard
                key={order.id}
                order={order}
                onAccept={() => acceptOrder(order)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Bottom Navigation */}
      <div style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        background: 'white',
        padding: '0.75rem',
        display: 'flex',
        justifyContent: 'space-around',
        boxShadow: '0 -2px 8px rgba(0,0,0,0.1)'
      }}>
        <NavButton icon="" label="Orders" active />
        <NavButton icon="" label="My Route" />
        <NavButton icon="📄" label="Docs" />
        <NavButton icon="️" label="Settings" />
      </div>
    </div>
  );
}

const StatCard: React.FC<{ icon: string; value: string; label: string }> = ({ icon, value, label }) => (
  <div style={{
    background: 'white',
    borderRadius: '12px',
    padding: '0.75rem',
    textAlign: 'center',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  }}>
    <div style={{ fontSize: '1.5rem' }}>{icon}</div>
    <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1a1a2e' }}>{value}</div>
    <div style={{ fontSize: '0.75rem', color: '#666' }}>{label}</div>
  </div>
);

const OrderCard: React.FC<{ order: Order; onAccept: () => void }> = ({ order, onAccept }) => (
  <div style={{
    border: '1px solid #e5e7eb',
    borderRadius: '12px',
    padding: '1rem',
    transition: 'all 0.2s'
  }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
      <span style={{ fontWeight: 600, color: '#3b82f6' }}>#{order.id}</span>
      <span style={{
        background: order.urgency_score >= 8 ? '#fee2e2' : '#d1fae5',
        color: order.urgency_score >= 8 ? '#991b1b' : '#065f46',
        padding: '0.25rem 0.5rem',
        borderRadius: '20px',
        fontSize: '0.75rem',
        fontWeight: 600
      }}>
        {order.urgency_score >= 8 ? '🔥 Urgent' : 'Normal'}
      </span>
    </div>

    <div style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '0.5rem' }}>
      {order.cargo_name}
    </div>

    <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>
      {order.weight_kg} kg • {order.cargo_type}
    </div>

    <div style={{ fontSize: '0.875rem', marginBottom: '0.75rem' }}>
      <div style={{ color: '#10b981' }}>📍 {order.pickup_address}</div>
      <div style={{ color: '#ef4444', marginTop: '0.25rem' }}>🏁 {order.delivery_address}</div>
    </div>

    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <span style={{ fontWeight: 700, color: '#1a1a2e' }}>
        {(order.budget_uzs / 1000).toFixed(0)}K UZS
      </span>
      <button
        onClick={onAccept}
        style={{
          background: '#10b981',
          color: 'white',
          border: 'none',
          padding: '0.5rem 1rem',
          borderRadius: '8px',
          fontWeight: 600,
          cursor: 'pointer'
        }}
      >
        Accept
      </button>
    </div>
  </div>
);

const NavButton: React.FC<{ icon: string; label: string; active?: boolean }> = ({ icon, label, active }) => (
  <button style={{
    background: 'none',
    border: 'none',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '0.25rem',
    cursor: 'pointer',
    opacity: active ? 1 : 0.6
  }}>
    <span style={{ fontSize: '1.25rem' }}>{icon}</span>
    <span style={{ fontSize: '0.75rem', color: active ? '#3b82f6' : '#666' }}>{label}</span>
  </button>
);

export default App;
