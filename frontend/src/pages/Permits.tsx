import React from 'react';
import {
  Card, CardHeader, CardBody, Button, Chip, Divider, Progress,
  Table, TableHeader, TableColumn, TableBody, TableRow, TableCell, Alert
} from '@heroui/react';

interface Permit {
  id: string;
  type: string;
  country: string;
  status: 'Available' | 'Reserved' | 'Issued' | 'In Use' | 'Returned' | 'Expired';
  quota_total: number;
  quota_used: number;
  deficit: boolean;
}

const mockPermits: Permit[] = [
  { id: 'PMT-001', type: 'Bilateral', country: 'Russia (RU)', status: 'Available', quota_total: 1000, quota_used: 850, deficit: false },
  { id: 'PMT-002', type: 'Transit', country: 'Kazakhstan (KZ)', status: 'Available', quota_total: 500, quota_used: 320, deficit: false },
  { id: 'PMT-003', type: 'Third Country', country: 'China (CN)', status: 'Reserved', quota_total: 200, quota_used: 195, deficit: true },
  { id: 'PMT-004', type: 'Bilateral', country: 'Turkey (TR)', status: 'Issued', quota_total: 300, quota_used: 280, deficit: false },
  { id: 'PMT-005', type: 'Transit', country: 'Kyrgyzstan (KG)', status: 'Available', quota_total: 400, quota_used: 150, deficit: false },
  { id: 'PMT-006', type: 'Bilateral', country: 'Tajikistan (TJ)', status: 'Available', quota_total: 250, quota_used: 180, deficit: false },
];

const Permits: React.FC = () => {
  const statusColor = (status: string) => {
    switch (status) {
      case 'Available': return 'success';
      case 'Reserved': return 'warning';
      case 'Issued': return 'primary';
      case 'In Use': return 'secondary';
      case 'Returned': return 'success';
      case 'Expired': return 'danger';
      default: return 'default';
    }
  };

  const deficitPermits = mockPermits.filter(p => p.deficit);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Permit Management</h1>
          <p className="text-muted mt-1">Manage ruhsatnoma and international permits</p>
        </div>
        <Button color="primary">Apply for Permit</Button>
      </div>

      {/* Deficit Alerts */}
      {deficitPermits.length > 0 && (
        <Card className="bg-danger/10 border border-danger/30">
          <CardBody className="p-4">
            <div className="flex items-center gap-3">
              <span className="text-2xl">️</span>
              <div className="flex-1">
                <h4 className="font-bold text-danger">Permit Deficit Alert</h4>
                <p className="text-sm text-muted">
                  {deficitPermits.length} routes experiencing permit shortage. Apply early!
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-2 mt-3">
              {deficitPermits.map((permit) => (
                <Chip key={permit.id} color="danger" variant="flat">
                  {permit.country} - {permit.quota_total - permit.quota_used} remaining
                </Chip>
              ))}
            </div>
          </CardBody>
        </Card>
      )}

      {/* AI Prediction Card */}
      <Card className="bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
        <CardBody className="p-6">
          <div className="flex items-center gap-4">
            <div className="text-4xl">🤖</div>
            <div className="flex-1">
              <h3 className="text-lg font-bold text-foreground">AI Permit Forecast</h3>
              <p className="text-muted text-sm">Next 30 days prediction based on historical data</p>
            </div>
            <Button color="primary" variant="flat">View Full Forecast</Button>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="text-center">
              <p className="text-2xl font-bold text-warning">China</p>
              <p className="text-xs text-muted">Deficit likely in 2 weeks</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-success">Russia</p>
              <p className="text-xs text-muted">Stable supply</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-success">Kazakhstan</p>
              <p className="text-xs text-muted">Good availability</p>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Quotas Table */}
      <Card className="bg-surface border border-white/10">
        <CardHeader className="px-6 pt-6">
          <h3 className="text-lg font-bold text-foreground">Permit Quotas by Country</h3>
        </CardHeader>
        <Divider />
        <CardBody className="p-0">
          <Table aria-label="Permits table" removeWrapper>
            <TableHeader>
              <TableColumn>Permit ID</TableColumn>
              <TableColumn>Type</TableColumn>
              <TableColumn>Country</TableColumn>
              <TableColumn>Quota Usage</TableColumn>
              <TableColumn>Remaining</TableColumn>
              <TableColumn>Status</TableColumn>
              <TableColumn>Actions</TableColumn>
            </TableHeader>
            <TableBody>
              {mockPermits.map((permit) => {
                const usagePercent = (permit.quota_used / permit.quota_total) * 100;
                const remaining = permit.quota_total - permit.quota_used;
                return (
                  <TableRow key={permit.id} className="hover:bg-white/5 transition">
                    <TableCell>
                      <Chip variant="flat" size="sm">{permit.id}</Chip>
                    </TableCell>
                    <TableCell>
                      <Chip size="sm" variant="flat">{permit.type}</Chip>
                    </TableCell>
                    <TableCell className="font-semibold text-foreground">{permit.country}</TableCell>
                    <TableCell className="min-w-[200px]">
                      <Progress value={usagePercent} color={usagePercent > 90 ? 'danger' : usagePercent > 70 ? 'warning' : 'success'} size="sm" />
                      <p className="text-xs text-muted mt-1">{permit.quota_used}/{permit.quota_total}</p>
                    </TableCell>
                    <TableCell className={remaining < 50 ? 'text-danger font-bold' : ''}>
                      {remaining}
                    </TableCell>
                    <TableCell>
                      <Chip color={statusColor(permit.status)} size="sm" variant="flat">
                        {permit.status}
                      </Chip>
                    </TableCell>
                    <TableCell>
                      <Button variant="flat" size="sm" color="primary" isDisabled={remaining === 0}>
                        Apply
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardBody>
      </Card>

      {/* Rules Card */}
      <Card className="bg-surface border border-white/10">
        <CardHeader className="px-6 pt-6">
          <h3 className="text-lg font-bold text-foreground">Permit Rules (from June 2026)</h3>
        </CardHeader>
        <Divider />
        <CardBody className="p-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-foreground mb-3">Quota ≤ 1000 permits</h4>
              <ul className="space-y-2 text-sm text-muted">
                <li>✅ Only round-trip routes with cargo</li>
                <li>✅ Profitability coefficient ≥ 1.0 required</li>
                <li>✅ Priority to experienced carriers</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-foreground mb-3">Quota &gt; 1000 permits</h4>
              <ul className="space-y-2 text-sm text-muted">
                <li>✅ Available to all carriers (with cargo)</li>
                <li>✅ Empty return: coefficient ≥ 0.7</li>
                <li>✅ Based on number of vehicles</li>
              </ul>
            </div>
          </div>
          <Divider className="my-4" />
          <div className="flex items-center gap-3 p-4 rounded-lg bg-primary/10">
            <span className="text-2xl"></span>
            <div>
              <p className="font-semibold text-foreground">Permit Fee</p>
              <p className="text-sm text-muted">82,500 UZS (1/4 BRV) per permit. Must return within 90 days.</p>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  );
};

export default Permits;
