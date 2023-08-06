# -*- coding: UTF-8 -*-
import _codecs
import codecs
import os
import random
import re
import sys
from encodings.aliases import aliases
from functools import reduce, wraps
from importlib import import_module
from inspect import currentframe
from itertools import chain, product
from math import log
from six import binary_type, string_types, text_type, BytesIO
from string import *
from types import FunctionType, ModuleType
try: # Python3
    from importlib import reload
except ImportError:
    pass
try:  # Python3
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
try:                 # Python 2
    from string import maketrans
except ImportError:  # Python 3
    maketrans = str.maketrans


__all__ = ["add", "add_map", "b", "clear", "codecs", "decode", "encode", "ensure_str", "examples", "guess",
           "generate_strings_from_regex", "get_alphabet_from_mask", "handle_error", "list_categories", "list_encodings",
           "lookup", "maketrans", "re", "register", "remove", "reset", "s2i", "search", "stopfunc", "BytesIO", "MASKS",
           "PY3"]
CODECS_REGISTRY = None
MASKS = {
    'a': printable,
    'b': "".join(chr(i) for i in range(256)),
    'd': digits,
    'h': digits + "abcdef",
    'H': digits + "ABCDEF",
    'l': ascii_lowercase,
    'p': punctuation,
    's': " ",
    'u': ascii_uppercase,
}
PY3 = sys.version[0] == "3"
__codecs_registry = []


entropy = lambda s: -sum([p * log(p, 2) for p in [float(s.count(c)) / len(s) for c in set(s)]])

isb = lambda s: isinstance(s, binary_type)
iss = lambda s: isinstance(s, string_types)
fix = lambda x, ref: b(x) if isb(ref) else ensure_str(x) if iss(ref) else x

s2i = lambda s: int(codecs.encode(s, "base16"), 16)


def add(ename, encode=None, decode=None, pattern=None, text=True, add_to_codecs=False, **kwargs):
    """ This adds a new codec to the codecs module setting its encode and/or decode functions, eventually dynamically
         naming the encoding with a pattern and with file handling.
    
    :param ename:         encoding name
    :param encode:        encoding function or None
    :param decode:        decoding function or None
    :param pattern:       pattern for dynamically naming the encoding
    :param text:          specify whether the codec is a text encoding
    :param add_to_codecs: also add the search function to the native registry
                           NB: this will make the codec available in the built-in open(...) but will make it impossible
                                to remove the codec later
    """
    if encode and not isinstance(encode, FunctionType):
        raise ValueError("Bad 'encode' function")
    if decode and not isinstance(decode, FunctionType):
        raise ValueError("Bad 'decode' function")
    if not encode and not decode:
        raise ValueError("At least one en/decoding function must be defined")
    glob = currentframe().f_back.f_globals
    # search function for the new encoding
    def getregentry(encoding):
        if encoding != ename and not (pattern and re.match(pattern, encoding)):
            return
        fenc, fdec, name = encode, decode, encoding
        # prepare CodecInfo input arguments
        if pattern:
            m = re.match(pattern, encoding)
            try:
                g = m.group(1) or ""
                if g.isdigit():
                    g = int(g)
                fenc = fenc(g) if fenc else fenc
                fdec = fdec(g) if fdec else fdec
            except AttributeError:
                # this occurs when m is None or there is an error in fenc(g) or fdec(g), meaning no match
                if m is not None:
                    raise
                return
            except IndexError:
                # this occurs while m is not None, but possibly no capture group that gives at least 1 group index ; in
                #  this case, if fenc/fdec is a decorated function, execute it with no arg
                if fenc and len(getfullargspec(fenc).args) == 1:
                    fenc = fenc()
                if fdec and len(getfullargspec(fdec).args) == 1:
                    fdec = fdec()
        if fenc:
            fenc = fix_inout_formats(fenc)
        if fdec:
            fdec = fix_inout_formats(fdec)
        
        class Codec(codecs.Codec):
            def encode(self, input, errors="strict"):
                if fenc is None:
                    raise NotImplementedError
                return fenc(input, errors)
            
            def decode(self, input, errors="strict"):
                if fdec is None:
                    raise NotImplementedError
                return fdec(input, errors)
        
        class IncrementalEncoder(codecs.IncrementalEncoder):
            def encode(self, input, final=False):
                if fenc is None:
                    raise NotImplementedError
                return b(fenc(input, self.errors)[0])
        
        class IncrementalDecoder(codecs.IncrementalDecoder):
            def decode(self, input, final=False):
                if fdec is None:
                    raise NotImplementedError
                return ensure_str(fdec(input, self.errors)[0])
        
        class StreamWriter(Codec, codecs.StreamWriter):
            charbuffertype = bytes
        
        class StreamReader(Codec, codecs.StreamReader):
            charbuffertype = bytes
        
        ci = codecs.CodecInfo(
            name=name,
            encode=Codec().encode,
            decode=Codec().decode,
            incrementalencoder=IncrementalEncoder,
            incrementaldecoder=IncrementalDecoder,
            streamwriter=StreamWriter,
            streamreader=StreamReader,
            _is_text_encoding=text,
        )
        ci.parameters = kwargs
        ci.parameters['name'] = ename
        ci.parameters['add_to_codecs'] = add_to_codecs
        ci.parameters['pattern'] = pattern
        ci.parameters['text'] = text
        f = glob.get('__file__', os.path.join("custom", "_"))
        ci.parameters['category'] = kwargs.get('category', f.split(os.path.sep)[-2].rstrip("s"))
        ci.parameters['examples'] = kwargs.get('examples', glob.get('__examples__'))
        ci.parameters['guess'] = kwargs.get('guess', glob.get('__guess__', [ename]))
        ci.parameters['module'] = kwargs.get('module', glob.get('__name__'))
        ci.parameters.setdefault("scoring", {})
        for attr in ["entropy", "len_charset", "printables_rate", "padding_char"]:
            a = kwargs.get(attr)
            if a is not None:
                ci.parameters['scoring'][attr] = a
        return ci
    
    getregentry.__name__ = re.sub(r"[\s\-]", "_", ename)
    getregentry.__pattern__ = pattern
    register(getregentry, add_to_codecs)


