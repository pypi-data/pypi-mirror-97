# -*- coding: UTF-8 -*-
"""Codecs extension module.

"""
from __future__ import print_function
from ast import literal_eval
from six import binary_type, text_type

from .__common__ import *
from .__info__ import __author__, __copyright__, __email__, __license__, __source__, __version__


__all__ = ["add", "add_map", "clear", "decode", "encode", "guess", "lookup",  "open", "register", "remove", "reset"]

decode   = codecs.decode
encode   = codecs.encode
guess    = codecs.guess
lookup   = codecs.lookup
open     = codecs.open

list = list_encodings  # not included in __all__ because of shadow name


reset()


def __literal_eval(o):
    """ Non-failing ast.literal_eval alias function. """
    try:
        return literal_eval(str(o))
    except ValueError:
        return literal_eval("'" + str(o) + "'")


def __stdin_pipe():
    """ Stdin pipe read function. """
    try:
        with open(0, 'rb') as f:
            for l in f:
                yield l
    except TypeError:
        import sys
        for l in sys.stdin:
            yield l


def main():
    import argparse, os
    descr = "Codecs Extension (CodExt) {}\n\nAuthor   : {} ({})\nCopyright: {}\nLicense  : {}\nSource   : {}\n" \
            "\nThis tool allows to encode/decode input strings/files with an extended set of codecs.\n\n" \
            .format(__version__, __author__, __email__, __copyright__, __license__, __source__)
    examples = "usage examples:\n- " + "\n- ".join([
        "codext search bitcoin",
        "codext decode base32 -i file.b32",
        "codext encode morse < to_be_encoded.txt",
        "echo \"test\" | codext encode base100",
        "echo -en \"test\" | codext encode braille -o test.braille",
        "codext encode base64 < to_be_encoded.txt > text.b64",
        "echo -en \"test\" | codext encode base64 | codext encode base32",
        "echo -en \"mrdvm6teie6t2cq=\" | codext encode upper | codext decode base32 | codext decode base64",
        "echo -en \"test\" | codext encode upper reverse base32 | codext decode base32 reverse lower",
        "echo -en \"test\" | codext encode upper reverse base32 base64 morse",
        "echo -en \"test\" | codext encode base64 gzip | codext guess",
        "echo -en \"test\" | codext encode base64 gzip | codext guess gzip -c base",
    ])
    parser = argparse.ArgumentParser(description=descr, epilog=examples, formatter_class=argparse.RawTextHelpFormatter)
    sparsers = parser.add_subparsers(dest="command", help="command to be executed")
    parser.add_argument("-i", "--input-file", dest="infile", help="input file (if none, take stdin as input)")
    parser.add_argument("-o", "--output-file", dest="outfile", help="output file (if none, display result to stdout)")
    parser.add_argument("-s", "--strip-newlines", action="store_true", dest="strip",
                        help="strip newlines from input (default: False)")
    encode = sparsers.add_parser("encode", help="encode input using the specified codecs")
    encode.add_argument("encoding", nargs="+", help="list of encodings to apply")
    encode.add_argument("-e", "--errors", default="strict", choices=["ignore", "leave", "replace", "strict"],
                        help="error handling (default: strict)")
    decode = sparsers.add_parser("decode", help="decode input using the specified codecs")
    decode.add_argument("encoding", nargs="+", help="list of encodings to apply")
    decode.add_argument("-e", "--errors", default="strict", choices=["ignore", "leave", "replace", "strict"],
                        help="error handling (default: strict)")
    guess = sparsers.add_parser("guess", help="try guessing the decoding codecs")
    guess.add_argument("encoding", nargs="*", help="list of known encodings to apply (default: none)")
    guess.add_argument("-c", "--codec-categories", help="codec categories to be included in the search ; "
                       "format: string|tuple|list(strings|tuples)")
    guess.add_argument("-d", "--depth", default=5, type=int, help="maximum codec search depth (default: 3)")
    guess.add_argument("-e", "--exclude-codecs", help="codecs to be explicitely not used ; "
                       "format: string|tuple|list(strings|tuples)")
    guess.add_argument("-f", "--stop-function", default="test", help="result checking function (default: text) ; "
                       "format: printables|text|flag|lang_[bigram]|[regex]")
    guess.add_argument("--extended", action="store_true",
                       help="while using the scoring heuristic, also consider null scores (default: False)")
    guess.add_argument("--heuristic", action="store_true",
                       help="use a scoring heuristic to accelerate guessing (default: False)")
    guess.add_argument("-s", "--do-not-stop", action="store_true",
                       help="do not stop if a valid output is found (default: False)")
    guess.add_argument("-v", "--verbose", action="store_true",
                       help="show guessing information and steps (default: False)")
    search = sparsers.add_parser("search", help="search for codecs")
    search.add_argument("pattern", nargs="+", help="encoding pattern to search")
    args = parser.parse_args()
    # if a search pattern is given, only handle it
    if args.command == "search":
        results = []
        for enc in args.pattern:
            results.extend(codecs.search(enc))
        print(", ".join(results) or "No encoding found")
        return
    # handle input file or stdin
    if args.infile:
        with open(args.infile, 'rb') as f:
            c = f.read()
    else:
        c = b("")
        for line in __stdin_pipe():
            c += line
    if args.strip:
        c = re.sub(r"\r?\n", "", c)
    if args.command in ["decode", "encode"]:
        # encode or decode
        for encoding in args.encoding:
            c = getattr(codecs, ["encode", "decode"][args.command == "decode"])(c, encoding, args.errors)
        # handle output file or stdout
        if args.outfile:
            with open(args.outfile, 'wb') as f:
                f.write(c)
        else:
            print(ensure_str(c or "Could not decode :-("), end="")
    elif args.command == "guess":
        sfunc = getattr(stopfunc, args.stop_function, args.stop_function)
        r = {}
        try:
            codecs.guess(c, sfunc, args.depth, __literal_eval(args.codec_categories),
                         __literal_eval(args.exclude_codecs), r, args.encoding, not args.do_not_stop, True,
                         args.heuristic, args.extended, args.verbose)
        except KeyboardInterrupt:
            pass
        for i, o in enumerate(r.items()):
            e, out = o
            if len(e) > 0:
                if args.outfile:
                    n, ext = os.path.splitext(args.outfile)
                    fn = args.outfile if len(r) == 1 else "%s-%d%s" % (n, i+1, ext)
                else:
                    print("Codecs: %s" % ", ".join(e))
                    print(ensure_str(out))
        if len(r) == 0:
            print("Could not decode :-(")

