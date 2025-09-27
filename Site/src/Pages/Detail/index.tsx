import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { getJob } from '../../services/data';
import ErrorDisplay from '../../components/ErrorDisplay';
import './styles.css';
import type { Job } from '../../../types';

const Detail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [job, setJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const jobId = searchParams.get('id');

  useEffect(() => {
    const fetchJob = async () => {
      if (!jobId) {
        setError('No job ID provided');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const jobData = await getJob(jobId);
        setJob(jobData);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch job details';
        setError(errorMessage);
        console.error('Error fetching job:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchJob();
  }, [jobId]);

  const handleBackToJobs = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="detail-loading-container">
        <h2>Loading job details...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <ErrorDisplay
        title={`Error: ${error}`}
        message="Unable to load job details. Please try again."
        showRetry={true}
        showBackToJobs={true}
        onRetry={() => window.location.reload()}
        customBackAction={handleBackToJobs}
      />
    );
  }

  if (!job) {
    return (
      <ErrorDisplay
        title="Job not found"
        message="The requested job could not be found."
        showRetry={false}
        showBackToJobs={true}
        customBackAction={handleBackToJobs}
      />
    );
  }

  return (
    <div className="detail-container">
      <div className="detail-header">
        <button 
          className="detail-back-btn"
          onClick={handleBackToJobs}
        >
          ← Back to Jobs
        </button>
        <h1 className="detail-title">{job.jobTitle}</h1>
        <p className="detail-job-id">Job ID: {job.jobviteId}</p>
      </div>

      <div className="detail-section">
        <p className="detail-section-content">{job.sector} | {job.workMode} | {job.country}</p>
      </div>

      <div className="detail-content">
        <div className="detail-description">
          <div 
            className="detail-description-text"
            dangerouslySetInnerHTML={{ __html: job.jobDescription }}
          />
        </div>
      </div>

      <div className="detail-footer">
        <button 
          className="detail-apply-btn"
          onClick={() => {
            const jobTitle = job.jobTitle;
            const jobId = job.jobviteId;
            const message = `Hello! I'm interested in applying for the position: ${jobTitle} (Job ID: ${jobId}). Could you please provide more information about the application process?`;
            const whatsappUrl = `https://wa.me/5554991259084?text=${encodeURIComponent(message)}`;
            window.open(whatsappUrl, '_blank');
          }}
        >
          Apply for this Job
        </button>
      </div>
    </div>
  );
};

export default Detail;