def add_map(ename, encmap, repl_char="?", sep="", ignore_case=None, no_error=False, intype=None, outype=None, **kwargs):
    """ This adds a new mapping codec (that is, declarable with a simple character mapping dictionary) to the codecs
         module dynamically setting its encode and/or decode functions, eventually dynamically naming the encoding with
         a pattern and with file handling (if text is True).
    
    :param ename:         encoding name
    :param encmap:        characters encoding map ; can be a dictionary of encoding maps (for use with the first capture
                           group of the regex pattern) or a function building the encoding map
    :param repl_char:     replacement char (used when errors handling is set to "replace")
    :param sep:           string of possible character separators (hence, only single-char separators are considered) ;
                           - while encoding, the first separator is used
                           - while decoding, separators can be mixed in the input text
    :param ignore_case:   ignore text case while encoding and/or decoding
    :param no_error:      this encoding triggers no error (hence, always in "leave" errors handling)
    :param intype:        specify the input type for pre-transforming the input text
    :param outype:        specify the output type for post-transforming the output text
    :param pattern:       pattern for dynamically naming the encoding
    :param text:          specify whether the codec is a text encoding
    :param add_to_codecs: also add the search function to the native registry
                           NB: this will make the codec available in the built-in open(...) but will make it impossible
                                to remove the codec later
    """
    outype = outype or intype
    if ignore_case not in [None, "encode", "decode", "both"]:
        raise ValueError("Bad ignore_case parameter while creating encoding map")
    if intype not in [None, "str", "bin", "ord"]:
        raise ValueError("Bad input type parameter while creating encoding map")
    if outype not in [None, "str", "bin", "ord"]:
        raise ValueError("Bad output type parameter while creating encoding map")
    
    def __generic_code(decode=False):
        def _wrapper(param):
            """ The parameter for wrapping comes from the encoding regex pattern ; e.g.
                 [no pattern]           => param will be None everytime
                 r"barbie[-_]?([1-4])$" => param could be int 1, 2, 3 or 4
                 r"^morse(|[-_]?.{3})$" => param could be None, "-ABC" (for mapping to ".-/")
            
            In order of precedence:
            1. when param is a key in mapdict or mapdict is a list of encoding maps (hence in the case of "barbie...",
                param MUST be an int, otherwise for the first case it could clash with a character of the encoding map)
            2. otherwise handle it as a new encoding character map "ABC" translates to ".-/" for morse
            """
            p = param
            if isinstance(encmap, FunctionType):
                mapdict = encmap(p)
                p = None
            else:
                mapdict = encmap
            if isinstance(mapdict, dict):
                smapdict = {k: v for k, v in mapdict.items()}
            elif isinstance(mapdict, list) and isinstance(mapdict[0], dict):
                smapdict = {k: v for k, v in mapdict[0].items()}
            else:
                raise ValueError("Bad mapping dictionary or list of mapping dictionaries")
            if p is not None:
                # case 1: param is empty string
                if p == "":
                    if isinstance(mapdict, list):
                        smapdict = {k: v for k, v in mapdict[0].items()}
                    elif isinstance(mapdict, dict):
                        if '' in mapdict.keys() and isinstance(mapdict[''], dict):
                            smapdict = {k: v for k, v in mapdict[''].items()}
                        else:
                            smapdict = {k: v for k, v in mapdict.items()}
                    # no 'else' handling a LookupError here ; this case is covered by the first if/elif/else block
                # case 2: list or dictionary or dictionary of numbered encodings
                elif isinstance(p, int):
                    # if mapdict is a list, we shall align the parameter (starting from 1) as an index (starting from 0)
                    if isinstance(mapdict, list):
                        p -= 1
                    if isinstance(mapdict, list) and 0 <= p < len(mapdict) or \
                       isinstance(mapdict, dict) and p in mapdict.keys():
                        smapdict = {k: v for k, v in mapdict[p].items()}
                    else:
                        raise LookupError("Bad parameter for encoding '{}': '{}'".format(ename, p))
                # case 3: dictionary of regex-selected encoding mappings
                elif isinstance(mapdict, dict) and isinstance(list(mapdict.values())[0], dict):
                    tmp = None
                    for r, d in mapdict.items():
                        if r == '':   # this is already handled in case 1 ; anyway, an empty regex always matches, hence
                            continue  #  it must be excluded
                        if re.match(r, p):
                            tmp = d
                            break
                    if tmp is None:
                        raise LookupError("Bad parameter for encoding '{}': '{}'".format(ename, p))
                    smapdict = tmp
                # case 4: encoding characters translation
                else:
                    # collect base tokens in order of appearance in the mapping dictionary
                    base_tokens = ""
                    for _, c in sorted(mapdict.items()):
                        for t in c:
                            for st in t:
                                if st not in base_tokens:
                                    base_tokens += st
                    if " " not in sep:
                        base_tokens = base_tokens.replace(" ", "")
                    if len(p) > 0 and p[0] in "-_" and len(p[1:]) == len(set(p[1:])) == len(base_tokens):
                        p = p[1:]
                    if len(p) == len(set(p)) == len(base_tokens):
                        t = maketrans(base_tokens, p)
                        for k, v in smapdict.items():
                            smapdict[k] = [x.translate(t) for x in v] if isinstance(v, list) else v.translate(t)
                    else:
                        raise LookupError("Bad parameter for encoding '{}': '{}'".format(ename, p))
            if ignore_case is not None:
                cases = ["upper", "lower"]
                case_d = cases[any(c in str(list(smapdict.values())) for c in "abcdefghijklmnopqrstuvwxyz")]
                case_e = cases[any(c in str(list(smapdict.keys())) for c in "abcdefghijklmnopqrstuvwxyz")]
                i = ignore_case
                smapdict = {getattr(k, case_e)() if i in ["both", "encode"] else k: \
                            ([getattr(x, case_d)() for x in v] if isinstance(v, list) else getattr(v, case_d)()) \
                                if i in ["both", "decode"] else v for k, v in smapdict.items()}
            if decode:
                tmp = {}
                # this has a meaning for encoding maps that could have clashes in encoded chars (e.g. Bacon's cipher ;
                #  I => abaaa but also J => abaaa, with the following, we keep I instead of letting J overwrite it)
                for k, v in sorted(smapdict.items()):
                    if not isinstance(v, list):
                        v = [v]
                    for x in v:
                        if x not in tmp.keys():
                            tmp[x] = k
                smapdict = tmp
            # this allows to avoid an error with Python2 in the "for i, c in enumerate(parts)" loop
            if '' not in smapdict.keys():
                smapdict[''] = ""
            # determine token and result lengths
            tmaxlen = max(map(len, smapdict.keys()))
            tminlen = max(1, min(map(len, set(smapdict.keys()) - {''})))
            l = []
            for x in smapdict.values():
                getattr(l, ["append", "extend"][isinstance(x, list)])(x)
            rminlen = max(1, min(map(len, set(l) - {''})))
            
            # generic encoding/decoding function for map encodings
            def code(text, errors="strict"):
                icase = ignore_case == "both" or \
                        decode and ignore_case == "decode" or \
                        not decode and ignore_case == "encode"
                if icase:
                    case = case_d if decode else case_e
                if no_error:
                    errors = "leave"
                text = ensure_str(text)
                if not decode:
                    if intype == "bin":
                        text = "".join("{:0>8}".format(bin(ord(c))[2:]) for c in text)
                    elif intype == "ord":
                        text = "".join(str(ord(c)).zfill(3) for c in text)
                r = ""
                lsep = "" if decode else sep if len(sep) <= 1 else sep[0]
                error_func = handle_error(ename, errors, lsep, repl_char, rminlen, decode)
                
                # get the value from the mapping dictionary, trying the token with its inverted case if relevant
                def __get_value(token, position, case_changed=False):
                    try:
                        result = smapdict[token]
                    except KeyError:
                        if icase and not case_changed:
                            token_inv_case = getattr(token, case)()
                            return __get_value(token_inv_case, position, True)
                        return error_func(token, position)
                    if isinstance(result, list):
                        result = random.choice(result)
                    return result + lsep
                
                # if a separator is defined, rely on it by splitting the input text
                if decode and len(sep) > 0:
                    for i, c in enumerate(re.split("[" + sep + "]", text)):
                        r += __get_value(c, i)
                # otherwise, move through the text using a cursor for tokenizing it ; this allows defining more complex
                #  encodings with variable token lengths
                else:
                    cursor, bad = 0, ""
                    while cursor < len(text):
                        token = text[cursor:cursor+1]
                        for l in range(tminlen, tmaxlen + 1):
                            token = text[cursor:cursor+l]
                            if token in smapdict.keys() or icase and getattr(token, case)() in smapdict.keys():
                                r += __get_value(token, cursor)
                                cursor += l
                                break
                        else:
                            # collect bad chars and only move the cursor one char to the right
                            bad += text[cursor]
                            cursor += 1
                            # if the number of bad chars is the minimum token length, consume it and start a new buffer
                            if len(bad) == tminlen or errors == "leave":
                                posn = cursor - len(bad)
                                r += error_func(bad, posn)
                                bad = ""
                if decode:
                    if outype in ["bin", "ord"]:
                        tmp, r = "", r.replace(lsep, "")
                        step = [3, 8][outype == "bin"]
                        for i in range(0, len(r), step):
                            s = r[i:i+step]
                            try:
                                tmp += chr(int(s, 2) if outype == "bin" else int(s))
                            except ValueError:
                                if len(s) > 0:
                                    tmp += "[" + s + "]"
                        r = tmp + lsep
                return r[:len(r)-len(lsep)], len(b(text))
            return code
        if re.search(r"\([^(?:)]", kwargs.get('pattern', "")) is None:
            # in this case, there is no capturing group for parametrization
            return _wrapper(None)
        return _wrapper

    glob = currentframe().f_back.f_globals
    kwargs['category'] = glob['__file__'].split(os.path.sep)[-2].rstrip("s")
    kwargs['examples'] = kwargs.get('examples', glob.get('__examples__'))
    kwargs['encmap'] = encmap
    kwargs['repl_char'] = repl_char
    kwargs['sep'] = sep
    kwargs['ignore_case'] = ignore_case
    kwargs['no_error'] = no_error
    kwargs['intype'] = intype
    kwargs['outype'] = outype
    kwargs['module'] = glob.get('__name__')
    try:
        if isinstance(encmap, dict):
            smapdict = {k: v for k, v in encmap.items()}
        elif isinstance(encmap, list) and isinstance(encmap[0], dict):
            smapdict = {k: v for k, v in encmap[0].items()}
        kwargs['repl_minlen'] = i = max(1, min(map(len, set(smapdict.values()) - {''})))
        kwargs['repl_minlen_b'] = max(1, min(map(len, map(b, set(smapdict.values()) - {''}))))
    except:
        pass
    add(ename, __generic_code(), __generic_code(True), **kwargs)
