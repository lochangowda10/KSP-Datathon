import React, { useState, useEffect } from 'react';
import VoiceInput from './components/VoiceInput';
import ChatWindow from './components/ChatWindow';
import VisualizationPanel from './components/VisualizationPanel';
import { useVoiceOutput } from './hooks/useVoiceOutput';
import { sendQuery } from './services/api';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [conversation, setConversation] = useState([]);
  const { isSpeaking, speak } = useVoiceOutput();

  // Speak the response when it changes
  useEffect(() => {
    if (response && response.answer && !isSpeaking) {
      speak(response.answer);
    }
  }, [response, isSpeaking, speak]);

  const handleTranscript = (transcript) => {
    setQuery(transcript);
    // Auto-submit when we get a transcript for a seamless voice experience
    handleSubmit();
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!query.trim()) return;

    // Add user message to conversation
    setConversation(prev => [...prev, { role: 'user', content: query }]);
    setResponse(null); // Clear previous response while waiting

    try {
      // Call the API (using English for now, can add language parameter later)
      const res = await sendQuery(query, 'en');
      setResponse(res);

      // Add bot response to conversation
      setConversation(prev => [...prev, { role: 'bot', content: res.answer || 'Sorry, I could not process that request.' }]);
    } catch (error) {
      console.error('Error calling API:', error);
      setResponse({ error: 'Failed to get response from server' });
      setConversation(prev => [...prev, { role: 'bot', content: 'Sorry, I encountered an error processing your request.' }]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>KSP Crime Data Assistant</h1>
        <p className="tagline">Voice-enabled conversational AI for crime data querying</p>
      </header>
      <main>
        <div className="interface">
          <div className="input-section">
            <VoiceInput onTranscript={handleTranscript} />

            {/* Manual text input as fallback */}
            <div className="manual-input">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Type your question here..."
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleSubmit();
                  }
                }}
                disabled={false} // We don't disable it during voice input because we are not sharing the listening state
              />
              <button
                onClick={handleSubmit}
                disabled={!query.trim()}
              >
                Ask
              </button>
            </div>
          </div>

          <div className="main-content">
            <ChatWindow
              conversation={conversation}
              isSpeaking={isSpeaking}
            />
            <VisualizationPanel
              response={response}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
