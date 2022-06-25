


from celery import shared_task


@shared_task
def prime_task(x):
    numberc = 1
    isprime = 0
    while x != isprime:
        numberc+=1
        c = 0
        for i in range(1,numberc):
            if(numberc%i == 0):
                c+=1
        if(c==1):
            isprime+=1
    
    if(isprime == x):
        return numberc

@shared_task
def palindrome_task(x):
    numberc = 1
    isprime = 0
    while x != isprime:
        numberc+=1
        c = 0
        for i in range(1,numberc):
            if(numberc%i == 0):
                c+=1
        if(c==1):
            if(str(numberc) == str(numberc)[::-1]):
                isprime+=1
    
    if(isprime == x):
        return numberc