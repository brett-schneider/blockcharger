# Abstract

We propose a charging station for electric devices available to the general public that can be installed at any house so that there is a dense charging infrastructure, e.g. for electric vehicles
- motivation
- application's general idea

# Main

- describe technical approach to achieve application goal
- identify technical challenges: security issues, privacy issues, trust issues
- discuss how to address challenges -> choose which ones to address as part of project
- identify necessary steps -> rough schedule with milestones

---

- Transaction guarantees for seller and buyers
  - time of payment: micro-payments?
  - control of delivery
  - secure trading protocol 
  - storage of sensitive data/privacy concerns


# requirements

- the recipient needs a client capable of using our protocol to purchase electricity
- the provider needs a client capable …
- the provider needs a power outlet that powers the station and electricity to sell

# to do

- program a smart contract that monitors electricity dispensed and manages token flow
- token exchange    
  - ours
  - anyone can exchange tokens
- configure station price?
- program clients for car and station


---

## notes 12.05.2020

- simulation for meters (html, nodejs?)
- blockchain explorer
- smart contract (develop)
- dispute settlement
  - escrow
  - [https://raiden.network raiden.network] micropayments
- smart contract api
  - nodejs
  - metamask.io
- privacy
  - the grid needs to know information about the endpoints
- to reduce complexity, the grid will just be viewed an entity, which transfers energy lika a cable
- hardware requirements