codecs.add_map = add_map


def clear():
    """ Clear codext's local registry of search functions. """
    global __codecs_registry
    __codecs_registry = []
codecs.clear = clear


def examples(encoding, number=10):
    """ Use the search function to get the matching encodings and provide examples of valid encoding names. """
    e = []
    for name in search(encoding):
        for search_function in __codecs_registry:
            n = search_function.__name__
            if name in [n, n.replace("_", "-")]:
                temp = []
                for s in generate_strings_from_regex(search_function.__pattern__, yield_max=16*number):
                    temp.append(s)
                random.shuffle(temp)
                i = 0
                while i < min(number, len(temp)):
                    if not temp[i].isdigit():
                        e.append(temp[i])
                    i += 1
        for alias, codec in aliases.items():
            if name == codec:
                if codec not in e:
                    e.append(codec)
                if not alias.isdigit():
                    e.append(alias)
    random.shuffle(e)
    return sorted([e[i] for i in range(min(number, len(e)))], key=_human_keys)
codecs.examples = examples


def list_categories():
    """ Get a list of all codec categories. """
    c = ["native"]
    root = os.path.dirname(__file__)
    for d in os.listdir(root):
        if os.path.isdir(os.path.join(root, d)) and not d.startswith("__"):
            c.append(d.rstrip("s"))
    # particular category, hardcoded from base/_base.py
    c += ["base-generic"]
    return c


