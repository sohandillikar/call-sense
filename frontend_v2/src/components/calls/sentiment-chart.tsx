import { useMemo } from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Call } from '@/types/calls';
import { getSentimentLevel } from '@/utils/sentiment';
import { TrendingUp, BarChart3, PieChart as PieChartIcon } from 'lucide-react';

interface SentimentChartProps {
  calls: Call[];
  isLoading?: boolean;
}

export const SentimentChart = ({ calls, isLoading = false }: SentimentChartProps) => {
  const sentimentData = useMemo(() => {
    const distribution = calls.reduce((acc, call) => {
      const level = getSentimentLevel(call.sentiments);
      acc[level] = (acc[level] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return [
      { name: 'Positive', value: distribution.positive || 0, color: 'hsl(var(--success))' },
      { name: 'Neutral', value: distribution.neutral || 0, color: 'hsl(var(--warning))' },
      { name: 'Negative', value: distribution.negative || 0, color: 'hsl(var(--destructive))' },
    ];
  }, [calls]);

  const trendData = useMemo(() => {
    if (calls.length === 0) return [];
    
    // Group calls by day and calculate average sentiment
    const groupedByDay = calls.reduce((acc, call) => {
      const date = new Date(call.created_at).toLocaleDateString();
      if (!acc[date]) {
        acc[date] = { sentiments: [], date };
      }
      acc[date].sentiments.push(call.sentiments);
      return acc;
    }, {} as Record<string, { sentiments: number[], date: string }>);

    return Object.values(groupedByDay)
      .map(({ sentiments, date }) => ({
        date,
        sentiment: (sentiments.reduce((sum, s) => sum + s, 0) / sentiments.length * 100).toFixed(1),
        calls: sentiments.length,
      }))
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
      .slice(-7); // Last 7 days
  }, [calls]);

  if (isLoading) {
    return (
      <Card className="border border-border/50 bg-gradient-to-br from-card to-card/80">
        <CardHeader>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-muted rounded animate-pulse" />
            <div className="w-32 h-5 bg-muted rounded animate-pulse" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="w-full h-64 bg-muted rounded animate-pulse" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border border-border/50 bg-gradient-to-br from-card to-card/80">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <TrendingUp className="h-5 w-5 text-primary" />
          Sentiment Analytics
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="distribution" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="distribution" className="flex items-center gap-2">
              <PieChartIcon className="h-4 w-4" />
              Distribution
            </TabsTrigger>
            <TabsTrigger value="trend" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Trend
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="distribution" className="space-y-4">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    formatter={(value: number) => [`${value} calls`, 'Count']}
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-3 gap-4 text-center">
              {sentimentData.map((item) => (
                <div key={item.name} className="space-y-1">
                  <div className="text-2xl font-bold" style={{ color: item.color }}>
                    {item.value}
                  </div>
                  <div className="text-sm text-muted-foreground">{item.name}</div>
                </div>
              ))}
            </div>
          </TabsContent>
          
          <TabsContent value="trend" className="space-y-4">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={trendData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="date" 
                    tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
                    tickFormatter={(value) => new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(new Date(value))}
                  />
                  <YAxis 
                    tick={{ fontSize: 12, fill: 'hsl(var(--muted-foreground))' }}
                    label={{ value: 'Sentiment %', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    formatter={(value: string, name: string) => [`${value}%`, 'Avg Sentiment']}
                    labelFormatter={(label) => `Date: ${label}`}
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar 
                    dataKey="sentiment" 
                    fill="hsl(var(--primary))"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};