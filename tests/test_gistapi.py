# -*- coding: utf-8 -*-

from tests import *
from unittest import TestCase

api = gistapi.Gist(opts.get('access_token'))
test_gist = api.create({
  'files': {
    'test_gist.txt': {
      'content': 'Gist test content'
    }
  }
})

class TestGistAPI(TestCase):
  def test_access_token(self):
    with self.assertRaises(gistapi.GistException):
      gistapi.Gist('')
    self.assertIsInstance(api, gistapi.Gist)
    self.assertIsNotNone(api)

  def test_create_gist(self):
    data = {'description': 'test description'}

    # Try to create a gist with invalid data
    # Without files object
    with self.assertRaises(gistapi.GistException):
      api.create(data)
    # With a wrong 'files' object
    with self.assertRaises(gistapi.GistException):
      api.create({
        'description': 'some description',
        'files': 'some files'
      })

    # Create a gist without description
    gist = api.create({
      'files': {
        'file.txt': {
          'content': 'content for this file.txt'
        }
      }
    })
    self.assertIsNotNone(gist.get('id'))
    # Delete test gist
    self.assertTrue(api.delete(gist.get('id')))

    # Create a gist with description and files
    data.update({ 'files': {
      'someFile': {
        'content': 'Content of this file'
      }
    }})
    gist = api.create(data)
    self.assertIsNotNone(gist.get('id'))
    gist_id = gist.get('id')

    # Get a list with all public gists
    gist_items = api.list()

    # Check if the created gist isn't public gist list
    for gist_item in gist_items:
      self.assertNotEqual(gist_item.get('id'), gist_id)
    # Delete test gist
    self.assertTrue(api.delete(gist_id))

  def test_edit_gist(self):
    # Get possible errors
    # Passing wrong parameters
    test_gist_id = test_gist.get('id')
    with self.assertRaises(gistapi.GistException):
      api.edit('some_id', {})
    # With wrong files object
    with self.assertRaises(gistapi.GistException):
      api.edit(test_gist_id, {
        'files': 'some content'
      })

    # Updating without changes
    gist = api.edit(test_gist_id, {})
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(len(gist.get('files')), 1)

    # Adding a new file
    gist = api.edit(test_gist_id, {
      'files': { 'other_file.txt': {
        'content': 'Some content'
      }}
    })
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(len(gist.get('files')), 2)

    # Removing the created file
    gist = api.edit(test_gist_id, {
      'files': { 'other_file.txt': None}
    })
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(len(gist.get('files')), 1)

  def test_get_gist(self):
    test_gist_id = test_gist.get('id')
    # Getting errors
    with self.assertRaises(gistapi.GistException):
      api.get('---')

    # Getting gist
    gist = api.get(test_gist_id)
    self.assertIsNotNone(gist.get('id'))
    self.assertEqual(test_gist_id, gist.get('id'))
    self.assertTrue(api.delete(test_gist_id))