def list_encodings(*categories):
    """ Get a list of all codecs. """
    # first, determine the list of valid categories
    valid_categories = list_categories()
    # then, if "non-native" is in the input list, extend the list with the whole categories but "native"
    categories = list(categories)
    for c in categories[:]:
        if c == "non-native":
            for c in valid_categories:
                if c == "native" or c in categories:
                    continue
                categories.append(c)
            categories.remove("non-native")
            break
    # now, filter codecs according to the input list of categories
    enc = []
    if len(categories) == 0 or "native" in categories:
        for a in set(aliases.values()):
            try:
                __orig_lookup(a)
            except LookupError:
                continue
            enc.append(a)
    for search_function in __codecs_registry:
        name = search_function.__name__.replace("_", "-")
        p = search_function.__pattern__
        if p is None:
            ci = search_function(name)
        else:
            ci = search_function(generate_string_from_regex(p))
        c = "other" if ci is None else ci.parameters['category']
        if len(categories) == 0 or c in categories:
            enc.append(name)
    for category in categories:
        if category not in valid_categories:
            raise ValueError("Category '%s' does not exist" % category)
    return sorted(list(set(enc)), key=_human_keys)


def remove(encoding):
    """ Remove all search functions matching the input encoding name from codext's local registry. """
    tbr = []
    for search_function in __codecs_registry:
        if search_function(encoding) is not None:
            tbr.append(search_function)
    for search_function in tbr:
        __codecs_registry.remove(search_function)
codecs.remove = remove


def reset():
    """ Reset codext's local registry of search functions. """
    global CODECS_REGISTRY, __codecs_registry
    clear()
    d = os.path.dirname(__file__)
    for pkg in sorted(os.listdir(d)):
        if pkg.startswith("_") or not os.path.isdir(os.path.join(d, pkg)):
            continue
        reload(import_module("codext." + pkg))
    # backup codext's registry
    if CODECS_REGISTRY is None:
        CODECS_REGISTRY = __codecs_registry[:]
    # restore codext's registry
    else:
        __codecs_registry = CODECS_REGISTRY[:]
