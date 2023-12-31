import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable

INVALID_OPERATION_ERROR = "Error: this operation doesn't exist. Possible operations : R() for \"read\" and W() for \"write\"."
INVALID_TRANSACTION_ERROR = "Error: invalid transaction format or value (maybe you typed the number which higher than the total number of transactions?)."
INVALID_VALUE_OF_VAR_ERROR = "Error: invalid value of variable. Variable must be a single character of any letter of English alphabet."
class Transaction:
    def __init__(self, transaction_number: int, operation: str, variable: str):
        self.transaction_number = transaction_number
        self.operation = operation
        self.variable = variable

    @staticmethod
    def parse_transaction(t_str: str, number_of_transactions: int):
        t, op = t_str.split('.', 1)
        transaction_num = t[1:]
        func = op[0].upper()
        var = op[2].upper()

        if t[0].upper() != 'T' or int(transaction_num) > number_of_transactions:
            raise ValueError(INVALID_TRANSACTION_ERROR)

        if func not in ('R', 'W'):
            raise ValueError(INVALID_OPERATION_ERROR)

        if not var.isalpha():
            raise ValueError(INVALID_VALUE_OF_VAR_ERROR)

        return Transaction(int(transaction_num)-1, func, var)

def print_menu():
    print("Following will be printed in order for the given schedule: \n")
    print("1. Print schedule chart")
    print("2. Check if the given schedule is serial")
    print("3. Check if the given schedule is conflict serializable")
    print("4. Check if the given schedule is view serializable\n")

def print_transactions_table(*txns):
    txn = PrettyTable()
    txn.field_names = [f"T{i + 1}" for i in range(len(txns))]

    for i in range(len(txns[0])):
        data = list()
        for j in range(len(txns)):
            data.append(txns[j][i])
        txn.add_row(data)

    print(txn)

def get_positive_integer_input(message):
    while True:
        num = input(message)
        if num.strip() == "" or not num.isdigit() or int(num) <= 0:
            print(INVALID_NUMBER_OF_TRANSACTIONS)
        else:
            return int(num)

INVALID_NUMBER_OF_TRANSACTIONS = "Error: invalid number of transactions!"
ENTER_NUMBER_OF_TRANSACTIONS_MESSAGE = "Enter number of transactions: "
DONE_WITH_ENTERING_TRANSACTIONS_COMMAND = "done"
ENTER_TRANSACTIONS_INFO_MESSAGE = f"Enter transactions in the chronological order in the following format \n\n\t\tT[transaction number].[read or write operation]([variable])\n\t\tFor example: T1.R(A) or T2.W(b) or t3.r(a).\n\nOr \'{DONE_WITH_ENTERING_TRANSACTIONS_COMMAND}\' if you've typed all transactions. Case-insensitive.\n"
def create_transactions():
    number_of_transactions = get_positive_integer_input(ENTER_NUMBER_OF_TRANSACTIONS_MESSAGE)
    txns, actions, data_items = [[] for _ in range(number_of_transactions)], [[] for _ in range(number_of_transactions)], [[] for _ in range(number_of_transactions)]

    print(ENTER_TRANSACTIONS_INFO_MESSAGE)

    transaction = None
    while True:
        choice = input("Enter transaction: ").strip()

        if choice.lower() == DONE_WITH_ENTERING_TRANSACTIONS_COMMAND:
            break
        
        try:
            transaction = Transaction.parse_transaction(choice, number_of_transactions)
        except ValueError as e:
            print(e)
            continue
        
        actions[transaction.transaction_number].append(transaction.operation)
        data_items[transaction.transaction_number].append(transaction.variable)
        txns[transaction.transaction_number].append(transaction.operation + f"({transaction.variable})")

        for i in range(number_of_transactions):
            if transaction.transaction_number != i:
                actions[i].append("*")
                data_items[i].append("*")
                txns[i].append("*")
        print_transactions_table(*txns)

    return txns

def do_serial_check(*txns):
    graph = nx.DiGraph()
    order = list()
    error = 0

    for i in range(len(txns[0])):
        for j in range(len(txns)):
            if txns[j][i] != "*":
                if not order:
                    order.append(f"T{j + 1}")
                else:
                    if f"T{j + 1}" in order:
                        if order[-1] == f"T{j + 1}":
                            pass
                        else:
                            order.append(f"T{j + 1}")
                            error = 1
                    else:
                        order.append(f"T{j + 1}")

    nodes = [f"T{i + 1}" for i in range(len(txns))]
    graph.add_nodes_from(nodes)
    edges = [(order[i], order[i + 1]) for i in range(len(order) - 1)]
    graph.add_edges_from(edges)

    try:
        nx.planar_layout(graph)
    except nx.exception.NetworkXException:
        pass

    if not error:
        print("The given schedule is serial schedule. See image.\n")
        plt.title("Serial Schedule", fontsize=10, color="red")
        nx.draw(graph, with_labels=True, node_size=1500, font_size=20, font_color="yellow", font_weight="bold", connectionstyle='arc3, rad = 0.1')
        plt.show()
    else:
        print("The given schedule is not a serial schedule.\n")
        plt.title("NOT a Serial Schedule", fontsize=10, color="red")
        nx.draw(graph, with_labels=True, node_size=1500, font_size=20, font_color="yellow", font_weight="bold", connectionstyle='arc3, rad = 0.1')
        plt.show()

