import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/leaderboard')
      .then(res => res.json())
      .then(data => setPlayers(data))
      .catch(err => console.error("Error fetching leaderboard", err));
  }, []);

  return (
    <div>
      <h2>🏆 Leaderboard</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Name</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, index) => (
            <tr key={p.name}>
              <td>{index + 1}</td>
              <td>{p.name}</td>
              <td>{p.rank}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
