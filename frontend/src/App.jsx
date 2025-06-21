import React from "react";
import { Routes, Route } from "react-router-dom"; // Remove BrowserRouter
import "./App.css";
import MatchmakingForm from "./components/MatchmakingForm";
import MatchResult from "./components/MatchResult";
import Leaderboard from "./components/Leaderboard";
import MatchHistory from "./components/MatchHistory";
import PlayerProfile from "./components/PlayerProfile";

const Layout = () => (
  <div className="app-layout">
    <div className="left-panel">
      <img
        src="https://images.unsplash.com/photo-1693929291343-f38cb7519d5d?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Gaming Arena"
        className="bg-image"
      />
      <div className="content">
        <h1 className="title">GAMING ARENA</h1>
        <h3 className="subtitle">WELCOME TO MATCHMAKING ARENA</h3>
        <p className="description">
          Step into the battlefield where skill meets strategy.
          Whether you're aggressive, defensive, or just dangerously balanced — this arena finds your perfect rival.
          Ready up, warrior.
        </p>
      </div>
    </div>

    <div className="right-panel" style={{ padding: '20px', overflowY: 'auto' }}>
      <MatchmakingForm />
      <hr />
      <MatchResult />
      <hr />
      <Leaderboard />
      <hr />
      <MatchHistory />
    </div>
  </div>
);

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />} />
      <Route path="/profile/:name" element={<PlayerProfile />} />
    </Routes>
  );
};

export default App;
