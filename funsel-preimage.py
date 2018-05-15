#!/usr/bin/env python
# mutatis mutandis

import argparse
import itertools
from os.path import basename

import web3

ARGTYPES = ['uint256', 'uint128', 'uint64', 'uint32', 'uint16', 'uint8',
            'int256', 'int128', 'int64', 'int32', 'int16', 'int8',
            'bytes32', 'bytes16','bytes8', 'bytes4', 'bytes1', 'bytes',
            'bool', 'string']

def load_dictionary(filename: str) -> list:
    with open(conf.dictfile) as fd:
        words = fd.readlines()
    words = [word.strip() for word in words]

    return words

def run(conf):
    # words' list for function name body
    words = load_dictionary(conf.dictfile)
    # TODO: allow "rotating" the word list, so generator starts with different letter
    # words = rotate_list(words, startletter=conf.startletter)
    # used in print()
    filenameshort = basename(conf.dictfile)[:8]
    targetshort = conf.target[:-2]

    for nwords in range(conf.minwords, conf.maxwords+1):
        # iterate through possible argument combinations (same args are OK)
        for argstuple in itertools.product(ARGTYPES, repeat=conf.nargs):
            argstr = '(' + ','.join(argstuple) + ')'

            print('#', filenameshort, nwords, 'words, args:', argstr)

            # iterate through combos of words in function name (no repeats!)
            for funwords in itertools.permutations(words, nwords):
                # human-readable function signature
                funsig = '_'.join(list(funwords)) + argstr
                # 4-byte function selector
                funsel = web3.Web3.toHex(web3.Web3.sha3(text=funsig)[:4])

                # print close-enoughs
                if funsel.startswith(targetshort): print(funsel, funsig)
                # print match
                if funsel == conf.target: print('### FOUND!', funsel, funsig)

    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, default='0x00000000',
                        help='function selector to search for')
    parser.add_argument('-a', '--nargs', type=int, default=1,
                        help='number of function arguments')
    parser.add_argument('-f', '--dictfile', type=str, default=None,
                        help='file name to read dictionary of words from')
    parser.add_argument('-w', '--minwords', type=int, default=1,
                        help='minimum number of words in function name')
    parser.add_argument('-W', '--maxwords', type=int, default=None,
                        help='maximum number of words in function name')

    conf = parser.parse_args()
    if not conf.maxwords: conf.maxwords = conf.minwords

    run(conf)
