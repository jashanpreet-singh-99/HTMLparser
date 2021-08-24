import re

class State:

    def __init__(self, state_count):
        self.tag = "T_" + str(state_count)
        self.transition = {}

    def add_path(self, path, condition, action):
        self.transition[path] = (condition, action)

    def next_transition(self, input):
        for path,value in self.transition.items():
            condition = value[0]
            action = value[1]
            if re.match(condition, input):
                #print(path, input, ": PASS :", self.tag, condition, action)
                if action:
                    action(input)
                return "T_" + path.split('_')[-1]
            else:
                pass
                #print(path, input, ": FAILED :", self.tag, condition)
        print("Deadlock no transition for input :", input, self.tag)

    def __str__(self):
        return self.tag + str(self.transition)


class Automata:

    def __init__(self):
        self.STATE_LIST = {}
        self.ENDPOINT = 0
        self.CUR_STATE = 0
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

    def add_transition(self, from_tag, to_tag, condition, function=None):
        if from_tag not in self.STATE_LIST.keys():
            print("Parent State not present. Please create the parent state before adding the transition.")
            return
        else:
            self.STATE_LIST[from_tag].add_path(from_tag.split("_")[-1] + "_" + to_tag.split("_")[-1], condition, function)
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

        for ch in input:
            next_state = self.CUR_STATE.next_transition(ch)
            self.CUR_STATE = self.STATE_LIST[next_state]

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
