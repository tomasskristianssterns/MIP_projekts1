import random

LEFT_BOUND = 20_000
RIGHT_BOUND = 30_000

VALID_DIVISORS = [2, 3, 4]
MAX_STARTING_NUMBERS = 5

def is_valid_number(number: int) -> bool:
  for divisor in VALID_DIVISORS:
    if number % divisor == 0:
      return True
  return False

def get_number() -> int:
  genereted_number = random.randint(LEFT_BOUND, RIGHT_BOUND)
  while not is_valid_number(genereted_number):
    genereted_number = random.randint(LEFT_BOUND, RIGHT_BOUND)
  return genereted_number

def main():
  starting_numbers = [get_number() for _ in range(MAX_STARTING_NUMBERS)]
  print(starting_numbers)

if __name__ == "__main__":
  main()
