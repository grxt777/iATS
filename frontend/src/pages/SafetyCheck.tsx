import React, { useState } from 'react';
import {
  Card, CardHeader, CardBody, Button, Input, Chip, Divider, Progress,
  Tabs, Tab, Alert
} from '@heroui/react';

const SafetyCheck: React.FC = () => {
  const [cargoName, setCargoName] = useState('');
  const [result, setResult] = useState<any>(null);

  const handleCheck = () => {
    if (!cargoName) return;

    const mockResult = {
      cargo_name: cargoName,
      detected_type: cargoName.toLowerCase().includes('apple') || cargoName.toLowerCase().includes('fruit') ? 'perishable' : 'general',
      adr_class: null,
      is_dangerous: false,
      is_perishable: cargoName.toLowerCase().includes('apple') || cargoName.toLowerCase().includes('fruit'),
      risk_score: 25,
      risk_level: 'low',
      required_documents: ['ettn', 'waybill', 'license', 'phytosanitary', 'sanitary'],
      documents_provided: ['ettn', 'waybill', 'license'],
      route_restrictions: [],
      special_requirements: ['temperature_control', 'ventilation'],
    };

    setResult(mockResult);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Cargo Safety Checker</h1>
        <p className="text-muted mt-1">AI-powered cargo classification and safety validation</p>
      </div>

      {/* Input Card */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-6">
          <div className="flex gap-4 items-end">
            <Input
              label="Cargo Name or Description"
              placeholder="e.g., Fresh Apples, Ammonium Nitrate, Electronics..."
              value={cargoName}
              onChange={(e) => setCargoName(e.target.value)}
              className="max-w-xl"
            />
            <Button color="primary" onPress={handleCheck}>
              Check Safety
            </Button>
          </div>
        </CardBody>
      </Card>

      {result && (
        <>
          {/* Risk Overview */}
          <div className="grid grid-cols-3 gap-4">
            <Card className="bg-surface border border-white/10">
              <CardBody className="p-6">
                <p className="text-sm text-muted mb-2">Risk Level</p>
                <div className="flex items-center gap-3">
                  <Chip color="success" size="lg" variant="flat">{result.risk_level.toUpperCase()}</Chip>
                </div>
                <Progress value={result.risk_score} color="success" className="mt-4" />
                <p className="text-xs text-muted mt-2">Risk Score: {result.risk_score}/100</p>
              </CardBody>
            </Card>

            <Card className="bg-surface border border-white/10">
              <CardBody className="p-6">
                <p className="text-sm text-muted mb-2">Cargo Classification</p>
                <div className="flex flex-wrap gap-2">
                  <Chip color="primary" variant="flat">{result.detected_type}</Chip>
                  {result.is_perishable && <Chip color="warning" variant="flat">Perishable</Chip>}
                  {result.is_dangerous && <Chip color="danger" variant="flat">Dangerous</Chip>}
                </div>
                <p className="text-xs text-muted mt-4">
                  Detected: {result.cargo_name}
                </p>
              </CardBody>
            </Card>

            <Card className="bg-surface border border-white/10">
              <CardBody className="p-6">
                <p className="text-sm text-muted mb-2">Documents Status</p>
                <div className="text-2xl font-bold text-warning">
                  {result.documents_provided.length}/{result.required_documents.length}
                </div>
                <Progress
                  value={(result.documents_provided.length / result.required_documents.length) * 100}
                  color="warning"
                  className="mt-4"
                />
                <p className="text-xs text-muted mt-2">
                  {result.required_documents.length - result.documents_provided.length} missing
                </p>
              </CardBody>
            </Card>
          </div>

          {/* Documents Section */}
          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-surface border border-white/10">
              <CardHeader className="px-6 pt-6">
                <h3 className="text-lg font-bold text-foreground">Required Documents</h3>
              </CardHeader>
              <Divider />
              <CardBody className="p-6 space-y-3">
                {result.required_documents.map((doc: string) => {
                  const provided = result.documents_provided.includes(doc);
                  return (
                    <div
                      key={doc}
                      className={`flex items-center justify-between p-3 rounded-lg border ${
                        provided ? 'bg-success/10 border-success/30' : 'bg-danger/10 border-danger/30'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span>{provided ? '✅' : '❌'}</span>
                        <span className="text-sm font-semibold capitalize">{doc.replace('_', ' ')}</span>
                      </div>
                      <Chip color={provided ? 'success' : 'danger'} size="sm" variant="flat">
                        {provided ? 'Provided' : 'Missing'}
                      </Chip>
                    </div>
                  );
                })}
              </CardBody>
            </Card>

            <Card className="bg-surface border border-white/10">
              <CardHeader className="px-6 pt-6">
                <h3 className="text-lg font-bold text-foreground">Route Restrictions</h3>
              </CardHeader>
              <Divider />
              <CardBody className="p-6">
                {result.route_restrictions.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-8">
                    <div className="text-4xl mb-2">✅</div>
                    <p className="text-foreground font-semibold">No Restrictions</p>
                    <p className="text-muted text-sm mt-1">This cargo has no route limitations</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {result.route_restrictions.map((r: string, i: number) => (
                      <Alert key={i} color="warning">{r}</Alert>
                    ))}
                  </div>
                )}

                {result.special_requirements.length > 0 && (
                  <>
                    <Divider className="my-4" />
                    <h4 className="font-semibold text-foreground mb-3">Special Requirements</h4>
                    <div className="flex flex-wrap gap-2">
                      {result.special_requirements.map((req: string, i: number) => (
                        <Chip key={i} color="primary" variant="flat">{req}</Chip>
                      ))}
                    </div>
                  </>
                )}
              </CardBody>
            </Card>
          </div>
        </>
      )}

      {/* Empty State */}
      {!result && (
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-12">
            <div className="flex flex-col items-center justify-center gap-4 text-center">
              <div className="text-6xl">🛡️</div>
              <h3 className="text-xl font-bold text-foreground">Check Your Cargo Safety</h3>
              <p className="text-muted max-w-md">
                Enter cargo name to get AI classification, ADR determination, required documents list and route restrictions
              </p>
              <div className="flex gap-3 mt-4">
                <Chip variant="flat">ADR Classification</Chip>
                <Chip variant="flat">Document Checklist</Chip>
                <Chip variant="flat">Route Restrictions</Chip>
              </div>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
};

export default SafetyCheck;
