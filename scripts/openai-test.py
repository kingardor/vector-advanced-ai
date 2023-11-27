import sys
sys.path.insert(1, 'src')

from customgpt import CustomGPT

if __name__ == '__main__':
    gpt = CustomGPT()
    while True:
        query = input("Query: ")
        answer = gpt.get_answer(query)
        print(f"Answer: {answer}")