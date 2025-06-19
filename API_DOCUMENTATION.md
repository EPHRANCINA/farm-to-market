# Farm to Market API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses session authentication. Users must be logged in to perform create, update, and delete operations.

## API Endpoints

### Products API

#### List All Products
```
GET http://localhost:8000/api/products/
```
Response:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Fresh Tomatoes",
            "description": "Organic tomatoes from local farm",
            "price": "2.99",
            "quantity": 100,
            "category": "vegetables",
            "category_name": "Vegetables",
            "image": "http://localhost:8000/media/products/tomatoes.jpg",
            "seller": 1,
            "seller_name": "John Doe",
            "harvest_date": "2024-05-27",
            "farm_location": "Kigali, Rwanda",
            "growing_method": "organic",
            "created_at": "2024-05-27T10:00:00Z",
            "updated_at": "2024-05-27T10:00:00Z"
        }
    ]
}
```

#### Get Product Details
```
GET http://localhost:8000/api/products/{id}/
```
Response:
```json
{
    "id": 1,
    "name": "Fresh Tomatoes",
    "description": "Organic tomatoes from local farm",
    "price": "2.99",
    "quantity": 100,
    "category": "vegetables",
    "category_name": "Vegetables",
    "image": "http://localhost:8000/media/products/tomatoes.jpg",
    "seller": 1,
    "seller_name": "John Doe",
    "harvest_date": "2024-05-27",
    "farm_location": "Kigali, Rwanda",
    "growing_method": "organic",
    "created_at": "2024-05-27T10:00:00Z",
    "updated_at": "2024-05-27T10:00:00Z"
}
```

#### Create Product
```
POST http://localhost:8000/api/products/
```
Request Body:
```json
{
    "name": "Fresh Tomatoes",
    "description": "Organic tomatoes from local farm",
    "price": "2.99",
    "quantity": 100,
    "category": "vegetables",
    "harvest_date": "2024-05-27",
    "farm_location": "Kigali, Rwanda",
    "growing_method": "organic"
}
```

#### Update Product
```
PUT http://localhost:8000/api/products/{id}/
```
Request Body:
```json
{
    "name": "Fresh Tomatoes",
    "description": "Updated description",
    "price": "3.99",
    "quantity": 50,
    "category": "vegetables",
    "harvest_date": "2024-05-27",
    "farm_location": "Kigali, Rwanda",
    "growing_method": "organic"
}
```

#### Delete Product
```
DELETE http://localhost:8000/api/products/{id}/
```

#### Get Seller Details
```
GET http://localhost:8000/api/products/{id}/seller_details/
```
Response:
```json
{
    "seller_name": "John Doe",
    "seller_email": "john@example.com",
    "seller_phone": "0712345678",
    "seller_address": "Kigali, Rwanda"
}
```

### Categories API

#### List All Categories
```
GET http://localhost:8000/api/categories/
```
Response:
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Vegetables",
            "description": "Fresh vegetables from local farms",
            "created_at": "2024-05-27T10:00:00Z"
        }
    ]
}
```

#### Get Category Details
```
GET http://localhost:8000/api/categories/{id}/
```
Response:
```json
{
    "id": 1,
    "name": "Vegetables",
    "description": "Fresh vegetables from local farms",
    "created_at": "2024-05-27T10:00:00Z"
}
```

#### Create Category
```
POST http://localhost:8000/api/categories/
```
Request Body:
```json
{
    "name": "Vegetables",
    "description": "Fresh vegetables from local farms"
}
```

#### Update Category
```
PUT http://localhost:8000/api/categories/{id}/
```
Request Body:
```json
{
    "name": "Vegetables",
    "description": "Updated description"
}
```

#### Delete Category
```
DELETE http://localhost:8000/api/categories/{id}/
```

### Users API

#### Register User
```
POST http://localhost:8000/api/users/
```
Request Body:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "0712345678",
    "address": "Kigali, Rwanda"
}
```

#### Get User Profile
```
GET http://localhost:8000/api/users/profile/
```
Response:
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "0712345678",
    "address": "Kigali, Rwanda",
    "date_joined": "2024-05-27T10:00:00Z"
}
```

#### Change Password
```
POST http://localhost:8000/api/users/change_password/
```
Request Body:
```json
{
    "old_password": "currentpassword",
    "new_password": "newsecurepassword123"
}
```

### Orders API

#### List Orders
```
GET http://localhost:8000/api/orders/
```
Response:
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "items": [
                {
                    "id": 1,
                    "product": {
                        "id": 1,
                        "name": "Fresh Tomatoes",
                        "price": "2.99"
                    },
                    "quantity": 2,
                    "subtotal": "5.98"
                }
            ],
            "total_amount": "5.98",
            "status": "pending",
            "shipping_address": "Kigali, Rwanda",
            "payment_method": "mobile_money",
            "payment_status": "pending",
            "created_at": "2024-05-27T10:00:00Z",
            "updated_at": "2024-05-27T10:00:00Z"
        }
    ]
}
```

#### Create Order
```
POST http://localhost:8000/api/orders/
```
Request Body:
```json
{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ],
    "shipping_address": "Kigali, Rwanda",
    "payment_method": "mobile_money"
}
```

#### Get Order Details
```
GET http://localhost:8000/api/orders/{id}/
```
Response:
```json
{
    "id": 1,
    "user": 1,
    "items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Fresh Tomatoes",
                "price": "2.99"
            },
            "quantity": 2,
            "subtotal": "5.98"
        }
    ],
    "total_amount": "5.98",
    "status": "pending",
    "shipping_address": "Kigali, Rwanda",
    "payment_method": "mobile_money",
    "payment_status": "pending",
    "created_at": "2024-05-27T10:00:00Z",
    "updated_at": "2024-05-27T10:00:00Z"
}
```

#### Cancel Order
```
POST http://localhost:8000/api/orders/{id}/cancel/
```
Response:
```json
{
    "status": "order cancelled"
}
```

### Reviews API

#### List Product Reviews
```
GET http://localhost:8000/api/products/{product_id}/reviews/
```
Response:
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "product": 1,
            "customer": 1,
            "customer_name": "John Doe",
            "rating": 5,
            "comment": "Excellent quality!",
            "created_at": "2024-05-27T10:00:00Z"
        }
    ]
}
```

#### Create Review
```
POST http://localhost:8000/api/products/{product_id}/reviews/
```
Request Body:
```json
{
    "rating": 5,
    "comment": "Excellent quality!"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": [
        "Error message"
    ]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Notes
- All timestamps are in UTC
- Images are served from the /media/ directory
- Pagination is set to 10 items per page
- All prices are in decimal format with 2 decimal places
- Category choices: vegetables, fruits, dairy, meat, grains, other
- Growing method choices: organic, conventional, hydroponic, greenhouse
- Phone numbers must start with '06' or '07' and be 10 digits long
- All dates should be in YYYY-MM-DD format
- Authentication is required for all POST, PUT, and DELETE requests
- Only product owners can update or delete their products
- Only order owners can view their orders
- Only authenticated users can create reviews
- Users can only review a product once 