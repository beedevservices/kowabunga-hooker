# HTML for collecting items/grades and adding to session & cartish:
---
```html
<!-- grade_entry.html -->
<form method="post">
    {% csrf_token %}
    <table>
        <thead>
            <tr>
                <th>Student ID</th>
                <th>Test Grade</th>
                <th>Homework Grade</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for student in students %}
                <tr>
                    <td>{{ student.student_id }}</td>
                    <td><input type="number" name="test_grade_{{ student.student_id }}"></td>
                    <td><input type="number" name="homework_grade_{{ student.student_id }}"></td>
                    <td><button type="submit" name="add_grade" value="{{ student.student_id }}">Add</button></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</form>
```

# Print of session/cart:
```python
request.session['cart'] = {
    '1': {'quantity': 3, 'price': 10, 'total': 30},
    '2': {'quantity': 2, 'price': 15, 'total': 30},
    # ... and so on
}

```

# To add these items to the cart/session
```python
# views.py
from django.shortcuts import render, redirect

def add_grades(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('test_grade_'):
                student_id = key.replace('test_grade_', '')
                test_grade = value
                # Save test_grade to session
                if 'grades' not in request.session:
                    request.session['grades'] = {}
                if student_id not in request.session['grades']:
                    request.session['grades'][student_id] = {}
                request.session['grades'][student_id]['test_grade'] = test_grade
            elif key.startswith('homework_grade_'):
                student_id = key.replace('homework_grade_', '')
                homework_grade = value
                # Save homework_grade to session
                if 'grades' not in request.session:
                    request.session['grades'] = {}
                if student_id not in request.session['grades']:
                    request.session['grades'][student_id] = {}
                request.session['grades'][student_id]['homework_grade'] = homework_grade
        
        return redirect('success_url')  # Redirect after processing

    # Retrieve the list of students (from session or database)
    students = [...]  # Replace with your actual student data
    context = {'students': students}
    return render(request, 'grade_entry.html', context)

```

# Example of models:
---
Here shelf would be order number
```python
from django.db import models

class Shelf(models.Model):
    shelf_number = models.CharField(max_length=10, unique=True)
    # Add any other fields relevant to the shelf
    
    def __str__(self):
        return f"Shelf {self.shelf_number}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    # Add any other fields relevant to the item
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.item} - {self.shelf} ({self.quantity})"

```


```python
def addToCart(request):
    product_id = request.POST.get('prod_id')
    action = request.POST.get('action')  # 'add', 'remove', etc.
    cart = request.session.get('cart', {})

    if action == 'add':
        cart_item = cart.get(str(product_id), {})
        quantity = cart_item.get('quantity', 0)
        cart_item['quantity'] = quantity + 1
        cart[str(product_id)] = cart_item

    request.session['cart'] = cart
    return redirect('/')
```

```python
from django.shortcuts import render, redirect
from .models import Order, OrderItem, Product
from django.db import transaction
from django.contrib import messages

def place_order(request):
    # Step 1: Create an Order instance
    errors, order_num = Order.objects.validate()  # Validate and generate order number
    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('cart_page')  # Redirect back to cart page if there are errors
    
    # Create the Order instance
    customer = request.user  # Assuming the authenticated user is the customer
    order = Order(orderNum=order_num, customer=customer)
    
    # Step 2: Iterate through session data and create OrderItem instances
    total_order_price = 0
    item_count = 0
    for product_id, product_data in request.session.items():
        if product_id.isnumeric():
            product = Product.objects.get(pk=product_id)
            quantity = product_data.get('quantity', 0)
            price = product_data.get('price', 0)
            total = int(quantity) * int(price)
            total_order_price += total
            item_count += quantity
            order_item = OrderItem(
                orderNum=order, product=product, quantity=quantity, total=str(total)
            )
            order_item.save()
    
    # Update the Order instance with item count and total price
    order.itemCount = item_count
    order.orderTotal = str(total_order_price)
    order.save()

    # Step 3: Save the order and order items
    order.save()

    # Clear the session cart after successfully placing the order
    request.session.clear()

    # Redirect to a success page or wherever you want
    messages.success(request, 'Order placed successfully!')
    return redirect('success_page')

```
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generate_cart_pdf(cart_data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cart.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    # Convert your cart_data into a list of rows for the table
    cart_rows = [
        ['Item #', 'Name', 'Price', 'Quantity', 'Total'],
        # ... Convert cart_data into rows ...
    ]

    # Create a table and style
    table = Table(cart_rows)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Build the PDF document
    story = [table]
    doc.build(story)

    return response

```
```python
cart_rows = [
    ['Item #', 'Name', 'Price', 'Quantity', 'Total']
]

for item_id, item_data in cart_data.items():
    # Fetch the corresponding product name, assuming you have a products lookup
    product_name = products_lookup.get(item_id, 'Unknown Product')

    # Extract item details
    quantity = item_data['quantity']
    price = item_data['price']
    total = item_data['total']

    # Append row to cart_rows
    cart_rows.append([item_id, product_name, price, quantity, total])
```
```python
    order_details_table = Table(orderDetails)
    order_details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Draw the table on the PDF canvas
    w, h = order_details_table.wrapOn(p, 0, 0)
    order_details_table.drawOn(p, 60, 550 - h)
```
```python
from webcolors import rgb_to_name
named_color = rgb_to_name((255,0,0), spec='css3')
print(named_color)
```

```python
from scipy.spatial import KDTree
from webcolors import (
    css3_hex_to_names,
    hex_to_rgb,
)
def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = css3_hex_to_names
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'
```
```python
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse

def sendOrderEmail(user, order):
    subject = f'Thank you, {user.first_name} for your order'
    message = f'{user.first_name}, thank you for placing an order. This is your confirmation email.\nYour order number is: {order.orderNum}\nYour current order total is: {order.orderTotal}\n\nI will reach out with the next steps.\n\nThe Kowabunga Hooker\nkaila@kowabunga-hooker.com\nhttps://kowabunga-hooker.com'
    email_from = settings.EMAIL_HOST_ORDER_USER
    recipient_list = [user.email, settings.EMAIL_HOST_ORDER_USER]

    # Get the URL for the invoice view with the order_id parameter
    invoice_url = reverse('invoice', args=[order.id])

    # Attach the PDF file or provide a link to the invoice view
    pdf_file_path = order.invoice.pdf.path  # Adjust the attribute according to your model
    pdf_attachment = None
    if pdf_file_path:
        # Attach the PDF file if available
        pdf_attachment = open(pdf_file_path, 'rb')

    # Create an EmailMessage instance
    email = EmailMessage(subject, message, email_from, recipient_list)
    
    # Attach the PDF file or add the link to the body of the email
    if pdf_attachment:
        email.attach('invoice.pdf', pdf_attachment.read(), 'application/pdf')
    else:
        email.body += f'\nYou can also view your invoice here: {settings.BASE_URL}{invoice_url}'
    
    # Send the email
    email.send()

    # Close the attached file if opened
    if pdf_attachment:
        pdf_attachment.close()
```