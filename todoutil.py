#! /usr/bin/env python

import json
import re

import requests

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

def parse_task(task_line):
  """Parses a single line of a todo.txt file into a Task object."""
  content = task_line
  task = Task()

  task.completion_date, content = __extract_first(
      '^x (\d{4}-\d{2}-\d{2})', content)
  task.priority, content = __extract_first(r'^\(([A-Z])\) ', content)
  task.creation_date, content = __extract_first(
      '^(\d{4}-\d{2}-\d{2}) ', content)
  task.projects, content = __extract_all(r' [+](\S+)', content)
  task.contexts, content = __extract_all(r' [@](\S+)', content)

  task.content = content
  return task


def __extract_first(regex, content):
  """Get the matching group from the regex and deletes it from content.

  regex -- The regex to match, it must contain exactly one capturing group.
  content -- The content to search.

  Returns a tuple where the first value is the content of the matching group
  content (or None if there is no match) and the second value is the content
  minus the match.
  """
  match_content = None
  match = re.search(regex, content)
  if match:
    match_content = match.group(1)
  filtered_content = re.sub(regex, '', content)

  return(match_content, filtered_content)

def __extract_all(regex, content):
  """Get the matching group from the regex and deletes it from content.

  regex -- The regex to match, it must contain exactly one capturing group.
  content -- The content to search.

  Returns a tuple where the first value is a list that contains the content of
  all of the group matches in the string content (or an empty list if there is
  no match) and the second value is the content minus the match.
  """
  match_content = re.findall(regex, content)
  filtered_content = re.sub(regex, '', content)

  return(match_content, filtered_content)

class TodoistApiHelper():
  def __init__(self, api_token):
    """Connects to todoist and loads the projects and labels."""
    self.api_token = api_token

    response = get_todoist(api_token, 'getProjects')
    self.projects = {}
    for p in response:
      self.projects[p['name']] = p['id']

    response = get_todoist(api_token, 'getLabels')
    self.labels = {}
    for name, l in response.iteritems():
      self.labels[name] = l['id']

  def get_or_create_project_id(self, name):
    """Gets the id for a specified project, creates it if it doesn't exist."""
    if not(name in self.projects):
      response = self.__post('addProject', {'name': name})
      self.projects[name] = response['id']
    return self.projects[name]

  def get_or_create_label_id(self, name):
    """Gets the id for a specified label, creates it if it doesn't exist."""
    if not(name in self.labels):
      response = self.__post('addLabel', {'name': name})
      self.labels[name] = response['id']
    return self.labels[name]

  def put_task(self, task):
    """Puts a task into todoist."""
    payload = {'content': task.content}
    if task.projects:
      payload['project_id'] = self.get_or_create_project_id(task.projects[0])
    else:
      payload['project_id'] = self.get_or_create_project_id('General')
    label_ids = []
    for label in task.contexts:
      label_ids.append(self.get_or_create_label_id(label))
    payload['labels'] = json.dumps(label_ids)

    priority = 1
    if task.priority == 'A':
      priority = 4
    if task.priority == 'B':
      priority = 3
    if task.priority == 'C':
      priority = 2
    payload['priority'] = priority

    return self.__post('addItem', payload)

  def __get(self, path, payload=None):
    return get_todoist(self.api_token, path, payload)

  def __post(self, path, payload=None):
    return post_todoist(self.api_token, path, payload)

def get_todoist(api_token, path, payload=None):
  params = {'token': api_token}
  if payload:
    params.update(payload)
  url = 'https://api.todoist.com/API/%s' % path
  r = requests.get(url, params=params)
  return r.json()

def post_todoist(api_token, path, payload=None):
  params = {'token': api_token}
  if payload:
    params.update(payload)
  url = 'https://api.todoist.com/API/%s' % path
  r = requests.post(url, data=params)
  return r.json()

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


