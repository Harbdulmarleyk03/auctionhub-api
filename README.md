# auctionhub-api
 A Simple Auction Marketplace API

# AuctionHub API

AuctionHub API is a RESTful auction marketplace backend built with Django and Django REST Framework. The platform allows users to create auctions, place bids, and track auction activity while enforcing business rules around bidding and ownership.

## Features

* User authentication with JWT
* Create, update, and delete auctions
* Place bids on active auctions
* Bid validation and auction status management
* Owner and admin-based permissions
* Pagination, filtering, and search support
* API documentation with Swagger/OpenAPI

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication (Simple JWT)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Harbdulmarleyk03/auctionhub-api.git
cd auctionhub-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Linux/macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```


### 3. Apply Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser

```bash
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

---

## Database Design Overview

The system consists of three primary models:

### User

Represents authenticated users of the platform.

### Auction

Represents an item available for bidding.

**Key Fields**

* title
* description
* starting_price
* current_price
* start_time
* end_time
* status
* user

**Relationships**

* One user can own multiple auctions.
* One auction can receive multiple bids.

### Bid

Represents a bid placed on an auction.

**Key Fields**

* bid_price
* user
* auction
* created_at

**Relationships**

* A user can place multiple bids.
* An auction can have multiple bids.

### Design Decisions

* Bid history is preserved in a dedicated `Bid` model.
* Auction prices are updated only when a valid higher bid is accepted.
* Frequently queried fields are indexed for performance.
* Bid placement uses database transactions to prevent race conditions and ensure consistency.

---

## Authentication Approach

Authentication is implemented using JSON Web Tokens (JWT).

### Authentication Flow

1. User registers an account.
2. User logs in and receives an access token and refresh token.
3. The access token is included in API requests.

Example:

```http
Authorization: Bearer <access_token>
```

### Why JWT?

* Stateless authentication
* Scalable for distributed systems
* Well-suited for web and mobile clients

---

## Permission Model

### Public Users

Can:

* View auction listings
* View auction details

### Authenticated Users

Can:

* Create auctions
* Place bids
* Manage their own auctions

### Auction Owners

Can:

* Update their own auctions
* Delete their own auctions

### Administrators

Can:

* Access and manage all resources

### Custom Permissions

A custom permission class ensures that only the auction owner or an administrator can modify or delete an auction.

---

## Architecture Decisions

### Service Layer Pattern

Business logic is separated from views and serializers using a service layer.

Benefits:

* Cleaner views
* Easier testing
* Better maintainability
* Clear separation of concerns

### Atomic Transactions

Bid placement is wrapped in database transactions to ensure:

* No conflicting bids are accepted simultaneously
* Auction data remains consistent
* Race conditions are minimized


## Assumptions Made

* Only authenticated users can create auctions.
* Only authenticated users can place bids.
* A bid must be greater than the current auction price.
* Users cannot bid on their own auctions.
* Expired auctions cannot receive new bids.
* Completed auctions cannot be modified.
* The highest valid bid becomes the auction's current price.
* Auction status is automatically updated when it expires.
* All timestamps are stored in UTC.

---

## API Documentation

Interactive API documentation is available through Swagger/OpenAPI after running the project.


```text
http://127.0.0.1:8000/api/v1/docs/#/Auctions
```

---

## Future Improvements

* Pagination and filtering and caching for performance optimization
* Auction categories and tags
* Bid notifications
* Auction watchlists
* Payment integration
* Well designed Token Blacklist and Refresh rotation to enhance security

---

## Author

**Abdulmalik Adebayo**

Backend Engineer | Django & Django REST Framework Developer

GitHub: [Harbdulmarleyk03](https://github.com/Harbdulmarleyk03?utm_source=chatgpt.com)
