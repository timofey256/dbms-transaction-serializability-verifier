# Transactions Serializability Verifier

This is a compact Python script designed to confirm the serializability of provided DBMS transactions. You can run it, type your transactions and see if they are 1) already serialized, 2) conflict-serializable, 3) view-serializable.

### How to use?
1. Clone the repo 
2. Install dependencies with `pip install matplotlib prettytable networkx`.
2. Start script with `python3 verifier.py`

### Simple Demo:
Upon running `verifier.py`, you'll encounter a prompt to input your transactions in chronological order. Follow the instructions by typing transactions in the format `T[transaction number].[read or write operation]([variable])`. For instance, `T1.R(A)` or `T2.W(b)` or `t3.r(a)`. Type `done` when all transactions are entered (case-insensitive).

Note: Once you've inputted all transactions, the application will generate windows displaying graphs showcasing dependencies and a potential topological sorting of those transactions.

Here's a small example:
```
[user@distro dbms-transaction-serializability-verifier]$ python3 verifier.py 
Following will be printed in order for the given schedule: 

1. Print schedule chart
2. Check if the given schedule is serial
3. Check if the given schedule is conflict serializable
4. Check if the given schedule is view serializable

Please follow the instructions to enter your values for schedule.

Enter number of transactions: 3
Enter transactions in the chronological order in the following format 

		T[transaction number].[read or write operation]([variable])
		For example: T1.R(A) or T2.W(b) or t3.r(a).

Or 'done' if you've typed all transactions. Case-insensitive.
Enter transaction: t1.r(a)
+------+----+----+
|  T1  | T2 | T3 |
+------+----+----+
| R(A) | *  | *  |
+------+----+----+
Enter transaction: t2.w(a)
+------+------+----+
|  T1  |  T2  | T3 |
+------+------+----+
| R(A) |  *   | *  |
|  *   | W(A) | *  |
+------+------+----+
Enter transaction: t3.r(a)
+------+------+------+
|  T1  |  T2  |  T3  |
+------+------+------+
| R(A) |  *   |  *   |
|  *   | W(A) |  *   |
|  *   |  *   | R(A) |
+------+------+------+
Enter transaction: done
The given schedule is serial schedule

This schedule is Conflict Serializable and Conflict Equivalent to <T1,T2,T3>

This schedule is View Serializable and View Equivalent to <T1,T2,T3>
```