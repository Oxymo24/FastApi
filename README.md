API Endpoints

 1. Create Product

- **Endpoint:** `/products`  
- **Method:** `POST`  
- **Description:** Adds a new product to the database.

2. List Products
Endpoint: /products

Method: GET

Description: Retrieves a list of products with optional filtering and pagination.

Query Parameters:

Parameter	Type	Description
name	string	Partial or regex-based product name search
size	string	Filter by size (e.g. size=large)
limit	int	Number of products to return (default: 10)
offset	int	Number of products to skip (default: 0)

3. Create Order
Endpoint: /orders

Method: POST

Description: Creates a new order for a user.

4. Get List of Orders (By User)
Endpoint: /orders/{user_id}

Method: GET

Description: Retrieves all orders for the given user.

Query Parameters:

Parameter	Type	Description
limit	int	Number of orders to return (default: 10)
offset	int	Number of orders to skip for pagination
