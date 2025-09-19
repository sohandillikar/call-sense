import React from 'react';
import { Phone, MessageSquare, BarChart3 } from 'lucide-react';

interface HeaderProps {
  currentTab: 'add' | 'search';
  onTabChange: (tab: 'add' | 'search') => void;
}

const Header: React.FC<HeaderProps> = ({ currentTab, onTabChange }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Phone className="w-8 h-8 text-primary-600 mr-3" />
            <div>
              <h1 className="text-xl font-bold text-gray-900">Customer Calls Manager</h1>
              <p className="text-sm text-gray-500">AI-powered call analytics and management</p>
            </div>
          </div>
          
          <nav className="flex space-x-1">
            <button
              onClick={() => onTabChange('add')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                currentTab === 'add'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="w-4 h-4 inline mr-2" />
              Add Call
            </button>
            <button
              onClick={() => onTabChange('search')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                currentTab === 'search'
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              <BarChart3 className="w-4 h-4 inline mr-2" />
              Search Calls
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
