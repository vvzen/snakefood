"""
Read snakefood dependencies from stdin and cluster according to filenames.

You need to call this script with the names of directories to cluster together,
for relative filenames.

See http://furius.ca/snakefood for details.
"""

import sys
from itertools import imap
from collections import defaultdict
from operator import itemgetter


# (Refactor candidate.)
def read_depends(f):
    "Generator for the dependencies read from the given file object."
    for line in f.xreadlines():
        try:
            yield eval(line)
        except Exception:
            logging.warning("Invalid line: '%s'" % line)

# (Refactor candidate.)
def output_depends(depdict):
    """Given a dictionary of (from -> list of targets), generate an appropriate
    output file."""
    # Output the dependencies.
    write = sys.stdout.write
    for (from_root, from_), tolist in sorted(depdict.iteritems(),
                                             key=itemgetter(0)):
        for to_root, to_ in sorted(tolist):
            write(repr( ((from_root, from_), (to_root, to_)) ))
            write('\n')

def apply_cluster(cdirs, root, fn):
    "If a cluster exists in 'cdirs' for the root/fn filename, reduce the filename."
    if root is None:
        return root, fn

    for cfn in cdirs:
        if fn.startswith(cfn):
            return root, cfn
    else:
        return root, fn  # no change.

def read_clusters(fn):
    "Return a list of cluster prefixes read from the file 'fn'."
    f = open(fn)
    clusters = []
    for x in imap(str.strip, f.xreadlines()):
        if not x:
            continue
        clusters.append(x)
    return clusters

def main():
    import optparse
    parser = optparse.OptionParser(__doc__.strip())

    parser.add_option('-f', '--from-file', action='store',
                      help="Read cluster list from the given filename.")

    opts, clusters = parser.parse_args()

    if opts.from_file:
        clusters.extend(read_clusters(opts.from_file))

    depends = read_depends(sys.stdin)

    clusfiles = defaultdict(set)
    for (froot, f), (troot, t) in depends:
        cfrom = apply_cluster(clusters, froot, f)
        cto = apply_cluster(clusters, troot, t)

        # Skip self-dependencies that may occur.
        if cfrom == cto:
            cto = (None, None)

        clusfiles[cfrom].add(cto)

    output_depends(clusfiles)


if __name__ == '__main__':
    main()