codecs.reset = reset


# conversion functions
def b(s):
    """ Non-crashing bytes conversion function. """
    if PY3:
        try:
            return s.encode("latin-1")
        except:
            pass
        try:
            return s.encode("utf-8")
        except:
            pass
    return s


def ensure_str(s, encoding='utf-8', errors='strict'):
    """ Similar to six.ensure_str. Adapted here to avoid messing up with six version errors. """
    if not PY3 and isinstance(s, text_type):
        return s.encode(encoding, errors)
    elif PY3 and isinstance(s, binary_type):
        try:
            return s.decode(encoding, errors)
        except:
            return s.decode("latin-1")
    return s


# make conversion functions compatible with input/output strings/bytes
def fix_inout_formats(f):
    """ This decorator ensures that the first output of f will have the same text format as the first input (str or
         bytes). """
    @wraps(f)
    def _wrapper(*args, **kwargs):
        a0 = args[0]
        a0_isb = isb(a0)
        a0 = ensure_str(a0) if iss(a0) or a0_isb else a0
        r = f(a0, *args[1:], **kwargs)
        # special case: input is in bytes ; ensure that the returned length is this of the bytes, not this processed by
        #                the decode/encode function
        if isinstance(r, (tuple, list)) and isinstance(r[1], int) and a0_isb:
            r = tuple([list(r)[0]] + [len(args[0])] + list(r)[2:])
        return (fix(r[0], args[0]), ) + r[1:] if isinstance(r, (tuple, list)) else fix(r, args[0])
    return _wrapper


# alphabet generation function from a given mask
def get_alphabet_from_mask(mask):
    """ This function generates an alphabet from the given mask. The style used is similar to Hashcat ; group keys are
         marked with a heading "?". """
    i, alphabet = 0, ""
    while i < len(mask):
        c = mask[i]
        if c == "?" and i < len(mask) - 1 and mask[i+1] in MASKS.keys():
            for c in MASKS[mask[i+1]]:
                if c not in alphabet:
                    alphabet += c
            i += 1
        elif c not in alphabet:
            alphabet += c
        i += 1
    return alphabet


# generic error handling function
def handle_error(ename, errors, sep="", repl_char="?", repl_minlen=1, decode=False, item="position"):
    """ This shortcut function allows to handle error modes given some tuning parameters.
    
    :param ename:       encoding name
    :param errors:      error handling mode
    :param sep:         token separator
    :param repl_char:   replacement character (for use when errors="replace")
    :param repl_minlen: repeat number for the replacement character
    :param decode:      whether we are encoding or decoding
    :param item:        position item description (for describing the error ; e.g. "group" or "token")
    """
    name = "".join(t.capitalize() for t in re.split(r"[-_+]", ename))
    # dynamically make dedicated exception classes bound to the related codec module
    exc = "%s%scodeError" % (name, ["En", "De"][decode])
    glob = {'__name__': "__main__"}
    exec("class %s(ValueError): pass" % exc, glob)
    
    def _handle_error(token, position):
        """ This handles an encoding/decoding error according to the selected handling mode.
        
        :param token:    input token to be encoded/decoded
        :param position: token position index
        """
        if errors == "strict":
            msg = "'{}' codec can't {}code character '{}' in {} {}"
            raise glob[exc](msg.format(ename, ["en", "de"][decode], token, item, position))
        elif errors == "leave":
            return token + sep
        elif errors == "replace":
            return repl_char * repl_minlen + sep
        elif errors == "ignore":
            return ""
        else:
            raise ValueError("Unsupported error handling '{}'".format(errors))
    return _handle_error


# codecs module hooks
__orig_lookup   = _codecs.lookup
__orig_register = _codecs.register


def __add(ename, encode=None, decode=None, pattern=None, text=True, add_to_codecs=True):
    add(ename, encode, decode, pattern, text, add_to_codecs)
__add.__doc__ = add.__doc__
codecs.add = __add


def decode(obj, encoding='utf-8', errors='strict'):
    """ Custom decode function relying on the hooked lookup function. """
    return lookup(encoding).decode(obj, errors)[0]
codecs.decode = decode


def encode(obj, encoding='utf-8', errors='strict'):
    """ Custom encode function relying on the hooked lookup function. """
    return lookup(encoding).encode(obj, errors)[0]
codecs.encode = encode


def lookup(encoding):
    """ Hooked lookup function for searching first for codecs in the local registry of this module. """
    # first, try to match the given encoding with codecs' search functions
    for search_function in __codecs_registry:
        codecinfo = search_function(encoding)
        if codecinfo is not None:
            return codecinfo
    # then, if a codec name was given, generate an encoding name from its pattern and get the CodecInfo
    for search_function in __codecs_registry:
        if search_function.__name__.replace("_", "-") == encoding:
            codecinfo = search_function(generate_string_from_regex(search_function.__pattern__))
            if codecinfo is not None:
                return codecinfo
    # finally, get a CodecInfo with the original lookup function and refine it with a dictionary of parameters
    ci = __orig_lookup(encoding)
    ci.parameters = {'category': "native", 'module': "codecs", 'name': aliases.get(ci.name, ci.name)}
    return ci
