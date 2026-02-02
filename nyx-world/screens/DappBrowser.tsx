import React, { useState } from 'react';

export const DappBrowser: React.FC = () => {
  const [url, setUrl] = useState('http://localhost:3000');
  const [activeUrl, setActiveUrl] = useState('');

  const handleGo = () => {
    let target = url;
    if (!target.startsWith('http')) {
      target = 'http://' + target;
    }
    setActiveUrl(target);
  };

  return (
    <div className="flex flex-col h-full gap-4">
      <div className="flex gap-2 p-2 bg-white rounded-lg border border-primary/20 shadow-sm">
        <input 
          className="flex-1 px-3 py-1 text-sm rounded border border-primary/10"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button 
          onClick={handleGo}
          className="px-4 py-1 text-xs font-bold bg-primary text-background-dark rounded"
        >
          GO
        </button>
      </div>

      <div className="flex-1 bg-white rounded-xl border border-primary/20 shadow-inner overflow-hidden min-h-[400px]">
        {activeUrl ? (
          <iframe 
            src={activeUrl}
            className="w-full h-full border-none"
            title="dApp View"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-text-subtle text-sm">
            Enter a URL to launch a dApp
          </div>
        )}
      </div>
    </div>
  );
};
