# WSS_Cloud
Assignment submissions for Winter Systems School 2022 organized by IIT Delhi.

More details on the assignment itself can be found in https://systems-rg.github.io/wss22-cloud-labs.html

## Day 1
Writing a program to count occurance of words in two ways
1. Serially : visiting each word one at a time
2. Parallely : using threads to parallelize the work

## Day 2
Using Redis to actually mimick a distributed system by using various methods like xadd, xreadgroup, xcreate_group and xack.
Code still running on a single machine but it can be deployed to use distributed systems at this point.

## Day 3 and 4
Code till Day 2 is functionally correct and will not generate any errors as long as workers DONT DIE.
Focus on Day 3 and 4 was to implement fault tolerance.
Since Redis does not support atomic functions on its own, we use Lua Scripts to define the functions which we want to run atomically, and call this functions from Redis.

The final code in this repository is functionally correct as well as fault tolerant.
