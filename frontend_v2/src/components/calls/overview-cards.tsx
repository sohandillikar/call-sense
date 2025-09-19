import { TrendingUp, TrendingDown, Phone, CheckCircle, XCircle, BarChart3 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CallStats } from '@/types/calls';
import { formatSentimentScore } from '@/utils/sentiment';

interface OverviewCardsProps {
  stats: CallStats;
  isLoading?: boolean;
}

export const OverviewCards = ({ stats, isLoading = false }: OverviewCardsProps) => {
  const cards = [
    {
      title: 'Total Calls',
      value: stats.total.toString(),
      icon: Phone,
      description: 'All customer calls',
      gradient: 'gradient-primary',
    },
    {
      title: 'Resolved Issues',
      value: `${stats.solved}/${stats.total}`,
      icon: CheckCircle,
      description: `${stats.total > 0 ? ((stats.solved / stats.total) * 100).toFixed(1) : 0}% resolution rate`,
      gradient: 'gradient-success',
    },
    {
      title: 'Pending Issues',
      value: stats.unsolved.toString(),
      icon: XCircle,
      description: 'Require follow-up',
      gradient: 'gradient-warning',
    },
    {
      title: 'Avg. Sentiment',
      value: `${formatSentimentScore(stats.averageSentiment)}%`,
      icon: stats.averageSentiment >= 0 ? TrendingUp : TrendingDown,
      description: stats.averageSentiment >= 0 ? 'Positive trend' : 'Needs attention',
      gradient: stats.averageSentiment >= 0 ? 'gradient-success' : 'gradient-destructive',
    },
  ];

  if (isLoading) {
    return (
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <div className="h-4 bg-muted rounded w-24"></div>
              <div className="h-4 w-4 bg-muted rounded"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-muted rounded w-16 mb-2"></div>
              <div className="h-3 bg-muted rounded w-20"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <Card 
            key={card.title} 
            className="group relative overflow-hidden border border-border/50 bg-gradient-to-br from-card to-card/80 hover:from-card-hover hover:to-card-hover/80 transition-all duration-300 hover:-translate-y-1 animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className={`absolute inset-0 opacity-[0.02] group-hover:opacity-[0.04] transition-opacity ${card.gradient}`}></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 relative z-10">
              <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors">
                {card.title}
              </CardTitle>
              <div className={`p-2 rounded-lg transition-all duration-300 ${card.gradient.includes('success') ? 'bg-success/10' : card.gradient.includes('warning') ? 'bg-warning/10' : card.gradient.includes('destructive') ? 'bg-destructive/10' : 'bg-primary/10'}`}>
                <Icon className={`h-4 w-4 ${card.gradient.includes('success') ? 'text-success' : card.gradient.includes('warning') ? 'text-warning' : card.gradient.includes('destructive') ? 'text-destructive' : 'text-primary'}`} />
              </div>
            </CardHeader>
            <CardContent className="relative z-10 pb-6">
              <div className="text-3xl font-bold text-card-foreground mb-2 group-hover:scale-105 transition-transform">
                {card.value}
              </div>
              <p className="text-sm text-muted-foreground group-hover:text-muted-foreground/80 transition-colors">
                {card.description}
              </p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
};