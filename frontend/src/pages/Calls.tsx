import { useState, useEffect } from 'react';
import { 
  Phone, 
  Upload, 
  Plus, 
  Search,
  Filter,
  Calendar,
  User,
  MessageSquare,
  TrendingUp,
  AlertCircle
} from 'lucide-react';
import { callsApi } from '../services/api';
import type { CallTranscription } from '../services/api';

export default function Calls() {
  const [calls, setCalls] = useState<CallTranscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTranscribeForm, setShowTranscribeForm] = useState(false);
  const [showUploadForm, setShowUploadForm] = useState(false);

  // Form states
  const [transcribeForm, setTranscribeForm] = useState({
    customer_phone: '',
    call_type: 'inbound',
    transcription_text: '',
  });

  const [uploadForm, setUploadForm] = useState({
    customer_phone: '',
    call_type: 'inbound',
  });

  useEffect(() => {
    fetchCalls();
  }, []);

  const fetchCalls = async () => {
    try {
      setLoading(true);
      const data = await callsApi.getCalls();
      setCalls(data);
    } catch (err) {
      setError('Failed to load calls');
      console.error('Calls error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTranscribeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await callsApi.transcribeCall(transcribeForm);
      setTranscribeForm({ customer_phone: '', call_type: 'inbound', transcription_text: '' });
      setShowTranscribeForm(false);
      fetchCalls();
    } catch (err) {
      setError('Failed to transcribe call');
    }
  };

  const handleFileUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = e.currentTarget.querySelector('input[type="file"]') as HTMLInputElement;
    
    if (fileInput?.files?.[0]) {
      formData.append('audio_file', fileInput.files[0]);
      formData.append('customer_phone', uploadForm.customer_phone);
      formData.append('call_type', uploadForm.call_type);
      
      try {
        await callsApi.uploadAndTranscribe(formData);
        setUploadForm({ customer_phone: '', call_type: 'inbound' });
        setShowUploadForm(false);
        fetchCalls();
      } catch (err) {
        setError('Failed to upload and transcribe call');
      }
    }
  };

  const getSentimentColor = (score: number) => {
    if (score >= 0.5) return 'text-green-600 bg-green-100';
    if (score >= 0) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getSentimentLabel = (score: number) => {
    if (score >= 0.5) return 'Positive';
    if (score >= 0) return 'Neutral';
    return 'Negative';
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-3/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Call Analysis</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage and analyze customer call transcriptions
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowTranscribeForm(true)}
            className="btn btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Transcribe Call
          </button>
          <button
            onClick={() => setShowUploadForm(true)}
            className="btn btn-secondary flex items-center"
          >
            <Upload className="h-4 w-4 mr-2" />
            Upload Audio
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search calls..."
                className="input pl-10"
              />
            </div>
          </div>
          <button className="btn btn-secondary flex items-center">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </button>
        </div>
      </div>

      {/* Calls List */}
      <div className="space-y-4">
        {calls.length === 0 ? (
          <div className="text-center py-12">
            <Phone className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No calls yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by transcribing your first call.
            </p>
          </div>
        ) : (
          calls.map((call) => (
            <div key={call.call_id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="flex items-center text-sm text-gray-500">
                      <User className="h-4 w-4 mr-1" />
                      {call.customer_phone}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(call.created_at).toLocaleDateString()}
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSentimentColor(call.sentiment_score)}`}>
                      {getSentimentLabel(call.sentiment_score)}
                    </span>
                  </div>
                  <p className="text-gray-900 mb-3 line-clamp-3">{call.transcription}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <div className="flex items-center">
                      <TrendingUp className="h-4 w-4 mr-1" />
                      Priority: {call.priority_score}/10
                    </div>
                    <div className="flex items-center">
                      <MessageSquare className="h-4 w-4 mr-1" />
                      {call.key_topics.length} topics
                    </div>
                  </div>
                </div>
              </div>
              
              {call.action_items.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Action Items:</h4>
                  <ul className="space-y-1">
                    {call.action_items.map((item, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <AlertCircle className="h-3 w-3 mr-2 mt-0.5 text-yellow-500" />
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Transcribe Call Modal */}
      {showTranscribeForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Transcribe Call</h3>
            <form onSubmit={handleTranscribeSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer Phone
                </label>
                <input
                  type="tel"
                  value={transcribeForm.customer_phone}
                  onChange={(e) => setTranscribeForm({ ...transcribeForm, customer_phone: e.target.value })}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Call Type
                </label>
                <select
                  value={transcribeForm.call_type}
                  onChange={(e) => setTranscribeForm({ ...transcribeForm, call_type: e.target.value })}
                  className="input"
                >
                  <option value="inbound">Inbound</option>
                  <option value="outbound">Outbound</option>
                  <option value="support">Support</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Transcription Text
                </label>
                <textarea
                  value={transcribeForm.transcription_text}
                  onChange={(e) => setTranscribeForm({ ...transcribeForm, transcription_text: e.target.value })}
                  className="input"
                  rows={4}
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowTranscribeForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Transcribe
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Upload Audio Modal */}
      {showUploadForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Audio File</h3>
            <form onSubmit={handleFileUpload} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer Phone
                </label>
                <input
                  type="tel"
                  value={uploadForm.customer_phone}
                  onChange={(e) => setUploadForm({ ...uploadForm, customer_phone: e.target.value })}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Call Type
                </label>
                <select
                  value={uploadForm.call_type}
                  onChange={(e) => setUploadForm({ ...uploadForm, call_type: e.target.value })}
                  className="input"
                >
                  <option value="inbound">Inbound</option>
                  <option value="outbound">Outbound</option>
                  <option value="support">Support</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Audio File
                </label>
                <input
                  type="file"
                  accept="audio/*"
                  className="input"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowUploadForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Upload & Transcribe
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {error && (
        <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg">
          {error}
        </div>
      )}
    </div>
  );
}
