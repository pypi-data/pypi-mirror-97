# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# Revised BSD License, included in this distribution as LICENSE

"""
Metapack CLI program for exditing metapack metadata in place
"""

from metapack.cli.core import MetapackCliMemo as _MetapackCliMemo
from metapack.cli.core import err, warn, write_doc
from metapack.package import Downloader

downloader = Downloader.get_instance()


class MetapackCliMemo(_MetapackCliMemo):

    def __init__(self, args, downloader):
        super().__init__(args, downloader)

        self.term = self.args.term[0]
        self.value = self.args.value[0] if hasattr(self.args, 'value') else None

        parts = self.term.split('.')

        if len(parts) != 2 and len(parts) != 3:
            err('Term arg must have 2 or 3 words seperated by a period')

        if len(parts) == 3:
            self.section, parts = parts[0], parts[1:]
            self.term = '.'.join(parts)
        else:
            self.section = 'Root'


def edit_args(subparsers):
    parser = subparsers.add_parser(
        'edit',
        help='Edit a metatab file'
    )

    cmds = parser.add_subparsers(help='Commands')

    parser.set_defaults(run_command=edit_cmd)

    parser.add_argument('-e', '--echo', help="Print the file after editing", action='store_true', required=False)

    cp_add = cmds.add_parser('add', help='Add a term')
    cp_add.set_defaults(edit_command=add_cmd)
    cp_add.add_argument('term', nargs=1,
                        help="A fully qualified term. Prefix with a third component to set the section "
                             "( 'Resources.Root.Datafile' ) ")
    cp_add.add_argument('value', nargs=1, help="The term value, for add and edit ")
    cp_add.add_argument('-a', '--arg', help="Add an additional argument: 'Name=value' ",
                        action='append', required=False)

    cp_add.add_argument('metatabfile', nargs='?',
                        help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv' ")

    cp_edit = cmds.add_parser('change', help='Edit a term')
    cp_edit.set_defaults(edit_command=change_cmd)
    cp_edit.add_argument('term', nargs=1,
                         help="A fully qualified term. Prefix with a third component to set the section"
                              " ( 'Resources.Root.Datafile' ) ")
    cp_edit.add_argument('value', nargs=1, help="The term value, for add and edit ")
    cp_edit.add_argument('metatabfile', nargs='?',
                         help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv' ")

    cp_delete = cmds.add_parser('delete', help='Delete a term')
    cp_delete.set_defaults(edit_command=delete_cmd)
    cp_delete.add_argument('term', nargs=1,
                           help="A fully qualified term. Prefix with a third component to set the section "
                                "( 'Resources.Root.Datafile' ) ")
    cp_delete.add_argument('metatabfile', nargs='?',
                           help="Path or URL to a metatab file. If not provided, defaults to 'metadata.csv' ")


def edit_cmd(args):
    m = MetapackCliMemo(args, downloader)
    m.args.edit_command(m)


def add_cmd(m):
    doc = m.doc

    args = dict(a.split('=', 1) for a in m.args.arg)

    doc[m.section].new_term(m.term, m.value, **args)

    if m.args.echo:
        print(doc.as_csv())

    write_doc(doc)


def change_cmd(m):
    doc = m.doc

    t = doc.find_first(m.term, section=m.section)

    t.value = m.value

    if m.args.echo:
        print(doc.as_csv())

    write_doc(doc)


def delete_cmd(m):
    doc = m.doc

    terms = doc.find(m.term, section=m.section)

    if not terms:
        warn("No terms found for: '{}' in section '{}' ".format(m.term, m.section))

    for term in terms:
        doc.remove_term(term)

    terms = doc.find(m.term, section=m.section)

    if terms:
        warn("Delete failed")

    if m.args.echo:
        print(doc.as_csv())

    write_doc(doc)
