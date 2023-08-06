import sys

def main():
    number_one = int(sys.argv[1])
    number_two = int(sys.argv[2])
    
    print("Adding your two numbers together...")
    print(number_one + number_two + 5)

if __name__ == "__main__":
    main()