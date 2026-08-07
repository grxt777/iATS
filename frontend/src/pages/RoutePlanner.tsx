import React, { useState } from 'react';
import {
  Card, CardHeader, CardBody, Button, Input, Chip, Divider, Progress, Alert,
  Tabs, Tab
} from '@heroui/react';

const RoutePlanner: React.FC = () => {
  const [pickup, setPickup] = useState('Tashkent');
  const [delivery, setDelivery] = useState('Samarkand');
  const [result, setResult] = useState<any>(null);

  const handlePlan = () => {
    setResult({
      routes: [
        {
          id: 1,
          distance: 270,
          duration: 4.5,
          fuel_cost: 3240000,
          validation_status: 'valid',
          weather: 'Clear',
          segments: 3,
          issues: [],
        },
        {
          id: 2,
          distance: 295,
          duration: 5.2,
          fuel_cost: 3540000,
          validation_status: 'warning',
          weather: 'Light Rain',
          segments: 4,
          issues: ['Road construction on M39', 'Recommended detour via A380'],
        },
      ],
      weather_forecast: [
        { day: 'Today', temp: 32, condition: 'Sunny', impact: 'low' },
        { day: 'Tomorrow', temp: 28, condition: 'Partly Cloudy', impact: 'low' },
        { day: 'Day 3', temp: 25, condition: 'Light Rain', impact: 'medium' },
      ],
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground">AI Route Planner</h1>
        <p className="text-muted mt-1">Smart routing with cargo restrictions, weather and traffic</p>
      </div>

      {/* Input */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-6">
          <div className="grid grid-cols-2 gap-4">
            <Input
              label="Pickup Location"
              value={pickup}
              onChange={(e) => setPickup(e.target.value)}
              placeholder="City or address"
            />
            <Input
              label="Delivery Location"
              value={delivery}
              onChange={(e) => setDelivery(e.target.value)}
              placeholder="City or address"
            />
          </div>
          <Button color="primary" className="mt-4 w-full" onPress={handlePlan}>
            Plan Route with AI
          </Button>
        </CardBody>
      </Card>

      {result && (
        <>
          {/* Weather Forecast */}
          <Card className="bg-surface border border-white/10">
            <CardHeader className="px-6 pt-6">
              <h3 className="text-lg font-bold text-foreground">Weather Forecast</h3>
            </CardHeader>
            <Divider />
            <CardBody className="p-6">
              <div className="grid grid-cols-3 gap-4">
                {result.weather_forecast.map((day: any, i: number) => (
                  <Card key={i} className="bg-primary/5 border border-primary/20">
                    <CardBody className="p-4 text-center">
                      <p className="text-sm font-semibold text-foreground">{day.day}</p>
                      <div className="text-3xl my-2">{day.condition === 'Sunny' ? '☀️' : day.condition === 'Partly Cloudy' ? '⛅' : '️'}</div>
                      <p className="text-2xl font-bold text-foreground">{day.temp}°C</p>
                      <Chip color={day.impact === 'low' ? 'success' : 'warning'} size="sm" className="mt-2">
                        {day.impact} impact
                      </Chip>
                    </CardBody>
                  </Card>
                ))}
              </div>
            </CardBody>
          </Card>

          {/* Routes */}
          <div className="grid grid-cols-2 gap-4">
            {result.routes.map((route: any) => (
              <Card key={route.id} className={`bg-surface border hover:border-primary/30 transition ${
                route.validation_status === 'valid' ? 'border-success/30' : 'border-warning/30'
              }`}>
                <CardHeader className="flex justify-between items-start px-6 pt-6">
                  <div>
                    <div className="flex items-center gap-2">
                      <Chip color={route.validation_status === 'valid' ? 'success' : 'warning'} variant="flat">
                        {route.validation_status === 'valid' ? 'OPTIMAL' : 'ALTERNATIVE'}
                      </Chip>
                      <span className="text-sm text-muted">Route #{route.id}</span>
                    </div>
                  </div>
                </CardHeader>
                <Divider />
                <CardBody className="p-6">
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-muted">Distance</p>
                      <p className="text-xl font-bold text-foreground">{route.distance} km</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted">Duration</p>
                      <p className="text-xl font-bold text-foreground">{route.duration} h</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted">Fuel Cost</p>
                      <p className="text-xl font-bold text-primary">{(route.fuel_cost / 1000).toFixed(0)}K UZS</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted">Weather</p>
                      <p className="text-xl font-bold text-foreground">{route.weather}</p>
                    </div>
                  </div>

                  {route.issues.length > 0 && (
                    <>
                      <Divider className="my-3" />
                      <div className="space-y-2">
                        {route.issues.map((issue: string, i: number) => (
                          <Alert key={i} color="warning" title="Warning">{issue}</Alert>
                        ))}
                      </div>
                    </>
                  )}
                </CardBody>
                <Divider />
                <Card className="bg-surface border-0 rounded-none">
                  <CardBody className="p-4">
                    <Button color="primary" fullWidth>
                      {route.id === 1 ? 'Select This Route' : 'View Alternative'}
                    </Button>
                  </CardBody>
                </Card>
              </Card>
            ))}
          </div>
        </>
      )}

      {!result && (
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-12">
            <div className="flex flex-col items-center justify-center gap-4 text-center">
              <div className="text-6xl">️</div>
              <h3 className="text-xl font-bold text-foreground">Plan Your Route</h3>
              <p className="text-muted max-w-md">
                Enter pickup and delivery locations to get AI-optimized routes with weather, traffic and cargo restrictions
              </p>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
};

export default RoutePlanner;
