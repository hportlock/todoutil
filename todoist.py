import json

import requests

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

