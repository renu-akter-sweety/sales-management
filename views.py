from django.shortcuts import render, redirect
from django.utils import timezone
from myapp.models import Salesmodel

# ---------------------------
# Add Sale Page
# ---------------------------
def Add_Salepage(request):
    
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        unit_price = float(request.POST.get("unit_price", 0))
        quantity = int(request.POST.get("quantity", 1))
        discount_percent = float(request.POST.get("discount_percent", 0))
        tax_percent = float(request.POST.get("tax_percent", 0))

        subtotal = unit_price * quantity
        discount_amount = subtotal * (discount_percent / 100)
        after_discount = subtotal - discount_amount
        tax_amount = after_discount * (tax_percent / 100)
        total_price = after_discount + tax_amount

        Salesmodel.objects.create(
            product_name=product_name,
            category=category,
            unit_price=unit_price,
            quantity=quantity,
            discount_percent=discount_percent,
            tax_percent=tax_percent,
            total_price=total_price,
        )
        return redirect('sale_listurl')

    sales2 = Salesmodel.objects.values_list("category", flat=True).distinct()
    sales = Salesmodel.objects.all()
    product_name = total_price = None
    selected_category = ""

    if request.method == "POST":
        selected_category = request.POST.get("filter_category")
        if selected_category:
            sales = Salesmodel.objects.filter(category=selected_category)
        else:
            sales = Salesmodel.objects.all()
           
        


    return render(request, "add_sale.html", {
        "sales2": sales2,
        "sales": sales,
        "selected_category": selected_category,
    })
    


# ---------------------------
# Sale List Page
# ---------------------------
def Sale_listpage(request):
    sales2 = Salesmodel.objects.values_list('category', flat=True).distinct()
    sales = Salesmodel.objects.all()
    selected_category = ""

    # Filter Form
    if request.method == "POST" and "filter_submit" in request.POST:
        selected_category = request.POST.get("filter_category")
        if selected_category:
            sales = Salesmodel.objects.filter(category=selected_category)
        else:
            sales = Salesmodel.objects.all()

    context = {
        "sales": sales,
        "sales2": sales2,
        "selected_sales": selected_category,  # pass to template
    }

    return render(request, "sale_list.html", context)


# -------------------------------
# Grade Page
# -------------------------------
def Gradepage(request):
    grade = None
    marks = None
    message = ""
    
    if request.method == "POST":
        marks_input = request.POST.get("marks", "")
        
        try:
            marks = float(marks_input)
            
            if marks < 0 or marks > 100:
                message = "Marks must be between 0 and 100."
                grade = None
            else:
                if marks >= 90:
                    grade = "A+"
                elif marks >= 80:
                    grade = "A"
                elif marks >= 70:
                    grade = "B+"
                elif marks >= 60:
                    grade = "B"
                elif marks >= 50:
                    grade = "C"
                elif marks >= 40:
                    grade = "D"
                else:
                    grade = "F"
        except ValueError:
            message = "Please enter a valid number for marks."
    
    context = {
        'grade': grade,
        'marks': marks,
        'message': message
    }
    return render(request, 'grade.html', context)
   


# -------------------------------
# CGPA Page
# Convert marks to GPA
def marks_to_gpa(marks):
    if marks >= 90:
        return 4.0
    elif marks >= 80:
        return 3.7
    elif marks >= 70:
        return 3.0
    elif marks >= 60:
        return 2.0
    elif marks >= 50:
        return 1.0
    else:
        return 0.0

# Single view for both CGPA types
def Cgpapage(request):
    context = {}

    if request.method == "POST":
        # ---------------- Subject-wise CGPA ----------------
        if "calc_subjects" in request.POST:
            english = float(request.POST.get("english"))
            math = float(request.POST.get("mathematics"))
            science = float(request.POST.get("science"))
            social = float(request.POST.get("social_studies"))
            computer = float(request.POST.get("computer"))

            english_cr = float(request.POST.get("engcredit"))
            math_cr = float(request.POST.get("mathcredit"))
            science_cr = float(request.POST.get("sciencecredit"))
            social_cr = float(request.POST.get("socialcredit"))
            computer_cr = float(request.POST.get("computercredit"))

            gp_english = marks_to_gpa(english)
            gp_math = marks_to_gpa(math)
            gp_science = marks_to_gpa(science)
            gp_social = marks_to_gpa(social)
            gp_computer = marks_to_gpa(computer)

            upore = (gp_english * english_cr +
                     gp_math * math_cr +
                     gp_science * science_cr +
                     gp_social * social_cr +
                     gp_computer * computer_cr)
            niche = english_cr + math_cr + science_cr + social_cr + computer_cr
            cgpa = upore / niche if niche > 0 else 0

            context["cgpa"] = round(cgpa, 2)

        # ---------------- 8-Semester CGPA ----------------
        elif "calc_semesters" in request.POST:
            semesters = []
            for i in range(1, 9):
                sgpa = float(request.POST.get(f"sgpa{i}", 0))
                credit = float(request.POST.get(f"credit{i}", 0))
                semesters.append((sgpa, credit))

            total_points = sum(sgpa * credit for sgpa, credit in semesters)
            total_credits = sum(credit for _, credit in semesters)
            total_cgpa = total_points / total_credits if total_credits > 0 else 0

            context["total_cgpa"] = round(total_cgpa, 2)

    return render(request, "cgpa.html", context)

# -------------------------------
# Base / Home Page
# -------------------------------
def basepage(request):
    return render(request, 'base.html')
