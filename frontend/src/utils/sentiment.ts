import { SentimentLevel, Call, CallStats } from '@/types/calls';

export const getSentimentLevel = (score: number): SentimentLevel => {
  if (score >= 0.2) return 'positive';
  if (score <= -0.2) return 'negative';
  return 'neutral';
};

export const getSentimentColor = (score: number): string => {
  const level = getSentimentLevel(score);
  switch (level) {
    case 'positive':
      return 'success';
    case 'negative':
      return 'destructive';
    case 'neutral':
      return 'warning';
  }
};

export const getSentimentLabel = (score: number): string => {
  const level = getSentimentLevel(score);
  switch (level) {
    case 'positive':
      return 'Positive';
    case 'negative':
      return 'Negative';
    case 'neutral':
      return 'Neutral';
  }
};

export const calculateCallStats = (calls: Call[]): CallStats => {
  if (calls.length === 0) {
    return {
      total: 0,
      solved: 0,
      unsolved: 0,
      averageSentiment: 0,
      sentimentDistribution: {
        positive: 0,
        neutral: 0,
        negative: 0,
      },
    };
  }

  const solved = calls.filter(call => call.solved).length;
  const unsolved = calls.length - solved;
  
  const averageSentiment = calls.reduce((sum, call) => sum + call.sentiments, 0) / calls.length;
  
  const sentimentDistribution = calls.reduce(
    (acc, call) => {
      const level = getSentimentLevel(call.sentiments);
      acc[level]++;
      return acc;
    },
    { positive: 0, neutral: 0, negative: 0 }
  );

  return {
    total: calls.length,
    solved,
    unsolved,
    averageSentiment,
    sentimentDistribution,
  };
};

export const formatSentimentScore = (score: number): string => {
  return (score * 100).toFixed(1);
};