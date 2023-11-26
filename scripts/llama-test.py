import sys
sys.path.insert(1, 'src')

from llama import Llamav2

def main():
    llama = Llamav2()
    while True:
        query = input("Query: ")
        answer = llama.get_answer(query)
        print(f"Answer: {answer}")

if __name__ == '__main__':
    main()