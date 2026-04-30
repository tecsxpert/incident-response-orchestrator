/**
 * useReportStream - Custom React hook for streaming incident reports via Server-Sent Events
 * Handles EventSource connection, token streaming, and cleanup
 */

import { useEffect, useRef, useState, useCallback } from 'react';

const useReportStream = (options = {}) => {
  const [tokens, setTokens] = useState('');
  const [metadata, setMetadata] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isComplete, setIsComplete] = useState(false);
  
  const eventSourceRef = useRef(null);
  const tokensRef = useRef('');
  
  const AI_SERVICE_URL = options.baseURL || import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:5000';

  /**
   * Stream report from AI service using Server-Sent Events
   * @param {Object} incidentData - Incident data to generate report for
   * @param {Function} onToken - Optional callback for each token received
   */
  const streamReport = useCallback(async (incidentData, onToken) => {
    try {
      setIsLoading(true);
      setError(null);
      setIsComplete(false);
      tokensRef.current = '';
      setTokens('');
      setMetadata(null);

      const eventSource = new EventSource(
        new Request(`${AI_SERVICE_URL}/api/describe/generate-report-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(incidentData),
        })
      );

      let isConnected = true;
      eventSource.onopen = () => {
        console.log('[SSE] Connected to report stream');
        isConnected = true;
      };

      eventSource.onmessage = (event) => {
        try {
          const data = event.data.trim();
          
          if (!data) return;

          // Try to parse as JSON (for metadata and completion events)
          try {
            const jsonData = JSON.parse(data);
            
            if (jsonData.type === 'metadata') {
              console.log('[SSE] Metadata received:', jsonData);
              setMetadata(jsonData);
            } else if (jsonData.type === 'complete') {
              console.log('[SSE] Stream complete:', jsonData);
              setIsComplete(true);
              setIsLoading(false);
              if (eventSource) {
                eventSource.close();
              }
            } else if (jsonData.type === 'error') {
              console.error('[SSE] Stream error:', jsonData.error);
              setError(jsonData.error);
              setIsLoading(false);
              if (eventSource) {
                eventSource.close();
              }
            }
          } catch (parseError) {
            // Not JSON, treat as token
            tokensRef.current += data;
            setTokens(tokensRef.current);
            
            if (onToken) {
              onToken(data);
            }
          }
        } catch (err) {
          console.error('[SSE] Error processing message:', err);
        }
      };

      eventSource.onerror = (err) => {
        console.error('[SSE] Connection error:', err);
        setError('Connection to stream failed');
        setIsLoading(false);
        isConnected = false;
        
        if (eventSource) {
          eventSource.close();
        }
      };

      eventSourceRef.current = eventSource;

    } catch (err) {
      console.error('[Stream] Error initiating stream:', err);
      setError(err.message || 'Failed to start report stream');
      setIsLoading(false);
    }
  }, [AI_SERVICE_URL]);

  /**
   * Cancel the ongoing stream
   */
  const cancelStream = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
      setIsLoading(false);
      console.log('[SSE] Stream cancelled');
    }
  }, []);

  /**
   * Cleanup EventSource on component unmount
   */
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return {
    tokens,
    metadata,
    isLoading,
    error,
    isComplete,
    streamReport,
    cancelStream,
  };
};

export default useReportStream;
