import React, { useEffect, useState } from 'react';
import './Leaderboard.css';

const Leaderboard = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5000/api/leaderboard');
        if (!response.ok) {
          throw new Error('Failed to fetch leaderboard');
        }
        const data = await response.json();
        setPlayers(data);
      } catch (err) {
        console.error("Error fetching leaderboard", err);
        setError('Failed to load leaderboard. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) {
    return <div className="leaderboard-loading">Loading leaderboard...</div>;
  }

  if (error) {
    return <div className="leaderboard-error">{error}</div>;
  }

  return (
    <div className="leaderboard-container">
      <h2 className="leaderboard-title">🏆 Leaderboard</h2>
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th className="rank-header">Rank</th>
            <th className="name-header">Player</th>
            <th className="points-header">Points</th>
          </tr>
        </thead>
        <tbody>
          {players.length > 0 ? (
            players.map((player, index) => (
              <tr 
                key={player.name} 
                className={`leaderboard-row ${index < 3 ? `top-${index + 1}` : ''}`}
              >
                <td className="rank-cell">
                  {index < 3 ? (
                    <span className="rank-medal">
                      {['🥇', '🥈', '🥉'][index]}
                    </span>
                  ) : (
                    <span className="rank-number">{index + 1}</span>
                  )}
                </td>
                <td className="name-cell">{player.name}</td>
                <td className="points-cell">{player.rank}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" className="no-players">No players found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
