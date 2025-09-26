import React, { useState } from 'react';
import { syncJobs } from '../../services/api';
import './styles.css';

const Admin: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSync = async () => {
    setIsLoading(true);
    setMessage('');
    
    try {
      const result = await syncJobs();
      setMessage('Jobs synchronized successfully!');
      console.log('Sync result:', result);
    } catch (error) {
      setMessage('Error synchronizing jobs. Please try again.');
      console.error('Sync error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="admin-container">
      <h1 className="admin-title">Admin Panel</h1>
      
      <div className="admin-content">
        <button 
          className="sync-btn"
          onClick={handleSync}
          disabled={isLoading}
        >
          {isLoading ? 'Syncing...' : 'Sync Jobs'}
        </button>
        
        {message && (
          <div className={`admin-message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}
      </div>
    </div>
  );
}

export default Admin;