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

















Session
report_data = [
    {'student_id': 1, 'q1_grade': 90, 'q2_grade': 85, 'q3_grade': 78, 'q4_grade': 92, 'year_average': 86.25},
    {'student_id': 2, 'q1_grade': 75, 'q2_grade': 80, 'q3_grade': 82, 'q4_grade': 88, 'year_average': 81.25},
    # ... and so on
]
request.session['report_data'] = report_data


models

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

views

# views.py
def process_shelf(request, shelf_number):
    shelf_data_key = f'shelf{shelf_number}_data'
    shelf_data = request.session.get(shelf_data_key, [])
    
    if request.method == 'POST':
        shelf_formset = InventoryItemForm(request.POST, queryset=shelf_data)
        if shelf_formset.is_valid():
            # Process and save the formset data for the specific shelf
            # ...
            del request.session[shelf_data_key]  # Clear session data after processing
            return redirect('success_url')  # Redirect to a success page
    else:
        shelf_formset = InventoryItemForm(queryset=shelf_data)
    
    return render(request, 'shelf_template.html', {'shelf_formset': shelf_formset})







from django.shortcuts import render, redirect
from .models import Order, LineItem

def place_order(request):
    # Step 1: Retrieve cart items from session
    cart_items = request.session.get('cart_items', [])

    # Step 2: Calculate order total
    order_total = sum(item['linePriceTotal'] for item in cart_items)

    # Step 3: Create an Order instance
    order = Order.objects.create(
        customer=request.user,
        orderNumber="generate_order_number_logic_here",  # Implement your logic
        orderTotal=order_total,
        # ... other order fields
    )

    # Step 4: Associate Line Items with the Order
    for cart_item in cart_items:
        line_item = LineItem.objects.create(
            product=cart_item['product'],  # You need to adjust this based on your cart structure
            customer=request.user,
            quantity=cart_item['quantity'],
            linePriceTotal=cart_item['linePriceTotal'],
            # ... other line item fields
        )
        order.items.add(line_item)  # Associate line item with the order

    # Step 5: Save the Order and Line Items
    order.save()

    # Clear cart items from session after the order is placed
    request.session['cart_items'] = []

    return redirect('order_placed')  # Redirect to a success page or do something else
