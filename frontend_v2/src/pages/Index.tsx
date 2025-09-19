import { useState } from 'react';
import { toast } from '@/hooks/use-toast';
import { LoginForm } from '@/components/calls/login-form';
import { Dashboard } from '@/pages/Dashboard';
import { ApiError } from '@/types/calls';
import { apiClient } from '@/utils/api';

const Index = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userPhone, setUserPhone] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [loginError, setLoginError] = useState<string | null>(null);

  const handleLogin = async (phone: string) => {
    setIsLoading(true);
    setLoginError(null);
    
    try {
      // Test the connection and fetch calls
      await apiClient.getCalls(phone);
      
      setUserPhone(phone);
      setIsLoggedIn(true);
      
      toast({
        title: "Welcome!",
        description: "Successfully connected to your call analytics dashboard.",
      });
    } catch (error) {
      const errorMessage = error instanceof ApiError 
        ? error.message 
        : 'Unable to connect. Please check your connection and try again.';
      
      setLoginError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserPhone('');
    setLoginError(null);
    
    toast({
      title: "Logged out",
      description: "You have been successfully logged out.",
    });
  };

  if (isLoggedIn && userPhone) {
    return <Dashboard phone={userPhone} onLogout={handleLogout} />;
  }

  return (
    <LoginForm 
      onLogin={handleLogin} 
      isLoading={isLoading}
      error={loginError}
    />
  );
};

export default Index;
