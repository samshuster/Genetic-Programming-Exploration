'''
Created on Apr 24, 2011

@author: Sam
'''
#!/usr/bin/python
import Tkinter as T
import tkMessageBox
import experiment
from experiment_exceptions import InputError

class ExperimentFrame(T.LabelFrame):
    """ Class to aid in GUI display """
    def __init__(self, parent, text, orientation, entry_default, variable, 
                 **kwargs):
        T.LabelFrame.__init__(self, parent, bd = 2, text = text)
        self.text = text
        self.width = 7
        for k in kwargs:
            if k == "width":
                self.width = kwargs[k]
        self.variable = variable
        self.orientation = orientation
        self.entry_default = entry_default  
        self.setup()
    
    def __call__(self):
        return {self.key():self.value()} 
       
    def setup(self):
        """ setup Widget """
        #self.label = T.Label(self, text=self.text)
        #self.label.pack( side = T.LEFT)
        self.entry = T.Entry(self, bd = 2,
                              width = self.width)
        self.entry.insert(T.INSERT, self.entry_default)
        self.entry.pack(side = T.TOP)
        self.pack(side = self.orientation, ipadx = 3, ipady = 3, padx = 5,
                  pady = 5)
        
    def key (self):
        """ Return key for **dict """
        return self.variable
    
    def value (self):
        """ Return value for ** dict """
        return self.entry.get()



ROOT = T.Tk()
ROOT.title("MicroGP")
EXP = experiment.Experiment()
INTVERTICALPADDING = 5
INTHORIZONTALPADDING = 10
VERTICALPADDING = 10
HORIZONTALPADDING = 10

#List for storing the params
PARAM = []

# Code to add widgets will go here...

def start_experiment():
    """ Start a microgp experiment """
    check_parameters()
    try:
        EXP.start()
    except InputError as inst:
        tkMessageBox.showinfo(inst.expr, inst.msg)
        
def check_parameters():
    """ Ask experiment class to check for param validity """
    for par in PARAM:
        if isinstance(par, ExperimentFrame):
            EXP.change_variable(**par())
        else:
            EXP.change_variable(**par)

def get_instructions():
    """ Loads readme file """
    readme = T.Toplevel(ROOT)
    readme.title("Instructions")
    
    try:
        inst_file = open("readme.txt")
    except IOError:
        tkMessageBox.showinfo("No Instruction File", 
                              "readme.txt could not be found")
    else:
        string_text = []
        while 1:
            line = inst_file.readline()
            if not line:
                break
            else:
                string_text.append(line)
        temp = ''.join(string_text)
        text = T.Label(readme, text = temp)
        text.pack()
            
        

#Frame organization

def build_initial() :
    """ Build initial framework of GUI """
    titleframe = T.Frame(ROOT)
    TITLE = T.Label(titleframe, text = "Welcome to Microgp!")
    var = T.StringVar()
    INSTRUCTIONS = T.Message(titleframe, textvariable = var, width = 100)
    var.set("By Erik and Sam")
    instruct_b = T.Button(titleframe, text = "Instructions",
                            command = get_instructions)
    instruct_b.pack(side = T.BOTTOM)
    TITLE.pack(side = T.TOP)
    INSTRUCTIONS.pack(side = T.BOTTOM)
    titleframe.pack()
    
def build_basic_frame():
    """Build Basic Framework for GUI"""
    param_frame = T.LabelFrame(ROOT, text = "Set Basic Experiment Parameters")
    pop_frame = ExperimentFrame(param_frame, "Population Size: ",
                           T.LEFT, EXP.pop_size, "pop_size")
    PARAM.append(pop_frame)
    gen_frame = ExperimentFrame(param_frame, "Number of Generations: ",
                           T.LEFT, EXP.num_generations, "num_generations")
    PARAM.append(gen_frame)
    max_depth_frame = ExperimentFrame(param_frame, "Max Depth of Tree: ", 
                                T.LEFT, EXP.max_depth, "max_depth")
    PARAM.append(max_depth_frame)
      
    selection_frame = T.LabelFrame(param_frame, text = "Selection Method")
    select_var = {"s_selection" : "greedy"}
    PARAM.append(select_var)
    def select():
        """ SelectionMethod Radio Button """
        PARAM.remove(select_var)
        select_var["s_selection"] = textv.get()
        PARAM.append(select_var)
    modes = [
        ("Greedy Selection", "greedy")
        #("Tournament Selection", "tournament"),
    ]
    textv = T.StringVar()
    for text, mode in modes:
        select_b = T.Radiobutton(selection_frame, text = text,
                        variable = textv, value = mode, command = select)
        select_b.pack(anchor=T.W)
    textv.set("greedy") # initialize
    selection_frame.pack(side = T.RIGHT)
    
    
    selection_frame2 = T.LabelFrame(param_frame, text = "Tree Type")
    
    tree_var = {"t_type" : "grow"}
    PARAM.append(tree_var)
    def treeselect():
        """ SelectionMethod Radio Button """
        tree_var["t_type"] = treev.get()
    modes = [
        ("Grow Tree", "grow"),
        ("Full Tree", "full"),
    ]
    treev = T.StringVar()
    for text, mode in modes:
        select_b = T.Radiobutton(selection_frame2, text = text,
                        variable = treev, value = mode, command = treeselect)
        select_b.pack(anchor=T.W)
    treev.set("grow") # initialize
    
    selection_frame2.pack(side = T.RIGHT)
    
    param_frame.pack(side = T.TOP, ipadx = INTHORIZONTALPADDING,
                      ipady = INTVERTICALPADDING, padx = HORIZONTALPADDING,
                      pady = VERTICALPADDING)
    

