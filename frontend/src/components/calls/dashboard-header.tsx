import { LogOut, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DashboardHeaderProps {
  phone: string;
  onLogout: () => void;
  onRefresh: () => void;
  isRefreshing?: boolean;
}

export const DashboardHeader = ({ 
  phone, 
  onLogout, 
  onRefresh, 
  isRefreshing = false 
}: DashboardHeaderProps) => {
  return (
    <header className="bg-card border-b border-border/50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-foreground">
              Call Analytics
            </h1>
            <div className="ml-4 px-3 py-1 bg-muted rounded-full text-sm text-muted-foreground">
              {phone}
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onRefresh}
              disabled={isRefreshing}
              className="gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={onLogout}
              className="gap-2"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};