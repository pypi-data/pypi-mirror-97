import errno
import os


def mkdir(dirname):
    """
    Create the given directory if it does not already exist.
    """
    
    if dirname == "":
        raise ValueError("Invalid dirname '{}'".format(dirname))
    try:
        os.makedirs(dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def ftable(rows):
    """
    Format the data specified in `rows` as table string.
    """
    
    col_sep = "  "
    sep_symbol = "-"
    
    # count the max length for each column
    col_count = max(len(row) for row in rows)
    col_lengths = [0] * col_count
    for row in rows:
        for n_col in range(col_count):
            col_lengths[n_col] = max(col_lengths[n_col], len(str(row[n_col])))
    
    
    # the line at the top and bottom
    sep_line = col_sep.join(sep_symbol * col_length for col_length in col_lengths)
    
    # transform rows into lines
    lines = []
    lines.append(sep_line)
    for row in rows:
        col_strs = []
        for (col_length, col) in zip(col_lengths, row):
            col_str = "{{: <{}}}".format(col_length).format(str(col))
            col_strs.append(col_str)
        lines.append(col_sep.join(col_strs))
    lines.append(sep_line)
    
    # return table as single string
    return "\n".join(lines)
    

def ptable(rows):
    """
    Print the data specified in `rows` as table.
    """
    
    print(ftable(rows=rows))
