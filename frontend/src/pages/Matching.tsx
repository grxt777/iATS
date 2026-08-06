import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import toast from 'react-hot-toast';
import './Matching.css';

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
      case 'high': return 'green';
      case 'medium': return 'yellow';
      case 'low': return 'red';
      default: return 'gray';
    }
  };

  return (
    <div className="matching-page">
      <div className="page-header">
        <h1>AI Smart Matching</h1>
        <p>Find the best vehicle for your cargo using AI</p>
      </div>
      
      <div className="matching-controls">
        <div className="input-group">
          <label>Order ID</label>
          <input
            type="number"
            value={orderId}
            onChange={(e) => setOrderId(e.target.value)}
            placeholder="Enter order ID"
          />
        </div>
        <button
          onClick={handleFindMatches}
          disabled={matchingMutation.isPending}
          className="find-button"
        >
          {matchingMutation.isPending ? 'AI is analyzing...' : 'Find Best Matches'}
        </button>
      </div>
      
      {matchingMutation.isPending && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>AI is analyzing vehicles and calculating compatibility scores...</p>
        </div>
      )}
      
      {results.length > 0 && (
        <div className="results-section">
          <h2>Top Matches ({results.length})</h2>
          <div className="results-grid">
            {results.map((result, index) => (
              <div key={result.vehicle_id} className="match-card">
                <div className="match-header">
                  <span className="match-rank">#{result.rank}</span>
                  <span className={`match-confidence ${getConfidenceColor(result.confidence)}`}>
                    {result.confidence.toUpperCase()}
                  </span>
                </div>
                
                <div className="match-score">
                  <div className="score-circle">
                    <span className="score-value">{result.overall_score}</span>
                    <span className="score-label">/ 100</span>
                  </div>
                  <span className="score-text">Compatibility</span>
                </div>
                
                <div className="match-details">
                  <div className="detail-row">
                    <span className="detail-label">Vehicle:</span>
                    <span className="detail-value">{result.vehicle_type}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">License:</span>
                    <span className="detail-value">{result.license_plate}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Distance:</span>
                    <span className="detail-value">{result.current_distance_km} km</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">Est. Cost:</span>
                    <span className="detail-value">{(result.estimated_cost_uzs / 1000).toFixed(0)}K UZS</span>
                  </div>
                </div>
                
                <div className="match-explanation">
                  <strong>Why this match?</strong>
                  <p>{result.explanation}</p>
                </div>
                
                <button className="select-button">
                  Select This Vehicle
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {results.length === 0 && !matchingMutation.isPending && (
        <div className="empty-state">
          <div className="empty-icon">🤖</div>
          <h3>Ready to Find Matches</h3>
          <p>Enter an Order ID and click "Find Best Matches" to see AI recommendations</p>
        </div>
      )}
    </div>
  );
};

export default Matching;