codecs.lookup = lookup


def register(search_function, add_to_codecs=False):
    """ Register function for registering new codecs in the local registry of this module and, if required, in the
         native codecs registry (for use with the built-in 'open' function).
    
    :param search_function: search function for the codecs registry
    :param add_to_codecs:   also add the search function to the native registry
                            NB: this will make the codec available in the built-in open(...) but will make it impossible
                                 to remove the codec later
    """
    if search_function not in __codecs_registry:
        __codecs_registry.append(search_function)
    if add_to_codecs:
        __orig_register(search_function)


def __register(search_function, add_to_codecs=True):
    """ Same as register(...), but with add_to_codecs set by default to True. """
    register(search_function, add_to_codecs)
codecs.register = __register


def search(encoding_regex):
    """ Function similar to lookup but allows to search for an encoding based on a regex instead. It searches this way
         into the local registry but also tries a simple lookup with the original lookup function. """
    matches = []
    for search_function in __codecs_registry:
        n = search_function.__name__
        for name in [n, n.replace("_", "-")]:
            if re.search(encoding_regex, name):
                matches.append(name)
                continue
        # in some cases, encoding_regex can match a generated string that uses a particular portion of its generating
        #  pattern ; e.g. we expect encoding_regex="uu_" to find "uu" and "uu_codec" while it can also find "morse" or
        #  "atbash" very rarely because of their dynamic patterns and the limited number of randomly generated strings
        # so, we can use a qualified majority voting to ensure we do not get a "junk" encoding in the list of matches ;
        #  executing 5 times the string generation for a given codec but adding the codec to the list of matches only
        #  if we get at least 3 matches ensures that we consider up to 2 failures that could be stochastic, therefore
        #  drastically decreasing the probability to get a "junk" encoding in the matches list
        c = 0
        for i in range(5):
            for s in generate_strings_from_regex(search_function.__pattern__):
                if re.search(encoding_regex, s):
                    c += 1
                    break
            if c >= 3:
                matches.append(n)
                break
    for s, n in aliases.items():
        if re.search(encoding_regex, s) or re.search(encoding_regex, n):
            matches.append(n)
            break
    return sorted(list(set(matches)), key=_human_keys)
codecs.search = search


# utility function for the search feature
CATEGORIES = {
    'digit':     digits,
    'not_digit': reduce(lambda x, c: x.replace(c, ""), digits, printable),
    'space':     whitespace,
    'not_space': reduce(lambda x, c: x.replace(c, ""), whitespace, printable),
    'word':      ascii_letters + digits + '_',
    'not_word':  reduce(lambda x, c: x.replace(c, ""), ascii_letters + digits + '_', printable),
}
REPEAT_MAX    = 10
STAR_PLUS_MAX = 10
YIELD_MAX     = 100


def __gen_str_from_re(regex, star_plus_max, repeat_max, yield_max, parsed=False):
    """ Recursive function to generate strings from a regex pattern. """
    if regex is None:
        return
    __groups = {}
    tokens = []
    negate = False
    for state in (regex if parsed else re.sre_parse.parse(b(getattr(regex, "pattern", regex)))):
        code = getattr(state[0], "name", state[0]).lower()
        value = getattr(state[1], "name", state[1])
        value = value.lower() if isinstance(value, str) else value
        if code in ["assert_not", "at"]:
            continue
        elif code == "any":
            tokens.append(printable.replace("\n", ""))  # should be ord(x) with x belongs to [0, 256[
        elif code == "assert":
            tokens.append(list(__gen_str_from_re(value[1], star_plus_max, repeat_max, yield_max, True)))
        elif code == "branch":
            result = []
            for r in value[1]:
                result += list(__gen_str_from_re(r, star_plus_max, repeat_max, yield_max, True)) or [""]
            tokens.append(result)
        elif code == "category":
            charset = CATEGORIES[value[9:]]
            if negate:
                negate = False
                charset = list(set(printable).difference(charset))
            tokens.append(charset)
        elif code == "groupref":
            tokens.extend(__groups[value])
        elif code == "in":
            subtokens = list(__gen_str_from_re(value, star_plus_max, repeat_max, yield_max, True))
            subtokens = [x for l in subtokens for x in l]
            tokens.append(subtokens)
        elif code == "literal":
            tokens.append(chr(value))
        elif code in ["max_repeat", "min_repeat"]:
            start, end = value[:2]
            end = min(end, star_plus_max)
            start = min(start, end)
            charset = list(__gen_str_from_re(value[-1], star_plus_max, repeat_max, yield_max, True))
            subtokens = []
            if start == 0 and end == 1:
                subtokens.append("")
                subtokens.extend(charset)
            elif len(charset) ** end > repeat_max:
                for i in range(min(repeat_max, 10 * len(charset))):
                    n = random.randint(start, end + 1)
                    token = "" if n == 0 else "".join(random.choice(charset) for i in range(n))
                    if token not in subtokens:
                        subtokens.append(token)
                    else:
                        i -= 1
            else:
                for n in range(start, end + 1):
                    for c in product(charset, repeat=n):
                        subtokens.append("".join(c))
            tokens.append(subtokens)
        elif code == "negate":
            negate = True
        elif code == "not_literal":
            tokens.append(printable.replace(chr(value), ""))
        elif code == "range":
            tokens.append("".join(chr(i) for i in range(value[0], value[1] + 1)))
        elif code == "subpattern":
            result = list(__gen_str_from_re(value[-1], star_plus_max, repeat_max, yield_max, True))
            if value[0]:
                __groups[value[0]] = result
            tokens.append(result)
        else:
            raise NotImplementedError("Unhandled code '{}'".format(code))
    if len(tokens) == 0:
        tokens = [""]
    i = 0
    for result in product(*tokens):
        yield "".join(result)
        i += 1
        if i >= yield_max:
            break


