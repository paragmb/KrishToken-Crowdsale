import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

load_dotenv()

from PIL import Image


if 'fishsticktotalsupply' not in st.session_state:
    st.session_state.fishsticktotalsupply=100
if 'janetotalsupply' not in st.session_state:    
    st.session_state.janetotalsupply=1000
if 'leadertotalsupply' not in st.session_state:    
    st.session_state.leadertotalsupply=2000
if 'peeleytotalsupply' not in st.session_state:    
    st.session_state.peeleytotalsupply=4000
if 'wildcardtotalsupply' not in st.session_state:    
    st.session_state.wildcardtotalsupply=8000



# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################


@st.cache(allow_output_mutation=True)
def load_artwork_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/artwork_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("ARTWORK_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract_artwork = load_artwork_contract()


@st.cache(allow_output_mutation=True)
def load_krishtokencrowdsale_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/krishtokencrowdsale_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("KRISHTOKENCROWDSALE_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract_krishtokencrowdsale = load_krishtokencrowdsale_contract()


@st.cache(allow_output_mutation=True)
def load_krishtoken_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/krishtoken_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("KRISHTOKEN_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract_krishtoken = load_krishtoken_contract()



################################################################################
# BUY KRISH TOKEN
################################################################################

st.title("BUY KRISH TOKEN (KTK)!!")
st.write("1 ETH = 1 KTK")
form = st.form(key='my-form')
txnHash = form.text_input('Enter your transaction hashgtag and press BUY')
submit = form.form_submit_button('BUY')



if submit:
    
    transaction  = w3.eth.getTransaction(txnHash)
    value_KTK=transaction['value']/1000000000000000000
    value=transaction['value']
    beneficiary=transaction['from']
    send_to_wallet=transaction['to']
    
    #st.write(transaction)
    st.write(f'You purchased {value_KTK} KTK!!')
    
    
    df = pd.read_csv("htag_db.csv")
    
    newtransaction=True
    for i in range(len(df['HashTags'])):
        if (df['HashTags'][i]==txnHash or os.getenv("WALLET_PUBLIC_KEY")!=send_to_wallet): 
            print(df['HashTags'][i])
            
            newtransaction=False

    if(newtransaction):
        with open("htag_db.csv", "a") as f:
            f.write('\n'+txnHash)  
            
        sendtransaction = contract_krishtokencrowdsale.functions.buyTokens(beneficiary).buildTransaction({
        'gas': 700000,
        'gasPrice': 30000,
        'from': os.getenv("WALLET_PUBLIC_KEY"),
        'value':value,
        'nonce': w3.eth.getTransactionCount(os.getenv("WALLET_PUBLIC_KEY"))
         }) 
         
        signed_txn = w3.eth.account.signTransaction(sendtransaction, private_key=os.getenv("PRIVATE_KEY"))
        w3.eth.sendRawTransaction(signed_txn.rawTransaction)       
        st.write("Succesful transaction!")
    else:
        st.write("You already purchased your tokens using this transaction or you send your ETH to a wrong address!!")  
   
  

form2 = st.form(key='my-form2')
beneficiary_address = form.text_input('Enter your public address to see your KTK balance')
submit2 = form.form_submit_button('Search')



if submit2:
    token_balance=contract_krishtoken.functions.balanceOf(beneficiary_address).call()
    token_balance_KTK=token_balance/1000000000000000000
    st.write(f'You have a balance of {token_balance_KTK} KTK!!')
    


st.title("CHOOSE YOUR AVATAR!!")

image1 = Image.open('Fishstick.PNG')
st.image(image1, caption='Fishstick: 1 KTK')

fishstick_URI="https://gateway.pinata.cloud/ipfs/QmP6ivinD1PRMHnWr1BBmyhRsrq1r3JuX8REWaDUE7F6y1"

image2 = Image.open('Jane.PNG')
st.image(image2, caption='Jane: 0.8 KTK')

jane_URI="https://gateway.pinata.cloud/ipfs/QmVjCm6VmEgPMgrwRp8TCosQJn9kQuyx2TQm5RX8yNpyc5"

image3 = Image.open('Leader.PNG')
st.image(image3, caption='Leader: 0.5 KTK')

leader_URI="https://gateway.pinata.cloud/ipfs/QmUEEma8pxQ5MWG2rMX2MNxLFPPC2bvZv2BFUEdJVP5wvi"

image4 = Image.open('Peeley.PNG')
st.image(image4, caption='Peeley: 0.3 KTK')

peeley_URI="https://gateway.pinata.cloud/ipfs/Qmf5FnyX8XYu4HYjXT6WP1LtWwVdb5ax9SLP1HVK7wNGK1"

image5 = Image.open('WildCard.PNG')
st.image(image5, caption='Wild Card: 0.2 KTK')

wildcard_URI="https://gateway.pinata.cloud/ipfs/QmRvsJr9fJ1uaUFzWnELnDWrzNtMBVqrvwsPv2eJgA68j5"



################################################################################
# Register New Artwork
################################################################################
st.title("Purchae your Avatar!")
accounts = w3.eth.accounts
# Use a streamlit component to get the address of the artwork owner from the user
#address = st.selectbox("Select Artwork Owner", options=accounts)
all_avatars=('Fishstick', 'Jane', 'Leader', 'Peeley','Wilds Card')
avatar = st.selectbox("Select your avatar!", options=all_avatars)


# Use a streamlit component to get the artwork's URI
address = st.text_input("Enter your public address")

uri_dict={'Fishstick':"https://gateway.pinata.cloud/ipfs/QmP6ivinD1PRMHnWr1BBmyhRsrq1r3JuX8REWaDUE7F6y1",
          'Jane':"https://gateway.pinata.cloud/ipfs/QmVjCm6VmEgPMgrwRp8TCosQJn9kQuyx2TQm5RX8yNpyc5",
          'Leader':"https://gateway.pinata.cloud/ipfs/QmUEEma8pxQ5MWG2rMX2MNxLFPPC2bvZv2BFUEdJVP5wvi",
          'Peeley':"https://gateway.pinata.cloud/ipfs/Qmf5FnyX8XYu4HYjXT6WP1LtWwVdb5ax9SLP1HVK7wNGK1",
          'Wilds Card':"https://gateway.pinata.cloud/ipfs/QmRvsJr9fJ1uaUFzWnELnDWrzNtMBVqrvwsPv2eJgA68j5"
                 
          }

price_dict={'Fishstick':1,
          'Jane':0.8,
          'Leader':0.5,
          'Peeley':0.3,
          'Wilds Card':0.2
                 
          }

# supply_dict={'Fishstick':fishsticktotalsupply,
#           'Jane':janetotalsupply,
#           'Leader':leadertotalsupply,
#           'Peeley':peeleytotalsupply,
#           'Wilds Card':wildcardtotalsupply
                 
#           }




artwork_uri =uri_dict[avatar]
transfer_amount=int(price_dict[avatar]*1000000000000000000)

if st.button("Purchase"):
    
    sendtransaction1 = contract_krishtoken.functions.approve(os.getenv("WALLET_PUBLIC_KEY"),transfer_amount).buildTransaction({
        'gas': 700000,
        'gasPrice': 30000,
        'from': os.getenv("CUSTOMER_PUBLIC_KEY"),
        'nonce': w3.eth.getTransactionCount(os.getenv("CUSTOMER_PUBLIC_KEY"))
    }) 
         
    signed_txn1 = w3.eth.account.signTransaction(sendtransaction1, private_key=os.getenv("CUSTOMER_PRIVATE_KEY"))
    w3.eth.sendRawTransaction(signed_txn1.rawTransaction) 
    
        
        
    sendtransaction2 = contract_krishtoken.functions.transferFrom(address,os.getenv("WALLET_PUBLIC_KEY"),transfer_amount).buildTransaction({
         'gas': 700000,
         'gasPrice': 30000,
         'from': os.getenv("WALLET_PUBLIC_KEY"),
         'nonce': w3.eth.getTransactionCount(os.getenv("WALLET_PUBLIC_KEY"))
    }) 
         
    signed_txn2 = w3.eth.account.signTransaction(sendtransaction2, private_key=os.getenv("PRIVATE_KEY"))
    w3.eth.sendRawTransaction(signed_txn2.rawTransaction) 
    
             
    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract_artwork.functions.registerArtwork(
        address,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    #supply_dict[avatar]=supply_dict[avatar]-1
    
    
    st.write("Transaction receipt mined:")
    #st.write(dict(receipt))
    if (avatar=='Fishstick'):
        st.session_state.fishsticktotalsupply -= 1
        st.write(f"Remaining supply of Fishstick is {st.session_state.fishsticktotalsupply}")
    elif (avatar=='Jane'):
        st.session_state.janetotalsupply -= 1  
        st.write(f"Remaining supply of Jane is {st.session_state.janetotalsupply}")
    elif (avatar=='Leader'):
        st.session_state.leadertotalsupply -= 1  
        st.write(f"Remaining supply of Leader is {st.session_state.leadertotalsupply}")
    elif (avatar=='Peeley'):  
        st.session_state.peeleytotalsupply -= 1  
        st.write(f"Remaining supply of Peeley is {st.session_state.peeleytotalsupply}")
    else:
        st.session_state.wildcardtotalsupply -= 1    
        st.write(f"Remaining supply of Wild Card is {st.session_state.wildcardtotalsupply}")

st.markdown("---")


################################################################################
# Display a Token
################################################################################
st.markdown("## Display your Avatar")

selected_address = st.text_input("Enter your  address")

tokens=0

try:
    
  tokens = contract_artwork.functions.balanceOf(selected_address).call()
  
except:
  print()    

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Artwork Tokens", list(range(tokens)))



if st.button("Display"):
    


    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract_artwork.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract_artwork.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)
