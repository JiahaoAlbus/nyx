import React from 'react';
import { Screen } from '../types';

interface BottomNavProps {
  activeTab: Screen;
  onTabChange: (tab: Screen) => void;
}

export const BottomNav: React.FC<BottomNavProps> = ({ activeTab, onTabChange }) => {
  const getButtonClass = (isActive: boolean) => 
    `flex flex-1 flex-col items-center gap-1 p-2 group transition-colors duration-300 ${isActive ? 'text-text-main dark:text-white' : 'text-text-subtle dark:text-gray-400 hover:text-text-main dark:hover:text-primary'}`;

  return (
    <nav className="fixed bottom-0 z-40 w-full max-w-md mx-auto bg-white/90 dark:bg-[#1f1c13]/90 backdrop-blur-xl border-t border-primary/10 pb-safe">
      <div className="flex items-center justify-between px-1 pt-2 pb-2">
        {/* World (Home) */}
        <button className={getButtonClass(activeTab === Screen.HOME)} onClick={() => onTabChange(Screen.HOME)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.HOME ? 'filled text-primary' : ''}`}>public</span>
          <span className="text-[9px] font-medium">Home</span>
        </button>

        {/* Wallet */}
        <button className={getButtonClass(activeTab === Screen.WALLET)} onClick={() => onTabChange(Screen.WALLET)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.WALLET ? 'filled text-primary' : ''}`}>account_balance_wallet</span>
          <span className="text-[9px] font-medium">Wallet</span>
        </button>

        {/* Exchange */}
        <button className={getButtonClass(activeTab === Screen.EXCHANGE)} onClick={() => onTabChange(Screen.EXCHANGE)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.EXCHANGE ? 'filled text-primary' : ''}`}>currency_exchange</span>
          <span className="text-[9px] font-medium">Trade</span>
        </button>

        {/* Chat */}
        <button className={getButtonClass(activeTab === Screen.CHAT)} onClick={() => onTabChange(Screen.CHAT)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.CHAT ? 'filled text-primary' : ''}`}>chat_bubble</span>
          <span className="text-[9px] font-medium">Chat</span>
        </button>

        {/* Store */}
        <button className={getButtonClass(activeTab === Screen.STORE)} onClick={() => onTabChange(Screen.STORE)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.STORE ? 'filled text-primary' : ''}`}>storefront</span>
          <span className="text-[9px] font-medium">Store</span>
        </button>

        {/* Activity */}
        <button className={getButtonClass(activeTab === Screen.ACTIVITY)} onClick={() => onTabChange(Screen.ACTIVITY)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.ACTIVITY ? 'filled text-primary' : ''}`}>history</span>
          <span className="text-[9px] font-medium">Activity</span>
        </button>

        {/* Evidence */}
        <button className={getButtonClass(activeTab === Screen.EVIDENCE)} onClick={() => onTabChange(Screen.EVIDENCE)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.EVIDENCE ? 'filled text-primary' : ''}`}>verified</span>
          <span className="text-[9px] font-medium">Proof</span>
        </button>

        {/* Settings */}
        <button className={getButtonClass(activeTab === Screen.SETTINGS)} onClick={() => onTabChange(Screen.SETTINGS)}>
          <span className={`material-symbols-outlined text-[22px] ${activeTab === Screen.SETTINGS ? 'filled text-primary' : ''}`}>settings</span>
          <span className="text-[9px] font-medium">Set</span>
        </button>
      </div>
    </nav>
  );
};