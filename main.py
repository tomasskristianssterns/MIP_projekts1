
class Game:
  
  def __init__(self, start="default", algorithm= "default"):
    self.start = start
    self.algorithm = algorithm
  
  def get_start(self):
    return self.start
  
  def set_start(self, new_start):
    self.start = new_start
  
  def get_algorithm(self):
    return self.algorithm
  
  def set_algorithm(self, new_algorithm):
        self.algorithm = new_algorithm
        
  def check_start(self):
    while True:  
        user_start = input("Choose who starts first (human or computer): ").strip().lower()
        if user_start in ["human", "computer"]:
            self.set_start(user_start)
            break
        else:
            print("Invalid input. Please type 'human' or 'computer'.")
  
  
  def check_algorithm(self):
    while True:  
      user_algorithm = input("Choose algorithm (minmax or alfa-beta): ").strip().lower()
      if user_algorithm in ["minmax", "alfa-beta"]:
          self.set_algorithm(user_algorithm)
          break
      else:
          print("Invalid input. Please type 'minmax' or 'alfa-beta'.")
      
      
      
def main():

  print("Hello, Welcome to the game")
  
  
  user = Game()
  
  user.check_start()
  print(f"Game will start with: {user.get_start()}")
  
  user.check_algorithm()
  print(f"Choosed algorithm: {user.get_algorithm()}")
  
  

if __name__ == "__main__":
  main()