import { Call, CallsResponse, CallsRequest, ApiError } from '@/types/calls';

const API_BASE_URL = 'http://localhost:8000';

class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.text();
        throw new ApiError(
          errorData || `HTTP error! status: ${response.status}`,
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      // Network or other errors
      throw new ApiError(
        error instanceof Error ? error.message : 'An unexpected error occurred'
      );
    }
  }

  async getCalls(phone: string): Promise<Call[]> {
    const requestBody: CallsRequest = { phone };
    const response = await this.request<CallsResponse>('/get_calls', {
      method: 'POST',
      body: JSON.stringify(requestBody),
    });
    return response.calls;
  }

  async healthCheck(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/');
  }
}

// Create a singleton instance
export const apiClient = new ApiClient();

// Helper functions
export const validatePhoneNumber = (phone: string): boolean => {
  // Basic phone number validation - accepts various formats
  const phoneRegex = /^\+?[\d\s\-\(\)]{10,}$/;
  return phoneRegex.test(phone.trim());
};

export const formatPhoneNumber = (phone: string): string => {
  // Remove all non-digit characters except +
  const cleaned = phone.replace(/[^\d+]/g, '');
  
  // Ensure it starts with + if it doesn't already
  if (!cleaned.startsWith('+')) {
    return `+${cleaned}`;
  }
  
  return cleaned;
};