import React from 'react';

const VisualizationPanel = ({ response }) => {
  return (
    <div>
      <h2>Visualization Panel</h2>
      {response && (
        <div>
          <p>Visualization data: {JSON.stringify(response)}</p>
        </div>
      )}
    </div>
  );
};

export default VisualizationPanel;