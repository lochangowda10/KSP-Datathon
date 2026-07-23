import React from 'react';

const ChatWindow = ({ response }) => {
  return (
    <div>
      <h2>Chat Window</h2>
      {response && (
        <div>
          <p>Response: {JSON.stringify(response)}</p>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;