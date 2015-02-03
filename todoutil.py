#! /usr/bin/env python

from tododottxt import parse_task
from todoist import TodoistApiHelper

def send_to_todoist(api_token, path):
  """Reads all of the tasks out of the file and pushes them to todoist."""
  apiHelper = TodoistApiHelper(api_token)
  with open(path, 'r') as f:
    for line in f:
      task = parse_task(line)
      if not task.complete():
        print "Uploading: %s" % line
        apiHelper.put_task(task)

if __name__ == "__main__":
  msg = "Path to todo.txt file to import [./todo.txt]: "
  path = raw_input(msg) or "./todo.txt"
  msg = "Your todoist API token: "
  api_token = raw_input(msg)
  send_to_todoist(api_token, path)


