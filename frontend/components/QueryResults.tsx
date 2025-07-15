import React from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
} from '@mui/material';
import { QueryResult } from '../types/api';

interface Props {
  results: QueryResult[];
  source: 'cache' | 'database';
  parsedQuery?: {
    target_db: string;
    operation: string;
    conditions: Record<string, string>;
  };
}

export const QueryResults: React.FC<Props> = ({ results, source, parsedQuery }) => {
  if (!results.length) {
    return (
      <Box sx={{ mt: 4 }}>
        <Typography color="textSecondary">No results found</Typography>
      </Box>
    );
  }

  // Get all unique keys from the results to use as columns
  const columns = Array.from(new Set(results.flatMap(r => Object.keys(r))));

  return (
    <Box sx={{ mt: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2 }}>
        {parsedQuery && (
          <>
            <Chip 
              label={parsedQuery.target_db}
              color="primary"
              size="small"
            />
            <Chip 
              label={parsedQuery.operation}
              color="secondary"
              size="small"
            />
          </>
        )}
        <Chip 
          label={source}
          color={source === 'cache' ? 'success' : 'info'}
          size="small"
        />
      </Box>
      <TableContainer component={Paper} elevation={2}>
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map(column => (
                <TableCell key={column}>{column}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {results.map((row, index) => (
              <TableRow key={index}>
                {columns.map(column => (
                  <TableCell key={column}>
                    {row[column] !== null ? row[column]?.toString() : ''}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Natural Language Response */}
      <Paper sx={{ mt: 3, p: 3, bgcolor: 'background.paper' }}>
        <Typography variant="h6" gutterBottom>
          Agent Response
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {parsedQuery ? (
            `I found ${results.length} results from the ${parsedQuery.target_db} database. ` +
            `This query was ${parsedQuery.operation === 'select' ? 'searching for' : parsedQuery.operation} ` +
            `data with these conditions: ${Object.entries(parsedQuery.conditions)
              .map(([key, value]) => `${key} is ${value}`)
              .join(', ')}.`
          ) : (
            'Here are the results of your query.'
          )}
        </Typography>
      </Paper>
    </Box>
  );
};

export default QueryResults;
