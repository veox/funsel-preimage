#!/usr/bin/env python
# mutatis mutandis

import itertools
import argparse

import web3

argtypes = ['uint256', 'uint64', 'uint32', 'uint8', 'bool', 'bytes32', 'bytes', 'string']

parser = argparse.ArgumentParser()
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

filenameshort = conf.dictfile[:8]

# words' list for function name body
with open(conf.dictfile) as fd:
    words = fd.readlines()
words = [word.strip() for word in words]

for nwords in range(conf.minwords, conf.maxwords+1):
    for argstuple in itertools.product(argtypes, repeat=conf.nargs):
        argstr = '(' + ','.join(argstuple) + ')'

        print('>>>', filenameshort, nwords, 'words, args:', argstr)

        for funwords in itertools.permutations(words, nwords):
            # human-readable function signature
            funsig = '_'.join(list(funwords)) + argstr
            # 4-byte function selector
            funsel = web3.Web3.toHex(web3.Web3.sha3(text=funsig)[:4])

            # print close-enoughs
            if funsel.startswith('0x000000'): print(funsel, funsig)
            # print match
            if funsel == '0x00000000': print('>>>>>> FOUND!', funsel, funsig)
