import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Orders from './pages/Orders';
import Vehicles from './pages/Vehicles';
import Matching from './pages/Matching';
import SafetyCheck from './pages/SafetyCheck';
import RoutePlanner from './pages/RoutePlanner';
import Documents from './pages/Documents';
import Permits from './pages/Permits';
import Analytics from './pages/Analytics';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      retry: 2,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="orders" element={<Orders />} />
              <Route path="vehicles" element={<Vehicles />} />
              <Route path="matching" element={<Matching />} />
              <Route path="safety" element={<SafetyCheck />} />
              <Route path="routing" element={<RoutePlanner />} />
              <Route path="documents" element={<Documents />} />
              <Route path="permits" element={<Permits />} />
              <Route path="analytics" element={<Analytics />} />
            </Route>
          </Routes>
          <Toaster position="top-right" />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
