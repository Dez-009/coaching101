export interface QueryRequest {
  text: string;
}

export interface QueryResult {
  id: number;
  username?: string;
  email?: string;
  role?: string;
  created_at?: string;
  last_login?: string | null;
  // Add other possible fields from different databases
  [key: string]: any;
}

export interface QueryResponse {
  result: QueryResult[];
  source: 'cache' | 'database';
  parsed_query?: {
    target_db: string;
    operation: string;
    conditions: Record<string, string>;
  };
}