def _human_keys(text):
    """ Sorting function for considering strings with numbers (e.g. base2, base10, base100) """
    tokens = []
    for s in re.split(r"(\d+|\D+)", text):
        tokens.append(int(s) if s.isdigit() else s)
    return tokens


def generate_string_from_regex(regex):
    """ Utility function to generate a single string from a regex pattern. """
    if regex:
        return list(generate_strings_from_regex(regex, yield_max=1))[0]


def generate_strings_from_regex(regex, star_plus_max=STAR_PLUS_MAX, repeat_max=REPEAT_MAX, yield_max=YIELD_MAX):
    """ Utility function to generate strings from a regex pattern. """
    i = 0
    for result in __gen_str_from_re(regex, star_plus_max, repeat_max, yield_max):
        yield result


# guess feature objects
stopfunc = ModuleType("stopfunc", """
    Predefined stop functions
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This submodule contains stop functions for the guess feature of codext.
    
    - `flag`:       searches for the pattern "[Ff][Ll1][Aa4@][Gg9]" (either UTF-8 or UTF-16)
    - `lang_**`:    checks if the given lang (any from the PROFILES_DIRECTORY of the langdetect module) is detected
    - `printables`: checks that every output character is in the set of printables
""")
stopfunc.printables = lambda s: all(c in printable for c in ensure_str(s))
stopfunc.regex      = lambda p: lambda s: re.search(p, ensure_str(s)) is not None
stopfunc.text       = lambda s: stopfunc.printables(s) and entropy(s) < 4.5

try:
    from langdetect import detect, PROFILES_DIRECTORY
    for lang in [p.replace("-", "") for p in os.listdir(PROFILES_DIRECTORY)]:
        setattr(stopfunc, "lang_%s" % lang, lambda s, l=lang: stopfunc.printables(s) and detect(s) == l)
except ImportError:
    pass


__flag = lambda x: re.search(r"[Ff][Ll1][Aa4@][Gg96]", x) is not None
def _flag(x):
    try:
        return __flag(ensure_str(b(x).decode("utf16")))
    except (UnicodeDecodeError, UnicodeEncodeError):
        return __flag(x)
stopfunc.flag = _flag


def __guess(prev_input, input, stop_func, depth, max_depth, codec_categories, exclude, result, found=(), stop=True,
            show=False, scoring_heuristic=False, extended=False, debug=False):
    """ Perform a breadth-first tree search using a ranking logic to select and prune the list of codecs. """
    if depth > 0 and stop_func(input):
        if not stop and show and found not in result:
            s = "[+] %s: %s" % (", ".join(found), ensure_str(input))
            print(s if len(s) <= 80 else s[:77] + "...")
        result[found] = input
    if depth >= max_depth or len(result) > 0 and stop:
        return
    # compute included and excluded codecs for this depth
    def expand(items, descr=None, transform=None):
        items = items or []
        # format 1: when string, take it as the only items at any depth
        if isinstance(items, string_types):
            r = (items, )
        # format 2: when tuple, consider it as a list of items at any depth
        elif isinstance(items, tuple):
            r = items
        # format 3: when list, consider it as the list of tuples of items with the order number corresponding to the
        #            applicable depth
        elif isinstance(items, list):
            try:
                r = items[depth] or ()
                if isinstance(r, string_types):
                    r = (r, )
            except IndexError:
                r = ()
        else:
            raise ValueError("Bad %sformat %s" % (["%s " % descr, ""][descr is None], items))
        return r if transform is None else transform(*r)
    # parse valid encodings, expanding included/excluded codecs
    c, e = expand(codec_categories, "codec_categories", list_encodings), expand(exclude, "exclude")
    for new_input, encoding in __rank(prev_input, input, c, scoring_heuristic, extended):
        if len(result) > 0 and stop:
            return
        if encoding in e:
            continue
        if debug:
            print("[*] Depth %d/%d ; trying %s" % (depth+1, max_depth, encoding))
        __guess(input, new_input, stop_func, depth+1, max_depth, codec_categories, exclude, result,
                found + (encoding, ), stop, show, scoring_heuristic, extended, debug)


def __rank(prev_input, input, codecs, heuristic=False, extended=False):
    """ Filter valid encodings and rank them by relevance. """
    ranking = {}
    for codec in codecs:
        for score, new_input, encoding in __score(prev_input, input, codec, heuristic, extended):
            ranking[encoding] = (score, new_input)
    for encoding, result in sorted(ranking.items(), key=lambda x: -x[1][0]):
        yield result[1], encoding


