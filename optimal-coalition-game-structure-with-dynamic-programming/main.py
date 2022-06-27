class CoalitionGeneration:

    def __init__(self, n, ch_function):
        self.n = n  
        self.final_coalition = []  
        self.discard = set() 
        self.chf_table = ch_function  

    def determine_optimal_coalition(self):

        while(len(self.discard) != self.n):
            self.locate_coalition()

    def locate_coalition(self):
        global payoff
        global optimal
        payoff = 0
        optimal = set()
        for x in range(self.n):
            if x in self.discard:
                continue

            t_payoff, t_optimal = self.calculate_opt_si(x)
            if (t_payoff > payoff):
                payoff = t_payoff
                optimal = t_optimal

        for x in optimal:
            self.discard.add(x)

        self.final_coalition.append(optimal)


    def calculate_opt_si(self, i):
        global payoff 
        
        global optimal  
        
        payoff = 0
        optimal = set()


        for coalition, _ in self.chf_table.items():
            d = set(coalition) 
            
            if i in coalition and len(d.intersection(self.discard)) == 0:
                if (self.chf_table[coalition]/(len(coalition)) > payoff):
                    optimal = coalition
                    payoff = self.chf_table[coalition]/len(coalition)



        return payoff, optimal


    def print_optimal_coalition(self):
        print("Final optimal coalition: ")
        for coalition in self.final_coalition:
            print(coalition)
        print('\n')

if __name__ == "__main__":

    file_name = str(input("Enter TXT File Name:\n"))

    print(file_name)

    import re

    C_i = []

    myfile = open(file_name, "r")
    for line in myfile:
        C_i.append( re.findall('[0-9]+', line))
    myfile.close()

    num_agents = int(C_i[0][0])

    C_integers = []
    for i,val in enumerate(C_i):
        C_integers.append(list(map(int, C_i[i])))
    
    C_i = C_integers

    values = []

    for i, val in enumerate(C_i):
        values.append(val[-1])
        val.pop()

    values = values [1:]

    C_i = C_i[1:]

    C_tuple = []

    for i in C_i:
        C_tuple.append(tuple(i))

    dictionary_map = dict(zip(C_tuple,values))

    print(dictionary_map)

    print("\n\n")



    #dic = {(1,): 30, (2,): 40, (3,): 25, (4,): 45, (1, 2): 50, (1, 3): 60, (1, 4): 80, (2, 3): 55, (2, 4): 70, (3, 4): 80, (1, 2, 3): 90, (1, 2, 4): 120, (1, 3, 4): 100, (2, 3, 4): 115, (1, 2, 3, 4): 140}



    coalition_obj = CoalitionGeneration(num_agents, dictionary_map)
    coalition_obj.determine_optimal_coalition()
    optimal_coalition = coalition_obj.final_coalition

    total_val = 0
    k = 0

    while k < len(optimal_coalition):
        if dictionary_map[optimal_coalition[k]]:
            total_val += dictionary_map[optimal_coalition[k]]
        k+=1

    coalition_obj.print_optimal_coalition()
    print("Value:")
    print(total_val)

    with open('optimalCS.txt', 'w') as f:
        f.write(str(total_val))
        f.write("\n")
        for item in optimal_coalition:
            f.write("{")
            f.write(str(item))
            f.write("}")
            f.write("\n")

    print("\nFile optimalCS.txt written successfully!")

    print("\n")
