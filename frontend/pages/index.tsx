import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import { orchestratorApi } from '../services/api';
import QueryResults from '../components/QueryResults';
import { ThemeProvider } from '@mui/material/styles';
import { theme } from '../styles/theme';

export default function Home() {
  const [query, setQuery] = useState('');
  
  const { data, error, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['query', query],
    queryFn: () => orchestratorApi.executeQuery({ text: query }),
    enabled: false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      refetch();
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Database Query Assistant
          </Typography>
          
          <Paper 
            component="form" 
            onSubmit={handleSubmit}
            elevation={2}
            sx={{ p: 3, mb: 4 }}
          >
            <TextField
              fullWidth
              label="Enter your query in natural language"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              multiline
              rows={3}
              variant="outlined"
              placeholder="Example: Find users with role admin"
              sx={{ mb: 2 }}
            />
            <Button 
              type="submit"
              variant="contained"
              size="large"
              disabled={!query.trim() || isLoading || isFetching}
              sx={{ minWidth: 150 }}
            >
              {(isLoading || isFetching) ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Execute Query'
              )}
            </Button>
          </Paper>

          {error ? (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error instanceof Error ? error.message : 'An error occurred'}
            </Alert>
          ) : data ? (
            <QueryResults 
              results={data.result} 
              source={data.source} 
              parsedQuery={data.parsed_query}
            />
          ) : null}
        </Box>
      </Container>
    </ThemeProvider>
  );
}
