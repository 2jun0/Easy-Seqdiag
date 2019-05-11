TYPE_EDGE = 1
TYPE_DEFINE = 2
TYPE_UNKNOWN = 3
TYPE_COMMENT = 4

EDGE_RECORD = {'left':None, 'right':None, 'direction':None, 'attributes':[]}

define_table = dict()
line_table = []

easy_to_origin_direction = {'<':'<-', '<<':'<--', '>':'->', '>>':'-->', '->':'->>', '<<-':'<<--', '<-':'<<-', '->>':'-->>', '>>>':'=>', '<<<':'<='}
easy_to_origin_attr = {'l':'label', 'n':'note', 'ln':'leftnote', 'rn':'rightnote', 're':'return', 'c':'color', 'f':'failed', 'fs':'fontsize', 'ff':'fontfamily'}

def convert_to_origin_seqdiag():

    origin_seqdig = 'seqdiag {\n'

    for line_record in line_table:
        convert_line = ''

        if line_record[0] == TYPE_UNKNOWN:
            convert_line = convert_line + line_record[1] + ';'

        elif line_record[0] == TYPE_EDGE:

            left = line_record[1]['left']
            right = line_record[1]['right']
            direction = line_record[1]['direction']
            attributes = line_record[1]['attributes']

            if left in define_table:
                left = define_table[left]

            if right in define_table:
                right = define_table[right]

            if (' ' in left or ':' in left):
                left = '\"' + left + '\"'
            if (' ' in right or ':' in right):
                right = '\"' + right + '\"'

            convert_line = convert_line + left + ' ' + direction + ' ' + right

            if len(attributes) > 0:
                convert_line = convert_line + '['
                for attribute in attributes:
                    # attribute[0] : attribute definition
                    # attribute[1] : attribute value
                    convert_line = convert_line + attribute[0] + ' = \"' + attribute[1] + '\",'

                convert_line = convert_line[:-1] + ']'

            convert_line = convert_line + ';'

        origin_seqdig = origin_seqdig + '\n\t' + convert_line

    origin_seqdig = origin_seqdig + '\n}'

    return origin_seqdig

def pre_process(str):
    split_lines = str.split('\n')
    for line in split_lines:
        pre_process_line(line)

def read_file_and_process(path):

    f = open(path, 'r')

    while True:
        line = f.readline()
        if not line:
            break

        pre_process_line(line)

    f.close()

def pre_process_line(line):

    line = line.strip()

    if len(line) < 1:
        return

    # This line is comment line?
    if line[0] is '//':
        return

    # This line is define line?
    if line[0] is '#':
        split_lines = line[1:].strip().split(' ')
        define_table[split_lines[-1]] = ' '.join(split_lines[:-1])

    # This line is edge line?
    elif ('<' in line) or ('>' in line):
        # Edge record attributes
        left = ''
        right = ''
        direction = ''
        attributes = []

        str = ''
        j = 0

        # Get left, right, direction
        while len(line) > j:

            # Direction
            if line[j] in ['<', '>', '-', '=']:
                left = str.strip()
                str = ''
                while line[j] in ['<', '>', '-', '=']:
                    direction = direction + line[j]
                    j = j + 1

            # Back slash mode
            elif line[j] is '\\':
                j = j + 1

            # Attributes
            elif line[j] is '#':
                break

            str = str + line[j]
            j = j + 1

        right = str.strip()

        # Attributes
        str = ''
        attrs = dict()
        attr_def = ''

        # Attribute definition start
        while len(line) > j and line[j] is '#':

            j = j + 1

            # Get attribute definition
            while len(line) > j:
                # Attribute definition end
                if line[j] is ' ':
                    j = j + 1
                    break
                else:
                    attr_def = attr_def + line[j]
                    j = j + 1

            # Error : unknown attribute
            if attr_def not in easy_to_origin_attr.keys():
                attr_def = attr_def + line[j]
                print('Error : unknown attribute')
                print('line {} : {}'.format(j, attr_def))

            # Attribute value
            if attr_def is not '':
                while len(line) > j and line[j] is not '#' :
                    str = str + line[j]
                    j = j + 1

                # Add attribute
                origin_attr = easy_to_origin_attr[attr_def]
                attr_value = str.strip()
                attributes.append((origin_attr,attr_value))
                str = ''
                attr_def = ''

        edge_record = EDGE_RECORD.copy()
        edge_record['left'] = left
        edge_record['right'] = right
        edge_record['direction'] = easy_to_origin_direction[direction]
        edge_record['attributes'] = attributes
        line_table.append((TYPE_EDGE, edge_record))
    else:
        line_table.append((TYPE_UNKNOWN, line))
