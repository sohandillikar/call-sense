export interface CallRecord {
  id: number;
  created_at: string;
  phone: string;
  transcript: string;
  sentiments: number | null;
  insights: string;
  solved: boolean;
}

export interface GetCallsRequest {
  phone: string;
}

export interface GetCallsResponse {
  calls: CallRecord[];
}

export interface SaveCallRequest {
  phone: string;
  transcript: string;
  sentiment: number;
  insight: string;
  solved: boolean;
}

export interface SaveCallResponse {
  success: boolean;
  call_id: number;
  message: string;
}

export interface ApiError {
  detail: string;
}
