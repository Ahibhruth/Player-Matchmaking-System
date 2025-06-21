import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './PlayerProfile.css';

const PlayerProfile = () => {
  const { name } = useParams();
  const navigate = useNavigate();
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    console.log('Fetching player data for:', name);
    const fetchPlayerData = async () => {
      try {
        setLoading(true);
        setError('');
        
        const response = await fetch(`http://localhost:5000/api/player_stats/${encodeURIComponent(name)}`);
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Player data received:', data);
        
        if (!response.ok) {
          throw new Error(data.error || 'Failed to fetch player data');
        }
        
        setPlayer(data);
      } catch (err) {
        console.error('Error in fetchPlayerData:', err);
        setError(err.message || 'Error loading player profile');
      } finally {
        setLoading(false);
      }
    };

    if (name) {
      fetchPlayerData();
    } else {
      setError('No player name provided');
      setLoading(false);
    }
  }, [name]);

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading">Loading player data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
        <div className="error">Error: {error}</div>
        <button onClick={() => navigate('/')} className="back-button">
          Back to Home
        </button>
      </div>
    );
  }

  if (!player) {
    return (
      <div className="profile-container">
        <div className="error">Player not found</div>
        <button onClick={() => navigate('/')} className="back-button">
          Back to Home
        </button>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-header">
        <h1>{player.name}'s Profile</h1>
        <button onClick={() => navigate('/')} className="back-button">
          Back to Home
        </button>
      </div>

      <div className="player-stats">
        <h2>Player Statistics</h2>
        <div className="stats-grid">
          <div className="stat-item">
            <span className="stat-label">Rank:</span>
            <span className="stat-value">{player.rank}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Playstyle:</span>
            <span className="stat-value">{player.playstyle}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Wins:</span>
            <span className="stat-value">{player.wins || 0}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Losses:</span>
            <span className="stat-value">{player.losses || 0}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Total Matches:</span>
            <span className="stat-value">{player.total_matches || 0}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Win Rate:</span>
            <span className="stat-value">{player.win_rate || 0}%</span>
          </div>
        </div>
      </div>

      {player.match_history && player.match_history.length > 0 ? (
        <div className="match-history">
          <h2>Match History</h2>
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Winner</th>
                <th>Loser</th>
              </tr>
            </thead>
            <tbody>
              {player.match_history.map((match, index) => (
                <tr key={index} className={match.winner === player.name ? 'won' : 'lost'}>
                  <td>{new Date(match.timestamp).toLocaleString()}</td>
                  <td>{match.winner}</td>
                  <td>{match.loser}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="no-matches">No match history found</div>
      )}
    </div>
  );

  if (loading) {
    return (
      <div style={{ color: 'white', padding: '20px' }}>
        <h2>Loading player data...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ color: 'red', padding: '20px' }}>
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
    );
  }

  if (!player) {
    return (
      <div style={{ color: 'white', padding: '20px' }}>
        <h2>Player not found</h2>
        <button onClick={() => navigate('/')}>Back to Home</button>
      </div>
    );
  }

  return (
    <div style={{
      color: 'white',
      padding: '20px',
      maxWidth: '800px',
      margin: '0 auto',
      fontFamily: 'Arial, sans-serif'
    }}>
      <button 
        onClick={() => navigate(-1)}
        style={{
          background: '#333',
          color: 'white',
          border: 'none',
          padding: '8px 16px',
          borderRadius: '4px',
          cursor: 'pointer',
          marginBottom: '20px'
        }}
      >
        ← Back
      </button>
      
      <h1 style={{ color: '#61dafb', marginBottom: '20px' }}>{player.name}'s Profile</h1>
      
      <div style={{
        background: '#2c2c2c',
        padding: '20px',
        borderRadius: '8px',
        marginBottom: '20px'
      }}>
        <h2 style={{ borderBottom: '1px solid #444', paddingBottom: '10px' }}>Player Stats</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div>
            <h3 style={{ color: '#888', margin: '10px 0 5px' }}>Rank</h3>
            <p style={{ fontSize: '24px', margin: '0', color: '#61dafb' }}>{player.rank}</p>
          </div>
          <div>
            <h3 style={{ color: '#888', margin: '10px 0 5px' }}>Playstyle</h3>
            <p style={{ fontSize: '24px', margin: '0', textTransform: 'capitalize' }}>{player.playstyle}</p>
          </div>
          <div>
            <h3 style={{ color: '#888', margin: '10px 0 5px' }}>Wins</h3>
            <p style={{ fontSize: '24px', margin: '0', color: '#4caf50' }}>{player.wins || 0}</p>
          </div>
          <div>
            <h3 style={{ color: '#888', margin: '10px 0 5px' }}>Losses</h3>
            <p style={{ fontSize: '24px', margin: '0', color: '#f44336' }}>{player.losses || 0}</p>
          </div>
          <div>
            <h3 style={{ color: '#888', margin: '10px 0 5px' }}>Win Rate</h3>
            <p style={{ fontSize: '24px', margin: '0' }}>
              {player.win_rate ? `${player.win_rate}%` : 'N/A'}
            </p>
          </div>
        </div>
      </div>

      <div style={{ background: '#2c2c2c', padding: '20px', borderRadius: '8px' }}>
        <h2 style={{ borderBottom: '1px solid #444', paddingBottom: '10px' }}>Match History</h2>
        {player.match_history && player.match_history.length > 0 ? (
          <div style={{ overflowX: 'auto' }}>
            <table style={{
              width: '100%',
              borderCollapse: 'collapse',
              marginTop: '10px',
              color: 'white'
            }}>
              <thead>
                <tr style={{ background: '#333' }}>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Winner</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>Loser</th>
                  <th style={{ padding: '12px', textAlign: 'left' }}>When</th>
                </tr>
              </thead>
              <tbody>
                {player.match_history.map((match, i) => (
                  <tr 
                    key={i} 
                    style={{
                      borderBottom: '1px solid #444',
                      background: match.winner === player.name ? 'rgba(76, 175, 80, 0.1)' : 'transparent'
                    }}
                  >
                    <td style={{ 
                      padding: '12px',
                      color: match.winner === player.name ? '#4caf50' : 'white',
                      fontWeight: match.winner === player.name ? 'bold' : 'normal'
                    }}>
                      {match.winner}
                    </td>
                    <td style={{ 
                      padding: '12px',
                      color: match.loser === player.name ? '#f44336' : 'white',
                      fontWeight: match.loser === player.name ? 'bold' : 'normal'
                    }}>
                      {match.loser}
                    </td>
                    <td style={{ padding: '12px', color: '#aaa' }}>
                      {new Date(match.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#888', textAlign: 'center', padding: '20px' }}>
            No match history available for this player.
          </p>
        )}
      </div>
    </div>
  );
};

export default PlayerProfile;
