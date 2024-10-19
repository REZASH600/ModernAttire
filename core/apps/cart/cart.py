class CartSession:
    def __init__(self, request):
        self.session = request.session
        self._cart = self.session.setdefault("cart", {})

    def get_cart_dict(self):
        """Return the cart as a dictionary."""
        return self._cart

    def unique_name(self, size, color, product_id):
        """Generate a unique name for the product in the cart."""
        return f"{product_id}-{size}-{color}"

    def add_product(self, product, size, color, quantity):
        """Add a product to the cart or update the quantity if it already exists."""
        name = self.unique_name(size, color, product.id)
        price = self.get_product_price(product, product.offer)

        # Initialize the cart entry if the product is new
        if name not in self._cart:
            self._cart[name] = {
                "product_name": product.name,
                "unique_name": name,
                "size": size,
                "color": color,
                "product_id": product.id,
                "quantity": 0,
                "price": price,
                "max_quantity": product.quantity,
            }

        # Update the quantity and total price
        self._cart[name]["quantity"] = min(
            self._cart[name]["quantity"] + int(quantity), product.quantity
        )
        self._cart[name]["total_price"] = self.get_total_price_of_product(name)

        self.save()

    def remove_product(self, name):
        """Remove a product from the cart based on its unique name."""
        if name in self._cart:
            del self._cart[name]
            self.save()

    def update_product_quantity(self, name, value):
        """Update the quantity of a product in the cart."""
        if name in self._cart:

            old_quantity = self._cart[name]["quantity"]
            new_quantity = old_quantity + int(value)

            if new_quantity <= 0:
                # Remove the product if the new quantity is 0 or less
                self.remove_product(name)
            else:
                # Ensure the new quantity does not exceed the maximum available
                self._cart[name]["quantity"] = min(
                    new_quantity, self._cart[name]["max_quantity"]
                )

                self._cart[name]["total_price"] = self.get_total_price_of_product(name)
                self.save()

    def get_product_price(self, product, offer=None):
        """Determine the price of the product based on current offers."""
        return (
            float(offer.apply_discount(product))
            if offer and offer.is_active
            else float(product.price)
        )

    def get_total_price_of_product(self, name):
        """Calculate the total price of a specific product in the cart."""
        item = self._cart.get(name)
        return item["price"] * item["quantity"] if item else 0

    def get_total_price_of_cart(self):
        """Calculate the total price of all products in the cart."""
        return sum(item["total_price"] for item in self._cart.values())

    def clear(self):
        """Clear the cart."""
        self._cart.clear()
        self.save()

    def save(self):
        """Save the cart back to the session."""
        self.session.modified = True

    def __iter__(self):
        """Iterate over the items in the cart."""
        for item in self._cart.values():
            yield item
