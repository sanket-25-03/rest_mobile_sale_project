### **Member 1: Backend Developer (Sanket)**

1. **Project and App Setup**:
   - Initialize the Django project and create the `products` app.
   - Configure Django REST Framework in the project settings.
   - Set up the database and migrate it.

2. **Model and Serializer Design**:
   - Create the `Product` model with fields for name, brand, price, description, and creation date.
   - Create the `Order` model with fields for product, quantity, customer name, and order date.
   - Build serializers for the `Product` and `Order` models to handle data input/output.

3. **API Endpoints**:
   - Create a **GET API for product listing**, including pagination.
   - Add filtering and sorting to the product listing API (e.g., filter by brand and price, sort by price).
   - Develop a **POST API for adding new products** to the database.
   - Create a **POST API for placing orders**.

4. **Data Seeding**:
   - Add dummy data to the database for products to test API functionality.

5. **Integration Support**:
   - Ensure APIs are well-documented for frontend integration.
   - Assist the frontend developer in debugging API calls.

6. **Deployment**:
   - Prepare the backend for deployment by updating production settings (e.g., disable debugging, configure allowed hosts).
   - Deploy the backend to a platform like Render or PythonAnywhere.
   - Share API URLs with the team.

### **Member 2: Frontend Developer**

1. **Frontend Setup**:
   - Initialize the frontend project using React (or static HTML/JavaScript if preferred).
   - Set up routing for the application with pages for:
     - Product List
     - Add Product
     - Buy Product.

2. **Page Development**:
   - **Product List Page**:
     - Fetch product data from the backend.
     - Display products in a user-friendly layout (grid or list).
     - Add filtering options for brand and price.
     - Add sorting functionality (e.g., price: low to high).
   - **Add Product Page**:
     - Create a form with fields for name, brand, price, and description.
     - Connect the form to the backend API for adding products.
   - **Buy Page**:
     - Create a page to display product details.
     - Add a form to place an order with fields for quantity and customer details.
     - Connect the form to the backend API for placing orders.

3. **API Integration**:
   - Test API calls for fetching, adding, and ordering products.
   - Handle errors gracefully and display appropriate messages to the user.

4. **Frontend Deployment**:
   - Prepare the frontend for deployment by building the project (if React).
   - Deploy the frontend to a platform like Netlify or Vercel.
   - Ensure the deployed frontend communicates with the backend.