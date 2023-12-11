#!/usr/bin/python3
"""Unittest for console.py"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestConsole(unittest.TestCase):
    """Test for the console"""

    def setUp(self):
        """Set up for the test"""
        self.console_o = HBNBCommand()

    def tearDown(self):
        """Tear down for the test"""
        pass

    def test_create(self):
        """Test for create"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create State name="California"')
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create State")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create State name="California"')
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create State name="California"')
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                'create User email="airbnb@gmail.com" \ password="root"'
            )
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create User email=" " password="root"')
            self.assertEqual("** value missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create User email=" " password=" "')

    def test_show(self):
        """Test for show"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("show State")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("show State 1234-1234-1234")
            self.assertEqual("** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "show State " + str(list(storage.all().values())[0].id)
            )
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "show BaseModel " + str(list(storage.all().values())[0].id)
            )
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "show MyModel " + str(list(storage.all().values())[0].id)
            )
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_destroy(self):
        """Test for destroy"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("destroy State")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("destroy State 1234-1234-1234")
            self.assertEqual("** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "destroy State " + str(list(storage.all().values())[0].id)
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "destroy BaseModel " + str(list(storage.all().values())[0].id)
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "destroy MyModel " + str(list(storage.all().values())[0].id)
            )
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_all(self):
        """Test for all"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("all State")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("all MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("all")
            self.assertTrue(len(f.getvalue()) > 0)

    def test_update(self):
        """Test for update"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("update State")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("update State 1234-1234-1234")
            self.assertEqual("** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update State " + str(list(storage.all().values())[0].id)
            )
            self.assertEqual("** attribute name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update State "
                + str(list(storage.all().values())[0].id)
                + ' name "California"'
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + ' name "California"'
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update MyModel "
                + str(list(storage.all().values())[0].id)
                + ' name "California"'
            )
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + ' first_name "John"'
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + " age 89"
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + ' email "will@gmail.com"'
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + ' password "root"'
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "update BaseModel "
                + str(list(storage.all().values())[0].id)
                + ' last_name "Smith"'
            )
            self.assertEqual("", f.getvalue())

    def test_count(self):
        """Test for count"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.count()")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("MyModel.count()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("count()")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_quit(self):
        """Test for quit"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("quit")
            self.assertEqual("", f.getvalue())

    def test_EOF(self):
        """Test for EOF"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("EOF")
            self.assertEqual("", f.getvalue())

    def test_help(self):
        """Test for help"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("help")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("help quit")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("help MyModel")
            self.assertEqual("** No help on MyModel **\n", f.getvalue())

    def test_emptyline(self):
        """Test for emptyline"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_do_create(self):
        """Test for do_create"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.create()")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("MyModel.create()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(".create()")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_do_show(self):
        """Test for do_show"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.show(1234-1234-1234)")
            self.assertEqual("** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "State.show(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "BaseModel.show(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "MyModel.show(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_do_destroy(self):
        """Test for do_destroy"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.destroy(1234-1234-1234)")
            self.assertEqual("** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "State.destroy(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "BaseModel.destroy(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertEqual("", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(
                "MyModel.destroy(" + str(list(storage.all().values())[0].id) + ")"
            )
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_do_all(self):
        """Test for do_all"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("State.all()")
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("MyModel.all()")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd(".all()")
            self.assertTrue(len(f.getvalue()) > 0)

    def test_create_missing_class(self):
        """Test for create missing class"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_create_invalid_class(self):
        """Test for create invalid class"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_create_missing_param(self):
        """Test for create missing param"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("create State")
            self.assertEqual("** value missing **\n", f.getvalue())

    def test_create_invalid_param(self):
        """Test for create invalid param"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create State name="California"')
            self.assertTrue(len(f.getvalue()) > 0)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd('create State name="California" invalid="invalid"')
            self.assertEqual("** unknown attribute **\n", f.getvalue())

    def test_show_missing_class(self):
        """Test for show missing class"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_show_invalid_class(self):
        """Test for show invalid class"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console_o.onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
