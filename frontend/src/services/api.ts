import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Types
export interface CallTranscription {
  call_id: string;
  customer_phone: string;
  call_type: string;
  transcription: string;
  sentiment_score: number;
  sentiment_label: string;
  key_topics: string[];
  action_items: string[];
  priority_score: number;
  similar_calls: any[];
  created_at: string;
}

export interface Review {
  platform: string;
  reviewer_name: string;
  rating: number;
  review_text: string;
  sentiment_score: number;
  sentiment_label: string;
  key_themes: string[];
}

export interface CompetitorAlert {
  id: number;
  competitor_name: string;
  alert_type: string;
  alert_description: string;
  severity: string;
  is_read: boolean;
  alert_metadata: any;
  created_at: string;
}

export interface BusinessInsight {
  id: number;
  insight_type: string;
  title: string;
  description: string;
  confidence_score: number;
  impact_level: string;
  recommendations: string[];
  created_at: string;
}

export interface AnalyticsOverview {
  period_days: number;
  customer_satisfaction: {
    data_points: number;
    trend: string;
  };
  recommendations: string[];
  last_updated: string;
}

// API functions
export const callsApi = {
  // Get all calls
  getCalls: async (): Promise<CallTranscription[]> => {
    const response = await api.get('/api/v1/calls/');
    return response.data;
  },

  // Transcribe a call
  transcribeCall: async (data: {
    customer_phone: string;
    call_type: string;
    transcription_text: string;
  }): Promise<CallTranscription> => {
    const response = await api.post('/api/v1/calls/transcribe', data);
    return response.data;
  },

  // Upload and transcribe call
  uploadAndTranscribe: async (formData: FormData): Promise<CallTranscription> => {
    const response = await api.post('/api/v1/calls/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const reviewsApi = {
  // Scrape company reviews
  scrapeCompanyReviews: async (data: {
    business_name: string;
    location?: string;
    platforms?: string[];
  }): Promise<Review[]> => {
    const response = await api.post('/api/v1/reviews/scrape-company', data);
    return response.data;
  },

  // Scrape competitor reviews
  scrapeCompetitorReviews: async (data: {
    business_name: string;
    location?: string;
    platforms?: string[];
  }): Promise<Review[]> => {
    const response = await api.post('/api/v1/reviews/scrape-competitor', data);
    return response.data;
  },

  // Get company reviews
  getCompanyReviews: async (companyName: string = 'default'): Promise<Review[]> => {
    const response = await api.get(`/api/v1/reviews/company/${companyName}`);
    return response.data;
  },

  // Get competitor reviews
  getCompetitorReviews: async (competitorName: string = 'default'): Promise<Review[]> => {
    const response = await api.get(`/api/v1/reviews/competitor/${competitorName}`);
    return response.data;
  },
};

export const competitorsApi = {
  // Get all competitors
  getCompetitors: async (): Promise<any[]> => {
    const response = await api.get('/api/v1/competitors/');
    return response.data;
  },

  // Get competitor alerts
  getAlerts: async (): Promise<CompetitorAlert[]> => {
    const response = await api.get('/api/v1/competitors/alerts');
    return response.data;
  },

  // Mark alert as read
  markAlertAsRead: async (alertId: number): Promise<void> => {
    await api.post(`/api/v1/competitors/alerts/${alertId}/mark-read`);
  },

  // Get competitor pricing
  getCompetitorPricing: async (competitorName: string): Promise<any> => {
    const response = await api.get(`/api/v1/competitors/pricing/${competitorName}`);
    return response.data;
  },

  // Add competitor
  addCompetitor: async (data: {
    competitor_name: string;
    website_url: string;
    industry: string;
    market_position?: string;
  }): Promise<any> => {
    const response = await api.post('/api/v1/competitors/add', data);
    return response.data;
  },

  // Monitor competitor (legacy - redirects to add)
  monitorCompetitor: async (data: {
    competitor_name: string;
    monitoring_type: string;
    frequency: string;
  }): Promise<any> => {
    // Convert monitoring request to add competitor request
    const addData = {
      competitor_name: data.competitor_name,
      website_url: `https://${data.competitor_name.toLowerCase().replace(/\s+/g, '')}.com`,
      industry: "Technology", // Default industry
      market_position: "competitive"
    };
    const response = await api.post('/api/v1/competitors/add', addData);
    return response.data;
  },
};

export const insightsApi = {
  // Get business insights
  getInsights: async (): Promise<BusinessInsight[]> => {
    const response = await api.get('/api/v1/insights/');
    return response.data;
  },

  // Generate insights
  generateInsights: async (data: {
    insight_type: string;
    data_sources: string[];
    analysis_period_days: number;
  }): Promise<BusinessInsight[]> => {
    const response = await api.post('/api/v1/insights/generate', data);
    return response.data;
  },
};

export const analyticsApi = {
  // Get analytics overview
  getOverview: async (): Promise<AnalyticsOverview> => {
    const response = await api.get('/api/v1/analytics/trends/overview');
    return response.data;
  },

  // Get metrics summary
  getMetricsSummary: async (): Promise<any> => {
    const response = await api.get('/api/v1/analytics/metrics/summary');
    return response.data;
  },

  // Get dashboard widgets
  getDashboardWidgets: async (): Promise<any[]> => {
    const response = await api.get('/api/v1/analytics/widgets');
    return response.data;
  },
};

export const healthApi = {
  // Check health
  checkHealth: async (): Promise<{ status: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
