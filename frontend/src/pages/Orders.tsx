import React, { useState } from 'react';
import {
  Card, CardHeader, CardBody, Button, Input, Chip, Divider,
  Table, TableHeader, TableColumn, TableBody, TableRow, TableCell,
  Tabs, Tab, Dropdown, DropdownTrigger, DropdownMenu, DropdownItem,
  Badge, User
} from '@heroui/react';

interface Order {
  id: string;
  cargo: string;
  type: string;
  weight: string;
  route: string;
  budget: string;
  status: 'Pending' | 'Matched' | 'In Transit' | 'Completed' | 'Cancelled';
  urgency: number;
  created: string;
}

const mockOrders: Order[] = [
  { id: '#1247', cargo: 'Fresh Apples', type: 'Refrigerated', weight: '20 tons', route: 'Tashkent → Samarkand', budget: '1.5M UZS', status: 'Matched', urgency: 8, created: '2026-08-06' },
  { id: '#1246', cargo: 'Textile Fabric', type: 'General', weight: '15 tons', route: 'Bukhara → Navoi', budget: '800k UZS', status: 'Pending', urgency: 5, created: '2026-08-06' },
  { id: '#1245', cargo: 'Construction Metal', type: 'Flatbed', weight: '25 tons', route: 'Fergana → Tashkent', budget: '2.1M UZS', status: 'In Transit', urgency: 3, created: '2026-08-05' },
  { id: '#1244', cargo: 'Electronics', type: 'Dry Van', weight: '5 tons', route: 'Tashkent → Bukhara', budget: '1.2M UZS', status: 'Completed', urgency: 6, created: '2026-08-05' },
  { id: '#1243', cargo: 'Chemical Drums', type: 'Hazardous (ADR)', weight: '12 tons', route: 'Chirchiq → Samarkand', budget: '3.0M UZS', status: 'Pending', urgency: 9, created: '2026-08-06' },
  { id: '#1242', cargo: 'Wheat Grain', type: 'Bulk', weight: '30 tons', route: 'Karakalpakstan → Tashkent', budget: '1.8M UZS', status: 'Matched', urgency: 4, created: '2026-08-04' },
  { id: '#1241', cargo: 'Furniture', type: 'General', weight: '8 tons', route: 'Namangan → Tashkent', budget: '950k UZS', status: 'Completed', urgency: 2, created: '2026-08-04' },
];

const Orders: React.FC = () => {
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [search, setSearch] = useState('');

  const filteredOrders = mockOrders.filter(order => {
    const matchesStatus = selectedStatus === 'all' || order.status.toLowerCase().replace(' ', '-') === selectedStatus;
    const matchesSearch = order.id.toLowerCase().includes(search.toLowerCase()) || 
                          order.cargo.toLowerCase().includes(search.toLowerCase()) ||
                          order.route.toLowerCase().includes(search.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  const statusColor = (status: string) => {
    switch (status) {
      case 'Completed': return 'success';
      case 'In Transit': return 'primary';
      case 'Matched': return 'secondary';
      case 'Pending': return 'warning';
      case 'Cancelled': return 'danger';
      default: return 'default';
    }
  };

  const stats = {
    total: mockOrders.length,
    pending: mockOrders.filter(o => o.status === 'Pending').length,
    inTransit: mockOrders.filter(o => o.status === 'In Transit').length,
    matched: mockOrders.filter(o => o.status === 'Matched').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Cargo Orders</h1>
          <p className="text-muted mt-1">Manage and track all shipment requests</p>
        </div>
        <Button color="primary" className="gradient-primary">
          + Create New Order
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Total Orders</p>
            <p className="text-2xl font-bold text-foreground">{stats.total}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Pending</p>
            <p className="text-2xl font-bold text-warning">{stats.pending}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">In Transit</p>
            <p className="text-2xl font-bold text-primary">{stats.inTransit}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Matched</p>
            <p className="text-2xl font-bold text-secondary">{stats.matched}</p>
          </CardBody>
        </Card>
      </div>

      {/* Filters */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-4">
          <div className="flex gap-4 items-center">
            <Input
              placeholder="Search orders..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="max-w-md"
              startContent={🔍}
            />
            <Tabs
              selectedKey={selectedStatus}
              onSelectionChange={(key) => setSelectedStatus(key as string)}
              variant="underlined"
              color="primary"
            >
              <Tab key="all" title="All" />
              <Tab key="pending" title="Pending" />
              <Tab key="matched" title="Matched" />
              <Tab key="in-transit" title="In Transit" />
              <Tab key="completed" title="Completed" />
            </Tabs>
          </div>
        </CardBody>
      </Card>

      {/* Orders Table */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-0">
          <Table aria-label="Orders table" removeWrapper>
            <TableHeader>
              <TableColumn>Order ID</TableColumn>
              <TableColumn>Cargo</TableColumn>
              <TableColumn>Type</TableColumn>
              <TableColumn>Weight</TableColumn>
              <TableColumn>Route</TableColumn>
              <TableColumn>Budget</TableColumn>
              <TableColumn>Urgency</TableColumn>
              <TableColumn>Status</TableColumn>
              <TableColumn>Actions</TableColumn>
            </TableHeader>
            <TableBody>
              {filteredOrders.map((order) => (
                <TableRow key={order.id} className="hover:bg-white/5 transition">
                  <TableCell>
                    <Chip variant="flat" size="sm" color="primary">{order.id}</Chip>
                  </TableCell>
                  <TableCell className="font-semibold text-foreground">{order.cargo}</TableCell>
                  <TableCell>
                    <Chip size="sm" variant="flat">{order.type}</Chip>
                  </TableCell>
                  <TableCell>{order.weight}</TableCell>
                  <TableCell className="text-muted">{order.route}</TableCell>
                  <TableCell className="font-semibold">{order.budget}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span>{'🔥'.repeat(Math.min(order.urgency, 3))}</span>
                      <span className="text-xs text-muted">{order.urgency}/10</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Chip color={statusColor(order.status)} size="sm" variant="flat">
                      {order.status}
                    </Chip>
                  </TableCell>
                  <TableCell>
                    <Dropdown>
                      <DropdownTrigger>
                        <Button variant="light" size="sm" isIconOnly>⋮</Button>
                      </DropdownTrigger>
                      <DropdownMenu>
                        <DropdownItem key="view">View Details</DropdownItem>
                        <DropdownItem key="edit">Edit Order</DropdownItem>
                        <DropdownItem key="match" color="primary">Run AI Matching</DropdownItem>
                        <DropdownItem key="cancel" color="danger">Cancel Order</DropdownItem>
                      </DropdownMenu>
                    </Dropdown>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
};

export default Orders;
