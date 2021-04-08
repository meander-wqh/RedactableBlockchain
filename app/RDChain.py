from web3 import Web3, Account
# from solc import compile_files
import random
import os
from time import time
import chainUtil as chain


def main():

    # offline part init

    chain.hashInit()
    msg_16kb = open("../data/msg.json").read()
    testNumList = [359, 944, 1258, 1501]
    repeat = 5

    # connect to blockchain and deploy contract

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
    if w3.isConnected() is False:
        raise Exception('error in connecting to block chain')

    print("connected to blockchain.\n")

    contract_instance = chain.DeployContract()

    print("contract deployed.\n")

    # test 1:
    # send 16kb redackable transact to chain and just send a 16kb msg simple trasact

    for _ in range(repeat):
        chain.addBlock(msg_16kb + str(random.randint(0,9999)).zfill(4))
    for _ in range(repeat):
        chain.addSimpleBlock(msg_16kb + str(random.randint(0,9999)).zfill(4))

    # test 2:
    # redackable transact test

    for rep in testNumList:
        for _ in range(repeat):
            blockNo = chain.addBlock((msg_16kb + str(random.randint(0,9999)).zfill(4)) * rep)
            chain.modifyBlock(blockNo, (msg_16kb + str(random.randint(0,9999)).zfill(4)) * (rep - 1) \
                            + (msg_16kb + str(random.randint(0,9999)).zfill(4)))

    # test 3:
    # appending mode to implement editable blockchain

    for rep in testNumList:
        # for _ in range(repeat):
        chain.addSimpleBlock((msg_16kb + str(random.randint(0,9999)).zfill(4)) * rep)
        chain.addSimpleBlock("{modfied_block: true, target_block: 1, start_pos: 0, end_pos: 16384}, " \
                                + msg_16kb + str(random.randint(0,9999)).zfill(4))

if __name__ == "__main__":
    main()
