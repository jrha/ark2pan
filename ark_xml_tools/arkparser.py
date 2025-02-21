#!/usr/bin/env python2
# encoding: utf-8

import xml.etree.ElementTree as ET

class ARKParser():

    def uniclean(self, s):
        s = s.replace(u'\u0087', u'')
        s = s.replace(u'\u0099', u'(TM)')
        s = s.replace(u'\u00ae', u'(R)')
        s = s.replace(u'\u2013', u'-')
        s = s.encode('ascii', 'ignore').strip()
        return s

    def kclean(self, k):
        return k.replace(' ', '_').replace('-', '').replace('#','Num')

    def vclean(self, v):
        if v == 'Yes':
            v = True
        elif v == 'No':
            v = False
        return v

    def parse(self, filename, preserve_empties=False):
        data_table = []
        max_row_width = 0
        with open(filename) as file_in:
            table = ET.fromstring(file_in.read().strip())
            for row in table.findall('tr'):
                input_row = []
                row_width = 0
                for cell in row.findall('td'):
                    input_data = ''
                    row_width += 1
                    if cell.text:
                        input_data = self.uniclean(cell.text)
                    input_row.append(input_data)
                # Trailing cells are trimmed from each row
                # In order to flip the table, we need them back
                max_row_width = max(max_row_width, row_width)
                input_row += [''] * (max_row_width - len(input_row))
                data_table.append(input_row)

            data_table = data_table[2:] # Drop first two rows

            data_table = zip(*data_table) # Flip rows and columns

            column_names = [self.kclean(c) for c in data_table[0]] # Extract and clean key names
            column_names[0] = 'Processor_Name' # Add missing title
            data_table = data_table[1:] # Remove column names from table

            # Construct a dictionary from column names and tabular data
            data_table = [dict(zip(column_names, [self.vclean(v) for v in r])) for r in data_table]
            if not preserve_empties:
                # Remove items with empty values
                data_table = [{k:v for k, v in r.items() if v} for r in data_table]

            return data_table
