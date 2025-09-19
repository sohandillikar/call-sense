import React, { useState } from 'react';
import type { SaveCallRequest } from '../types/api';
import { Phone, MessageSquare, Brain, CheckCircle, XCircle, Save } from 'lucide-react';

interface CallFormProps {
  onSubmit: (callData: SaveCallRequest) => void;
  isLoading?: boolean;
}

const CallForm: React.FC<CallFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<SaveCallRequest>({
    phone: '',
    transcript: '',
    sentiment: 0,
    insight: '',
    solved: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    }

    if (!formData.transcript.trim()) {
      newErrors.transcript = 'Transcript is required';
    }

    if (!formData.insight.trim()) {
      newErrors.insight = 'Insight is required';
    }

    if (formData.sentiment < -1 || formData.sentiment > 1) {
      newErrors.sentiment = 'Sentiment must be between -1 and 1';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleInputChange = (field: keyof SaveCallRequest, value: string | number | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.1) return 'text-green-600';
    if (sentiment < -0.1) return 'text-red-600';
    return 'text-yellow-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
        <MessageSquare className="w-6 h-6 text-primary-600 mr-2" />
        Add New Call Record
      </h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
            <Phone className="w-4 h-4 inline mr-1" />
            Phone Number
          </label>
          <input
            type="tel"
            id="phone"
            value={formData.phone}
            onChange={(e) => handleInputChange('phone', e.target.value)}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
              errors.phone ? 'border-red-300' : 'border-gray-300'
            }`}
            placeholder="+1234567890"
          />
          {errors.phone && <p className="mt-1 text-sm text-red-600">{errors.phone}</p>}
        </div>

        <div>
          <label htmlFor="transcript" className="block text-sm font-medium text-gray-700 mb-2">
            <MessageSquare className="w-4 h-4 inline mr-1" />
            Call Transcript
          </label>
          <textarea
            id="transcript"
            value={formData.transcript}
            onChange={(e) => handleInputChange('transcript', e.target.value)}
            rows={4}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
              errors.transcript ? 'border-red-300' : 'border-gray-300'
            }`}
            placeholder="Enter the call transcript..."
          />
          {errors.transcript && <p className="mt-1 text-sm text-red-600">{errors.transcript}</p>}
        </div>

        <div>
          <label htmlFor="sentiment" className="block text-sm font-medium text-gray-700 mb-2">
            <Brain className="w-4 h-4 inline mr-1" />
            Sentiment Score
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="range"
              id="sentiment"
              min="-1"
              max="1"
              step="0.1"
              value={formData.sentiment}
              onChange={(e) => handleInputChange('sentiment', parseFloat(e.target.value))}
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <span className={`text-sm font-medium min-w-[60px] ${getSentimentColor(formData.sentiment)}`}>
              {formData.sentiment.toFixed(1)}
            </span>
          </div>
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Negative (-1)</span>
            <span>Neutral (0)</span>
            <span>Positive (1)</span>
          </div>
          {errors.sentiment && <p className="mt-1 text-sm text-red-600">{errors.sentiment}</p>}
        </div>

        <div>
          <label htmlFor="insight" className="block text-sm font-medium text-gray-700 mb-2">
            <Brain className="w-4 h-4 inline mr-1" />
            AI Insights
          </label>
          <textarea
            id="insight"
            value={formData.insight}
            onChange={(e) => handleInputChange('insight', e.target.value)}
            rows={3}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 ${
              errors.insight ? 'border-red-300' : 'border-gray-300'
            }`}
            placeholder="Enter AI-generated insights about this call..."
          />
          {errors.insight && <p className="mt-1 text-sm text-red-600">{errors.insight}</p>}
        </div>

        <div>
          <label className="flex items-center space-x-3">
            <input
              type="checkbox"
              checked={formData.solved}
              onChange={(e) => handleInputChange('solved', e.target.checked)}
              className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <div className="flex items-center">
              {formData.solved ? (
                <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              ) : (
                <XCircle className="w-5 h-5 text-red-500 mr-2" />
              )}
              <span className="text-sm font-medium text-gray-700">Issue was solved</span>
            </div>
          </label>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {isLoading ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
          ) : (
            <Save className="w-4 h-4 mr-2" />
          )}
          {isLoading ? 'Saving...' : 'Save Call Record'}
        </button>
      </form>
    </div>
  );
};

export default CallForm;
