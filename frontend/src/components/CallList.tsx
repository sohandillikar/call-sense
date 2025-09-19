import React, { useState } from 'react';
import type { CallRecord } from '../types/api';
import { callsApi } from '../services/api';
import CallCard from './CallCard';
import { Phone, Search, AlertCircle, Loader2 } from 'lucide-react';

const CallList: React.FC = () => {
  const [phone, setPhone] = useState('');
  const [calls, setCalls] = useState<CallRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!phone.trim()) return;

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await callsApi.getCalls(phone.trim());
      setCalls(response.calls);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch calls');
      setCalls([]);
    } finally {
      setLoading(false);
    }
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhone(e.target.value);
    // Clear results when phone number changes
    if (hasSearched) {
      setCalls([]);
      setError(null);
      setHasSearched(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
          <Search className="w-6 h-6 text-primary-600 mr-2" />
          Search Call Records
        </h2>

        <form onSubmit={handleSearch} className="flex space-x-4">
          <div className="flex-1">
            <label htmlFor="phone-search" className="block text-sm font-medium text-gray-700 mb-2">
              <Phone className="w-4 h-4 inline mr-1" />
              Phone Number
            </label>
            <input
              type="tel"
              id="phone-search"
              value={phone}
              onChange={handlePhoneChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Enter phone number to search calls..."
            />
          </div>
          <div className="flex items-end">
            <button
              type="submit"
              disabled={loading || !phone.trim()}
              className="bg-primary-600 text-white py-2 px-6 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin mr-2" />
              ) : (
                <Search className="w-4 h-4 mr-2" />
              )}
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <div className="flex">
            <AlertCircle className="w-5 h-5 text-red-400 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {hasSearched && !loading && calls.length === 0 && !error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
          <div className="flex">
            <AlertCircle className="w-5 h-5 text-yellow-400 mr-2" />
            <div>
              <h3 className="text-sm font-medium text-yellow-800">No calls found</h3>
              <p className="text-sm text-yellow-700 mt-1">
                No call records found for phone number: {phone}
              </p>
            </div>
          </div>
        </div>
      )}

      {calls.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-medium text-gray-900">
              Call Records ({calls.length})
            </h3>
            <div className="text-sm text-gray-500">
              Sorted by most recent
            </div>
          </div>
          <div className="grid gap-6">
            {calls.map((call) => (
              <CallCard key={call.id} call={call} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CallList;
