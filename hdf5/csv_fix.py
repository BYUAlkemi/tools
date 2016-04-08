import sys

def fix_line(line, schema=False):
    if schema:
        return line.replace('Position', 'positionX,positionY')
    else:
        if not line:
            return line
	columns = line.split(',')
        fixed = line.replace('Vector2d', '').replace('<', '')\
            .replace('>', '').replace(' ', '')
        return fixed

def main():
    try:
        execname, fn, out_fn = sys.argv
        with open(fn, 'r') as read_fh, open(out_fn, 'w') as out_fh:
            # chunk = 50000  # write chunks at a time, give drive a break
            chunk = 50
            lines = []
            line = read_fh.next()
            while not line.strip():
                line = read_fh.next()
            lines.append('{},{}'.format("timestep", fix_line(line, True)))
            timestep = 0
            for line in read_fh:
                if line.strip():
                    if line[0].isalpha():
                        if line.startswith("Sim"):
                            timestep += 1
                        continue
                    fixed = fix_line(line)
                    lines.append('{},{}'.format(timestep, fixed))
                    if (len(lines) % chunk) == 0:
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
