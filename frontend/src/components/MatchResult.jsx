import React, { useState } from 'react';

const MatchResult = () => {
  const [winner, setWinner] = useState('');
  const [loser, setLoser] = useState('');
  const [message, setMessage] = useState('');

  const reportMatch = () => {
    fetch('http://localhost:5000/api/report_result', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ winner, loser }),
    })
      .then(res => res.json())
      .then(data => {
        setMessage(`${data.message} 🏆 New Ranks: ${winner}: ${data.new_winner_rank}, ${loser}: ${data.new_loser_rank}`);
      })
      .catch(err => {
        setMessage("Error reporting match.");
        console.error(err);
      });
  };

  return (
    <div>
      <h2>Report Match Result</h2>
      <input
        type="text"
        placeholder="Winner name"
        value={winner}
        onChange={(e) => setWinner(e.target.value)}
      />
      <input
        type="text"
        placeholder="Loser name"
        value={loser}
        onChange={(e) => setLoser(e.target.value)}
      />
      <button onClick={reportMatch}>Submit Result</button>
      <p>{message}</p>
    </div>
  );
};

export default MatchResult;
