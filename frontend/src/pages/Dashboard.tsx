import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Progress,
  Chip,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Badge,
  Divider,
  Tooltip,
  Sparkles
} from '@heroui/react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface KPIProps {
  title: string;
  value: string | number;
  icon: string;
  change: string;
  color: 'primary' | 'success' | 'warning' | 'danger' | 'secondary';
  trend: 'up' | 'down';
}

const KPICard: React.FC<KPIProps> = ({ title, value, icon, change, color, trend }) => (
  <Card className="bg-surface border border-white/10 hover:border-primary/30 transition-all hover:scale-105">
    <CardBody className="p-6">
      <div className="flex justify-between items-start mb-4">
        <div className={`w-12 h-12 rounded-xl bg-${color}/20 flex items-center justify-center text-2xl`}>
          {icon}
        </div>
        <Chip
          color={trend === 'up' ? 'success' : 'danger'}
          variant="flat"
          size="sm"
        >
          {change}
        </Chip>
      </div>
      <h3 className="text-3xl font-bold text-foreground mb-1">{value}</h3>
      <p className="text-sm text-muted">{title}</p>
    </CardBody>
  </Card>
);

const Dashboard: React.FC = () => {
  const { data: healthData, isLoading } = useQuery({
    queryKey: ['health'],
    queryFn: () => axios.get(`${API_URL}/health`).then(res => res.data),
  });

  const recentOrders = [
    { id: 1247, route: 'Tashkent → Samarkand', status: 'matched', cargo: 'Electronics', driver: 'Alisher K.' },
    { id: 1246, route: 'Bukhara → Navoi', status: 'pending', cargo: 'Cotton', driver: '—' },
    { id: 1245, route: 'Fergana → Tashkent', status: 'transit', cargo: 'Food Products', driver: 'Rustam M.' },
    { id: 1244, route: 'Namangan → Andijan', status: 'matched', cargo: 'Textiles', driver: 'Jamshid T.' },
  ];

  const insights = [
    { icon: '️', title: 'Permit Deficit Alert', desc: 'China route permits running low', color: 'warning' },
    { icon: '✅', title: 'Safety Check Passed', desc: 'Order #1247 apples - phytosanitary valid', color: 'success' },
    { icon: '💡', title: 'Return Load Found', desc: 'Vehicle #34 has return cargo', color: 'primary' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted mt-1">AI Smart Logistics Platform Overview</p>
        </div>
        <div className="flex gap-3">
          <Button color="primary" variant="flat">
            Export Report
          </Button>
          <Button color="primary">
            + New Order
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <Progress size="lg" isIndeterminate aria-label="Loading..." className="max-w-md" />
        </div>
      ) : (
        <>
          {/* KPI Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            <KPICard title="Active Orders" value="247" icon="" change="+12%" color="primary" trend="up" />
            <KPICard title="Vehicles" value="89" icon="🚛" change="+5" color="success" trend="up" />
            <KPICard title="AI Matches" value="156" icon="🤖" change="94%" color="secondary" trend="up" />
            <KPICard title="Safety Checks" value="42" icon="️" change="3" color="warning" trend="down" />
            <KPICard title="Empty Trips" value="38" icon="" change="-30%" color="success" trend="up" />
            <KPICard title="Fuel Saved" value="2.4M" icon="" change="-18%" color="danger" trend="up" />
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recent Orders */}
            <Card className="lg:col-span-2 bg-surface border border-white/10">
              <CardHeader className="flex justify-between items-center px-6 pt-6">
                <div>
                  <h3 className="text-lg font-bold text-foreground">Recent Orders</h3>
                  <p className="text-sm text-muted">Latest cargo requests</p>
                </div>
                <Button size="sm" variant="flat">View All</Button>
              </CardHeader>
              <Divider />
              <CardBody className="p-0">
                <Table aria-label="Recent orders" removeWrapper>
                  <TableHeader>
                    <TableColumn>ID</TableColumn>
                    <TableColumn>Route</TableColumn>
                    <TableColumn>Cargo</TableColumn>
                    <TableColumn>Driver</TableColumn>
                    <TableColumn>Status</TableColumn>
                  </TableHeader>
                  <TableBody>
                    {recentOrders.map((order) => (
                      <TableRow key={order.id}>
                        <TableCell>
                          <Chip variant="flat" size="sm">#{order.id}</Chip>
                        </TableCell>
                        <TableCell className="text-foreground">{order.route}</TableCell>
                        <TableCell>{order.cargo}</TableCell>
                        <TableCell>{order.driver}</TableCell>
                        <TableCell>
                          <Chip
                            color={
                              order.status === 'matched' ? 'success' :
                              order.status === 'pending' ? 'warning' : 'primary'
                            }
                            size="sm"
                            variant="flat"
                          >
                            {order.status}
                          </Chip>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardBody>
            </Card>

            {/* AI Insights */}
            <Card className="bg-surface border border-white/10">
              <CardHeader className="px-6 pt-6">
                <div className="flex items-center gap-2">
                  <Sparkles className="text-primary" />
                  <h3 className="text-lg font-bold text-foreground">AI Insights</h3>
                </div>
              </CardHeader>
              <Divider />
              <CardBody className="space-y-4 p-6">
                {insights.map((insight, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-xl bg-${insight.color}/10 border border-${insight.color}/20`}
                  >
                    <div className="flex gap-3">
                      <span className="text-2xl">{insight.icon}</span>
                      <div>
                        <h4 className="font-semibold text-foreground text-sm">{insight.title}</h4>
                        <p className="text-xs text-muted mt-1">{insight.desc}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </CardBody>
              <CardFooter className="px-6 pb-6">
                <Button fullWidth color="primary" variant="flat" size="sm">
                  View All Insights
                </Button>
              </CardFooter>
            </Card>
          </div>

          {/* Bottom Stats */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="bg-surface border border-white/10">
              <CardHeader className="px-6 pt-6">
                <h3 className="text-lg font-bold text-foreground">System Performance</h3>
              </CardHeader>
              <Divider />
              <CardBody className="p-6 space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-muted">API Response Time</span>
                    <span className="text-foreground font-semibold">45ms</span>
                  </div>
                  <Progress value={95} color="success" size="sm" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-muted">ML Accuracy</span>
                    <span className="text-foreground font-semibold">94%</span>
                  </div>
                  <Progress value={94} color="primary" size="sm" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-muted">Database Uptime</span>
                    <span className="text-foreground font-semibold">99.9%</span>
                  </div>
                  <Progress value={99.9} color="secondary" size="sm" />
                </div>
              </CardBody>
            </Card>

            <Card className="bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
              <CardBody className="p-6">
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-foreground mb-2">AI Platform Active</h3>
                  <p className="text-muted mb-6">All systems operational</p>
                  <div className="grid grid-cols-3 gap-4 mb-6">
                    <div>
                      <p className="text-3xl font-bold text-primary">3</p>
                      <p className="text-xs text-muted">AI Models</p>
                    </div>
                    <div>
                      <p className="text-3xl font-bold text-success">9</p>
                      <p className="text-xs text-muted">Services</p>
                    </div>
                    <div>
                      <p className="text-3xl font-bold text-secondary">24/7</p>
                      <p className="text-xs text-muted">Uptime</p>
                    </div>
                  </div>
                  <Chip color="success" variant="flat">
                    API Version: {healthData?.version || '1.0.0'}
                  </Chip>
                </div>
              </CardBody>
            </Card>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
