# BlockChat
Final project of the course Distributed Systems - 9th semester, Electrical Computer Engineering, National Technical University of Athens.

Implementation of BlockChat, a blockchain-based platform for message exchanges and transaction recording. 

Implementation uses Python 3.12 and REST API.

Project assignment can be found [here]([https://github.com/despoinavdl/AdvancedDatabasesNTUA23/blob/main/advanced_db_project.pdf](https://github.com/Fleria/NTUA-ECE-Distributed-Systems/blob/main/DistributedProject2024.pdf)).

Detailed description in the form of a report can be found [here]([https://github.com/despoinavdl/AdvancedDatabasesNTUA23/blob/main/03119111_03119442.pdf](https://github.com/Fleria/BlockChat-NTUA-ECE-Distributed-Systems/blob/main/BlockChat%20report.pdf)).

# Execution
System supports any number of BlockChat nodes (clients). To initialise each node, execute 
```bash
main -p port
client -p port
```

Client functions include:

- t <recipient_id> <message> : user sends a transaction to the user with an id of <recipient_id>. 
The transaction is a coin transaction if <message> is a number, otherwise it is a message transaction.

- balance : shows balance of BC wallet of user.
  
- view : shows validator id of the Proof-of-Stake algorithm that is used for consensus, and the transactions
of the last validated blockchain block.

- stake <amount> : releases the last stake of the node and registers <amount> as the new stake.

- help : shows list of functions available.
