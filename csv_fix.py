import sys

def fix_line(line, schema=False):
    if schema:
        return line.replace('Position', 'PositionX,PositionY')
    else:
        if not line:
            return line
        fixed = line.replace('Vector2d', '').replace('<', '')\
            .replace('>', '').replace(' ', '')
        return fixed

def main():
    try:
        execname, fn, out_fn = sys.argv
        with open(fn, 'r') as read_fh, open(out_fn, 'w') as out_fh:
            chunk = 100000  # write chunks at a time, give drive a break
            lines = []
            line = read_fh.next()
            while not line.strip():
                lines.append(line)
                line = read_fh.next()
            lines.append(fix_line(line, True))
            lines.append(read_fh.next())  # line with simulation time
            for line in read_fh:
                fixed = fix_line(line)
                lines.append(fixed)
                if len(lines) == chunk:
                    out_fh.writelines(lines)
                    lines = []
            # write any remaining lines
            out_fh.writelines(lines)
    except ValueError:
        execname = sys.argv[0]
        print >>sys.stderr, 'usage: {0} in_file out_file'.format(execname)
        sys.exit(-1)

if __name__ == '__main__':
    main()