def build_rates_frame():
    """Build Rates Frame segment of GUI"""
    rate_frame = T.LabelFrame(ROOT,
                              text = "Set Reproduction Rates")
    mrate_frame = ExperimentFrame(rate_frame,
                               "Mutation Rate: ",
                              T.LEFT, EXP.m_rate_const, "m_rate")
    PARAM.append(mrate_frame)
    crate_frame = ExperimentFrame(rate_frame,
                               "Crossover Rate: ",
                              T.LEFT, EXP.c_rate_const, "c_rate")
    PARAM.append(crate_frame)
    erate_frame = ExperimentFrame(rate_frame,
                                 "Cloning Rate: ",
                                 T.LEFT, EXP.e_rate_const, "e_rate")
    PARAM.append(erate_frame)
    elite_frame = ExperimentFrame(rate_frame,
                                 "Elitism number: ",
                                 T.LEFT, EXP.elitism_num, "elitism_num")
    PARAM.append(elite_frame)
    rate_frame.pack(side = T.TOP, ipadx = INTHORIZONTALPADDING,
                     ipady = INTVERTICALPADDING, padx = HORIZONTALPADDING,
                     pady = VERTICALPADDING)

def build_constant_frame():
    """Build Constant Frame segment of GUI"""
    constant_frame = T.LabelFrame(ROOT, 
                                 text = "Set Constant Range for Individuals")

    conmin_frame = ExperimentFrame(constant_frame,
                               "Minimum Possible Constant Value: ",
                              T.LEFT, EXP.constant_min, "constant_min")
    PARAM.append(conmin_frame)
    conmax_frame = ExperimentFrame(constant_frame,
                               "Maximum Possible Constant Value: ",
                               T.LEFT, EXP.constant_max, "constant_max")
    PARAM.append(conmax_frame)
    connum_frame = ExperimentFrame(constant_frame,
                              "Number of Constant Values: ",
                              T.LEFT, EXP.constant_num, "constant_num")
    PARAM.append(connum_frame)
    constant_frame.pack(side = T.TOP, ipadx = INTHORIZONTALPADDING,
                        ipady = INTVERTICALPADDING, padx = HORIZONTALPADDING,
                        pady = VERTICALPADDING)

def build_fitness_frame():
    """Build Fitness Frame"""
    fitness_frame = T.LabelFrame(ROOT, 
                                 text = "Set Fitness Parameters")

    fitmin_frame = ExperimentFrame(fitness_frame,
                               "Minimum Fitness Testing Value: ",
                              T.LEFT, EXP.fitness_min, "fitness_min")
    PARAM.append(fitmin_frame)
    fitmax_frame = ExperimentFrame(fitness_frame,
                               "Maximum Fitness Testing Value: ",
                               T.LEFT, EXP.fitness_max, "fitness_max")
    PARAM.append(fitmax_frame)
    fitincr_frame = ExperimentFrame(fitness_frame,
                              "Fitness Increment: ",
                              T.LEFT, EXP.fitness_incr, "fitness_incr")
    PARAM.append(fitincr_frame)
    fitcutoff_frame = ExperimentFrame(fitness_frame,
                                   "Fitness Success Cutoff: ",
                                   T.LEFT, EXP.fitness_cutoff,
                                    "fitness_cutoff")
    PARAM.append(fitcutoff_frame)
    fitness_frame.pack(side = T.TOP, ipadx = INTHORIZONTALPADDING,
                        ipady = INTVERTICALPADDING, padx = HORIZONTALPADDING,
                        pady = VERTICALPADDING)

def build_fitfunc_frame():
    """Build fit_func frame"""
    fitfunc_frame = ExperimentFrame(ROOT,
                                   "Target Function: ",
                                   T.LEFT, EXP.target_func, "target_func",
                                   **{"width" : 50})
    PARAM.append(fitfunc_frame)
    
def build_start_frame():
    """ Build start frame """
    start_frame = T.Frame(ROOT)
    start_button = T.Button(start_frame, text ="Start Experiment",
                        command = start_experiment)
    start_button.pack()
    start_frame.pack(side = T.LEFT)



#Build Logic
build_initial()
build_basic_frame()
build_rates_frame()
build_constant_frame()
build_fitness_frame()
build_fitfunc_frame()
build_start_frame()
ROOT.mainloop()
