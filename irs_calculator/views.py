from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

def index(request):
    data = {
        'title': 'Home Page'
    }
    return render(request, 'index.html', data)

def compute_tax(request):
    # if request.is_ajax():
    if is_ajax(request=request):
        annual_income = request.GET.get('annual_income', None)
        filing_status = request.GET.get('filing_status', None)
        adjustments = request.GET.get('adjustments', None)
        federal_tax_witheld = request.GET.get('federal_tax_witheld', None)

        if annual_income is not None:
            annual_income = float(annual_income)
        else:
            annual_income = 0

        if adjustments is not None:
            adjustments = float(adjustments)
        else:
            adjustments = 0

        if federal_tax_witheld is not None:
            federal_tax_witheld = float(federal_tax_witheld)
        else:
            federal_tax_witheld = 0

        gross_income = annual_income-adjustments

        std_deduction = 0
        if filing_status == "1":
            std_deduction = 13850
        elif filing_status == "2":
            std_deduction = 20800
        elif filing_status == "3":
            std_deduction = 27700
        elif filing_status == "4":
            std_deduction = 1850
        elif filing_status == "5":
            std_deduction = 1500
        
        gross_income = gross_income-std_deduction
        taxable_income = gross_income

        if gross_income < 0:
            gross_income = 0

        total_tax = 0
        if gross_income > 0:
            total_tax += 11000 * 0.10
            gross_income -= 11000

        if gross_income > 0 and gross_income <= 33725:
            total_tax += gross_income * 0.12
            gross_income -= 33725
        
        if gross_income > 0 and gross_income <= 50650:
            total_tax += gross_income * 0.22
            gross_income -= 50650

        if gross_income > 0 and gross_income <= 86725:
            total_tax += gross_income * 0.24
            gross_income -= 86725

        if gross_income > 0 and gross_income <= 49150:
            total_tax += gross_income * 0.32
            gross_income -= 49150

        if gross_income > 0 and gross_income <= 346875:
            total_tax += gross_income * 0.35
            gross_income -= 346875

        if gross_income >= 578126:
            total_tax += gross_income * 0.37

        refund = 0
        for_payment = 0
        if total_tax > federal_tax_witheld:
            for_payment = total_tax-federal_tax_witheld
        elif federal_tax_witheld > total_tax:
            refund = federal_tax_witheld-total_tax

        response = {}
        response['tax_liability'] = total_tax
        response['taxable_income'] = taxable_income
        response['for_payment'] = for_payment
        response['refund'] = refund
        response['federal_tax_witheld'] = federal_tax_witheld
        return HttpResponse(json.dumps(response), content_type="application/json")

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'