# Generated Retail Data

## Sample Store

partition key attribute: store_id

```
{
  "store_id": 6441,
  "city": "Jamesfurt",
  "address": "823 Miller Mountains",
  "state": "WI"
}
```

## Sample Product

partition key attribute: product_id

```
{
  "product_id": 729934,
  "catalog": "Toys",
  "name": "Shirt, Carbon Fiber, New, Large",
  "price": 717.32
}
```

## Sample Customer

partition key attribute: customer_id

```
{
  "customer_id": 932540,
  "first_name": "John",
  "last_name": "Keith",
  "full_name": "John Keith",
  "address": "3756 Wise Branch Apt. 570",
  "city": "Port Andrewborough",
  "state": "HI"
}
```

## Sample Sale

partition key attribute: sale_id

```
{
  "doctype": "sale",
  "sale_id": "8536bf36-178a-4a39-9a96-7855690fbcb7",
  "date": "2024-12-31",
  "dow": "tue",
  "customer_id": 935680,
  "store_id": 9512,
  "item_count": 3,
  "total_sale": 1607.63
}
```

## Sample Line Item

partition key attribute: sale_id

```
{
  "doctype": "line_item",
  "seq": 3,
  "sale_id": "8536bf36-178a-4a39-9a96-7855690fbcb7",
  "customer_id": 935680,
  "store_id": 9512,
  "date": "2024-12-31",
  "dow": "tue",
  "product_id": 587464,
  "product_name": "Keyboard, Steel, Sleek, Extra Large",
  "qty": 1,
  "price": 989.39,
  "total": 989.39
}
```