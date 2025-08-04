import { useState, useEffect } from 'react';
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
  InputGroup,
  InputLeftElement,
  Box,
  Spinner,
  Text,
  Link,
  Badge,
  Heading,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  orders_count: number;
  created_at: string;
}

const API_URL = '/api'; // Using proxy from Vite config

export default function CustomerList() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axios.get(`${API_URL}/customers`);
        setCustomers(response.data.data);
      } catch (error) {
        console.error('Error fetching customers:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(
    (customer) =>
      customer.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" />
      </Box>
    );
  }

  return (
    <Box>
      <Box mb={6}>
        <Heading size="lg" mb={4}>Customers</Heading>
        <InputGroup maxW="md" mb={6}>
          <InputLeftElement pointerEvents="none">
            <SearchIcon color="gray.300" />
          </InputLeftElement>
          <Input
            placeholder="Search customers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            bg="white"
          />
        </InputGroup>

        <Box bg="white" borderRadius="lg" boxShadow="sm" overflow="hidden">
          <Table variant="simple">
            <Thead bg="gray.50">
              <Tr>
                <Th>Name</Th>
                <Th>Email</Th>
                <Th isNumeric>Orders</Th>
                <Th>Member Since</Th>
              </Tr>
            </Thead>
            <Tbody>
              {filteredCustomers.length > 0 ? (
                filteredCustomers.map((customer) => (
                  <Tr key={customer.id} _hover={{ bg: 'gray.50' }}>
                    <Td>
                      <Link as={RouterLink} to={`/customers/${customer.id}`} color="blue.500">
                        {customer.first_name} {customer.last_name}
                      </Link>
                    </Td>
                    <Td>{customer.email}</Td>
                    <Td isNumeric>
                      <Badge colorScheme={customer.orders_count > 0 ? 'green' : 'gray'}>
                        {customer.orders_count} orders
                      </Badge>
                    </Td>
                    <Td>{new Date(customer.created_at).toLocaleDateString()}</Td>
                  </Tr>
                ))
              ) : (
                <Tr>
                  <Td colSpan={4} textAlign="center" py={8}>
                    No customers found
                  </Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </Box>
      </Box>
    </Box>
  );
}
