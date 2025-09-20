import { useState } from 'react';
import { Phone } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { validatePhoneNumber, formatPhoneNumber } from '@/utils/api';

interface LoginFormProps {
  onLogin: (phone: string) => void;
  isLoading?: boolean;
  error?: string | null;
}

export const LoginForm = ({ onLogin, isLoading = false, error }: LoginFormProps) => {
  const [phone, setPhone] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const trimmedPhone = phone.trim();
    
    if (!trimmedPhone) {
      setValidationError('Please enter a phone number');
      return;
    }
    
    if (!validatePhoneNumber(trimmedPhone)) {
      setValidationError('Please enter a valid phone number');
      return;
    }
    
    setValidationError(null);
    const formattedPhone = formatPhoneNumber(trimmedPhone);
    onLogin(formattedPhone);
  };

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhone(e.target.value);
    if (validationError) {
      setValidationError(null);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-light via-background to-accent p-4">
      <div className="animate-fade-in">
        <Card className="w-full max-w-md shadow-xl border-0 bg-card/95 backdrop-blur-sm">
          <CardHeader className="text-center space-y-4">
            <div className="mx-auto w-16 h-16 bg-primary rounded-2xl flex items-center justify-center shadow-lg">
              <Phone className="w-8 h-8 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold">Customer Calls Analytics</CardTitle>
              <CardDescription className="text-muted-foreground mt-2">
                Enter your phone number to view your call analytics
              </CardDescription>
            </div>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="tel"
                  placeholder="+1 (555) 123-4567"
                  value={phone}
                  onChange={handlePhoneChange}
                  disabled={isLoading}
                  className="h-12 text-lg transition-all duration-200"
                  autoFocus
                />
                {validationError && (
                  <p className="text-destructive text-sm animate-fade-in">
                    {validationError}
                  </p>
                )}
                {error && (
                  <p className="text-destructive text-sm animate-fade-in">
                    {error}
                  </p>
                )}
              </div>
              
              <Button
                type="submit"
                disabled={isLoading || !phone.trim()}
                className="w-full h-12 text-lg font-semibold gradient-primary hover:opacity-90 transition-all duration-300"
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <LoadingSpinner size="sm" />
                    Connecting...
                  </div>
                ) : (
                  'Access Dashboard'
                )}
              </Button>
            </form>
            
            <div className="mt-6 text-center">
              <p className="text-xs text-muted-foreground">
                No password required. Your phone number is used to identify your calls.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};