import sympy

def check_prime_sympy(n):
    """
    Checks if a number is prime using sympy.isprime().
    """
    if sympy.isprime(n):
        return f"{n} is a prime number."
    else:
        return f"{n} is not a prime number."

# Example usage
print(check_prime_sympy(17))
print(check_prime_sympy(30))