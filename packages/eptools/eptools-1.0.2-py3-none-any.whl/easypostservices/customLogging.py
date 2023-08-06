class CustomLogger:
  def __init__(self, logger):
    self.logger = logger
    
  def debug(self, msg, pr=True):
            if pr:
                print(msg)
            if self.logger != None:
                self.logger.debug(msg)

  def info(self, msg, pr=True):
      if pr:
          print(msg)
      if self.logger != None:
          self.logger.info(msg)

  def error(self, msg, pr=True):
      if pr:
          print(msg)
      if self.logger != None:
          self.logger.error(msg) 


          