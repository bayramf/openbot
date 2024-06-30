from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext, ConversationHandler
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from web3 import Web3
import nest_asyncio
import time
import asyncio

nest_asyncio.apply()

# Connect to OpenGPU Devnet node
opengpu_rpc_url = 'https://nerpc.ogpuscan.io'
web3 = Web3(Web3.HTTPProvider(opengpu_rpc_url))

oGPU_chain_id = 201720082023
WoGPU_address_checksum = '0xcdAD45eB05eaE8DFA1ee40be4BCa97dCbf82367b'
router_address = web3.to_checksum_address('0xACc384a831BBbbd031846Ff97964D857b5F6d9fA')

# Define service and options for WebDriver
service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("headless")

# Placeholder for the ABIs
router_abi = [{
        "inputs": [
            {
                "internalType": "address",
                "name": "_factory",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_WETH",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "WETH",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "tokenA",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "tokenB",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountADesired",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountBDesired",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountAMin",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountBMin",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "addLiquidity",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountA",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountB",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "liquidity",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amountTokenDesired",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountTokenMin",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountETHMin",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "addLiquidityETH",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountToken",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountETH",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "liquidity",
                "type": "uint256"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "factory",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveOut",
                "type": "uint256"
            }
        ],
        "name": "getAmountIn",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveOut",
                "type": "uint256"
            }
        ],
        "name": "getAmountOut",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            }
        ],
        "name": "getAmountsIn",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            }
        ],
        "name": "getAmountsOut",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountA",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveA",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "reserveB",
                "type": "uint256"
            }
        ],
        "name": "quote",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "amountB",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapETHForExactTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactETHForTokensSupportingFeeOnTransferTokens",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactTokensForETH",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactTokensForETHSupportingFeeOnTransferTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountOutMin",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactTokensForTokensSupportingFeeOnTransferTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountInMax",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapTokensForExactETH",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "amountInMax",
                "type": "uint256"
            },
            {
                "internalType": "address[]",
                "name": "path",
                "type": "address[]"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapTokensForExactTokens",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }]  # Replace with actual ABI
token_abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_symbol",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "_decimals",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "_totalSupply",
                "type": "uint256"
            },
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "description",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "logoUri",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "projectGif",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "projectEmoji",
                        "type": "string"
                    },
                    {
                        "internalType": "string[]",
                        "name": "socialKeys",
                        "type": "string[]"
                    },
                    {
                        "internalType": "string[]",
                        "name": "socialUris",
                        "type": "string[]"
                    }
                ],
                "internalType": "struct MemeCoinORC20.CompetitionMetadata",
                "name": "metadata",
                "type": "tuple"
            },
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_owner",
                "type": "address"
            }
        ],
        "stateMutability": "payable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "pair",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "isActive",
                "type": "bool"
            }
        ],
        "name": "ActivePairsUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "string",
                "name": "key",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "value",
                "type": "string"
            }
        ],
        "name": "MetadataUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "symbol",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "decimals",
                "type": "uint8"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "totalSupply",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "description",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "logoUri",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectGif",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectEmoji",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialPlatforms",
                "type": "string[]"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialUris",
                "type": "string[]"
            }
        ],
        "name": "NewORC20Created",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "symbol",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "uint8",
                "name": "decimals",
                "type": "uint8"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "totalSupply",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "description",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "logoUri",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectGif",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectEmoji",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialPlatforms",
                "type": "string[]"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialUris",
                "type": "string[]"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "pair",
                "type": "address"
            }
        ],
        "name": "NewORC20CreatedWithPair",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "maker",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "swapType",
                "type": "bool"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokenAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "description",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "logoUri",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectGif",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "projectEmoji",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialPlatforms",
                "type": "string[]"
            },
            {
                "indexed": False,
                "internalType": "string[]",
                "name": "socialUris",
                "type": "string[]"
            }
        ],
        "name": "Swap",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "WETH",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "Winner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "addLP",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "remaining",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "success",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "balance",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getMetadata",
        "outputs": [
            {
                "internalType": "string",
                "name": "description",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "logoUri",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "projectGif",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "projectEmoji",
                "type": "string"
            },
            {
                "internalType": "string[]",
                "name": "socialPlatforms",
                "type": "string[]"
            },
            {
                "internalType": "string[]",
                "name": "socialUris",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "platform",
                "type": "string"
            }
        ],
        "name": "getSocials",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "pair",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "isActive",
                "type": "bool"
            }
        ],
        "name": "setActivePairs",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newDescription",
                "type": "string"
            }
        ],
        "name": "setDescription",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newLogoUri",
                "type": "string"
            }
        ],
        "name": "setLogo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newEmoji",
                "type": "string"
            }
        ],
        "name": "setProjectEmoji",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newGifUri",
                "type": "string"
            }
        ],
        "name": "setProjectGif",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "platform",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "uri",
                "type": "string"
            }
        ],
        "name": "setSocials",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "success",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "success",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "uniswapV2Pair",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "uniswapV2Router",
        "outputs": [
            {
                "internalType": "contract IUniswapV2Router02",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "stateMutability": "payable",
        "type": "receive"
    }
]

