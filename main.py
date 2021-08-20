from automata import Automata

autoM = Automata()

autoM.create_state(0)
autoM.add_transition("T_0", "T_6", "0-9")
autoM.create_state(1)
autoM.add_transition("T_0", "T_1", "0-9")
autoM.add_transition("T_1", "T_1", "0-9")
autoM.add_transition("T_1", "T_5", "0-9")
autoM.add_transition("T_1", "T_2", "0-9")
autoM.create_state(2)
autoM.add_transition("T_2", "T_3", "0-9")
autoM.create_state(3)
autoM.add_transition("T_3", "T_4", "0-9")
autoM.create_state(4)
autoM.create_state("T_5")
autoM.add_transition("T_2", "T_1", "0-9")
autoM.add_transition("T_6", "T_2", "0-9")
autoM.add_transition("T_5", "T_3", "0-9")

print(autoM)
