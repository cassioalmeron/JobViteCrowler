import { useNavigate } from 'react-router-dom';
import './ErrorDisplay.css';

interface ErrorDisplayProps {
  title: string;
  message: string;
  showRetry?: boolean;
  showBackToJobs?: boolean;
  onRetry?: () => void;
  customBackAction?: () => void;
  customBackText?: string;
}

const ErrorDisplay = ({ 
  title, 
  message, 
  showRetry = true, 
  showBackToJobs = true,
  onRetry,
  customBackAction,
  customBackText = "Back to Jobs"
}: ErrorDisplayProps) => {
  const navigate = useNavigate();

  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      window.location.reload();
    }
  };

  const handleBackToJobs = () => {
    if (customBackAction) {
      customBackAction();
    } else {
      navigate('/');
    }
  };

  return (
    <div className="error-display-container">
      <h2 className="error-display-title">{title}</h2>
      <p className="error-display-message">{message}</p>
      <div className="error-display-buttons">
        {showRetry && (
          <button 
            className="error-display-retry-btn"
            onClick={handleRetry}
          >
            Retry
          </button>
        )}
        {showBackToJobs && (
          <button 
            className="error-display-back-btn"
            onClick={handleBackToJobs}
          >
            {customBackText}
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorDisplay;
