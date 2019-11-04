#!/usr/bin/python

# SYNTAX: python python_module_edit.py FILE_PATH ID [ATTRIBUTE_NAME_1=ATTRIBUTE_EXPRESSION_1;...;ATTRIBUTE_NAME_N=ATTRIBUTE_EXPRESSION_N]
# Note: An ATTRIBUTE_EXPRESSION may contain an `{ID}` variable which will be replaced by the subfolders name.

#####
#   #
#####

import sys


def line_defines_attribute(line, attribute_name):
    return line.startswith(attribute_name)


def create_new_line(attribute_name, expression, tag, id):
    if "{ID}" in expression:
        # inset parametes into expression
        expression = expression.replace("{ID}", "(" + id + ")")
        # evaluate expresion
        locals = {"ret": None}
        exec("ret = " + expression, {}, locals)
        expression = str(locals["ret"])
    # crate new attribute definition
    return attribute_name + " = " + expression + " #" + tag + "\n"


if __name__ == "__main__":
    # extract file path
    file_path = sys.argv[1]
    # extract id
    id = sys.argv[2]
    # extract overwrite attributes
    overwrite_attributes = sys.argv[3]
    overwrite_attributes = overwrite_attributes.split(";")
    overwrite_attributes = [e.split("=") for e in overwrite_attributes]
    overwrite_attributes = {e[0]: e[1] for e in overwrite_attributes}

    lines = []
    # read file
    with open(file_path, "r") as file:
        lines = file.readlines()
    # overwrite first appearence of each attribute when present
    for i in range(len(lines)):
        for attribute_name, expression in overwrite_attributes.items():
            if line_defines_attribute(lines[i], attribute_name):
                lines[i] = create_new_line(
                    attribute_name, expression, "overwritten", id
                )
                del overwrite_attributes[attribute_name]
                break
    # append new attributes to end of file
    if overwrite_attributes:
        lines.append("\n\n")
    for attribute_name, expression in overwrite_attributes.items():
        line = create_new_line(attribute_name, expression, "added", id)
        lines.append(line)
    # write file
    with open(file_path, "w") as file:
        file.writelines(lines)