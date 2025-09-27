import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getJobs } from '../../services/data';
import './styles.css';
import logo from '../../assets/LeanTechLogo.svg';
import type { JobsResponse } from '../../../types';

const Jobs = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<JobsResponse>({ jobs: [], lastUpdated: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        setError(null);
        const jobsData = await getJobs();
        
        // Validate the response data
        setJobs(jobsData);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch jobs';
        setError(errorMessage);
        console.error('Error fetching jobs:', err);
        setJobs({ jobs: [], lastUpdated: '' }); // Reset jobs array on error
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

  if (loading) {
    return (
      <div className="loading-container">
        <h2>Loading jobs...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2 className="error-title">Error: {error}</h2>
        <p className="error-message">
          Unable to connect to the API server. Please make sure the backend is running on http://localhost:8000
        </p>
        <button 
          className="retry-btn"
          onClick={() => window.location.reload()}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="jobs-container">
      <a href="https://www.leangroup.com/solutions-and-services/technology" target='_blank'>
        <img src={logo} alt="Lean Tech" className="logo" />
      </a>
      
      {jobs.jobs.length === 0 ? (
        <p className="no-jobs-message">No jobs available at the moment.</p>
      ) : (
        <div className="jobs-grid">
          {jobs.jobs.map((job) => (
            <div key={job.jobviteId} className="job-card">
              <div className="job-header">
                <h2 className="job-title">
                  {job.jobTitle}
                </h2>
                
                <button
                  className="view-details-btn"
                  onClick={() => {
                    // Navigate to job detail page
                    navigate(`/detail?id=${job.jobviteId}`);
                  }}
                >
                  View Details
                </button>
              </div>

              <div className="job-section">
                <p className="job-section-content">{job.sector} | {job.workMode} | {job.country}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      
      <div className="jobs-counter">
        Total jobs: {jobs.jobs.length}
      </div>
      <div className="jobs-counter">
        Last updated: {jobs.lastUpdated}
      </div>
    </div>
  );
};

export default Jobs;