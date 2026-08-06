import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Input,
  Progress,
  Chip,
  Divider,
  Spinner,
  Tooltip,
  Badge,
  User,
  Skeleton
} from '@heroui/react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface MatchingResult {
  vehicle_id: number;
  rank: number;
  overall_score: number;
  confidence: string;
  driver_name: string;
  vehicle_type: string;
  license_plate: string;
  current_distance_km: number;
  estimated_cost_uzs: number;
  explanation: string;
}

const Matching: React.FC = () => {
  const [orderId, setOrderId] = useState<string>('1');
  const [results, setResults] = useState<MatchingResult[]>([]);

  const matchingMutation = useMutation({
    mutationFn: (orderId: number) =>
      axios.post(`${API_URL}/api/v1/matching/`, { order_id: orderId, top_k: 5 }),
    onSuccess: (response) => {
      setResults(response.data.results || []);
      toast.success(`Found ${response.data.results?.length || 0} matches in ${response.data.processing_time_ms}ms`);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Matching failed');
    }
  });

  const handleFindMatches = () => {
    if (!orderId) {
      toast.error('Please enter Order ID');
      return;
    }
    matchingMutation.mutate(parseInt(orderId));
  };

  const getConfidenceColor = (confidence: string) => {
    switch (confidence) {
      case 'high': return 'success';
      case 'medium': return 'warning';
      case 'low': return 'danger';
      default: return 'default';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">AI Smart Matching</h1>
          <p className="text-muted mt-1">Find the best vehicle for your cargo using AI</p>
        </div>
        <Chip color="primary" variant="flat" size="lg">
          ML Powered
        </Chip>
      </div>

      {/* Search Section */}
      <Card className="bg-surface border border-white/10">
        <CardBody className="p-6">
          <div className="flex gap-4 items-end">
            <Input
              label="Order ID"
              placeholder="Enter order ID"
              type="number"
              value={orderId}
              onChange={(e) => setOrderId(e.target.value)}
              className="max-w-xs"
              classNames={{
                label: 'text-muted',
                input: 'text-foreground',
              }}
            />
            <Button
              color="primary"
              size="lg"
              onPress={handleFindMatches}
              isLoading={matchingMutation.isPending}
            >
              {matchingMutation.isPending ? 'AI Analyzing...' : 'Find Best Matches'}
            </Button>
          </div>
        </CardBody>
      </Card>

      {/* Loading State */}
      {matchingMutation.isPending && (
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-12">
            <div className="flex flex-col items-center justify-center gap-4">
              <Spinner size="lg" color="primary" />
              <div className="text-center">
                <h3 className="text-lg font-semibold text-foreground">AI is analyzing vehicles...</h3>
                <p className="text-muted mt-2">Calculating compatibility scores using XGBoost model</p>
              </div>
              <Progress size="sm" isIndeterminate className="max-w-md" />
            </div>
          </CardBody>
        </Card>
      )}

      {/* Results */}
      {results.length > 0 && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-foreground">
              Top Matches
              <Chip color="primary" variant="flat" className="ml-3">
                {results.length} vehicles
              </Chip>
            </h2>
            <Chip color="success" variant="flat">
              Processed in {matchingMutation.data?.data?.processing_time_ms || 0}ms
            </Chip>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {results.map((result, index) => (
              <Card
                key={result.vehicle_id}
                className={`bg-surface border hover:border-primary/50 transition-all hover:scale-105 ${
                  index === 0 ? 'border-primary/30' : 'border-white/10'
                }`}
              >
                <CardHeader className="flex justify-between items-start px-6 pt-6">
                  <div className="flex items-center gap-3">
                    <Badge
                      content={`#${result.rank}`}
                      color={index === 0 ? 'primary' : 'default'}
                      shape="circle"
                    >
                      <div className="w-12 h-12 rounded-full gradient-primary flex items-center justify-center text-xl">
                        
                      </div>
                    </Badge>
                    <div>
                      <h3 className="font-bold text-foreground">Vehicle #{result.vehicle_id}</h3>
                      <p className="text-sm text-muted">{result.vehicle_type}</p>
                    </div>
                  </div>
                  <Chip
                    color={getConfidenceColor(result.confidence)}
                    variant="flat"
                    size="sm"
                  >
                    {result.confidence.toUpperCase()}
                  </Chip>
                </CardHeader>

                <Divider />

                <CardBody className="p-6">
                  {/* Score Circle */}
                  <div className="flex items-center gap-4 mb-4">
                    <div className="relative w-20 h-20">
                      <svg className="w-full h-full transform -rotate-90">
                        <circle
                          cx="40"
                          cy="40"
                          r="35"
                          stroke="currentColor"
                          strokeWidth="8"
                          fill="transparent"
                          className="text-white/10"
                        />
                        <circle
                          cx="40"
                          cy="40"
                          r="35"
                          stroke="url(#gradient)"
                          strokeWidth="8"
                          fill="transparent"
                          strokeDasharray={`${(result.overall_score / 100) * 220} 220`}
                          strokeLinecap="round"
                        />
                        <defs>
                          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#006FEE" />
                            <stop offset="100%" stopColor="#7828C8" />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-2xl font-bold text-foreground">{result.overall_score}</span>
                        <span className="text-xs text-muted">/ 100</span>
                      </div>
                    </div>
                    <div className="flex-1">
                      <p className="text-sm text-muted mb-1">Compatibility Score</p>
                      <Progress
                        value={result.overall_score}
                        color="primary"
                        size="sm"
                        className="max-w-full"
                      />
                    </div>
                  </div>

                  {/* Details */}
                  <div className="space-y-3">
                    <div className="flex justify-between items-center py-2 border-b border-white/5">
                      <span className="text-sm text-muted">License Plate</span>
                      <span className="text-sm font-semibold text-foreground">{result.license_plate}</span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-white/5">
                      <span className="text-sm text-muted">Distance</span>
                      <span className="text-sm font-semibold text-foreground">{result.current_distance_km} km</span>
                    </div>
                    <div className="flex justify-between items-center py-2">
                      <span className="text-sm text-muted">Est. Cost</span>
                      <span className="text-sm font-semibold text-primary">{(result.estimated_cost_uzs / 1000).toFixed(0)}K UZS</span>
                    </div>
                  </div>
                </CardBody>

                <Divider />

                <CardFooter className="px-6 pb-6 pt-4">
                  <div className="w-full space-y-3">
                    <div className="p-3 rounded-lg bg-primary/10 border border-primary/20">
                      <p className="text-xs font-semibold text-primary mb-1">Why this match?</p>
                      <p className="text-xs text-muted">{result.explanation}</p>
                    </div>
                    <Button color="primary" fullWidth>
                      Select This Vehicle
                    </Button>
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {results.length === 0 && !matchingMutation.isPending && (
        <Card className="bg-surface border border-white/10">
          <CardBody className="p-12">
            <div className="flex flex-col items-center justify-center gap-4 text-center">
              <div className="text-6xl">🤖</div>
              <h3 className="text-xl font-bold text-foreground">Ready to Find Matches</h3>
              <p className="text-muted max-w-md">
                Enter an Order ID and click "Find Best Matches" to see AI recommendations powered by XGBoost
              </p>
              <div className="flex gap-4 mt-4">
                <Chip variant="flat">XGBoost ML</Chip>
                <Chip variant="flat">15+ Features</Chip>
                <Chip variant="flat">&lt; 1s Response</Chip>
              </div>
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
};

export default Matching;
