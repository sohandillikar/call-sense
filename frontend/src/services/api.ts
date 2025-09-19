import type { 
  GetCallsResponse, 
  SaveCallRequest, 
  SaveCallResponse
} from '../types/api';

const API_BASE_URL = 'http://localhost:8000';

// Helper function to handle API responses
const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

// Helper function to make API requests
const apiRequest = async <T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  console.log(`Making ${options.method || 'GET'} request to ${url}`);
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const response = await fetch(url, { ...defaultOptions, ...options });
  
  if (!response.ok) {
    console.error('API Error:', response.status, response.statusText);
  }
  
  return handleResponse<T>(response);
};

export const callsApi = {
  // Get all calls for a specific phone number
  getCalls: async (phone: string): Promise<GetCallsResponse> => {
    try {
      return await apiRequest<GetCallsResponse>('/get_calls', {
        method: 'POST',
        body: JSON.stringify({ phone }),
      });
    } catch (error: any) {
      throw new Error(error.message || 'Failed to fetch calls');
    }
  },

  // Save a new call record
  saveCall: async (callData: SaveCallRequest): Promise<SaveCallResponse> => {
    try {
      return await apiRequest<SaveCallResponse>('/save_call', {
        method: 'POST',
        body: JSON.stringify(callData),
      });
    } catch (error: any) {
      throw new Error(error.message || 'Failed to save call');
    }
  },

  // Check if API is running
  healthCheck: async (): Promise<{ message: string }> => {
    try {
      return await apiRequest<{ message: string }>('/');
    } catch (error: any) {
      throw new Error('API is not available');
    }
  },
};

// Export the base API URL for other uses
export { API_BASE_URL };
