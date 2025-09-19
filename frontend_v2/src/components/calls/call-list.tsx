import { useState } from 'react';
import { 
  Calendar, 
  ChevronDown, 
  ChevronUp, 
  MessageSquare, 
  Lightbulb,
  CheckCircle,
  XCircle,
  Phone
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Call } from '@/types/calls';
import { getSentimentColor, getSentimentLabel } from '@/utils/sentiment';

interface CallListProps {
  calls: Call[];
  isLoading?: boolean;
}

export const CallList = ({ calls, isLoading = false }: CallListProps) => {
  const [expandedCalls, setExpandedCalls] = useState<Set<number>>(new Set());

  const toggleExpanded = (callId: number) => {
    const newExpanded = new Set(expandedCalls);
    if (newExpanded.has(callId)) {
      newExpanded.delete(callId);
    } else {
      newExpanded.add(callId);
    }
    setExpandedCalls(newExpanded);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric' 
      }),
      time: date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
    };
  };

  if (isLoading) {
    return (
      <Card className="shadow-md border-0">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5" />
            Call History
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="animate-pulse">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-muted rounded"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-muted rounded w-32"></div>
                    <div className="h-3 bg-muted rounded w-24"></div>
                  </div>
                </div>
                <div className="h-6 bg-muted rounded w-16"></div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  if (calls.length === 0) {
    return (
      <Card className="shadow-md border-0">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5" />
            Call History
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Phone className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No calls found for this number</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-md border-0">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5" />
          Call History ({calls.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {calls.map((call, index) => {
            const { date, time } = formatDate(call.created_at);
            const sentimentColor = getSentimentColor(call.sentiments);
            const sentimentLabel = getSentimentLabel(call.sentiments);
            const isExpanded = expandedCalls.has(call.id);

            return (
              <Collapsible
                key={call.id}
                open={isExpanded}
                onOpenChange={() => toggleExpanded(call.id)}
              >
                <div 
                  className="animate-fade-in border border-border/50 rounded-lg hover:bg-card-hover transition-all duration-300 hover:border-primary/30"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <CollapsibleTrigger asChild>
                    <Button
                      variant="ghost"
                      className="w-full p-4 h-auto justify-between hover:bg-card-hover"
                    >
                      <div className="flex items-center gap-3 text-left">
                        <div className="flex flex-col items-center">
                          <Calendar className="w-4 h-4 text-muted-foreground" />
                          <span className="text-xs text-muted-foreground mt-1">
                            {date}
                          </span>
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium">{call.phone}</span>
                            <Badge 
                              variant={call.solved ? "default" : "secondary"}
                              className={`text-xs ${
                                call.solved 
                                  ? "bg-success text-success-foreground" 
                                  : "bg-warning text-warning-foreground"
                              }`}
                            >
                              {call.solved ? (
                                <><CheckCircle className="w-3 h-3 mr-1" />Resolved</>
                              ) : (
                                <><XCircle className="w-3 h-3 mr-1" />Pending</>
                              )}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-2 text-sm text-muted-foreground">
                            <span>{time}</span>
                            <Badge 
                              variant="outline" 
                              className={`border-${sentimentColor} text-${sentimentColor}`}
                            >
                              {sentimentLabel}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      {isExpanded ? (
                        <ChevronUp className="w-4 h-4" />
                      ) : (
                        <ChevronDown className="w-4 h-4" />
                      )}
                    </Button>
                  </CollapsibleTrigger>
                  
                  <CollapsibleContent className="px-4 pb-4 animate-slide-up">
                    <div className="space-y-4 mt-2 border-t pt-4">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <MessageSquare className="w-4 h-4 text-muted-foreground" />
                          <span className="font-medium text-sm">Transcript</span>
                        </div>
                        <div className="bg-muted/50 p-3 rounded-md text-sm leading-relaxed">
                          {call.transcript}
                        </div>
                      </div>
                      
                      {call.insights && (
                        <div>
                          <div className="flex items-center gap-2 mb-2">
                            <Lightbulb className="w-4 h-4 text-muted-foreground" />
                            <span className="font-medium text-sm">AI Insights</span>
                          </div>
                          <div className="bg-primary-light/50 p-3 rounded-md text-sm leading-relaxed border-l-4 border-primary">
                            {call.insights}
                          </div>
                        </div>
                      )}
                    </div>
                  </CollapsibleContent>
                </div>
              </Collapsible>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};