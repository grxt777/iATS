import React from 'react';
import {
  Card, CardHeader, CardBody, Button, Chip, Divider, Progress,
  Table, TableHeader, TableColumn, TableBody, TableRow, TableCell,
  Tabs, Tab, Badge
} from '@heroui/react';

interface Document {
  id: string;
  type: string;
  name: string;
  order: string;
  status: 'Verified' | 'Pending' | 'Expired' | 'Rejected';
  expiry: string;
  uploaded: string;
}

const mockDocuments: Document[] = [
  { id: 'DOC-001', type: 'ETTN', name: 'Electronic Waybill #1247', order: '#1247', status: 'Verified', expiry: '2026-08-10', uploaded: '2026-08-06' },
  { id: 'DOC-002', type: 'Phytosanitary', name: 'Phytosanitary Certificate - Apples', order: '#1247', status: 'Verified', expiry: '2026-08-21', uploaded: '2026-08-05' },
  { id: 'DOC-003', type: 'License', name: 'Carrier License - TransService', order: '#1246', status: 'Verified', expiry: '2027-01-15', uploaded: '2026-01-15' },
  { id: 'DOC-004', type: 'ADR Certificate', name: 'Driver DOPOG - Alisher Q.', order: '#1243', status: 'Pending', expiry: '2026-09-30', uploaded: '2026-08-06' },
  { id: 'DOC-005', type: 'CMR', name: 'International CMR - Kazakhstan', order: '#1240', status: 'Verified', expiry: '2026-08-15', uploaded: '2026-08-04' },
  { id: 'DOC-006', type: 'Insurance', name: 'Cargo Insurance Policy', order: '#1245', status: 'Expired', expiry: '2026-07-30', uploaded: '2026-01-30' },
];

const Documents: React.FC = () => {
  const statusColor = (status: string) => {
    switch (status) {
      case 'Verified': return 'success';
      case 'Pending': return 'warning';
      case 'Expired': return 'danger';
      case 'Rejected': return 'danger';
      default: return 'default';
    }
  };

  const stats = {
    total: mockDocuments.length,
    verified: mockDocuments.filter(d => d.status === 'Verified').length,
    pending: mockDocuments.filter(d => d.status === 'Pending').length,
    expired: mockDocuments.filter(d => d.status === 'Expired').length,
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Document Management</h1>
          <p className="text-muted mt-1">Track and verify all shipping documents</p>
        </div>
        <Button color="primary">+ Upload Document</Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Total Documents</p>
            <p className="text-2xl font-bold text-foreground">{stats.total}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Verified</p>
            <p className="text-2xl font-bold text-success">{stats.verified}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Pending Review</p>
            <p className="text-2xl font-bold text-warning">{stats.pending}</p>
          </CardBody>
        </Card>
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-4">
            <p className="text-sm text-muted">Expired</p>
            <p className="text-2xl font-bold text-danger">{stats.expired}</p>
          </CardBody>
        </Card>
      </div>

      {/* Verification Progress */}
      <Card className="bg-surface border border-white/10">
        <CardHeader className="px-6 pt-6">
          <h3 className="text-lg font-bold text-foreground">Document Verification Progress</h3>
        </CardHeader>
        <Divider />
        <CardBody className="p-6">
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-muted">Verified Documents</span>
                <span className="text-success font-semibold">{((stats.verified / stats.total) * 100).toFixed(0)}%</span>
              </div>
              <Progress value={(stats.verified / stats.total) * 100} color="success" size="sm" />
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-muted">Pending Review</span>
                <span className="text-warning font-semibold">{((stats.pending / stats.total) * 100).toFixed(0)}%</span>
              </div>
              <Progress value={(stats.pending / stats.total) * 100} color="warning" size="sm" />
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Documents Table */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-0">
          <Table aria-label="Documents table" removeWrapper>
            <TableHeader>
              <TableColumn>ID</TableColumn>
              <TableColumn>Type</TableColumn>
              <TableColumn>Document Name</TableColumn>
              <TableColumn>Order</TableColumn>
              <TableColumn>Status</TableColumn>
              <TableColumn>Expiry Date</TableColumn>
              <TableColumn>Actions</TableColumn>
            </TableHeader>
            <TableBody>
              {mockDocuments.map((doc) => (
                <TableRow key={doc.id} className="hover:bg-white/5 transition">
                  <TableCell>
                    <Chip variant="flat" size="sm">{doc.id}</Chip>
                  </TableCell>
                  <TableCell>
                    <Chip size="sm" variant="flat" color="primary">{doc.type}</Chip>
                  </TableCell>
                  <TableCell className="font-semibold text-foreground">{doc.name}</TableCell>
                  <TableCell>
                    <Chip size="sm" variant="flat">{doc.order}</Chip>
                  </TableCell>
                  <TableCell>
                    <Badge color={statusColor(doc.status)} variant="flat" shape="circle" content="">
                      <Chip color={statusColor(doc.status)} size="sm" variant="flat">
                        {doc.status}
                      </Chip>
                    </Badge>
                  </TableCell>
                  <TableCell className={doc.status === 'Expired' ? 'text-danger font-semibold' : ''}>
                    {doc.expiry}
                  </TableCell>
                  <TableCell>
                    <Button variant="flat" size="sm" color="primary">View</Button>
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

export default Documents;
