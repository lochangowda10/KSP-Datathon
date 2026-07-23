import React from 'react';
import useVoiceInput from '../hooks/useVoiceInput';

const VoiceInput = () => {
  const { transcript, isListening, startListening, stopListening } = useVoiceInput();

  return (
    <div className="voice-input">
      <div className="voice-controls">
        <button
          onClick={isListening ? stopListening : startListening}
          disabled={false}
          className={`mic-button ${isListening ? 'listening' : ''}`}
        >
          {/* Using Unicode microphone icon */}
          🎤
        </button>
        <div className="voice-status">
          {isListening ? (
            <span className="status-listening">🔴 Listening...</span>
          ) : (
            <span className="status-ready">🔴 Click to speak</span>
          )}
        </div>
      </div>
      {transcript && !isListening && (
        <div className="transcript-preview">
          <p><strong>You said:</strong> {transcript}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;