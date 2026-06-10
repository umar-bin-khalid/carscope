import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export interface Car {
  id: number | string;
  make: string;
  model: string;
  year: number;
  price: number;
  mileage: number;
  location: string;
  description?: string;
  image_url?: string;
  source?: string;        // "local" or "marketcheck"
  listing_url?: string;   // Marketcheck VDP URL
  vin?: string;
  trim?: string;
}

export interface SearchFilters {
  make?: string;
  model?: string;
  year_min?: number;
  year_max?: number;
  price_min?: number;
  price_max?: number;
  mileage_max?: number;
  location?: string;
}

export interface MarketCheckFilters {
  make?: string;
  model?: string;
  year?: number;
  price_min?: number;
  price_max?: number;
  mileage_max?: number;
  zip?: string;
  radius?: number;
  car_type?: string;
  start?: number;
  rows?: number;
}

export interface MarketCheckSearchResponse {
  num_found: number;
  listings: Car[];
}

export interface ToolCallRecord {
  tool: string;
  args: Record<string, unknown>;
  result_summary: string;
}

export interface ChatRequest {
  question: string;
  current_car_id?: number | string;
  search_filters?: Record<string, unknown>;
  saved_car_ids?: (number | string)[];
  /** Full car objects so the agent can reason about Marketcheck listings */
  current_cars_snapshot?: Car[];
  saved_cars_snapshot?: Car[];
}

export interface ChatResponse {
  answer: string;
  tool_calls: ToolCallRecord[];
}

// Local car API
export const carAPI = {
  getAll: (filters?: SearchFilters) => apiClient.get<Car[]>('/cars', { params: filters }),
  getById: (id: number) => apiClient.get<Car>(`/cars/${id}`),
};

// Marketcheck API (proxied through backend)
export const marketcheckAPI = {
  search: (filters?: MarketCheckFilters) =>
    apiClient.get<MarketCheckSearchResponse>('/marketcheck/search', { params: filters }),
  getDetail: (listingId: string) =>
    apiClient.get<Car>(`/marketcheck/listing/${listingId}`),
};

// Chat API
export const chatAPI = {
  ask: (request: ChatRequest) => apiClient.post<ChatResponse>('/chat/ask', request),
};
