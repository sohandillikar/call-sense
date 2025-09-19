import { useState, useEffect } from 'react';
import { 
  Lightbulb, 
  Plus, 
  Search,
  Filter,
  Calendar,
  TrendingUp,
  Target,
  Brain,
  RefreshCw
} from 'lucide-react';
import { insightsApi } from '../services/api';
import type { BusinessInsight } from '../services/api';

export default function Insights() {
  const [insights, setInsights] = useState<BusinessInsight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showGenerateForm, setShowGenerateForm] = useState(false);

  // Form states
  const [generateForm, setGenerateForm] = useState({
    insight_type: 'customer_satisfaction',
    data_sources: ['calls', 'reviews'],
    analysis_period_days: 30,
  });

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      const data = await insightsApi.getInsights();
      setInsights(data);
    } catch (err) {
      setError('Failed to load insights');
      console.error('Insights error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await insightsApi.generateInsights(generateForm);
      setGenerateForm({ 
        insight_type: 'customer_satisfaction', 
        data_sources: ['calls', 'reviews'], 
        analysis_period_days: 30 
      });
      setShowGenerateForm(false);
      fetchInsights();
    } catch (err) {
      setError('Failed to generate insights');
    }
  };

  const getInsightTypeColor = (type: string) => {
    switch (type.toLowerCase()) {
      case 'customer_satisfaction':
        return 'bg-green-100 text-green-800';
      case 'competitor_analysis':
        return 'bg-blue-100 text-blue-800';
      case 'market_trends':
        return 'bg-purple-100 text-purple-800';
      case 'operational_efficiency':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getImpactLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'text-red-600 bg-red-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
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
          <h1 className="text-2xl font-bold text-gray-900">Business Insights</h1>
          <p className="mt-1 text-sm text-gray-500">
            AI-powered insights and recommendations for your business
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowGenerateForm(true)}
            className="btn btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Generate Insights
          </button>
          <button
            onClick={fetchInsights}
            className="btn btn-secondary flex items-center"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Lightbulb className="h-8 w-8 text-yellow-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Insights</p>
                <p className="text-2xl font-semibold text-gray-900">{insights.length}</p>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-green-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">High Impact</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {insights.filter(insight => insight.impact_level === 'high').length}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Brain className="h-8 w-8 text-purple-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Avg Confidence</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {insights.length > 0 
                    ? Math.round(insights.reduce((acc, insight) => acc + insight.confidence_score, 0) / insights.length * 100) / 100
                    : 0
                  }
                </p>
              </div>
            </div>
          </div>
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
                placeholder="Search insights..."
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

      {/* Insights List */}
      <div className="space-y-4">
        {insights.length === 0 ? (
          <div className="text-center py-12">
            <Lightbulb className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No insights yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Generate your first AI-powered business insight.
            </p>
          </div>
        ) : (
          insights.map((insight) => (
            <div key={insight.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getInsightTypeColor(insight.insight_type)}`}>
                      {insight.insight_type.replace('_', ' ').toUpperCase()}
                    </span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getImpactLevelColor(insight.impact_level)}`}>
                      {insight.impact_level.toUpperCase()} IMPACT
                    </span>
                    <div className="flex items-center text-sm text-gray-500">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(insight.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">{insight.title}</h3>
                  <p className="text-gray-600 mb-4">{insight.description}</p>
                  
                  {insight.recommendations.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-900 mb-2">Recommendations:</h4>
                      <ul className="space-y-1">
                        {insight.recommendations.map((recommendation, index) => (
                          <li key={index} className="text-sm text-gray-600 flex items-start">
                            <Target className="h-3 w-3 mr-2 mt-0.5 text-blue-500" />
                            {recommendation}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
                <div className="ml-4 text-right">
                  <div className="text-sm text-gray-500 mb-1">Confidence</div>
                  <div className={`text-lg font-semibold ${getConfidenceColor(insight.confidence_score)}`}>
                    {Math.round(insight.confidence_score * 100)}%
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Generate Insights Modal */}
      {showGenerateForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Generate Insights</h3>
            <form onSubmit={handleGenerateSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Insight Type
                </label>
                <select
                  value={generateForm.insight_type}
                  onChange={(e) => setGenerateForm({ ...generateForm, insight_type: e.target.value })}
                  className="input"
                >
                  <option value="customer_satisfaction">Customer Satisfaction</option>
                  <option value="competitor_analysis">Competitor Analysis</option>
                  <option value="market_trends">Market Trends</option>
                  <option value="operational_efficiency">Operational Efficiency</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Data Sources
                </label>
                <div className="space-y-2">
                  {['calls', 'reviews', 'competitors', 'analytics'].map((source) => (
                    <label key={source} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={generateForm.data_sources.includes(source)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setGenerateForm({
                              ...generateForm,
                              data_sources: [...generateForm.data_sources, source],
                            });
                          } else {
                            setGenerateForm({
                              ...generateForm,
                              data_sources: generateForm.data_sources.filter(s => s !== source),
                            });
                          }
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 capitalize">{source}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Analysis Period (Days)
                </label>
                <input
                  type="number"
                  value={generateForm.analysis_period_days}
                  onChange={(e) => setGenerateForm({ ...generateForm, analysis_period_days: parseInt(e.target.value) })}
                  className="input"
                  min="1"
                  max="365"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowGenerateForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Generate
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
