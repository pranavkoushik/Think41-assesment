import { ChakraProvider, Box, Container, extendTheme } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ErrorBoundary } from 'react-error-boundary';
import CustomerList from './components/CustomerList';
import CustomerDetails from './components/CustomerDetails';
import Navbar from './components/Navbar';

// Extend the default theme
const theme = extendTheme({
  styles: {
    global: {
      'html, body': {
        fontFamily: 'Inter, system-ui, sans-serif',
      },
    },
  },
  colors: {
    brand: {
      50: '#e6f7ff',
      100: '#b3e0ff',
      500: '#0080ff',
      600: '#0066cc',
    },
  },
});

// Error boundary fallback component
function ErrorFallback({ error, resetErrorBoundary }: any) {
  return (
    <Box p={8} maxW="container.md" mx="auto" textAlign="center">
      <Box p={8} borderWidth={1} borderRadius="lg" boxShadow="md" bg="white">
        <h1 style={{ fontSize: '24px', color: 'red', marginBottom: '16px' }}>Something went wrong</h1>
        <pre style={{ 
          padding: '16px', 
          marginBottom: '24px',
          textAlign: 'left',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word'
        }}>
          {error.message}
        </pre>
        <button 
          onClick={resetErrorBoundary}
          style={{
            backgroundColor: '#0080ff',
            color: 'white',
            padding: '8px 24px',
            borderRadius: '4px',
            border: 'none',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Try again
        </button>
      </Box>
    </Box>
  );
}

function App() {
  return (
    <ChakraProvider theme={theme}>
      <ErrorBoundary
        FallbackComponent={ErrorFallback}
        onReset={() => {
          window.location.href = '/';
        }}
      >
        <Router>
          <Box minH="100vh" bg="gray.50">
            <Navbar />
            <Container maxW="container.xl" py={8}>
              <Routes>
                <Route path="/" element={<CustomerList />} />
                <Route path="/customers/:id" element={<CustomerDetails />} />
              </Routes>
            </Container>
          </Box>
        </Router>
      </ErrorBoundary>
    </ChakraProvider>
  );
}

export default App;
