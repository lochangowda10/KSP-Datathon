import React from 'react';
import VoiceInput from './components/VoiceInput';
import ChatWindow from './components/ChatWindow';
import VisualizationPanel from './components/VisualizationPanel';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>KSP Crime Data Assistant</h1>
      </header>
      <main>
        <VoiceInput />
        <ChatWindow />
        <VisualizationPanel />
      </main>
    </div>
  );
}

export default App;