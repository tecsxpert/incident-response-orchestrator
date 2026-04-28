import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// TODO: Import pages and components
// import List from './pages/List';
// import Detail from './pages/Detail';
// import Form from './pages/Form';
// import Login from './pages/Login';
// import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          {/* TODO: Configure routes */}
          <Route path="/" element={<div>Welcome</div>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
