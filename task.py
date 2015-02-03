class Task():
  priority = None
  creation_date = None
  content = None
  projects = []
  contexts = []
  completion_date = None

  def complete(self):
    """Returns True if the task is complete, False otherwise."""
    return self.completion_date != None