class _Text(object):
    def __init__(self, text, pad_char=None):
        self.len = len(text)
        self.lcharset = len(set(text))
        self.padding = pad_char is not None and text[-1] in [pad_char, b(pad_char)]
        self.printables = float(len([c for c in text if (chr(c) if isinstance(c, int) else c) in printable])) / self.len
        self.entropy = entropy(text)


def __score(prev_input, input, codec, heuristic=False, extended=False):
    """ Score relevant encodings given an input. """
    obj, ci = None, lookup(codec)  # NB: lookup(...) won't fail as the codec value comes from list_encodings(...)
    for encoding in ci.parameters.get('guess', [codec]):
        # ignore encodings that fail to decode with their default errors handling value
        try:
            new_input = decode(input, encoding)
        except:
            continue
        # ignore encodings that give an output identical to the input (identity transformation) or to the previous input
        if b(input) == b(new_input) or b(prev_input) == b(new_input):
            continue
        # compute input's characteristics only once and only if the control flow reaches this point
        pad = ci.parameters.get('scoring', {}).get('padding_char')
        if obj is None:
            obj = _Text(input, pad)
        if heuristic:
            # from here, the goal (e.g. if the input is Base32) is to rank candidate encodings (e.g. multiple base
            #  codecs) so that we can put the right one as early as possible and eventually exclude bad candidates
            s = .0
            # first, apply a bonus if the length of input text's charset is exactly the same as encoding's charset ;
            #  on the contrary, if the length of input text's charset is strictly greater, give a penalty
            lcs = ci.parameters.get('scoring', {}).get('len_charset', 256)
            if isinstance(lcs, type(lambda: None)):
                lcs = int(lcs(encoding))
            if (pad and obj.padding and lcs + 1 == obj.lcharset) or lcs == obj.lcharset:
                s += .3
            elif (pad and obj.padding and lcs + 1 < obj.lcharset) or lcs < obj.lcharset:
                s -= .2  # this can occur for encodings with no_error set to True
            # then, take padding into account, giving a bonus if padding is to be encountered and effectively present,
            #  or a penalty when it should not be encountered but it is present
            if pad and obj.padding:
                s += .2  # when padding is encountered while it is legitimate, it could be a good indication => bonus
            elif not pad and obj.padding:
                s -= .1  # it could arise a padding character is encountered while not being padding => small penalty
            # give a bonus when the rate of printable characters is greater or equal than expected and a penalty when
            #  lower only for codecs that tolerate errors (otherwise, the printables rate can be biased)
            if not ci.parameters.get('no_error', False):
                pr = ci.parameters.get('scoring', {}).get('printables_rate', 0)
                if isinstance(pr, type(lambda: None)):
                    pr = float(pr(obj.printables))
                if obj.printables - pr <= .05:
                    s += .1
            # afterwards, if the input text has an entropy close to the expected one, give a bonus weighted on the
            #  number of input characters to take bad entropies of shorter strings into account
            entr = ci.parameters.get('entropy', {})
            entr = entr.get(encoding, entr.get('default')) if isinstance(entr, dict) else entr
            if isinstance(entr, type(lambda: None)):
                try:  # this case allows to consider the current encoding name from the current codec
                    entr = entr(obj.entropy, encoding)
                except TypeError:
                    entr = entr(obj.entropy)
            if entr is not None:
                # use a quadratic heuristic to compute a weight for the entropy delta, aligned on (100w,.1) and (200w,1)
                d_entr = min(4e-05 * obj.len**2 - .003 * obj.len, 1) * abs(entr - obj.entropy)
                if d_entr <= .5:
                    s += .5 - d_entr
            # finally, if relevant, apply a custom bonus (e.g. when a regex pattern is matched)
            bonus = ci.parameters.get('scoring', {}).get('bonus_func')
            if bonus is not None:
                if isinstance(bon, type(lambda: None)):
                    bonus = bonus(obj, ci, encoding)
                if bonus:
                    s += .2
        else:
            s = 1.
        # exclude negative (and eventually null) scores as they are (hopefully) not relevant
        if extended and s >= .0 or not extended and s > .0:
            yield s, new_input, encoding


def guess(input, stop_func=stopfunc.printables, max_depth=5, codec_categories=None, exclude=None, result=None, found=(),
          stop=True, show=False, scoring_heuristic=False, extended=False, debug=False):
    """ Try decoding without the knowledge of the encoding(s). """
    if max_depth <= 0:
        raise ValueError("Depth must be a non-null positive integer")
    if len(found) > 0:
        for encoding in found:
            input = decode(input, encoding)
    if isinstance(stop_func, string_types):
        stop_func = stopfunc.regex(stop_func)
    if len(input) > 0:
        result = result or {}
        # breadth-first search
        for d in range(max_depth):
            __guess("", input, stop_func, 0, d+1, codec_categories, exclude, result, tuple(found), stop, show,
                    scoring_heuristic, extended, debug)
            if stop and len(result) > 0:
                return result
    return result
codecs.guess = guess

