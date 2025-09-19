import React from 'react';
import type { CallRecord } from '../types/api';
import { Phone, Calendar, MessageSquare, Brain, CheckCircle, XCircle, TrendingUp, TrendingDown } from 'lucide-react';

interface CallCardProps {
  call: CallRecord;
}

const CallCard: React.FC<CallCardProps> = ({ call }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  const getSentimentColor = (sentiment: number | null) => {
    if (sentiment === null) return 'text-gray-500';
    if (sentiment > 0.1) return 'text-green-600';
    if (sentiment < -0.1) return 'text-red-600';
    return 'text-yellow-600';
  };

  const getSentimentIcon = (sentiment: number | null) => {
    if (sentiment === null) return null;
    if (sentiment > 0.1) return <TrendingUp className="w-4 h-4" />;
    if (sentiment < -0.1) return <TrendingDown className="w-4 h-4" />;
    return null;
  };

  const getSentimentLabel = (sentiment: number | null) => {
    if (sentiment === null) return 'No sentiment data';
    if (sentiment > 0.1) return 'Positive';
    if (sentiment < -0.1) return 'Negative';
    return 'Neutral';
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Phone className="w-5 h-5 text-primary-600" />
          <span className="font-medium text-gray-900">{call.phone}</span>
        </div>
        <div className="flex items-center space-x-2">
          {call.solved ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : (
            <XCircle className="w-5 h-5 text-red-500" />
          )}
          <span className={`text-sm font-medium ${call.solved ? 'text-green-600' : 'text-red-600'}`}>
            {call.solved ? 'Solved' : 'Unsolved'}
          </span>
        </div>
      </div>

      <div className="flex items-center text-sm text-gray-500 mb-4">
        <Calendar className="w-4 h-4 mr-2" />
        {formatDate(call.created_at)}
      </div>

      <div className="mb-4">
        <div className="flex items-center mb-2">
          <MessageSquare className="w-4 h-4 text-gray-500 mr-2" />
          <span className="text-sm font-medium text-gray-700">Transcript</span>
        </div>
        <p className="text-gray-600 text-sm leading-relaxed bg-gray-50 p-3 rounded-md">
          {call.transcript}
        </p>
      </div>

      {call.sentiments !== null && (
        <div className="mb-4">
          <div className="flex items-center mb-2">
            <Brain className="w-4 h-4 text-gray-500 mr-2" />
            <span className="text-sm font-medium text-gray-700">Sentiment Analysis</span>
          </div>
          <div className={`flex items-center space-x-2 ${getSentimentColor(call.sentiments)}`}>
            {getSentimentIcon(call.sentiments)}
            <span className="text-sm font-medium">
              {getSentimentLabel(call.sentiments)} ({call.sentiments.toFixed(2)})
            </span>
          </div>
        </div>
      )}

      <div>
        <div className="flex items-center mb-2">
          <Brain className="w-4 h-4 text-gray-500 mr-2" />
          <span className="text-sm font-medium text-gray-700">Insights</span>
        </div>
        <p className="text-gray-600 text-sm leading-relaxed bg-blue-50 p-3 rounded-md">
          {call.insights}
        </p>
      </div>
    </div>
  );
};

export default CallCard;
