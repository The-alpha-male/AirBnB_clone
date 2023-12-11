#!/usr/bin/python3
"""This module creates a console for the AirBnB project"""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """Class for the entry point of the command interpreter."""

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """EOF command to exit the program"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Handles empty line + ENTER"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id."""
        if not line:
            print("** class name missing **")
        elif line != "BaseModel":
            print("** class doesn't exist **")
        else:
            new_model = BaseModel()
            new_model.save()
            print(new_model.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the class
        name and id."""
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id (save the change
        into the JSON file)."""
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation
        of all instances based or not on the
        class name."""
        args = line.split()
        if not line:
            print([str(value) for value in storage.all().values()])
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            print(
                [
                    str(value)
                    for key, value in storage.all().items()
                    if key.split(".")[0] == args[0]
                ]
            )

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)."""
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing **")
        elif len(args) < 4:
            print("** value missing **")
        else:
            key = args[0] + "." + args[1]
            if key in storage.all():
                setattr(storage.all()[key], args[2], args[3])
                storage.save()
            else:
                print("** no instance found **")

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        Here we check if the command is of the form <class name>.command().
        If it is, we extract the class name and the command and pass it to
        the corresponding do_<command> method."""
        args = line.split(".")
        if len(args) == 2:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                self.do_count(args[0])
            elif args[1][:5] == "show(" and args[1][-1] == ")":
                self.do_show(args[0] + " " + args[1][6:-2])
            elif args[1][:8] == "destroy(" and args[1][-1] == ")":
                self.do_destroy(args[0] + " " + args[1][9:-2])
            elif args[1][:7] == "update(" and args[1][-1] == ")":
                args[1] = args[1][7:-1]
                args[1] = args[1].replace('"', "")
                args[1] = args[1].replace("'", "")
                args[1] = args[1].replace(",", "")
                args[1] = args[1].split()
                if len(args[1]) == 2:
                    args[1].append("")
                if len(args[1]) == 3:
                    args[1].append("")
                self.do_update(
                    args[0] + " " + args[1][0] + " " +
                    args[1][1] + " " + args[1][2]
                )
            else:
                cmd.Cmd.default(self, line)
        else:
            cmd.Cmd.default(self, line)

    def do_count(self, line):
        """Retrieves the number of instances of a class"""
        args = line.split()
        if not line:
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            print(
                len(
                    [
                        value
                        for key, value in storage.all().items()
                        if key.split(".")[0] == args[0]
                    ]
                )
            )


if __name__ == "__main__":
    HBNBCommand().cmdloop()
