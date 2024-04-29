---

# Vendor Management System API

This is a RESTful API in Django Rest Framework for a vendor management system. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
  - [1. Vendor Profile Management](#1-vendor-profile-management)
  - [2. Purchase Order Tracking](#2-purchase-order-tracking)
  - [3. Vendor Performance](#3-vendor-performance)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create, read, update, and delete vendor profiles.
- Create, read, update, and delete purchase orders.
- Retrieve vendor performance metrics.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/vendor-management-system.git
   ```

2. **Install dependencies:**

   ```bash
   cd vendor-management-system
   pip install -r requirements.txt
   ```

3. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

6. **Access the API:**

   Open your browser and go to `http://localhost:8000/api/` to view the browsable API.

## API Endpoints

### 1. Vendor Profile Management

- **POST /api/vendors/**

  Create a new vendor.

- **GET /api/vendors/**

  List all vendors.

- **GET /api/vendors/{vendor_id}/**

  Retrieve details of a specific vendor.

- **PUT /api/vendors/{vendor_id}/**

  Update a vendor's details.

- **DELETE /api/vendors/{vendor_id}/**

  Delete a vendor.

### 2. Purchase Order Tracking

- **POST /api/purchase_orders/**

  Create a new purchase order.

- **GET /api/purchase_orders/**

  List all purchase orders. You can filter by vendor using query parameters.

- **GET /api/purchase_orders/{po_id}/**

  Retrieve details of a specific purchase order.

- **PUT /api/purchase_orders/{po_id}/**

  Update a purchase order.

- **DELETE /api/purchase_orders/{po_id}/**

  Delete a purchase order.

- **POST /api/purchase_orders/{po_id}/acknowledge**

  Acknowledge a purchase order.

### 3. Vendor Performance

- **GET /api/vendors/{vendor_id}/performance/**

  Retrieve calculated performance metrics for a specific vendor.


## Usage

To use the API endpoints, you can use tools like [Postman](https://www.postman.com/) or send HTTP requests using any programming language.

Here's an example using Postman:
![Screenshot 2024-04-29 134210](https://github.com/Mohd-Daniyal/Vendor-Management-System/assets/96229438/31c7929a-c9e7-498d-ac2d-fcdf5e82b157)

## Testing

To run tests, use the following command:

```bash
python manage.py test
```
