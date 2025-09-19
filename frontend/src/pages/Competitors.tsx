import { useState, useEffect } from 'react';
import { 
  Users, 
  Plus, 
  Search,
  Filter,
  Calendar,
  AlertCircle,
  TrendingUp,
  DollarSign,
  Eye,
  EyeOff,
  Trash2
} from 'lucide-react';
import { competitorsApi } from '../services/api';
import type { CompetitorAlert } from '../services/api';

export default function Competitors() {
  const [alerts, setAlerts] = useState<CompetitorAlert[]>([]);
  const [competitors, setCompetitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showMonitorForm, setShowMonitorForm] = useState(false);

  // Form states
  const [monitorForm, setMonitorForm] = useState({
    competitor_name: '',
    monitoring_type: 'pricing',
    frequency: 'daily',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [alertsData, competitorsData] = await Promise.all([
        competitorsApi.getAlerts(),
        competitorsApi.getCompetitors()
      ]);
      setAlerts(alertsData);
      setCompetitors(competitorsData);
    } catch (err) {
      setError('Failed to load competitor data');
      console.error('Competitors error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAlerts = async () => {
    try {
      const data = await competitorsApi.getAlerts();
      setAlerts(data);
    } catch (err) {
      setError('Failed to load competitor alerts');
      console.error('Competitors error:', err);
    }
  };

  const handleMonitorSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await competitorsApi.monitorCompetitor(monitorForm);
      setMonitorForm({ competitor_name: '', monitoring_type: 'pricing', frequency: 'daily' });
      setShowMonitorForm(false);
      fetchData(); // Refresh both alerts and competitors
      setError(null); // Clear any previous errors
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Failed to start monitoring';
      setError(errorMessage);
      console.error('Monitor competitor error:', err);
    }
  };

  const handleMarkAsRead = async (alertId: number) => {
    try {
      await competitorsApi.markAlertAsRead(alertId);
      setAlerts(alerts.map(alert => 
        alert.id === alertId ? { ...alert, is_read: true } : alert
      ));
    } catch (err) {
      setError('Failed to mark alert as read');
    }
  };

  const handleDeleteCompetitor = async (competitorId: number) => {
    if (window.confirm('Are you sure you want to delete this competitor?')) {
      try {
        await competitorsApi.deleteCompetitor(competitorId);
        fetchData(); // Refresh the data
        setError(null);
      } catch (err) {
        setError('Failed to delete competitor');
      }
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const unreadAlerts = alerts.filter(alert => !alert.is_read);
  const readAlerts = alerts.filter(alert => alert.is_read);

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
          <h1 className="text-2xl font-bold text-gray-900">Competitor Monitoring</h1>
          <p className="mt-1 text-sm text-gray-500">
            Track competitor activities and pricing changes
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowMonitorForm(true)}
            className="btn btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Monitor Competitor
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <AlertCircle className="h-8 w-8 text-red-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Unread Alerts</p>
                <p className="text-2xl font-semibold text-gray-900">{unreadAlerts.length}</p>
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
                <p className="text-sm font-medium text-gray-500">Total Alerts</p>
                <p className="text-2xl font-semibold text-gray-900">{alerts.length}</p>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-200 rounded-lg">
          <div className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <DollarSign className="h-8 w-8 text-blue-500" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Price Changes</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {alerts.filter(alert => alert.alert_type === 'pricing').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Existing Competitors */}
      {competitors.length > 0 && (
        <div className="bg-white shadow-sm border border-gray-200 rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Monitored Competitors</h3>
            <p className="text-sm text-gray-500">Currently tracking {competitors.length} competitors</p>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {competitors.map((competitor) => (
                <div key={competitor.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{competitor.competitor_name}</h4>
                      <p className="text-sm text-gray-500">{competitor.industry}</p>
                      <p className="text-xs text-gray-400">{competitor.website_url}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        Active
                      </span>
                      <button
                        onClick={() => handleDeleteCompetitor(competitor.id)}
                        className="p-1 text-red-500 hover:text-red-700 hover:bg-red-50 rounded"
                        title="Delete competitor"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search alerts..."
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

      {/* Unread Alerts */}
      {unreadAlerts.length > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Unread Alerts</h3>
          <div className="space-y-4">
            {unreadAlerts.map((alert) => (
              <div key={alert.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      <div className="flex items-center text-sm text-gray-500">
                        <Users className="h-4 w-4 mr-1" />
                        {alert.competitor_name}
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar className="h-4 w-4 mr-1" />
                        {new Date(alert.created_at).toLocaleDateString()}
                      </div>
                    </div>
                    <h4 className="text-lg font-medium text-gray-900 mb-2">{alert.alert_description}</h4>
                    <p className="text-gray-600 mb-4">{alert.alert_description}</p>
                  </div>
                  <button
                    onClick={() => handleMarkAsRead(alert.id)}
                    className="btn btn-secondary flex items-center"
                  >
                    <EyeOff className="h-4 w-4 mr-2" />
                    Mark as Read
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Read Alerts */}
      {readAlerts.length > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Read Alerts</h3>
          <div className="space-y-4">
            {readAlerts.map((alert) => (
              <div key={alert.id} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 opacity-75">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      <div className="flex items-center text-sm text-gray-500">
                        <Users className="h-4 w-4 mr-1" />
                        {alert.competitor_name}
                      </div>
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar className="h-4 w-4 mr-1" />
                        {new Date(alert.created_at).toLocaleDateString()}
                      </div>
                      <div className="flex items-center text-sm text-green-600">
                        <Eye className="h-4 w-4 mr-1" />
                        Read
                      </div>
                    </div>
                    <h4 className="text-lg font-medium text-gray-900 mb-2">{alert.alert_description}</h4>
                    <p className="text-gray-600">{alert.alert_description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {alerts.length === 0 && (
        <div className="text-center py-12">
          <Users className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No alerts yet</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by monitoring a competitor.
          </p>
        </div>
      )}

      {/* Monitor Competitor Modal */}
      {showMonitorForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Monitor Competitor</h3>
            <form onSubmit={handleMonitorSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Competitor Name
                </label>
                <input
                  type="text"
                  value={monitorForm.competitor_name}
                  onChange={(e) => setMonitorForm({ ...monitorForm, competitor_name: e.target.value })}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Monitoring Type
                </label>
                <select
                  value={monitorForm.monitoring_type}
                  onChange={(e) => setMonitorForm({ ...monitorForm, monitoring_type: e.target.value })}
                  className="input"
                >
                  <option value="pricing">Pricing</option>
                  <option value="reviews">Reviews</option>
                  <option value="products">Products</option>
                  <option value="marketing">Marketing</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Frequency
                </label>
                <select
                  value={monitorForm.frequency}
                  onChange={(e) => setMonitorForm({ ...monitorForm, frequency: e.target.value })}
                  className="input"
                >
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowMonitorForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Start Monitoring
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
