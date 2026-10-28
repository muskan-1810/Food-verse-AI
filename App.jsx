import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';

// Component/Pages placeholder components
function Dashboard() {
  return <h2>Welcome to Food-Verse AI Dashboard</h2>;
}
function FoodRecognition() {
  return <h2>Food Recognition & Nutrition Module</h2>;
}
function FreshnessDetector() {
  return <h2>Food Freshness & Spoilage Detection</h2>;
}
function HygieneMonitor() {
  return <h2>Restaurant Hygiene & Smart Kitchen Monitor</h2>;
}
function MealPlanner() {
  return <h2>Personalized Meal Planner</h2>;
}

function App() {
  return (
    <Router>
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <nav style={{ background: '#2c3e50', color: '#fff', padding: '15px', borderRadius: '8px', marginBottom: '20px', display: 'flex', gap: '15px' }}>
          <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>Dashboard</Link>
          <Link to="/food-recognition" style={{ color: '#fff', textDecoration: 'none' }}>Food Recognition</Link>
          <Link to="/freshness" style={{ color: '#fff', textDecoration: 'none' }}>Freshness</Link>
          <Link to="/hygiene" style={{ color: '#fff', textDecoration: 'none' }}>Hygiene</Link>
          <Link to="/meal-planner" style={{ color: '#fff', textDecoration: 'none' }}>Meal Planner</Link>
        </nav>

        <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px', minHeight: '300px' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/food-recognition" element={<FoodRecognition />} />
            <Route path="/freshness" element={<FreshnessDetector />} />
            <Route path="/hygiene" element={<HygieneMonitor />} />
            <Route path="/meal-planner" element={<MealPlanner />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;