router_contract = web3.eth.contract(address=router_address, abi=router_abi)

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TOKEN = 'YOUR_TOKEN_HERE'

# States for the conversation handler
WALLET_ADDRESS, PRIVATE_KEY, TOKEN_ADDRESS, AMOUNT_TO_BUY, ACTION_CHOICE, LIMIT_PRICE = range(6)

# Welcome message
WELCOME_MESSAGE = """Welcome to OpenBot!

The first sniper and purchasing bot on the OpenGPU Network.

Commands:
/begin

GitHub: https://github.com/bayramf/openbot/
Telegram: https://t.me/+V8UY4bGqyEAxZmQ0"""

# Wallet Setup
step_one = """⚙️ Wallet Setup"""

def get_start_keyboard():
    keyboard = [
        [InlineKeyboardButton("✨ Create Wallet", callback_data='create_wallet')],
        [InlineKeyboardButton("✍️ Import Wallet", callback_data='import_wallet')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_action_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎯 Snipe", callback_data='snipe')],
        [InlineKeyboardButton("🔄 Swap", callback_data='swap'),
         InlineKeyboardButton("📈 Limit Order", callback_data='limit_order')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_buy_sell_keyboard(action):
    keyboard = [
        [InlineKeyboardButton("🔵 Buy", callback_data=f'{action}_buy'),
         InlineKeyboardButton("🔴 Sell", callback_data=f'{action}_sell')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def welcome(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)

async def wallet_setup(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(step_one, reply_markup=get_start_keyboard())

async def panel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome to the panel. More functionalities will be added soon.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.lower()
    if text == "panel":
        await panel(update, context)
    else:
        await echo(update, context)

async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_data = context.user_data
    await query.answer()

    if query.data == 'create_wallet':
        # Create a new Ethereum account
        acc = web3.eth.account.create()
        private_key = web3.to_hex(acc.key)
        wallet_address = acc.address
        user_data['wallet_address'] = wallet_address
        user_data['private_key'] = private_key
        response_text = (
            f"✅ Successfully Created Wallet\n\n"
            f"⚠️ Save your private key. If you delete this message, we will not show you your private key again.\n\n"
            f"💡 **Private Key:** {private_key}\n\n"
            f"💡 **Wallet Address:** {wallet_address}"
        )
        await query.edit_message_text(text=response_text)
        await query.message.reply_text("Please enter the token contract address:")
        return TOKEN_ADDRESS

    elif query.data == 'import_wallet':
        await query.message.reply_text("Please enter your Wallet Address:")
        return WALLET_ADDRESS

    elif query.data == 'snipe':
        user_data['action'] = query.data
        token_address = user_data['token_address']
        wallet_address = user_data['wallet_address']
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        token_symbol = token_contract.functions.symbol().call()
        oGPU_balance = web3.eth.get_balance(wallet_address) / 10**18
        response_text = (
            f"💡 Total oGPU Balance: {oGPU_balance}\n\n"
            f"Please enter the amount of oGPU you want to snipe {token_symbol} for:"
        )
        await query.message.reply_text(response_text)
        return AMOUNT_TO_BUY

    elif query.data in ['swap', 'limit_order']:
        user_data['action'] = query.data
        await query.message.reply_text("Choose your action:", reply_markup=get_buy_sell_keyboard(query.data))
        return ACTION_CHOICE

    elif query.data.endswith('_buy'):
        user_data['action_choice'] = query.data
        token_address = user_data['token_address']
        wallet_address = user_data['wallet_address']
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        token_symbol = token_contract.functions.symbol().call()
        oGPU_balance = web3.eth.get_balance(wallet_address) / 10**18
        
        response_text = (
            f"💡 Total oGPU Balance: {oGPU_balance}\n\n"
            f"Please enter the amount of oGPU you want to buy {token_symbol} for:"
        )
        await query.message.reply_text(response_text)
        return AMOUNT_TO_BUY

    elif query.data.endswith('_sell'):
        user_data['action_choice'] = query.data
        token_address = user_data['token_address']
        wallet_address = user_data['wallet_address']
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        token_balance = token_contract.functions.balanceOf(wallet_address).call()
        token_symbol = token_contract.functions.symbol().call()
        
        response_text = (
            f"💡 Total {token_symbol} Balance: {token_balance / 10**18}\n\n"
            f"Please enter the amount of {token_symbol} you want to sell:"
        )
        await query.message.reply_text(response_text)
        return AMOUNT_TO_BUY

async def amount_to_buy(update: Update, context: CallbackContext) -> None:
    try:
        amount_to_buy = int(update.message.text)
        if amount_to_buy <= 0:
            await update.message.reply_text("Amount must be greater than zero. Please enter a valid amount:")
            return AMOUNT_TO_BUY

        context.user_data['amount_to_buy'] = amount_to_buy
        token_address = context.user_data['token_address']
        action = context.user_data['action']
        wallet_address = context.user_data['wallet_address']
        if action in ['snipe', 'swap']:
            oGPU_balance = web3.eth.get_balance(wallet_address) / 10**18
            estimated_gas = 0.01  # Estimated gas fee in oGPU
            if amount_to_buy + estimated_gas > oGPU_balance:
                await update.message.reply_text("Insufficient oGPU balance to cover the transaction and gas fees. Please enter a valid amount:")
                return AMOUNT_TO_BUY
        elif action == 'limit_order':
            token_contract = web3.eth.contract(address=token_address, abi=token_abi)
            token_balance = token_contract.functions.balanceOf(wallet_address).call() / 10**18
            if amount_to_buy > token_balance:
                await update.message.reply_text("Insufficient token balance. Please enter a valid amount:")
                return AMOUNT_TO_BUY

        if action == 'snipe':
            await snipe(update, context)
        elif action == 'swap':
            action_choice = context.user_data['action_choice']
            if action_choice == 'swap_buy':
                await swap_buy(update, context)
            else:
                await swap_sell(update, context)
        elif action == 'limit_order':
            action_choice = context.user_data['action_choice']
            token_address = context.user_data['token_address']
            path = [token_address, WoGPU_address_checksum]
            amount_in = 1 * 10**18  # 1 token, adjust decimals based on token's decimals

            amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
            token_price = amounts_out[1] / 10**18  # Token price in terms of oGPU
            token_contract = web3.eth.contract(address=token_address, abi=token_abi)
            token_symbol = token_contract.functions.symbol().call()
            
            response_text = (
                f"💡 Actual price for {token_symbol} in oGPU: {token_price}\n\n"
                f"Please enter a price limit for the order to be executed:"
            )
            await update.message.reply_text(response_text)
            return LIMIT_PRICE
    except Exception as e:
        await update.message.reply_text(f"Insufficient balance to cover transaction and gas fees. Please enter a valid amount:")
        return AMOUNT_TO_BUY

async def limit_price(update: Update, context: CallbackContext) -> None:
    try:
        limit_price = float(update.message.text)
        if limit_price <= 0:
            await update.message.reply_text("Price limit must be greater than zero. Please enter a valid price limit:")
            return LIMIT_PRICE

        context.user_data['limit_price'] = limit_price
        action_choice = context.user_data['action_choice']
        if action_choice == 'limit_order_buy':
            await limit_order_buy(update, context)
        else:
            await limit_order_sell(update, context)
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f"Price limit must be greater than zero. Please enter a valid price limit:")
        return LIMIT_PRICE

async def snipe(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
    
    # Prepare the swap function call parameters
    buy_path = [WoGPU_address_checksum, token_address]
    amount_to_buy_for = int(amount_to_buy) * 10**18

    async def snipe_order():
        n = 1
        while True:
            driver = webdriver.Chrome(service=service, options=options)
            token_url = f"https://dex.ogpuscan.io/token/{token_address}"  # Replace with the actual URL
            driver.get(token_url)
            await asyncio.sleep(3)

            try:
                submit_button = driver.find_element(By.XPATH, "//button[text()='Buy']")  # Replace with actual XPath

                buy_tx_params = {
                    "nonce": web3.eth.get_transaction_count(wallet_address),
                    "from": wallet_address,
                    "chainId": oGPU_chain_id,
                    "gas": 500_000,
                    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
                    "maxFeePerGas": 100 * 10**10,
                    "value": amount_to_buy_for,    
                }
                buy_tx = router_contract.functions.swapExactETHForTokens(
                    0,  # Min amount out
                    buy_path,
                    wallet_address,
                    int(time.time()) + 180  # Deadline now + 180 sec
                ).build_transaction(buy_tx_params)

                signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                snipe_text = (
                    f"✅ Snipe Order Executed! \n\n"
                    f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
                )
                await update.message.reply_text(snipe_text)
                await asyncio.sleep(1.5)
                driver.quit()
                break
            
            except:
                if n == 1:
                    await update.message.reply_text(f"⚠️ Snipe Order Placed!")
                n = n + 1
                driver.quit()
                pass

    asyncio.create_task(snipe_order())
    await reset_bot_state(update, context)  # Reset the bot state after the operation

async def swap(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Choose your action:", reply_markup=get_buy_sell_keyboard('swap'))

async def swap_buy(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
 
    buy_path = [WoGPU_address_checksum, token_address]
    amount_to_buy_for = int(amount_to_buy) * 10**18
    
    async def swap_buy_ex():
        buy_tx_params = {
            "nonce": web3.eth.get_transaction_count(wallet_address),
            "from": wallet_address,
            "chainId": oGPU_chain_id,
            "gas": 500_000,
            "maxPriorityFeePerGas": web3.eth.max_priority_fee,
            "maxFeePerGas": 100 * 10**10,
            "value": amount_to_buy_for,    
        }
        buy_tx = router_contract.functions.swapExactETHForTokens(
            0,  # Min amount out
            buy_path,
            wallet_address,
            int(time.time()) + 180  # Deadline now + 180 sec
        ).build_transaction(buy_tx_params)

        signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        swap_buy_text = (
            f"✅ Swap Executed! \n\n"
            f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
        )
        await update.message.reply_text(text=swap_buy_text)
        await asyncio.sleep(1.5)
    asyncio.create_task(swap_buy_ex())
    await reset_bot_state(update, context)  # Reset the bot state after the operation

async def swap_sell(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
    
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    sell_path = [token_address, WoGPU_address_checksum]
    
    async def swap_sell_ex():
        # before we can sell we need to approve the router to spend our token
        approve_tx = token_contract.functions.approve(router_address, int(amount_to_buy) * 10**18).build_transaction({
            "gas": 500_000,
            "maxPriorityFeePerGas": web3.eth.max_priority_fee,
            "maxFeePerGas": 100 * 10**10,
            "nonce": web3.eth.get_transaction_count(wallet_address),
        })    

        signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)

        tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        sell_tx_params = {
            "nonce": web3.eth.get_transaction_count(wallet_address),
            "from": wallet_address,
            "chainId": oGPU_chain_id,
            "gas": 500_000,
            "maxPriorityFeePerGas": web3.eth.max_priority_fee,
            "maxFeePerGas": 100 * 10**10,
        }
        sell_tx = router_contract.functions.swapExactTokensForETH(
            int(amount_to_buy) * 10**18, # amount to sell
            0, # min amount out
            sell_path,
            wallet_address,
            int(time.time())+180 # deadline now + 180 sec
        ).build_transaction(sell_tx_params)

        signed_sell_tx = web3.eth.account.sign_transaction(sell_tx, private_key)

        tx_hash = web3.eth.send_raw_transaction(signed_sell_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        swap_sell_text = (
            f"✅ Swap Executed! \n\n"
            f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
        )
        await update.message.reply_text(text=swap_sell_text)
        await asyncio.sleep(1.5)
    asyncio.create_task(swap_sell_ex())
    await reset_bot_state(update, context)  # Reset the bot state after the operation

async def limit_order(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Choose your action:", reply_markup=get_buy_sell_keyboard('limit_order'))
    
async def limit_order_buy(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
    limit_price = user_data['limit_price']
    
    path = [token_address, WoGPU_address_checksum]
    amount_in = 1 * 10**18  # 1 token, adjust decimals based on token's decimals
    buy_path = [WoGPU_address_checksum, token_address]
    amount_to_buy_for = int(amount_to_buy) * 10**18

    async def limit_order_buy_ex():
        m = 1
        while True:
            amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
            token_price = amounts_out[1] / 10**18  # Token price in terms of oGPU
            
            if token_price <= limit_price:
                buy_tx_params = {
                    "nonce": web3.eth.get_transaction_count(wallet_address),
                    "from": wallet_address,
                    "chainId": oGPU_chain_id,
                    "gas": 500_000,
                    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
                    "maxFeePerGas": 100 * 10**10,
                    "value": amount_to_buy_for,    
                }
                buy_tx = router_contract.functions.swapExactETHForTokens(
                    0,  # Min amount out
                    buy_path,
                    wallet_address,
                    int(time.time()) + 180  # Deadline now + 180 sec
                ).build_transaction(buy_tx_params)

                signed_buy_tx = web3.eth.account.sign_transaction(buy_tx, private_key)
                tx_hash = web3.eth.send_raw_transaction(signed_buy_tx.rawTransaction)
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                limit_buy_text = (
                    f"✅ Buy Limit Order with {amount_to_buy} oGPU at price limit {limit_price} oGPU executed!\n\n"
                    f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
                )
                await update.message.reply_text(text=limit_buy_text)
                await asyncio.sleep(1.5)
                break
            else:
                if m == 1:
                    # Implement the logic for limit order buy
                    await update.message.reply_text(f"Buy Limit Order with {amount_to_buy} oGPU at price limit {limit_price} oGPU placed!")
                m = m + 1
    asyncio.create_task(limit_order_buy_ex())
    await reset_bot_state(update, context)  # Reset the bot state after the operation

async def limit_order_sell(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    wallet_address = user_data['wallet_address']
    private_key = user_data['private_key']
    token_address = user_data['token_address']
    amount_to_buy = user_data['amount_to_buy']
    limit_price = user_data['limit_price']
    
    path = [token_address, WoGPU_address_checksum]
    amount_in = 1 * 10**18  # 1 token, adjust decimals based on token's decimals
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    token_symbol = token_contract.functions.symbol().call() 
    sell_path = [token_address, WoGPU_address_checksum]
    
    async def limit_order_sell_ex():
        z = 1
        while True:
            amounts_out = router_contract.functions.getAmountsOut(amount_in, path).call()
            token_price = amounts_out[1] / 10**18  # Token price in terms of oGPU
            
            if token_price >= limit_price:
                # before we can sell we need to approve the router to spend our token
                approve_tx = token_contract.functions.approve(router_address, int(amount_to_buy) * 10**18).build_transaction({
                    "gas": 500_000,
                    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
                    "maxFeePerGas": 100 * 10**10,
                    "nonce": web3.eth.get_transaction_count(wallet_address),
                })    

                signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)

                tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                sell_tx_params = {
                    "nonce": web3.eth.get_transaction_count(wallet_address),
                    "from": wallet_address,
                    "chainId": oGPU_chain_id,
                    "gas": 500_000,
                    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
                    "maxFeePerGas": 100 * 10**10,
                }
                sell_tx = router_contract.functions.swapExactTokensForETH(
                    int(amount_to_buy) * 10**18, # amount to sell
                    0, # min amount out
                    sell_path,
                    wallet_address,
                    int(time.time())+180 # deadline now + 180 sec
                ).build_transaction(sell_tx_params)

                signed_sell_tx = web3.eth.account.sign_transaction(sell_tx, private_key)

                tx_hash = web3.eth.send_raw_transaction(signed_sell_tx.rawTransaction)
                limit_sell_text = (
                    f"✅ Sell Limit Order with {amount_to_buy} {token_symbol} at price limit {limit_price} oGPU executed!\n\n"
                    f"💡 Tx Hash: {Web3.to_hex(tx_hash)}"
                )
                await update.message.reply_text(text=limit_sell_text)
                await asyncio.sleep(1.5)
                break
            else:
                if z == 1:
                    # Implement the logic for limit order buy
                    await update.message.reply_text(f"Sell Limit Order with {amount_to_buy} {token_symbol} at price limit {limit_price} oGPU placed!")
                z = z + 1
    asyncio.create_task(limit_order_sell_ex())
    await reset_bot_state(update, context)  # Reset the bot state after the operation
    
async def wallet_address(update: Update, context: CallbackContext) -> None:
    context.user_data['wallet_address'] = update.message.text
    await update.message.reply_text("Please enter your Private Key:")
    return PRIVATE_KEY

async def private_key(update: Update, context: CallbackContext) -> None:
    context.user_data['private_key'] = update.message.text
    wallet_address = context.user_data['wallet_address']
    private_key = context.user_data['private_key']
    # Validate the private key
    account = web3.eth.account.from_key(private_key)
    if account.address.lower() != wallet_address.lower():
        await update.message.reply_text("The provided private key does not match the wallet address. Please try again.")
        return PRIVATE_KEY
    else:
        response_text = (
            f"✅ Wallet imported successfully!\n\n"
            f"💡 **Wallet address:** {wallet_address}"
        )
        await update.message.reply_text(text=response_text)
        await update.message.reply_text("Please enter the token contract address:")
        return TOKEN_ADDRESS

async def token_address(update: Update, context: CallbackContext) -> None:
    token_address = update.message.text
    try:
        context.user_data['token_address'] = web3.to_checksum_address(token_address)
        await update.message.reply_text("Choose your action:", reply_markup=get_action_keyboard())
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Token Contract Address is not correct. Please enter a valid token contract address.")
        return TOKEN_ADDRESS

def cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Import wallet process canceled.')
    return ConversationHandler.END

async def reset_bot_state(update: Update, context: CallbackContext) -> None:
    context.user_data.clear()
    await update.message.reply_text("The bot has been reset to its initial state. You can start a new operation.")

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Conversation handler for importing a wallet
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback)],
        states={
            WALLET_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_address)],
            PRIVATE_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, private_key)],
            TOKEN_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, token_address)],
            AMOUNT_TO_BUY: [MessageHandler(filters.TEXT & ~filters.COMMAND, amount_to_buy)],
            LIMIT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, limit_price)],
            ACTION_CHOICE: [CallbackQueryHandler(button_callback)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", welcome))
    application.add_handler(CommandHandler("begin", wallet_setup))
    application.add_handler(CommandHandler("panel", panel))

    # Handle callback queries from inline keyboard buttons
    application.add_handler(conv_handler)

    # on noncommand i.e message - handle the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
