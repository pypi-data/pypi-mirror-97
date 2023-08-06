class node: 
    
    """A class to create blueprints of the nodes in the Bayesian Network.""" 
    
    def __init__(self, name, parents, CPT): 
        
        """
        Constructs the required attributes for the node being created
        
        Parameters
        -----------
        name : str 
            Name of the node being created 
            
        parents : list 
            List of the nodes' parents. Note that the names of the parents in a list should not be entered as strings. 
            
        CPT : dict 
            Nested dictonary defining the conditional probability table of the node given its parents. 
        
        """
        
        self.name = name
        self.parents = parents
        self.CPT = CPT


class model: 
    
    """A class used to build up the bayesian network by adding nodes and extract probabilities"""
    
    def __init__(self): 
        
        self.nodes = {}
        
          
    def add_node(self, node):
        
        self.nodes[node.name] = node
        
        
    def list_possibilities(self, nodes):
        
        """Constructs a list of the state of all possible combinations of the input nodes""" 
        
        l = []
        
        if len(nodes) > 0: 
            
            remaining = self.list_possibilities(nodes[1: ])
                        
            for possibility in remaining: 
                
                newposs = possibility.copy()
                
                newposs[nodes[0].name] = True 
                
                l.append(newposs)
                
                newposs = possibility.copy()
                
                newposs[nodes[0].name] = False 
                
                l.append(newposs)
              
            if len(remaining) == 0: 
                l.append({nodes[0].name: True })
                l.append({nodes[0].name: False })

        return l 
    
            
    def joint(self, inferred_nodes):
        
        """
        Calculates the joint probability of certain input nodes being in a certain input state.
        
        Parameters
        ----------
        inferred_nodes : dict
            the names of the nodes and their state in one dictonary      
            
        Returns 
        ---------
        Joint probability of the inferred nodes rounded to 4 decimal places. 
        
        """
        
        remaining_nodes = []
        
        for name in self.nodes: 
            if name not in inferred_nodes:
            
                remaining_nodes.append(self.nodes[name])
     
        possibilities = self.list_possibilities(remaining_nodes) 
                          
        if len(possibilities) == 0: 
            possibilities.append({})
               
        for name in inferred_nodes: 
            
            for i in range(len(possibilities)): 
                
                possibilities[i][name] = inferred_nodes[name]                
            
        prob = 0 
        
        for possibility in possibilities: 
            
            p = 1 
            
            for name in self.nodes: 
                node = self.nodes[name]
                parents_values = {}
                
                for parent in node.parents:
                    parents_values[parent.name] = possibility[parent.name] 
                
                cp = node.CPT 
                
                for i in parents_values: 
                    
                    cp = cp[parents_values[i]]
                    
                cp = cp[possibility[name]]
            
                p *= cp             
                
            prob += p 
    
        return round(prob, 4)
    
    
    def conditional(self, inferred_nodes, observed_nodes):
        
        """
        Calculates the conditional probability of certain input nodes being in a certain
        state given that other nodes are known to be in certain other prescribed states.
        
        Parameters
        ----------
        inferred_nodes : dict
            the name of the node and its state in a dictonary
            
        observed_nodes : dict
            the name of the node and its state in a dictonary
            
        Returns 
        ---------
        Conditional probability rounded to 4 decimal places. 
        
        """
        prob = 1 
        
        empty_dict = {}

        for keys in inferred_nodes:
            empty_dict[keys] =  inferred_nodes[keys]

        for keys in observed_nodes: 
            
            if keys in inferred_nodes and inferred_nodes[keys] != observed_nodes[keys]:
                prob=0


            empty_dict[keys] =  observed_nodes[keys]
        
        prob *= self.joint(empty_dict) / self.joint(observed_nodes)
        
        

        return round(prob, 4)