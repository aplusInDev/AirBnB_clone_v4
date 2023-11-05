#!/usr/bin/python3
"""
This module  contains the entry point of the command interpreter
"""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.__init__ import storage


class HBNBCommand(cmd.Cmd):
    """entry point of the command interpreter"""

    prompt = '(hbnb) '
    class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review
    }

    def do_help(self, arg):
        '''help (usage: help argument) This command print giving argument
        information'''
        super().do_help(arg)
        print()

    def do_EOF(self, line):
        '''end of file command to exit the program'''
        print()
        exit()

    def do_quit(self, line):
        '''Quit command to exit the program'''
        exit()

    def emptyline(self):
        """emptyline method to escap new line"""
        pass

    def do_create(self, arg):
        '''Create commant to make new instance of giving class'''
        if not arg:
            print("** class name missing **")
            return
        line = arg.split(" ")
        class_name = arg.split(" ")[0]
        if class_name not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.class_dict[class_name]()
        if len(line) > 1:
            params = line[1:]
            for param in params:
                key = param.split("=")[0]
                value = param.split("=")[1].replace("_", " ")
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                try:
                    value = eval(value)
                except:
                    pass
                setattr(new_instance, key, value)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, line):
        '''Command prints the string representation of an instance based
        on the class name and
        Usage: show <class name> <instance id>'''
        if not line:
            print("** class name missing **")
            return
        arg_list = line.split(" ")
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        if arg_list[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        key = arg_list[0] + "." + arg_list[1]
        try:
            print(storage.all()[key])
        except Exception:
            print("** no instance found **")

    def do_destroy(self, line):
        '''Command destroy a giving instance
        Usage:
            destroy <class name> <instance id>'''
        if not line:
            print("** class name missing **")
            return
        arg_list = line.split(" ")
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        if arg_list[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        key = arg_list[0] + "." + arg_list[1]
        try:
            del (storage.all()[key])
            storage.save()
        except Exception:
            print("** no instance found **")

    def do_all(self, line):
        '''all command that show all giving class instances
        Usage: all <class name>'''
        all_list = []
        if line:
            if line not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
                return
            for key, value in storage.all().items():
                if line == key.split(".")[0]:
                    all_list.append(str(value))
        else:
            for key, value in storage.all().items():
                all_list.append(str(value))
        print(all_list)

    def do_update(self, line, **kwargs):
        '''update command to update giving instance base on giving
        class name and id by adding or updating attribute
        Usage: update <class name> <id> <attribute name> "<attribute value>"'''

        if not line:
            print("** class name missing **")
            return
        line_list = line.split(" ")
        try:
            class_name = line_list[0]
            instance_id = line_list[1]
            if not kwargs:
                new_attr = line_list[2]
                new_value = line_list[3]
            try:
                new_value = eval(new_value)
            except Exception:
                pass
        except Exception:
            pass
        if class_name not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        if len(line_list) < 2:
            print("** instance id missing **")
            return
        giving_key = class_name + "." + instance_id
        if giving_key not in storage.all():
            print("** no instance found **")
            return
        if len(line_list) < 3 and not kwargs:
            print("** attribute name missing **")
            return
        if len(line_list) < 4 and not kwargs:
            print("** value missing **")
            return
        try:
            new_dict = storage.all()[giving_key]
            if kwargs:
                new_dict.__dict__.update(kwargs)
            else:
                if new_attr in ['updated_at', 'created_at']:
                    return
                new_dict.__dict__.update({new_attr: new_value})
            new_dict.save()
        except Exception:
            pass

    def count(self, arg):
        """count method counts giving class instances"""
        counter = 0
        for key in storage.all().keys():
            if key.split(".")[0] == arg:
                counter += 1
        print(counter)

    def default(self, line):
        """default method manage different command type
        Usage: <class name>.<class method> """
        if ('.' in line and '(' in line and ')' in line):
            try:
                class_name = line[: line.find('.')]
                class_method = line[line.find('.') + 1: line.find('(')]
                arg_s = line[line.find('(') + 1: line.find(')')]
            except Exception:
                return
            arg_str = arg_s.replace('\"', '')
            arg_d = class_name + " " + arg_str
            if class_name in HBNBCommand.class_dict:
                if class_method == "all":
                    return self.do_all(class_name)
                if class_method == "count":
                    return self.count(class_name)
                if class_method == "show":
                    return self.do_show(arg_d)
                if class_method == "destroy":
                    return self.do_destroy(arg_d)
                if class_method == "update":
                    if ('{' and '}') in arg_s:
                        update_id = arg_s[:arg_s.find(',')]
                        update_id = update_id.replace('\"', '')
                        key = class_name + " " + update_id
                        update_dict = eval(arg_s[arg_s.find(',') + 1:])
                        return self.do_update(key, **update_dict)
                    update_arg = arg_d.replace(',', '')
                    return self.do_update(update_arg)
        return super().default(line)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
