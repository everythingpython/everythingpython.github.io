def fibo(n):
    a = 0
    b = 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def main():
    n = int(input("Enter the number of Fibonacci numbers to generate: "))
    print("Fibonacci sequence:")
    for num in fibo(n):
        print(num, end=' ')
    print()
