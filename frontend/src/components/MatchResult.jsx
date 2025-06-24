import React, { useState } from 'react';
import './MatchResult.css';

const MatchResult = () => {
  const [winner, setWinner] = useState('');
  const [loser, setLoser] = useState('');
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const reportMatch = (e) => {
    e.preventDefault();
    if (!winner.trim() || !loser.trim()) {
      setMessage('Please fill in both fields');
      return;
    }
    
    setIsSubmitting(true);
    setMessage('');
    
    fetch('http://127.0.0.1:5000/api/report_result', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ winner: winner.trim(), loser: loser.trim() })
    })
      .then(res => res.json())
      .then(data => {
        setMessage(data.message);
        if (data.message.includes('recorded')) {
          setWinner('');
          setLoser('');
        }
      })
      .catch(err => {
        setMessage('Error submitting match result');
        console.error('Error:', err);
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  };

  return (
    <div className="match-result-container">
      <h2 className="match-result-title">Report Match Result</h2>
      <form onSubmit={reportMatch}>
        <div className="input-group">
          <label htmlFor="winner">Winner's Name</label>
          <input
            id="winner"
            type="text"
            className="input-field"
            placeholder="Enter winner's name"
            value={winner}
            onChange={(e) => setWinner(e.target.value)}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="loser">Loser's Name</label>
          <input
            id="loser"
            type="text"
            className="input-field"
            placeholder="Enter loser's name"
            value={loser}
            onChange={(e) => setLoser(e.target.value)}
            required
          />
        </div>
        <button 
          type="submit" 
          className="submit-button"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Match Result'}
        </button>
        {message && (
          <p className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
};

export default MatchResult;
