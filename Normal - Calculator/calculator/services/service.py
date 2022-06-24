


from .task import palindrome_task, prime_task
from django.http import HttpResponse


def prime(request, x):
    result = prime_task(x)
    response = '<html><h1>Index {} Prime Number = {}</h1></html>'.format(x, result)
    return HttpResponse(response)

def palindrome(request, x):
    result = palindrome_task(x)
    response = '<html><h1>Index {} Prime Palindrome Number = {}</h1></html>'.format(x, result)
    return HttpResponse(response)