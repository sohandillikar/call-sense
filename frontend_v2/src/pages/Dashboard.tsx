import { useState, useEffect, useMemo } from 'react';
import { toast } from '@/hooks/use-toast';
import { Call, ApiError } from '@/types/calls';
import { apiClient } from '@/utils/api';
import { calculateCallStats, getSentimentLevel } from '@/utils/sentiment';
import { DashboardHeader } from '@/components/calls/dashboard-header';
import { OverviewCards } from '@/components/calls/overview-cards';
import { SearchFilter } from '@/components/calls/search-filter';
import { CallList } from '@/components/calls/call-list';
import { SentimentChart } from '@/components/calls/sentiment-chart';

interface DashboardProps {
  phone: string;
  onLogout: () => void;
}

export const Dashboard = ({ phone, onLogout }: DashboardProps) => {
  const [calls, setCalls] = useState<Call[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'solved' | 'unsolved'>('all');
  const [sentimentFilter, setSentimentFilter] = useState<'all' | 'positive' | 'neutral' | 'negative'>('all');

  const loadCalls = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setIsRefreshing(true);
      }
      
      const callsData = await apiClient.getCalls(phone);
      setCalls(callsData);
      
      if (isRefresh) {
        toast({
          title: "Data refreshed",
          description: `Loaded ${callsData.length} calls`,
        });
      }
    } catch (error) {
      const errorMessage = error instanceof ApiError 
        ? error.message 
        : 'Failed to load calls. Please try again.';
      
      toast({
        title: "Error loading calls",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadCalls();
  }, [phone]);

  // Filter calls based on search and filters
  const filteredCalls = useMemo(() => {
    return calls.filter(call => {
      // Search filter
      if (searchTerm && !call.phone.toLowerCase().includes(searchTerm.toLowerCase())) {
        return false;
      }

      // Status filter
      if (statusFilter !== 'all') {
        if (statusFilter === 'solved' && !call.solved) return false;
        if (statusFilter === 'unsolved' && call.solved) return false;
      }

      // Sentiment filter
      if (sentimentFilter !== 'all') {
        const callSentiment = getSentimentLevel(call.sentiments);
        if (callSentiment !== sentimentFilter) return false;
      }

      return true;
    });
  }, [calls, searchTerm, statusFilter, sentimentFilter]);

  // Calculate stats for filtered calls
  const stats = useMemo(() => calculateCallStats(filteredCalls), [filteredCalls]);

  const handleRefresh = () => {
    loadCalls(true);
  };

  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader
        phone={phone}
        onLogout={onLogout}
        onRefresh={handleRefresh}
        isRefreshing={isRefreshing}
      />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Overview Cards */}
          <section>
            <h2 className="text-2xl font-bold mb-6 animate-fade-in">Overview</h2>
            <OverviewCards stats={stats} isLoading={isLoading} />
          </section>

          {/* Sentiment Analytics */}
          <section className="animate-fade-in" style={{ animationDelay: '0.1s' }}>
            <SentimentChart calls={filteredCalls} isLoading={isLoading} />
          </section>

          {/* Search and Filters */}
          <section className="animate-fade-in" style={{ animationDelay: '0.2s' }}>
            <SearchFilter
              searchTerm={searchTerm}
              onSearchChange={setSearchTerm}
              statusFilter={statusFilter}
              onStatusFilterChange={setStatusFilter}
              sentimentFilter={sentimentFilter}
              onSentimentFilterChange={setSentimentFilter}
            />
          </section>

          {/* Call List */}
          <section className="animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <CallList calls={filteredCalls} isLoading={isLoading} />
          </section>
        </div>
      </main>
    </div>
  );
};