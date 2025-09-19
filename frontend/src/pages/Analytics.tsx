import { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  RefreshCw,
  Calendar,
  Activity,
  Target,
  AlertCircle
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { analyticsApi } from '../services/api';

interface AnalyticsOverview {
  period_days: number;
  customer_satisfaction: {
    data_points: number;
    trend: string;
  };
  recommendations: string[];
  last_updated: string;
}

export default function Analytics() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null);
  const [metricsSummary, setMetricsSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Mock data for charts (in real app, this would come from the API)
  const sentimentData = [
    { date: '2024-01-01', positive: 65, neutral: 25, negative: 10 },
    { date: '2024-01-02', positive: 70, neutral: 20, negative: 10 },
    { date: '2024-01-03', positive: 68, neutral: 22, negative: 10 },
    { date: '2024-01-04', positive: 72, neutral: 18, negative: 10 },
    { date: '2024-01-05', positive: 75, neutral: 15, negative: 10 },
    { date: '2024-01-06', positive: 73, neutral: 17, negative: 10 },
    { date: '2024-01-07', positive: 78, neutral: 12, negative: 10 },
  ];

  const callVolumeData = [
    { day: 'Mon', calls: 45 },
    { day: 'Tue', calls: 52 },
    { day: 'Wed', calls: 38 },
    { day: 'Thu', calls: 61 },
    { day: 'Fri', calls: 55 },
    { day: 'Sat', calls: 28 },
    { day: 'Sun', calls: 22 },
  ];

  const reviewPlatformData = [
    { name: 'Google', value: 45, color: '#4285F4' },
    { name: 'Yelp', value: 30, color: '#FF1A1A' },
    { name: 'TripAdvisor', value: 15, color: '#00BFA5' },
    { name: 'Others', value: 10, color: '#9C27B0' },
  ];

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const [overviewData, metricsData] = await Promise.all([
        analyticsApi.getOverview(),
        analyticsApi.getMetricsSummary(),
      ]);
      setOverview(overviewData);
      setMetricsSummary(metricsData);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'up':
      case 'increasing':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'down':
      case 'decreasing':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'up':
      case 'increasing':
        return 'text-green-600';
      case 'down':
      case 'decreasing':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="h-64 bg-gray-200 rounded"></div>
            <div className="h-64 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="mx-auto h-12 w-12 text-red-500" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">Error</h3>
        <p className="mt-1 text-sm text-gray-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Comprehensive insights into your business performance
          </p>
        </div>
        <button
          onClick={fetchAnalytics}
          className="btn btn-secondary flex items-center"
        >
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </button>
      </div>

      {/* Overview Cards */}
      {overview && (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-3 rounded-md bg-blue-500">
                    <BarChart3 className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Data Points</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {overview.customer_satisfaction.data_points}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-3 rounded-md bg-green-500">
                    <TrendingUp className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Trend</p>
                  <div className="flex items-center">
                    {getTrendIcon(overview.customer_satisfaction.trend)}
                    <span className={`ml-2 text-lg font-semibold ${getTrendColor(overview.customer_satisfaction.trend)}`}>
                      {overview.customer_satisfaction.trend}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-3 rounded-md bg-purple-500">
                    <Calendar className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Period</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {overview.period_days} days
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="p-3 rounded-md bg-orange-500">
                    <Target className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-500">Recommendations</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {overview.recommendations.length}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Charts Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Sentiment Trend Chart */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Sentiment Trend</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={sentimentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="positive" stroke="#10B981" strokeWidth={2} />
                <Line type="monotone" dataKey="neutral" stroke="#F59E0B" strokeWidth={2} />
                <Line type="monotone" dataKey="negative" stroke="#EF4444" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Call Volume Chart */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Call Volume</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={callVolumeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="calls" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Review Platform Distribution */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Review Platform Distribution</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={reviewPlatformData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {reviewPlatformData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recommendations</h3>
          <div className="space-y-3">
            {overview?.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start">
                <div className="flex-shrink-0">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
                </div>
                <p className="ml-3 text-sm text-gray-600">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Metrics Summary */}
      {metricsSummary && (
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Metrics Summary</h3>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">TigerData Status</h4>
              <p className="text-sm text-gray-600 mt-1">
                {metricsSummary.tigerdata_configured ? 'Connected' : 'Not Configured'}
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Available Metrics</h4>
              <p className="text-sm text-gray-600 mt-1">
                {metricsSummary.available_metrics?.length || 0} metric types
              </p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-900">Last Updated</h4>
              <p className="text-sm text-gray-600 mt-1">
                {new Date(metricsSummary.last_updated).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
