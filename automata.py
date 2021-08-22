class State:

    tag = "T_"
    transition = {}

    def __init__(self, state_count):
        self.tag += str(state_count)

    def add_path(self, path, condition):
        self.transition[path] = condition

    def __str__(self):
        return self.tag


class Automata:

    STATE_LIST = {}

    STARTPOINT = 0
    ENDPOINT = 0

    CUR_STATE = 0

    def __init__(self):
        self.STARTPOINT = self.create_state()

    def create_state(self, state_count=-1):
        if len(str(state_count).split("_")) > 1:
            state_count = int(state_count.split("_")[-1])
        if state_count == -1:
            state_tag_c = [int(x.split('_')[-1]) for x in self.STATE_LIST.keys()]
            state_tag_c.sort()

            if len(state_tag_c) > 1:
                for i in range(1,len(state_tag_c)):
                    if state_tag_c[i] - state_tag_c[i-1] != 1:
                        state_count = state_tag_c[i-1] + 1
                        break
                if state_count == -1:
                    if (state_tag_c[-1]) < len(state_tag_c):
                        state_count = state_tag_c[-1] + 1
            elif len(state_tag_c) == 1:
                state_count = 1
            else:
                state_count = 0
        if "T_"+str(state_count) not in self.STATE_LIST.keys():
            self.STATE_LIST["T_" + str(state_count)] = State(state_count)
        return self.STATE_LIST["T_"+str(state_count)]

    def add_transition(self, from_tag, to_tag, condition):
        if from_tag not in self.STATE_LIST.keys():
            print("Parent State not present. Please create the parent state before adding the transition.")
            return
        else:
            self.STATE_LIST[from_tag].add_path("0_0", condition)
        if to_tag not in self.STATE_LIST.keys():
            print("Travelling end point not present, Creating one.")
            self.create_state(to_tag)
        FROM_FLAG = False
        TO_FLAG   = False

    def set_endpoint(self, tag):
        if len(str(tag).split("_")) == 1:
            tag = "T_" + str(tag)
        if tag in self.STATE_LIST.keys():
            self.STARTPOINT = self.STATE_LIST[tag]

    def set_endpoint(self, tag):
        if len(str(tag).split("_")) == 1:
            tag = "T_" + str(tag)
        if tag in self.STATE_LIST.keys():
            self.ENDPOINT = self.STATE_LIST[tag]

    def run(self, input):
        self.CUR_STATE = self.STARTPOINT


        if self.CUR_STATE == self.ENDPOINT:
            print("The input data passed the checks, system is compatible.")
        else :
            print("Unable to reach the end point, please recheck the transitions. CUR_STATE :", self.CUR_STATE)

    def __str__(self):
        if self.ENDPOINT == 0:
            return "Emdpoint not set. Use set_endpoint(<state>) to do so."
        return_data = "\n".join(self.STATE_LIST.keys())
        return_data += "\n\nSTART_POINT : " + self.STARTPOINT.tag
        return_data += "\nEND_POINT   : " + self.ENDPOINT.tag
        return return_data
