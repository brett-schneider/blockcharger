# Project Title - Group Nickname
##### Prepared by: Christoph Bretschneider, Diana Nguyen, Mateusz Piotrowski, Luisa Rahn
*20 May, 2020*


## Background Motivation
As pressure for the international community rises to meet the agreed climate goals the integration of E-mobility among other low-carbon energy technologies becomes increasingly important. To successfuly implement changes within the transport sector a widespread, client friendly and easily accessible charging infrastructure is needed. Main stakeholders in the charging business are Charg Point Operators (CPOs) manageing the charging stations and eMobility Service Providers (eMSPs) employing settlement services (including apps, charging cards, etc.). The latter appear with a wide variety of tariffs and concepts, making it difficult for users to charge barrier-free at low cost. Our project aims to provide an uniform **P2P/B2P/E-Mobility-Roaming??** (ERP) energy trading solution guaranteeing transparent, non-discriminatory access to all clients.

- MSPs notwendig?
- Rollenmodel EU-Richtlinie?

## Technical Approach

- implemented as smart contract (e.g. in Ethereum)
- ...
- Registration and Setup
- Communication
- Authentification?

### Assumptions
- CPOs/eMSPs set the price
- Within system bounderies: CPO MSP client (electric utilities/grid not being considered)

### Technical Challenges
Security, privacy and trust issues are being addressed ...

1. **Security and Trust through Micropayments**:

	Currently, we believe that we might use micropayments to address most of the challenges. The idea is to use something like https://raiden.network/ and just then pass the money to the operator every time the consumer confirms the delivery of the energy unit. This way either party may terminate the ongoing transaction if the other party seems to cheat. Also, the potential amount of money that could be disputed is going to be very low.

	How would you control that they actually delivered what they promised?
	The smart contract would transfer money to the charging station operator every time the consumer confirms the energy has been delivered.
	
	How would you implement a secure trading protocol so that no involved party can
	cheat?
	As I mentioned before, we hope that with micropayments we might be able to minimize the amount of damage a cheating party could cause. However, we've not come up with an idea yet how to prevent any form of cheating.
	
	As the blockchain is publicly availably, what (sensitive) data do
	you store on the blockchain, are there privacy concerns, and if so, how
	would you solve these?
	We've not addressed this problem yet.
	
	  For example, when exactly would a party get paid?
	
	  Instantly. We would like to utilize micropayments (e.g., https://raiden.network) so that money could be transferred whenever a little amount of energy gets transferred. This way we want to avoid disputes over huge amount of money.
	  Raiden lets you make hash-locked transfers that need no global consensus against an ERC-20 token on-chain deposit. The deposit initiates a payment channel.
	  The remainder of the deposit is locked in the payment channel until it is closed.
	
	
	  How would you control that they actually delivered what they promised?
	
	
	  Since the energy is being traded in small amounts at a time, the potential loss is small.
	  
	  *TODO: Is it even possible to trade enegry this way?
	  Micropayments could be fast but they are probably not as fast as electricity being transfered from one household to another.
	  ultra rapid chargers give 100 kW, a normal household has around 25 kW. 1 kWh is roughly 0.25 EUR, so at most, 25 EUR/h split up in 0.05 EUR units is 500 payments per hour. Raiden claims their payments are as quick as text messages, whatever that means*

2. **Scam Prevention...**

  TODO: Do we want to introduce some kind of a scam prevention system? Even though a single transaction loss could be small, if we allow for many little scam transactions to happen constantly then we might have a huge problem on the network.


  How would you implement a secure trading protocol so that no involved party can cheat?

  We assume that micropayments are going to render this problem insignificant.
  
3. **Trust through Escrows**
  
  Alternatively, we may think about escrows:

  See http://www.jbonneau.com/doc/GBGN17-FC-physical_escrow.pdf

  Raiden has an on-chain deposit system that locks it in a smart contract until one party closes the payment channel by sending in their balance sheet. The other party has to then send in their balance sheet. If they match, funds from the deposit are distributed accordingly. We should think of a system to settle disputes for when they do not.

4. **Privacy ...**
  As the blockchain is publicly availably, what (sensitive) data do you store on the blockchain, are there privacy concerns, and if so, how would you solve these?


  Grouping transactions together to hide exact amounts of energy transfers and fees.
  The final payment can be seen on-chain after the closure of the channel. This is a privacy risk in the way that the movements of a car can be traced much like with Cash Machine withdrawals and should be addressed ... 


## Milestones

### Requirement List
mark minimum acceptance requirements

- Implement virtual meters, which track amount of transceived energy.
- Must-have: a program capable of updating our blockchain-based smart contract with information about send/received energy
- Technology: whatever language we pick to talk to our smart contract
- Nice-to-have: web interface
- Implement a smart contract managing the transfer of energy between a producer and a consumer in exchange for a fee.
- Take dispute settlement under consideration when designing & implementing the contract.
- Escrows?
- Backlog:
	 - hardware requirements
	  It's a good idea to discuss hardware requirements in the final presentation/report, but for the implementation phase it is probably irrelevant.
	 - Blockchain explorer
	TODO: As far as I understand, the idea here was to have an interface to browse our blockchain. If that's true, this is probably not really an essential todo, because:
Our blockchain is most likely going to come with an interface designed exactly for this purpose.
 It's a UI, which is nice to have, but not vital.
 It's a programming exercise in UI technologies like JS, and HTML, which is not the goal of this course.

List of interesting technologies:


  NodeJS
  
  https://metamask.io
  
  raiden.network micropayments


## References
Share and Charge (Open Charging Network, eRoaming): https://shareandcharge.com/open-charging-network/


## Appendix

[Lade-Report] (http://macdown.uranusjr.comhttps://www.prognos.com/fileadmin/pdf/publikationsdatenbank/20200207__Prognos_Lade-Report_2020.pdf):

Most providers have kWh-based tariffs, as will be required in the future by the legal metrology-based billing system. More expensive tariffs are usually quoted for DC charges due to the higher investment costs for such a charging infrastructure. Overall, the prices range from 29 to 41 ct/kWh for AC and from 35 to 50 ct/kWh for DC.
Additionally roaming services are provided. Eg. charging at Telekom's "other CPOs" for a uniform 89 ct/kWh for AC and DC.


## Requirements

motivate and describe the application's general idea
indicate how to achieve this goal by describing the technical approach
identify the technical challenges (e.g. security issues, privacy issues, trust issues) that arise from the problem space and your chosen technical approach 
describe as concretely as possible how you aim to address these challenges
identify a number of necessary steps towards completing the project and provide a rough schedule with milestones for them

fontsize: 10pt
Blocksatz
