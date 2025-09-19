import React, { useState } from 'react';
import Header from './components/Header';
import CallForm from './components/CallForm';
import CallList from './components/CallList';
import type { SaveCallRequest } from './types/api';
import { callsApi } from './services/api';
import { CheckCircle, AlertCircle } from 'lucide-react';

type Tab = 'add' | 'search';

const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<Tab>('add');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleCallSubmit = async (callData: SaveCallRequest) => {
    setIsSubmitting(true);
    setSubmitMessage(null);

    try {
      const response = await callsApi.saveCall(callData);
      setSubmitMessage({
        type: 'success',
        text: `Call record saved successfully! ID: ${response.call_id}`
      });
      
      // Clear the form by resetting the tab
      setTimeout(() => {
        setCurrentTab('search');
      }, 2000);
    } catch (error: any) {
      setSubmitMessage({
        type: 'error',
        text: error.message || 'Failed to save call record'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTabChange = (tab: Tab) => {
    setCurrentTab(tab);
    setSubmitMessage(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentTab={currentTab} onTabChange={handleTabChange} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {submitMessage && (
          <div className={`mb-6 p-4 rounded-md ${
            submitMessage.type === 'success' 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex">
              {submitMessage.type === 'success' ? (
                <CheckCircle className="w-5 h-5 text-green-400 mr-2" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
              )}
              <div>
                <h3 className={`text-sm font-medium ${
                  submitMessage.type === 'success' ? 'text-green-800' : 'text-red-800'
                }`}>
                  {submitMessage.type === 'success' ? 'Success' : 'Error'}
                </h3>
                <p className={`text-sm mt-1 ${
                  submitMessage.type === 'success' ? 'text-green-700' : 'text-red-700'
                }`}>
                  {submitMessage.text}
                </p>
              </div>
            </div>
          </div>
        )}

        {currentTab === 'add' ? (
          <CallForm onSubmit={handleCallSubmit} isLoading={isSubmitting} />
        ) : (
          <CallList />
        )}
      </main>
    </div>
  );
};

export default App;