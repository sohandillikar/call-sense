import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Phone, 
  Star, 
  Users, 
  TrendingUp, 
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react';
import { callsApi, reviewsApi, competitorsApi } from '../services/api';

interface DashboardStats {
  totalCalls: number;
  totalReviews: number;
  competitorAlerts: number;
  avgSentiment: number;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<DashboardStats>({
    totalCalls: 0,
    totalReviews: 0,
    competitorAlerts: 0,
    avgSentiment: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [calls, reviews, alerts] = await Promise.all([
          callsApi.getCalls(),
          reviewsApi.getCompanyReviews(),
          competitorsApi.getAlerts(),
        ]);

        // Calculate average sentiment from calls and reviews
        const allSentiments = [
          ...calls.map(call => call.sentiment_score),
          ...reviews.map(review => review.sentiment_score),
        ];
        const avgSentiment = allSentiments.length > 0 
          ? allSentiments.reduce((a, b) => a + b, 0) / allSentiments.length 
          : 0;

        setStats({
          totalCalls: calls.length,
          totalReviews: reviews.length,
          competitorAlerts: alerts.filter(alert => !alert.is_read).length,
          avgSentiment: Math.round(avgSentiment * 100) / 100,
        });
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const statCards = [
    {
      name: 'Total Calls',
      value: stats.totalCalls,
      icon: Phone,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'positive' as const,
    },
    {
      name: 'Reviews Analyzed',
      value: stats.totalReviews,
      icon: Star,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'positive' as const,
    },
    {
      name: 'Active Alerts',
      value: stats.competitorAlerts,
      icon: AlertCircle,
      color: 'bg-red-500',
      change: '-3%',
      changeType: 'negative' as const,
    },
    {
      name: 'Avg Sentiment',
      value: stats.avgSentiment,
      icon: TrendingUp,
      color: 'bg-purple-500',
      change: '+5%',
      changeType: 'positive' as const,
    },
  ];

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              </div>
            ))}
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
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your AI Business Assistant metrics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <div key={card.name} className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
            <div className="p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`p-3 rounded-md ${card.color}`}>
                    <card.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {card.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900">
                        {card.value}
                      </div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        card.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {card.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow-sm border border-gray-200 rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <button 
              onClick={() => navigate('/calls')}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <Phone className="h-5 w-5 text-blue-500 mr-3" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Transcribe Call</div>
                <div className="text-sm text-gray-500">Upload or enter call transcription</div>
              </div>
            </button>
            <button 
              onClick={() => navigate('/reviews')}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <Star className="h-5 w-5 text-green-500 mr-3" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Analyze Reviews</div>
                <div className="text-sm text-gray-500">Scrape and analyze customer reviews</div>
              </div>
            </button>
            <button 
              onClick={() => navigate('/competitors')}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <Users className="h-5 w-5 text-red-500 mr-3" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Monitor Competitors</div>
                <div className="text-sm text-gray-500">Track competitor activities</div>
              </div>
            </button>
            <button 
              onClick={() => navigate('/analytics')}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <TrendingUp className="h-5 w-5 text-purple-500 mr-3" />
              <div className="text-left">
                <div className="font-medium text-gray-900">View Analytics</div>
                <div className="text-sm text-gray-500">Interactive charts and insights</div>
              </div>
            </button>
            <button 
              onClick={() => navigate('/insights')}
              className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
            >
              <AlertCircle className="h-5 w-5 text-yellow-500 mr-3" />
              <div className="text-left">
                <div className="font-medium text-gray-900">AI Insights</div>
                <div className="text-sm text-gray-500">Generate business recommendations</div>
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white shadow-sm border border-gray-200 rounded-lg">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <div className="flex-1">
                <p className="text-sm text-gray-900">System is running normally</p>
                <p className="text-xs text-gray-500">All services are operational</p>
              </div>
              <Clock className="h-4 w-4 text-gray-400" />
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <div className="flex-1">
                <p className="text-sm text-gray-900">Database connected</p>
                <p className="text-xs text-gray-500">PostgreSQL and Redis are healthy</p>
              </div>
              <Clock className="h-4 w-4 text-gray-400" />
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <div className="flex-1">
                <p className="text-sm text-gray-900">AI models loaded</p>
                <p className="text-xs text-gray-500">Sentiment analysis ready</p>
              </div>
              <Clock className="h-4 w-4 text-gray-400" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
