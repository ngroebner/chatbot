def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# Test function
def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    print("Test passed.")

# Run the test
if __name__ == "__main__":
    test_factorial()