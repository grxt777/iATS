import React, { useState } from 'react';
import {
  Card, CardHeader, CardBody, Button, Input, Chip, Divider,
  Tabs, Tab, Progress, User, Badge, Tooltip
} from '@heroui/react';

interface Vehicle {
  id: number;
  type: string;
  brand: string;
  model: string;
  plate: string;
  capacity: string;
  status: 'Available' | 'In Transit' | 'Maintenance' | 'Offline';
  driver: string;
  rating: number;
  trips: number;
  location: string;
}

const mockVehicles: Vehicle[] = [
  { id: 1, type: 'Truck Large', brand: 'MAN', model: 'TGX', plate: '01 777 AAA', capacity: '22t / 80m³', status: 'Available', driver: 'Alisher Qodirov', rating: 4.9, trips: 247, location: 'Tashkent Depot' },
  { id: 2, type: 'Refrigerator', brand: 'Volvo', model: 'FH16', plate: '01 456 BCD', capacity: '20t / 70m³', status: 'In Transit', driver: 'Rustam Mirzayev', rating: 4.7, trips: 189, location: 'Tashkent → Samarkand' },
  { id: 3, type: 'Flatbed', brand: 'Scania', model: 'R500', plate: '01 123 EFG', capacity: '25t / 120m³', status: 'Available', driver: 'Jamshid Turaev', rating: 4.8, trips: 156, location: 'Fergana Hub' },
  { id: 4, type: 'Tanker', brand: 'Mercedes', model: 'Actros', plate: '01 888 HIJ', capacity: '30t / 40m³', status: 'Maintenance', driver: '—', rating: 4.6, trips: 98, location: 'Service Center' },
  { id: 5, type: 'Van', brand: 'Ford', model: 'Transit', plate: '01 333 KLM', capacity: '3t / 15m³', status: 'Available', driver: 'Sardor Aliyev', rating: 4.5, trips: 312, location: 'Tashkent City' },
  { id: 6, type: 'Container', brand: 'DAF', model: 'XF', plate: '01 555 NOP', capacity: '28t / 90m³', status: 'In Transit', driver: 'Bobur Karimov', rating: 4.9, trips: 201, location: 'Bukhara → Navoi' },
];

const Vehicles: React.FC = () => {
  const [search, setSearch] = useState('');
  const [selectedType, setSelectedType] = useState('all');

  const filteredVehicles = mockVehicles.filter(v => {
    const matchesSearch = v.brand.toLowerCase().includes(search.toLowerCase()) || 
                          v.plate.toLowerCase().includes(search.toLowerCase()) ||
                          v.driver.toLowerCase().includes(search.toLowerCase());
    const matchesType = selectedType === 'all' || v.type.toLowerCase() === selectedType;
    return matchesSearch && matchesType;
  });

  const statusColor = (status: string) => {
    switch (status) {
      case 'Available': return 'success';
      case 'In Transit': return 'primary';
      case 'Maintenance': return 'warning';
      case 'Offline': return 'danger';
      default: return 'default';
    }
  };

  const stats = {
    total: mockVehicles.length,
    available: mockVehicles.filter(v => v.status === 'Available').length,
    inTransit: mockVehicles.filter(v => v.status === 'In Transit').length,
    maintenance: mockVehicles.filter(v => v.status === 'Maintenance').length,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Fleet Management</h1>
          <p className="text-muted mt-1">Track and manage all vehicles in the system</p>
        </div>
        <Button color="primary">+ Add Vehicle</Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">🚛</div>
              <div>
                <p className="text-sm text-muted">Total Fleet</p>
                <p className="text-2xl font-bold text-foreground">{stats.total}</p>
              </div>
            </div>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-success/20 flex items-center justify-center">✅</div>
              <div>
                <p className="text-sm text-muted">Available</p>
                <p className="text-2xl font-bold text-success">{stats.available}</p>
              </div>
            </div>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center">️</div>
              <div>
                <p className="text-sm text-muted">In Transit</p>
                <p className="text-2xl font-bold text-primary">{stats.inTransit}</p>
              </div>
            </div>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center">🔧</div>
              <div>
                <p className="text-sm text-muted">Maintenance</p>
                <p className="text-2xl font-bold text-warning">{stats.maintenance}</p>
              </div>
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Filters */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-4">
          <div className="flex gap-4 items-center">
            <Input
              placeholder="Search by brand, plate or driver..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="max-w-md"
              startContent={🔍}
            />
            <Tabs
              selectedKey={selectedType}
              onSelectionChange={(key) => setSelectedType(key as string)}
              variant="underlined"
              color="primary"
            >
              <Tab key="all" title="All Types" />
              <Tab key="truck large" title="Large Trucks" />
              <Tab key="refrigerator" title="Refrigerators" />
              <Tab key="flatbed" title="Flatbeds" />
              <Tab key="tanker" title="Tankers" />
            </Tabs>
          </div>
        </CardBody>
      </Card>

      {/* Vehicles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filteredVehicles.map((vehicle) => (
          <Card
            key={vehicle.id}
            className="bg-surface border border-white/10 hover:border-primary/30 transition-all hover:scale-105"
          >
            <CardHeader className="flex justify-between items-start px-6 pt-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full gradient-primary flex items-center justify-center text-xl">
                  
                </div>
                <div>
                  <h3 className="font-bold text-foreground">{vehicle.brand} {vehicle.model}</h3>
                  <p className="text-sm text-muted">{vehicle.type}</p>
                </div>
              </div>
              <Chip color={statusColor(vehicle.status)} size="sm" variant="flat">
                {vehicle.status}
              </Chip>
            </CardHeader>
            <Divider />
            <CardBody className="p-6">
              <div className="space-y-3">
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-sm text-muted">Plate Number</span>
                  <span className="text-sm font-semibold text-foreground">{vehicle.plate}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-sm text-muted">Capacity</span>
                  <span className="text-sm font-semibold text-foreground">{vehicle.capacity}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-white/5">
                  <span className="text-sm text-muted">Location</span>
                  <span className="text-sm font-semibold text-primary">{vehicle.location}</span>
                </div>
                <div className="flex justify-between items-center py-2">
                  <div className="flex items-center gap-2">
                    <User
                      name={vehicle.driver}
                      description={Total trips: {vehicle.trips}}
                      avatarProps={{ showFallback: true }}
                    />
                  </div>
                  <div className="flex items-center gap-1">
                    <span>⭐</span>
                    <span className="font-semibold">{vehicle.rating}</span>
                  </div>
                </div>
              </div>
            </CardBody>
            <Divider />
            <Card className="bg-primary/5 border-0 rounded-none">
              <CardBody className="p-3">
                <div className="flex justify-between text-xs">
                  <span className="text-muted">Reliability Score</span>
                  <span className="font-bold text-primary">{(vehicle.rating * 20).toFixed(0)}%</span>
                </div>
                <Progress value={vehicle.rating * 20} color="primary" size="sm" className="mt-2" />
              </CardBody>
            </Card>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Vehicles;
