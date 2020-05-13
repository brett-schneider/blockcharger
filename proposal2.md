What the product could be
-------------------------

-	market, which entails publishing and buying energy offers

Market
------

### Logic

-	easily implementable as a smart contract, (e.g., in Ethereum)

### Challenges

What properties this kind of transactions guarantee for the seller and buyer of energy.

-	For example, when exactly would a party get paid?
	-	Instantly. We would like to utilize micropayments (e.g., https://raiden.network) so that money could be transferred whenever a little amount of energy gets transferred. This way we want to avoid disputes over huge amount of money.
-	How would you control that they actually delivered what they promised?
	-	Since the energy is being traded in small amounts at a time, the potential loss is small.
		-	TODO: Is it even possible to trade enegry this way? Micropayments could be fast but they are probably not as fast as electricity being transfered from one household to another.
		-	TODO: Do we want to introduce some kind of a scam prevention system? Even though a single transaction loss could be small, if we allow for many little scam transactions to happen constantly then we might have a huge problem on the network.
-	How would you implement a secure trading protocol so that no involved party can cheat?
	-	We assume that micropayments are going to render this problem insignificant.
	-	Alternatively, we may think about escrows:
		-	See http://www.jbonneau.com/doc/GBGN17-FC-physical_escrow.pdf
-	As the blockchain is publicly availably, what (sensitive) data do you store on the blockchain, are there privacy concerns, and if so, how would you solve these?
	-	Grouping transactions together to hide exact amounts of energy transfers and fees.

Grid-related challenges:

-	The grid operator needs to know information about the endpoints sending and receiving energy. This is a probably a problem from a privacy perspective.
-	To reduce complexity, the grid will just be viewed an entity, which transfers energy like a cable.

Technical challenges regarding...

-	Security

	-	TODO

-	Privacy

	-	TODO

-	Trust

	-	TODO

### Tasks

-	[ ] Implement virtual meters, which track amount of transceived energy.
	-	Must-have: a program capable of updating our blockchain-based smart contract with information about send/received energy
		-	Technology: whatever language we pick to talk to our smart contract
	-	Nice-to-have: web interface
-	[ ] Implement a smart contract managing the transfer of energy between a producer and a consumer in exchange for a fee.
	-	[ ] Take dispute settlement under consideration when designing & implementing the contract.
		-	Escrows?

Backlog:

-	hardware requirements
	-	It's a good idea to discuss hardware requirements in the final presentation/report, but for the implementation phase it is probably irrelevant.
-	Blockchain explorer
	-	TODO: As far as I understand, the idea here was to have an interface to browse our blockchain. If that's true, this is probably not really an essential todo, because:
		1.	Our blockchain is most likely going to come with an interface designed exactly for this purpose.
		2.	It's a UI, which is nice to have, but not vital.
		3.	It's a programming exercise in UI technologies like JS, and HTML, which is not the goal of this course.

List of interesting technologies:

-	NodeJS
-	https://metamask.io
-	[raiden.network](https://raiden.network) micropayments

#### requirement list

-	TODO

#### list of minimum acceptance requirements

-	TODO

#### timeline & milestones

-	TODO
