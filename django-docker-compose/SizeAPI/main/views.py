from django.http import HttpResponse, JsonResponse
import numpy as np

import pickle

NEEDED_KEY = "4KN4EWQ-983M1HX-PEFRVQC-Q6D1VJH"

def get_size(weight, height, age):
    bmi = 100*(weight / (height**2))
    if bmi > 0.4 and weight > 65:
        return "XXL"
    elif bmi > 0.35:
        return "XL"
    model = pickle.load(open("model.pkl", "rb"))
    return model.predict([[height,weight,age,bmi]])[0]

SIZE_NAMES = {
    "XS": "Extra Small",
    "S": "Small",
    "M":"Medium",
    "L": "Large",
    "XL": "Extra Large"
}

def size(request):
    try:
        needed_inputs = ["apiKey", "height", "weight", "age", "userId"]
        inps = dict(request.GET)
        inps = {i:j[0] if isinstance(j, list) else j for i,j in inps.items()}
        if inps["age"] <= 0 or inps["weight"] >= 150 or inps["height"] >= 200:
            return JsonResponse({"status":"Failure", "body":f"Out of bounds inputs!"})
        missing = [i for i in needed_inputs if i not in inps]
        if missing:
            return JsonResponse({"status":"Failure", "body":f"The following inputs are missing! {needed_inputs}"})

        s = get_size(float(inps['weight']), float(inps['height']), float(inps['age']))
        return JsonResponse({"status":"Success", "size":s})
    except:
        return JsonResponse({"status":"Failure", "body":f"An unexpected error occured."})