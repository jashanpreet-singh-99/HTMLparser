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

    STATE_LIST = []

    STARTPOINT = 0
    ENDPOINT = 0

    def __init__(self):
        self.create_state()
        self.STARTPOINT = "T_0"

    def create_state(self, state_count=-1):
        if len(str(state_count).split("_")) > 1:
            state_count = int(state_count.split("_")[-1])
        if state_count == -1:
            state_tag_c = [int(x.tag.split('_')[-1]) for x in self.STATE_LIST]
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
        state_tag = [x.tag for x in self.STATE_LIST]
        if "T_"+str(state_count) not in state_tag:
            self.STATE_LIST.append(State(state_count))

    def add_transition(self, from_tag, to_tag, condition):
        FROM_FLAG = False
        TO_FLAG   = False
        for state in self.STATE_LIST:
            if state.tag == from_tag:
                FROM_FLAG = True
                state.add_path("0_0", condition)
            if state.tag == to_tag:
                TO_FLAG = True
        if not FROM_FLAG:
            print("Parent State not present. Please create the parent state before adding the transition.")
            return
        if not TO_FLAG :
            print("Travelling end point not present, Creating one.")
            self.create_state(to_tag.split("_")[-1])

    def set_endpoint(self, tag):
        if len(str(tag).split("_")) == 1:
            tag = "T_" + str(tag)
        state_tag = [x.tag for x in self.STATE_LIST]
        if tag in state_tag:
            self.STARTPOINT = tag

    def set_endpoint(self, tag):
        if len(str(tag).split("_")) == 1:
            tag = "T_" + str(tag)
        state_tag = [x.tag for x in self.STATE_LIST]
        if tag in state_tag:
            self.ENDPOINT = tag

    def run(self, input):
        pass

    def __str__(self):
        state_tag = [x.tag for x in self.STATE_LIST]
        return_data = "\n".join(state_tag)
        return_data += "\n\nSTART_POINT : " + self.STARTPOINT
        return_data += "\nEND_POINT   : " + self.ENDPOINT
        return return_data
