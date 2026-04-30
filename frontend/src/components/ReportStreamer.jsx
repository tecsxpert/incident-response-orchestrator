/**
 * ReportStreamer - React component for displaying streamed incident reports
 * Uses Server-Sent Events (SSE) to display tokens in real-time as they arrive
 */

import React, { useState, useEffect } from 'react';
import useReportStream from '../hooks/useReportStream';
import '../styles/ReportStreamer.css';

const ReportStreamer = ({
  incidentData,
  onComplete,
  onError,
  baseURL = null,
  autoStart = false,
}) => {
  const {
    tokens,
    metadata,
    isLoading,
    error,
    isComplete,
    streamReport,
    cancelStream,
  } = useReportStream({ baseURL });

  const [displayedTokens, setDisplayedTokens] = useState('');
  const [wordCount, setWordCount] = useState(0);

  // Auto-start streaming if autoStart prop is true
  useEffect(() => {
    if (autoStart && incidentData && !isLoading) {
      startStreaming();
    }
  }, [autoStart, incidentData]);

  // Update word count as tokens arrive
  useEffect(() => {
    setDisplayedTokens(tokens);
    const words = tokens.trim().split(/\s+/).filter(w => w.length > 0);
    setWordCount(words.length);
  }, [tokens]);

  // Handle completion callback
  useEffect(() => {
    if (isComplete && onComplete) {
      onComplete({
        content: tokens,
        metadata,
        wordCount,
      });
    }
  }, [isComplete, tokens, metadata, wordCount, onComplete]);

  // Handle error callback
  useEffect(() => {
    if (error && onError) {
      onError(error);
    }
  }, [error, onError]);

  const startStreaming = () => {
    if (!incidentData) {
      console.error('No incident data provided');
      return;
    }

    streamReport(incidentData, (token) => {
      // Optional: Perform action for each token if needed
      console.debug('[Token]:', token);
    });
  };

  return (
    <div className="report-streamer">
      {/* Metadata Section */}
      {metadata && (
        <div className="metadata-section">
          <div className="metadata-info">
            <span className="metadata-label">Incident:</span>
            <span className="metadata-value">{metadata.title}</span>
          </div>
          <div className="metadata-info">
            <span className="metadata-label">Type:</span>
            <span className={`metadata-value type-${metadata.incident_type}`}>
              {metadata.incident_type}
            </span>
          </div>
          <div className="metadata-info">
            <span className="metadata-label">Severity:</span>
            <span className={`metadata-value severity-${metadata.severity}`}>
              {metadata.severity.toUpperCase()}
            </span>
          </div>
          <div className="metadata-info">
            <span className="metadata-label">Model:</span>
            <span className="metadata-value">{metadata.model}</span>
          </div>
        </div>
      )}

      {/* Controls Section */}
      <div className="controls-section">
        <button
          className="btn btn-primary"
          onClick={startStreaming}
          disabled={isLoading || !incidentData}
        >
          {isLoading ? 'Streaming...' : 'Start Report'}
        </button>

        {isLoading && (
          <button className="btn btn-danger" onClick={cancelStream}>
            Cancel
          </button>
        )}

        {isComplete && (
          <span className="complete-badge">✓ Complete</span>
        )}
      </div>

      {/* Error Section */}
      {error && (
        <div className="error-section">
          <span className="error-icon">⚠️</span>
          <span className="error-message">{error}</span>
        </div>
      )}

      {/* Loading Indicator */}
      {isLoading && (
        <div className="loading-section">
          <div className="spinner"></div>
          <span className="loading-text">Generating report...</span>
          <span className="word-count">{wordCount} words</span>
        </div>
      )}

      {/* Report Content Section */}
      <div className="report-content">
        {displayedTokens ? (
          <div className="content-text">
            {displayedTokens}
            {isLoading && <span className="cursor">▌</span>}
          </div>
        ) : (
          !isLoading && (
            <div className="empty-state">
              <p>Click "Start Report" to generate an incident report</p>
            </div>
          )
        )}
      </div>

      {/* Statistics Section */}
      {(displayedTokens || isComplete) && (
        <div className="statistics-section">
          <div className="stat">
            <span className="stat-label">Words:</span>
            <span className="stat-value">{wordCount}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Characters:</span>
            <span className="stat-value">{displayedTokens.length}</span>
          </div>
          {isComplete && metadata && (
            <div className="stat">
              <span className="stat-label">Streamed:</span>
              <span className="stat-value">{metadata.tokens_streamed || 'N/A'}</span>
            </div>
          )}
        </div>
      )}

      {/* Export Section */}
      {displayedTokens && (
        <div className="export-section">
          <button
            className="btn btn-secondary"
            onClick={() => {
              const element = document.createElement('a');
              const file = new Blob([displayedTokens], { type: 'text/plain' });
              element.href = URL.createObjectURL(file);
              element.download = `report-${Date.now()}.txt`;
              document.body.appendChild(element);
              element.click();
              document.body.removeChild(element);
            }}
          >
            📥 Download Report
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => {
              navigator.clipboard.writeText(displayedTokens);
              alert('Report copied to clipboard');
            }}
          >
            📋 Copy to Clipboard
          </button>
        </div>
      )}
    </div>
  );
};

export default ReportStreamer;