def blind_write(dataset, *txns):
    for d in dataset:
        for i in range(len(txns)):
            read_check = 0
            for j in range(len(txns[0])):
                if txns[i][j] == "*":
                    continue
                if txns[i][j][2] == d:
                    if txns[i][j][0] == "R":
                        read_check = 1
                    if txns[i][j][0] == "W":
                        if read_check == 0:
                            return 1
                        else:
                            break

    return 0

def do_conflict_serializability_check(*txns):
    edges = list()
    for i in range(len(txns)):
        flag = 0
        for j in range(len(txns[0])):
            if flag:
                break
            if txns[i][j] != "*":
                if txns[i][j][0] == "W":
                    for m in range(len(txns)):
                        if m == i:
                            continue
                        for n in range(j + 1, len(txns[0])):
                            if txns[m][n] == "*":
                                continue
                            if txns[i][j][2] == txns[m][n][2]:
                                if (f"T{i + 1}", f"T{m + 1}") not in edges:
                                    edges.append((f"T{i + 1}", f"T{m + 1}"))
                                flag = 1
                                break
                if txns[i][j][0] == "R":
                    for m in range(len(txns)):
                        if m == i:
                            continue
                        for n in range(j + 1, len(txns[0])):
                            if txns[m][n] == "*" or txns[m][n][0] == "R":
                                continue
                            if txns[i][j][2] == txns[m][n][2]:
                                if (f"T{i + 1}", f"T{m + 1}") not in edges:
                                    edges.append((f"T{i + 1}", f"T{m + 1}"))
                                flag = 1
                                break

    graph = nx.DiGraph()
    graph.add_nodes_from([f"T{i + 1}" for i in range(len(txns))])
    graph.add_edges_from(edges)

    try:
        nx.planar_layout(graph)
    except nx.exception.NetworkXException:
        pass

    try:
        nx.find_cycle(graph)
        plt.title("Not Conflict Serializable", fontsize=10, color="red")
        print("This schedule is not Conflict Serializable.\n")
        nx.draw(graph, with_labels=True, node_size=1500, font_size=20, font_color="yellow", font_weight="bold", connectionstyle='arc3, rad = 0.1')
        plt.show()
        return 1, graph
    except nx.exception.NetworkXNoCycle:
        plt.title(f"Conflict Serializable: <{','.join(nx.topological_sort(graph))}>", fontsize=10, color="red")
        print(f"This schedule is Conflict Serializable and Conflict Equivalent to <{','.join(nx.topological_sort(graph))}>. See image.\n")
        plt.show()
        return 0, ""

def do_view_serializability_check(conflict_status, graph_status, *txns):
    dataset = set([txns[i][j][2] for i in range(len(txns)) for j in range(len(txns[0])) if txns[i][j] != "*"])
    edges = list()

    for d in dataset:
        update_list = list()
        first_reads = list()
        last_update = ""
        for i in range(len(txns[0])):
            for j in range(len(txns)):
                if txns[j][i] == "*":
                    continue
                if txns[j][i][2] == d:
                    if txns[j][i][0] == "W":
                        update_list.append(f"T{j + 1}")
                        last_update = f"T{j + 1}"
                    if txns[j][i][0] == "R":
                        if not last_update:
                            first_reads.append(f"T{j + 1}")
                        else:
                            edges.append((last_update, f"T{j + 1}"))

        update_list_read = list(set(update_list) - set(first_reads))
        update_list = list(set(update_list))

        if first_reads:
            edges.extend([(x, y) for x in first_reads for y in update_list_read if x != y])
        if last_update:
            edges.extend([(x, last_update) for x in update_list if x != last_update])

    edges = [(e[0], e[1]) for e in edges if e[0] != e[1]]
    edges = list(set(edges))
    graph = nx.DiGraph()
    graph.add_nodes_from([f"T{x + 1}" for x in range(len(txns))])
    graph.add_edges_from(edges)

    if conflict_status and not blind_write(dataset, *txns):
        graph.clear()
        print("There is no Blind Write!")
        graph = graph_status

    try:
        nx.planar_layout(graph)
    except nx.exception.NetworkXException:
        pass

    try:
        nx.find_cycle(graph)
        plt.title("Not View Serializable", fontsize=10, color="red")
        print("This schedule is not View Serializable.\n")
        nx.draw(graph, with_labels=True, node_size=1500, font_size=20, font_color="yellow", font_weight="bold", connectionstyle='arc3, rad = 0.1')
    except nx.exception.NetworkXNoCycle:
        plt.title(f"View Serializable: <{','.join(nx.topological_sort(graph))}>", fontsize=10, color="red")
        print(f"This schedule is View Serializable and View Equivalent to <{','.join(nx.topological_sort(graph))}>\n. See image.")
        nx.draw(graph, with_labels=True, node_size=1500, font_size=20, font_color="yellow", font_weight="bold", connectionstyle='arc3, rad = 0.1')

    plt.show()

if __name__ == "__main__":
    while 1:
        print_menu()
        print("Please follow the instructions to enter your values for schedule.\n")
        schedule = create_transactions()
        #print_transactions_table(*schedule)

        do_serial_check(*schedule) # checks whether the given transactions are already serial.
        conflict = do_conflict_serializability_check(*schedule) # checks conflict serializability
        do_view_serializability_check(conflict[0], conflict[1], *schedule) # checks view serializability