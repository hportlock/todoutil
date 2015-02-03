import re

from task import Task

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
