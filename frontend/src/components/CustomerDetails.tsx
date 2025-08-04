import { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Heading,
  Text,
  Badge,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  VStack,
  HStack,
  Divider,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Link,
} from '@chakra-ui/react';
import { ArrowBackIcon, EmailIcon, PhoneIcon } from '@chakra-ui/icons';
import axios from 'axios';

interface Order {
  id: number;
  status: string;
  created_at: string;
  items_count: number;
  items: Array<{
    id: number;
    quantity: number;
    price: number;
    product: {
      name: string;
    };
  }>;
}

interface Customer {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  created_at: string;
  orders: Order[];
  orders_count: number;
}

const API_URL = '/api'; // Using proxy from Vite config

export default function CustomerDetails() {
  const { id } = useParams<{ id: string }>();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCustomer = async () => {
      try {
        const response = await axios.get(`${API_URL}/customers/${id}`);
        setCustomer(response.data.data);
        setError('');
      } catch (err) {
        setError('Failed to fetch customer details');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchCustomer();
    }
  }, [id]);

  if (loading) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert status="error" borderRadius="md" mb={6}>
        <AlertIcon />
        <Box>
          <AlertTitle>Error loading customer</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Box>
      </Alert>
    );
  }

  if (!customer) {
    return (
      <Box textAlign="center" py={10}>
        <Text>Customer not found</Text>
      </Box>
    );
  }

  return (
    <VStack align="stretch" spacing={6}>
      <Box>
        <Link
          as={RouterLink}
          to="/"
          display="inline-flex"
          alignItems="center"
          color="blue.500"
          mb={4}
          _hover={{ textDecoration: 'none' }}
        >
          <ArrowBackIcon mr={2} /> Back to Customers
        </Link>

        <Box bg="white" p={6} borderRadius="lg" boxShadow="sm">
          <HStack justify="space-between" mb={6}>
            <VStack align="start" spacing={1}>
              <Heading size="lg">
                {customer.first_name} {customer.last_name}
              </Heading>
              <HStack spacing={4}>
                <Text color="gray.600">
                  <EmailIcon mr={2} />
                  {customer.email}
                </Text>
                {customer.phone_number && (
                  <Text color="gray.600">
                    <PhoneIcon mr={2} />
                    {customer.phone_number}
                  </Text>
                )}
              </HStack>
            </VStack>
            <Badge colorScheme="blue" fontSize="md" px={3} py={1}>
              {customer.orders_count} {customer.orders_count === 1 ? 'Order' : 'Orders'}
            </Badge>
          </HStack>

          <Divider my={4} />

          <Box>
            <Heading size="md" mb={4}>
              Recent Orders
            </Heading>
            {customer.orders && customer.orders.length > 0 ? (
              <Box overflowX="auto">
                <Table variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Order ID</Th>
                      <Th>Status</Th>
                      <Th>Date</Th>
                      <Th isNumeric>Items</Th>
                      <Th isNumeric>Total</Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {customer.orders.map((order) => (
                      <Tr key={order.id} _hover={{ bg: 'gray.50' }}>
                        <Td>
                          <Link
                            as={RouterLink}
                            to={`/orders/${order.id}`}
                            color="blue.500"
                            _hover={{ textDecoration: 'none' }}
                          >
                            #{order.id}
                          </Link>
                        </Td>
                        <Td>
                          <Badge
                            colorScheme={
                              order.status === 'completed'
                                ? 'green'
                                : order.status === 'cancelled'
                                ? 'red'
                                : 'blue'
                            }
                          >
                            {order.status}
                          </Badge>
                        </Td>
                        <Td>{new Date(order.created_at).toLocaleDateString()}</Td>
                        <Td isNumeric>{order.items_count || 0} items</Td>
                        <Td isNumeric>
                          ${order.items?.reduce((sum, item) => sum + (item.price * item.quantity), 0).toFixed(2) || '0.00'}
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
            ) : (
              <Box
                border="1px dashed"
                borderColor="gray.200"
                borderRadius="md"
                p={6}
                textAlign="center"
                bg="gray.50"
              >
                <Text color="gray.500">No orders found for this customer</Text>
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </VStack>
  );
}
