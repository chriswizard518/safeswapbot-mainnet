# -*- coding: utf-8 -*-

def tokenAbi(address):

        filename = f'ABI_{address}.txt'
        with open(f"data/{filename}") as f:
            abi = f.readlines()
            return abi[0]



