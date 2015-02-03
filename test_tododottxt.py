#! /usr/bin/env python

import unittest

from task import Task
from tododottxt import parse_task

class TestParseTodo(unittest.TestCase):

  def test_parse_priority(self):
    task = parse_task('(A) Call Mom')
    self.assertEqual(task.priority, 'A')
    self.assertEqual(task.content, 'Call Mom')

  def test_parse_no_priority(self):
    task = parse_task('Really gotta call Mom (A) @phone @someday')
    self.assertIsNone(task.priority)
    task = parse_task('(b) Get back to the boss')
    self.assertIsNone(task.priority)
    task = parse_task('(B)->Submit TPS report')
    self.assertIsNone(task.priority)

  def test_parse_creation_date(self):
    task = parse_task('2011-03-02 Document +TodoTxt task format')
    self.assertEqual(task.creation_date, '2011-03-02')

  def test_parse_creation_date_with_pri(self):
    task = parse_task('(A) 2011-03-02 Call Mom')
    self.assertEqual(task.creation_date, '2011-03-02')

  def test_parse_no_creation_date(self):
    task = parse_task('(A) Call Mom 2011-03-02')
    self.assertIsNone(task.creation_date)

  def test_parse_project(self):
    line = '(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone'
    task = parse_task(line)
    self.assertListEqual(
        sorted(task.projects),
        sorted(['Family', 'PeaceLoveAndHappiness']))

  def test_parse_no_project(self):
    task = parse_task('Learn how to add 2+2')
    self.assertEqual(task.projects, [])

  def test_parse_context(self):
    line = '(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone'
    task = parse_task(line)
    self.assertListEqual(
        sorted(task.contexts),
        sorted(['iphone', 'phone']))

  def test_parse_no_context(self):
    task = parse_task('Email SoAndSo at soandso@example.com')
    self.assertEqual(task.contexts, [])

  def test_parse_complete(self):
    task = parse_task('x 2011-03-03 Call Mom')
    self.assertEqual(task.completion_date, '2011-03-03')

  def test_parse_not_complete(self):
    task = parse_task('xylophone lesson')
    self.assertIsNone(task.completion_date)

    task = parse_task('X 2012-01-01 Make resolutions')
    self.assertIsNone(task.completion_date)

    task = parse_task('(A) x Find ticket prices')
    self.assertIsNone(task.completion_date)

  def test_parse_content(self):
    line = '(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone'
    task = parse_task(line)
    self.assertEqual(task.content, 'Call Mom')

if __name__ == "__main__":
  unittest.main()
