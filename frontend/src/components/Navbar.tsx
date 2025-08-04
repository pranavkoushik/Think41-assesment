import { Box, Flex, Heading, Link } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

export default function Navbar() {
  return (
    <Box bg="white" boxShadow="sm" px={4} py={3} mb={8}>
      <Flex maxW="container.xl" mx="auto" align="center">
        <Link as={RouterLink} to="/" _hover={{ textDecoration: 'none' }}>
          <Heading size="lg" color="blue.600">
            Customer Dashboard
          </Heading>
        </Link>
        <Box flex={1} />
        <Box>
          <Link as={RouterLink} to="/" px={3} py={2} fontWeight="medium">
            Customers
          </Link>
        </Box>
      </Flex>
    </Box>
  );
}
