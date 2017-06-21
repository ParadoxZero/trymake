# Trymake

The trymake is divided into multiple packages.

## TrymakeAPI

Contains the settings and configurations for the Django project.

## Customer

API calls related to customers

- Create
- Verify
- Update
- Login
- Set Address
- Get Address

## Vendor

- Create
- Verify
- Update
- Login

## Admin

- Login
- get sales report
- get popular search queries
- get analytics
- create new admin
- get permission list

## Product

- Create
- Update
- Remove
- Stock
- Create category
- Update category
- Rate product
- Remove category
- Get product
- Get popular
- Get featured
- Get features category
- Get popular category
- Search product
- Search category
- Search
- Filter category

## Order

- Sync Cart

    Updates the cart to backend store of cart.
    
- Get Payment methods
- Get order review
- Place order
- Get Order status
- Cancel Order
- Change Order status
- Set order note

## Complaints

- Create complaint: 

    Complaints will be assigned to the admin who registers the complaint. 
In case the complaint is created by customer. Super Admin will need to assign it to someone.

- Get complaint
- Get complaint Count
- Get Unresolved Complaint List
- Get Unresolved Complaint Count
- Change complaint status
- Send Customer message
- Get Customer Message
- Assign admin to Customer