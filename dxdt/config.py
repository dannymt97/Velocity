#!/usr/bin/env python3

"""Implementation of a class for sourcing configuration from a given file.

Author: Dan Theriault
Feature-incomplete and under active development.
"""

import configparser
import os.path


def source():
    """return configuration file path."""
    configdir = os.path.expanduser('~/.dxdt')
    source = BookHandler(configdir+'/config')
    return source


class BookHandler:
    """Class for handling dxdt's configuration file."""

    def __init__(self, config_file):
        """Class Instantiation.

        configfile is most likely in $HOME/.dxdt/
        """
        self.file = config_file
        self.parser = configparser.ConfigParser()
        self.parser.read(self.file)
        self.config = {}

    def default_book(self):
        """Used primarily when 'book' argument to dxdt() is None."""
        return self.parser['default']['book']

    def get_books(self):
        """return a list of books based off the configfile."""
        sections = self.parser.sections()
        sections.remove('default')
        return sections

    def read(self, book):
        """Read configuration information and return as a dict."""
        self.config = {
            'path': os.path.expanduser(self.parser[book]['path']),
            'extension': self.parser[book]['extension'],
            'args': []
        }

        # Get editor for book if available: else, use global default
        if 'editor' in self.parser[book]:
            self.config['editor'] = self.parser[book]['editor']
        else:
            self.config['editor'] = self.parser['default']['editor']

        i = 1
        while 'arg' + str(i) in self.parser[book]:
            self.config['args'].append(self.parser[book]['arg'+str(i)])
            i = i + 1

        if 'template' in self.parser[book]:
            self.config['template'] = self.parser[book]['template']

        return self.config

    def write(self, book, key, value):
        """Basic implementation of writing new values to config."""
        if key == 'args':
            i = 1
            for arg in value:
                self.parser[book]['arg' + str(i)] = arg
                i = i + 1
        elif len(value) == 1:
            self.parser[book][key] = value[0]
        else:
            raise ValueError('too many args: ' + str(len(value)))
        self.parser.write(open(self.file, 'w'))

    def new_book(self, name, path, extension):
        """Create a book with given name if none exists."""
        sections = self.getbooks()
        if name not in sections:
            self.parser.add_section(name)
            self.parser[name]['path'] = path
            self.parser[name]['extension'] = extension
            self.parser.write(open(self.file, 'w'))
        else:
            raise ValueError('book already exists: ' + name)

    def remove_book(self, name):
        """Remove an existing book."""
        sections = self.getbooks()
        if name not in sections:
            raise ValueError('book does not exist: ' + name)
        else:
            self.parser.remove_section(name)
            self.parser.write(open(self.file, 'w'))