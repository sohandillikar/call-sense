export interface Call {
  id: number;
  created_at: string;
  phone: string;
  transcript: string;
  sentiments: number;
  insights: string;
  solved: boolean;
}

export interface CallsResponse {
  calls: Call[];
}

export interface CallsRequest {
  phone: string;
}

export class ApiError extends Error {
  status?: number;
  
  constructor(message: string, status?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

export type SentimentLevel = 'positive' | 'neutral' | 'negative';

export interface CallStats {
  total: number;
  solved: number;
  unsolved: number;
  averageSentiment: number;
  sentimentDistribution: {
    positive: number;
    neutral: number;
    negative: number;
  };
}