import { useState, useEffect } from 'react';
import { 
  Star, 
  Plus, 
  Search,
  Filter,
  User,
  ExternalLink,
  RefreshCw
} from 'lucide-react';
import { reviewsApi } from '../services/api';
import type { Review } from '../services/api';

export default function Reviews() {
  const [companyReviews, setCompanyReviews] = useState<Review[]>([]);
  const [competitorReviews, setCompetitorReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'company' | 'competitor'>('company');
  const [showScrapeForm, setShowScrapeForm] = useState(false);

  // Form states
  const [scrapeForm, setScrapeForm] = useState({
    business_name: '',
    location: '',
    platforms: ['google', 'yelp'],
  });

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const [company, competitor] = await Promise.all([
        reviewsApi.getCompanyReviews(),
        reviewsApi.getCompetitorReviews(),
      ]);
      setCompanyReviews(company);
      setCompetitorReviews(competitor);
    } catch (err) {
      setError('Failed to load reviews');
      console.error('Reviews error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleScrapeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (activeTab === 'company') {
        await reviewsApi.scrapeCompanyReviews(scrapeForm);
      } else {
        await reviewsApi.scrapeCompetitorReviews(scrapeForm);
      }
      setScrapeForm({ business_name: '', location: '', platforms: ['google', 'yelp'] });
      setShowScrapeForm(false);
      fetchReviews();
    } catch (err) {
      setError('Failed to scrape reviews');
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

  const getRatingStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`h-4 w-4 ${
          i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  const currentReviews = activeTab === 'company' ? companyReviews : competitorReviews;

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
          <h1 className="text-2xl font-bold text-gray-900">Review Analysis</h1>
          <p className="mt-1 text-sm text-gray-500">
            Monitor and analyze customer reviews across platforms
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowScrapeForm(true)}
            className="btn btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Scrape Reviews
          </button>
          <button
            onClick={fetchReviews}
            className="btn btn-secondary flex items-center"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('company')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'company'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Company Reviews ({companyReviews.length})
          </button>
          <button
            onClick={() => setActiveTab('competitor')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'competitor'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Competitor Reviews ({competitorReviews.length})
          </button>
        </nav>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search reviews..."
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

      {/* Reviews List */}
      <div className="space-y-4">
        {currentReviews.length === 0 ? (
          <div className="text-center py-12">
            <Star className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No reviews yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by scraping reviews for your business.
            </p>
          </div>
        ) : (
          currentReviews.map((review, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <div className="flex items-center text-sm text-gray-500">
                      <User className="h-4 w-4 mr-1" />
                      {review.reviewer_name}
                    </div>
                    <div className="flex items-center text-sm text-gray-500">
                      <ExternalLink className="h-4 w-4 mr-1" />
                      {review.platform}
                    </div>
                    <div className="flex items-center">
                      {getRatingStars(review.rating)}
                    </div>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSentimentColor(review.sentiment_score)}`}>
                      {getSentimentLabel(review.sentiment_score)}
                    </span>
                  </div>
                  <p className="text-gray-900 mb-3">{review.review_text}</p>
                  
                  {review.key_themes.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {review.key_themes.map((theme, themeIndex) => (
                        <span
                          key={themeIndex}
                          className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full"
                        >
                          {theme}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Scrape Reviews Modal */}
      {showScrapeForm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Scrape {activeTab === 'company' ? 'Company' : 'Competitor'} Reviews
            </h3>
            <form onSubmit={handleScrapeSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Business Name
                </label>
                <input
                  type="text"
                  value={scrapeForm.business_name}
                  onChange={(e) => setScrapeForm({ ...scrapeForm, business_name: e.target.value })}
                  className="input"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location (Optional)
                </label>
                <input
                  type="text"
                  value={scrapeForm.location}
                  onChange={(e) => setScrapeForm({ ...scrapeForm, location: e.target.value })}
                  className="input"
                  placeholder="City, State"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Platforms
                </label>
                <div className="space-y-2">
                  {['google', 'yelp', 'tripadvisor'].map((platform) => (
                    <label key={platform} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={scrapeForm.platforms.includes(platform)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setScrapeForm({
                              ...scrapeForm,
                              platforms: [...scrapeForm.platforms, platform],
                            });
                          } else {
                            setScrapeForm({
                              ...scrapeForm,
                              platforms: scrapeForm.platforms.filter(p => p !== platform),
                            });
                          }
                        }}
                        className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 capitalize">{platform}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowScrapeForm(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Scrape Reviews
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
