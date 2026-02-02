import React from 'react';
import { PortalSession } from '../api';

interface SettingsProps {
  session: PortalSession | null;
  seed: string;
  runId: string;
  onSeedChange: (v: string) => void;
  onRunIdChange: (v: string) => void;
  onLogout: () => void;
}

export const Settings: React.FC<SettingsProps> = ({ session, seed, runId, onSeedChange, onRunIdChange, onLogout }) => {
  return (
    <div className="flex flex-col gap-6">
      <h2 className="text-xl font-bold">Settings</h2>
      
      <div className="flex flex-col gap-4">
        <section className="p-4 rounded-xl bg-white border border-primary/20 shadow-sm">
          <h3 className="text-sm font-bold uppercase text-text-subtle mb-3">Account</h3>
          <div className="flex flex-col gap-2">
            <div className="text-sm font-medium">Handle: @{session?.handle}</div>
            <div className="text-[10px] font-mono break-all text-text-subtle">ID: {session?.account_id}</div>
            <button 
              onClick={onLogout}
              className="mt-2 text-sm font-bold text-red-600 underline text-left"
            >
              Logout / Reset Session
            </button>
          </div>
        </section>

        <section className="p-4 rounded-xl bg-white border border-primary/20 shadow-sm">
          <h3 className="text-sm font-bold uppercase text-text-subtle mb-3">Deterministic Run</h3>
          <div className="flex flex-col gap-3">
            <label className="flex flex-col gap-1">
              <span className="text-xs font-medium">Global Seed</span>
              <input 
                className="h-9 rounded-lg border border-primary/20 bg-white px-3 text-sm"
                value={seed}
                onChange={(e) => onSeedChange(e.target.value)}
              />
            </label>
            <label className="flex flex-col gap-1">
              <span className="text-xs font-medium">Run ID</span>
              <input 
                className="h-9 rounded-lg border border-primary/20 bg-white px-3 text-sm"
                value={runId}
                onChange={(e) => onRunIdChange(e.target.value)}
              />
            </label>
          </div>
        </section>

        <section className="p-4 rounded-xl bg-white border border-primary/20 shadow-sm">
          <h3 className="text-sm font-bold uppercase text-text-subtle mb-3">About NYX</h3>
          <div className="text-xs text-text-subtle leading-relaxed">
            NYX is a deterministic, verifiable portal infrastructure. 
            This is a Testnet Portal v1 preview. All state transitions 
            generate evidence that can be replayed for correctness.
          </div>
        </section>
      </div>
    </div>
  );
};
