import datetime
import json
import os
import random
import uuid

from faker import Faker  # https://faker.readthedocs.io/en/master/index.html
from faker.providers import internet

class RetailDataGenerator:
    """
    This class is used to create fake/synthetic retail data
    and is partly based on the code in the 'faker-commerce' PyPi library.
    See https://github.com/nicobritos/python-faker-commerce
    See https://pypi.org/project/faker-commerce/
    """

    def __init__(self, opts={}):
        self.fake = Faker()
        self.fake.add_provider(internet)
        self.store_dict = dict()
        self.cust_dict = dict()
        self.product_dict = dict()
        self.sample_store = None
        self.sample_customer = None 
        self.sample_product = None
        self.sample_sale = None
        self.sample_line_item = None

    def generate_stores(self, count) -> list[str]:
        lines = list()
        for idx in range(count):
            store_id = self.random_store_id()
            obj = dict()
            obj['store_id'] = store_id
            obj['city']     = self.fake.city()
            obj['address']  = self.fake.street_address().replace(',',' ')
            obj['state']    = self.fake.state_abbr()
            lines.append(json.dumps(obj))
            self.store_dict[store_id] = obj
            self.sample_store = obj
        return lines

    def generate_products(self, count) -> list[str]:
        lines = list()
        for idx in range(count):
            first = self.fake.first_name().replace(',',' ')
            last  = self.fake.last_name().replace(',',' ')
            obj = dict()
            product_id = self.random_product_id()
            obj['product_id'] = product_id
            obj['catalog'] = random.choice(self.product_catalog_categories())
            obj['name'] = self.random_product_name()
            obj['price'] = self.random_price()
            lines.append(json.dumps(obj))
            self.product_dict[product_id] = obj
            self.sample_product = obj
        return lines

    def generate_customers(self, count) -> list[str]:
        lines = list()
        for idx in range(count):
            first = self.fake.first_name().replace(',',' ')
            last  = self.fake.last_name().replace(',',' ')
            obj = dict()
            customer_id = self.random_cust_id()
            obj['customer_id'] = customer_id
            obj['first_name'] = first
            obj['last_name'] = last
            obj['full_name'] = '{} {}'.format(first, last)
            obj['address'] = self.fake.street_address().replace(',',' ')
            obj['city'] = self.fake.city()
            obj['state'] = self.fake.state_abbr()
            lines.append(json.dumps(obj))
            self.cust_dict[customer_id] = obj
            self.sample_customer = obj
        return lines

    def generate_sales(self, year, mm):
        lines = list()
        ldm = self.last_day_of_month(mm)
        start_date = "{}-{}-{}".format(year, mm, "01")
        end_date = "{}-{}-{}".format(year, mm, ldm)
        days = self.calendar_days(start_date, end_date)
        for day in days:
            day_sales_count = random.randint(100,120)
            for sale_idx in range(day_sales_count):
                sale_id = str(uuid.uuid4())
                customer_id = random.choice(sorted(self.cust_dict.keys()))
                store_id = random.choice(sorted(self.store_dict.keys()))
                total_sale = 0.0
                line_item_count = random.randint(1,3)
                line_items = self.random_line_items(
                    sale_id, customer_id, store_id, day, line_item_count)
                for line_item in line_items:
                    total_sale = total_sale + line_item["total"]

                sale_obj = dict()
                sale_obj['doctype'] = 'sale'
                sale_obj['sale_id'] = sale_id
                sale_obj['date'] = day['date']
                sale_obj['dow']  = day['dow'].lower()
                sale_obj['customer_id'] = customer_id
                sale_obj['store_id'] = store_id
                sale_obj['item_count'] = len(line_items)
                sale_obj['total_sale'] = total_sale
                lines.append(json.dumps(sale_obj))
                self.sample_sale = sale_obj

                for line_item in line_items:
                    lines.append(json.dumps(line_item))
                    self.sample_line_item = line_item

        print("generate_sales {} {} -> {} lines".format(year, mm, len(lines)))
        return lines

    def random_line_items(self, sale_id, customer_id, store_id, day, count):
        items = list()
        for idx in range(count):
            product_id = random.choice(sorted(self.product_dict.keys()))
            product = self.product_dict[product_id]
            item = dict()
            qty = random.randint(1,3)
            item['doctype'] = 'line_item'
            item["seq"] = idx + 1
            item["sale_id"] = sale_id
            item["customer_id"] = customer_id
            item["store_id"] = store_id
            item['date'] = day['date']
            item['dow']  = day['dow'].lower()
            item["product_id"] = product_id
            item["product_name"] = product["name"]
            item["qty"] = qty
            item["price"] = product["price"]
            item["total"] = product["price"] * qty
            items.append(item)
        return items

    def random_store_id(self):
        continue_to_process = True
        while continue_to_process:
            id = self.fake.pyint(min_value=1, max_value=10000)
            if id in self.store_dict.keys():
                pass  # try again
            else:
                self.store_dict[id] = {}
                continue_to_process = False
                return id

    def random_cust_id(self):
        continue_to_process = True
        while continue_to_process:
            id = self.fake.pyint(min_value=1, max_value=999999)
            if id in self.cust_dict.keys():
                pass  # try again
            else:
                self.cust_dict[id] = {}
                continue_to_process = False
                return id
                     
    def random_product_id(self):
        continue_to_process = True
        while continue_to_process:
            id = self.fake.pyint(min_value=1, max_value=999999)
            if id in self.cust_dict.keys():
                pass  # try again
            else:
                self.product_dict[id] = {}
                continue_to_process = False
                return id

    def random_price(self):
        dec = self.fake.pydecimal(min_value=0.99, max_value=1500.00, right_digits=2)
        return float(str(dec))

    def random_product_name(self):
        name = random.choice(self.product_names())
        matl = random.choice(self.product_materials())
        adj  = random.choice(self.product_adjectives())
        size = random.choice(self.product_sizes())
        return "{}, {}, {}, {}".format(name, matl, adj, size)

    def calendar_days(self, start_date, end_date):
        days = list()
        date1 = self.parse_yyyymmdd(start_date)
        date2 = self.parse_yyyymmdd(end_date)
        dates = self.inclusive_dates_between(date1, date2, 1000)
        for idx, d in enumerate(dates):
            day = dict()
            day['seq']    = idx
            day['date']   = str(d)
            day['daynum'] = d.isoweekday()
            day['dow']    = d.strftime('%a')
            days.append(day)
        return days

    def parse_yyyymmdd(self, date_str):
        # parse the given 'yyyy-mm-dd' string to a datetime.date
        tokens = date_str.split('-')
        for idx, token in enumerate(tokens):
            tokens[idx] = int(token)
        return datetime.date(tokens[0], tokens[1], tokens[2])

    def inclusive_dates_between(self, start_date, end_date, max_count):
        # return a list of datetime.date objects
        dates = list()
        curr_date = start_date
        end_date_str = str(end_date)
        one_day = datetime.timedelta(days=1)
        continue_to_process = True

        for idx, token in enumerate(range(int(max_count))):
            if continue_to_process:
                dates.append(curr_date)
                if str(curr_date) == end_date_str:
                    continue_to_process = False
                else:
                    curr_date = curr_date + one_day
        return dates

    def last_day_of_month(self, mm):
        # Thirty days hath September, April, June, and November,
        # all the rest have thirty-one. Except February
        if mm == "02":
            return 28
        if mm in ["04", "06", "09", "11"]:
            return 30
        return 31

    def markdown_doc(self):
        lines = list()
        lines.append("# Generated Retail Data")
        lines.append("")
        lines.append("## Sample Store")
        lines.append("")
        lines.append("partition key attribute: store_id")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(self.sample_store, sort_keys=False, indent=2))
        lines.append("```")

        lines.append("")
        lines.append("## Sample Product")
        lines.append("")
        lines.append("partition key attribute: product_id")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(self.sample_product, sort_keys=False, indent=2))
        lines.append("```")

        lines.append("")
        lines.append("## Sample Customer")
        lines.append("")
        lines.append("partition key attribute: customer_id")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(self.sample_customer, sort_keys=False, indent=2))
        lines.append("```")

        lines.append("")
        lines.append("## Sample Sale")
        lines.append("")
        lines.append("partition key attribute: sale_id")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(self.sample_sale, sort_keys=False, indent=2))
        lines.append("```")

        lines.append("")
        lines.append("## Sample Line Item")
        lines.append("")
        lines.append("partition key attribute: sale_id")
        lines.append("")
        lines.append("```")
        lines.append(json.dumps(self.sample_line_item, sort_keys=False, indent=2))
        lines.append("```")

        return "\n".join(lines)

    def product_catalog_categories(self) -> list:
        return [
            "Books",
            "Movies",
            "Music",
            "Games",
            "Electronics",
            "Computers",
            "Home",
            "Garden",
            "Tools",
            "Grocery",
            "Health",
            "Beauty",
            "Toys",
            "Kids",
            "Baby",
            "Clothing",
            "Shoes",
            "Jewelery",
            "Sports",
            "Outdoors",
            "Automotive",
            "Industrial",
        ]

    def product_names(self) -> list:
        return [
            "Chair",
            "Car",
            "Computer",
            "Keyboard",
            "Mouse",
            "Bike",
            "Ball",
            "Gloves",
            "Pants",
            "Shirt",
            "Table",
            "Shoes",
            "Hat",
            "Towels",
            "Soap",
            "Tuna",
            "Chicken",
            "Fish",
            "Cheese",
            "Bacon",
            "Pizza",
            "Salad",
            "Sausages",
            "Chips",
        ]

    def product_materials(self) -> list:
        return [
            "Steel",
            "Wooden",
            "Carbon Fiber",
            "Concrete",
            "Plastic",
            "Cotton",
            "Granite",
            "Rubber",
            "Metal",
            "Soft",
            "Fresh",
            "Frozen",
        ]

    def product_adjectives(self) -> list:
        return [
            "Digital",
            "Ergonomic",
            "Rustic",
            "Intelligent",
            "Gorgeous",
            "Incredible",
            "Fantastic",
            "Practical",
            "Sleek",
            "Awesome",
            "Generic",
            "Handcrafted",
            "Handmade",
            "Licensed",
            "Refined",
            "Unbranded",
            "Tasty",
            "New",
            "Gently Used",
            "Used",
            "For repair",
        ]

    def product_sizes(self) -> list:
        return [
            "Small",
            "Medium",
            "Large",
            "Extra Large"
        ]
