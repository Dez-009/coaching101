import axios from 'axios';
import { QueryRequest, QueryResponse } from '../types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const orchestratorApi = {
  async executeQuery(request: QueryRequest): Promise<QueryResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/query`, request, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      return response.data as QueryResponse;
    } catch (error) {
      if (error && typeof error === 'object' && 'response' in error) {
        throw new Error(error.response?.data?.detail || (error as Error).message);
      }
      throw error;
    }
  }
};
