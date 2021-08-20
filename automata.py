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

    def __init__(self):
        self.create_state()

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
        # state_tag = [x.tag for x in self.STATE_LIST]
        # if from_tag not in state_tag:
        #     print("Parent State not present. Please create the parent state before adding the transition.")
        # else:
        #     if to_tag not in state_tag:
        #         self.create_state(to_tag.split("_")[-1])
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


    def __str__(self):
        state_tag = [x.tag for x in self.STATE_LIST]
        return "\n".join(state_tag)
