import React from 'react';
import {
  Card, CardHeader, CardBody, Chip, Divider, Progress,
  Tabs, Tab, Button
} from '@heroui/react';

const Analytics: React.FC = () => {
  const kpis = {
    totalRevenue: '45.2M UZS',
    totalTrips: 1247,
    avgDeliveryTime: '4.2 hours',
    onTimeRate: '94%',
    fuelSaved: '2.4M UZS',
    emptyTripsReduced: '38%',
  };

  const regions = [
    { name: 'Tashkent', orders: 487, revenue: '18.5M UZS', growth: '+15%' },
    { name: 'Samarkand', orders: 312, revenue: '12.1M UZS', growth: '+22%' },
    { name: 'Bukhara', orders: 198, revenue: '7.8M UZS', growth: '+8%' },
    { name: 'Fergana', orders: 156, revenue: '4.9M UZS', growth: '+12%' },
    { name: 'Navoi', orders: 94, revenue: '1.9M UZS', growth: '+5%' },
  ];

  const monthlyData = [
    { month: 'Mar', orders: 856, revenue: '32.1M' },
    { month: 'Apr', orders: 943, revenue: '35.8M' },
    { month: 'May', orders: 1087, revenue: '40.2M' },
    { month: 'Jun', orders: 1156, revenue: '42.7M' },
    { month: 'Jul', orders: 1198, revenue: '44.1M' },
    { month: 'Aug', orders: 1247, revenue: '45.2M' },
  ];

  const maxOrders = Math.max(...monthlyData.map(m => m.orders));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Analytics & Insights</h1>
          <p className="text-muted mt-1">Business intelligence and AI-driven insights</p>
        </div>
        <div className="flex gap-3">
          <Button variant="flat">Export Report</Button>
          <Button color="primary">AI Insights</Button>
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-6 gap-4">
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">Total Revenue</p>
            <p className="text-xl font-bold text-foreground">{kpis.totalRevenue}</p>
            <Chip color="success" size="sm" variant="flat" className="mt-2">+18%</Chip>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">Total Trips</p>
            <p className="text-xl font-bold text-foreground">{kpis.totalTrips}</p>
            <Chip color="success" size="sm" variant="flat" className="mt-2">+12%</Chip>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">Avg Delivery</p>
            <p className="text-xl font-bold text-foreground">{kpis.avgDeliveryTime}</p>
            <Chip color="success" size="sm" variant="flat" className="mt-2">-15%</Chip>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">On-Time Rate</p>
            <p className="text-xl font-bold text-success">{kpis.onTimeRate}</p>
            <Chip color="success" size="sm" variant="flat" className="mt-2">+5%</Chip>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">Fuel Saved</p>
            <p className="text-xl font-bold text-primary">{kpis.fuelSaved}</p>
            <Chip color="primary" size="sm" variant="flat" className="mt-2">-18%</Chip>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-xs text-muted">Empty Trips</p>
            <p className="text-xl font-bold text-secondary">{kpis.emptyTripsReduced}</p>
            <Chip color="secondary" size="sm" variant="flat" className="mt-2">-30%</Chip>
          </CardBody>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-6">
        {/* Monthly Orders Chart */}
        <Card className="bg-surface border border-white/10">
          <CardHeader className="px-6 pt-6">
            <h3 className="text-lg font-bold text-foreground">Monthly Orders Trend</h3>
          </CardHeader>
          <Divider />
          <CardBody className="p-6">
            <div className="space-y-4">
              {monthlyData.map((month) => (
                <div key={month.month}>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-foreground font-semibold">{month.month}</span>
                    <span className="text-muted">{month.orders} orders • {month.revenue} UZS</span>
                  </div>
                  <Progress value={(month.orders / maxOrders) * 100} color="primary" size="sm" />
                </div>
              ))}
            </div>
          </CardBody>
        </Card>

        {/* Regional Performance */}
        <Card className="bg-surface border border-white/10">
          <CardHeader className="px-6 pt-6">
            <h3 className="text-lg font-bold text-foreground">Regional Performance</h3>
          </CardHeader>
          <Divider />
          <CardBody className="p-6">
            <div className="space-y-4">
              {regions.map((region) => (
                <div key={region.name} className="flex items-center justify-between p-3 rounded-lg bg-white/5 hover:bg-white/10 transition">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg gradient-primary flex items-center justify-center text-white font-bold">
                      {region.name[0]}
                    </div>
                    <div>
                      <p className="font-semibold text-foreground">{region.name}</p>
                      <p className="text-xs text-muted">{region.orders} orders</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-foreground">{region.revenue}</p>
                    <Chip color="success" size="sm" variant="flat">{region.growth}</Chip>
                  </div>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      </div>

      {/* AI Insights */}
      <Card className="bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
        <CardHeader className="px-6 pt-6">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🤖</span>
            <h3 className="text-lg font-bold text-foreground">AI-Generated Insights</h3>
          </div>
        </CardHeader>
        <Divider />
        <CardBody className="p-6">
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-success/10 border border-success/20">
              <h4 className="font-bold text-success mb-2">Demand Forecast</h4>
              <p className="text-sm text-muted">Tashkent-Samarkand route expected to grow +35% next month. Consider adding 5 more vehicles.</p>
            </div>
            <div className="p-4 rounded-xl bg-warning/10 border border-warning/20">
              <h4 className="font-bold text-warning mb-2">Anomaly Detected</h4>
              <p className="text-sm text-muted">Unusual pricing pattern on Fergana-Tashkent route. 3 carriers bidding 40% below market.</p>
            </div>
            <div className="p-4 rounded-xl bg-primary/10 border border-primary/20">
              <h4 className="font-bold text-primary mb-2">Optimization</h4>
              <p className="text-sm text-muted">Return load matching can save 2.1M UZS monthly. 23 vehicles returning empty weekly.</p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};

export default Analytics;
