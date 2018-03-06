stmt = '''
import evolution_cycle_nocomp as evol
import plotting as p
import csv
import numpy as np
import collections as col
import precision_calc as prc

# log_toy = {
#     'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
#     'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
#     'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
#     'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}
# amtlog_toy = len(log_toy)
# amtlog = amtlog_toy
# full_logfabio2m = log_toy

log_5alunos_100traces = col.OrderedDict([(194, ['E', 'D', 'D', 'D', 'D', 'D', 'C', 'A']), (487, ['E', 'D', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'A']), (367, ['E', 'D', 'D', 'B', 'B', 'B', 'B', 'F', 'D', 'C', 'A']), (336, ['E', 'D', 'N', 'A']), (522, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (490, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'D', 'B', 'B', 'A']), (23, ['E', 'D', 'A']), (34, ['E', 'D', 'D', 'D', 'D', 'B', 'C', 'C', 'D', 'B', 'D', 'D', 'D', 'A']), (577, ['E', 'D', 'D', 'D', 'D', 'D', 'B', 'D', 'A']), (418, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'A']), (171, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'A']), (377, ['E', 'D', 'F', 'F', 'A']), (466, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'C', 'A']), (327, ['E', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'C', 'C', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'C', 'D', 'C', 'D', 'B', 'B', 'C', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'B', 'C', 'D', 'D', 'B', 'B', 'A']), (551, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'C', 'C', 'D', 'C', 'D', 'B', 'A']), (290, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (398, ['E', 'D', 'D', 'C', 'C', 'A']), (282, ['E', 'D', 'D', 'F', 'D', 'D', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'A']), (452, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (29, ['E', 'D', 'F', 'D', 'G', 'C', 'D', 'D', 'D', 'D', 'B', 'B', 'A']), (165, ['E', 'D', 'D', 'F', 'D', 'H', 'H', 'A']), (21, ['E', 'D', 'D', 'D', 'A']), (331, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'A']), (77, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'A']), (462, ['E', 'D', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'A']), (43, ['E', 'A']), (309, ['E', 'C', 'A']), (469, ['E', 'D', 'D', 'D', 'C', 'C', 'A']), (267, ['E', 'D', 'D', 'F', 'A']), (160, ['E', 'D', 'D', 'H', 'I', 'H', 'D', 'H', 'D', 'D', 'D', 'B', 'D', 'H', 'I', 'H', 'D', 'C', 'G', 'F', 'D', 'D', 'D', 'A']), (510, ['E', 'D', 'F', 'D', 'A']), (236, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'A']), (272, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (473, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'A']), (169, ['E', 'D', 'B', 'D', 'D', 'D', 'C', 'C', 'C', 'B', 'D', 'D', 'D', 'K', 'F', 'A']), (264, ['E', 'D', 'D', 'C', 'C', 'F', 'D', 'D', 'A']), (277, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (576, ['E', 'D', 'F', 'D', 'A']), (215, ['E', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'A']), (372, ['E', 'D', 'F', 'F', 'F', 'F', 'F', 'A']), (120, ['E', 'D', 'D', 'D', 'D', 'A']), (104, ['E', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'A']), (139, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'B', 'A']), (532, ['E', 'D', 'D', 'C', 'G', 'A']), (254, ['E', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (411, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'B', 'D', 'C', 'D', 'A']), (426, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'B', 'D', 'D', 'A']), (572, ['E', 'D', 'D', 'F', 'A']), (444, ['E', 'D', 'D', 'K', 'D', 'H', 'A', 'D', 'A']), (301, ['E', 'D', 'D', 'D', 'B', 'B', 'D', 'D', 'A']), (575, ['E', 'D', 'D', 'D', 'B', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (563, ['E', 'D', 'D', 'F', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'A']), (524, ['E', 'D', 'D', 'D', 'C', 'C', 'A']), (258, ['E', 'D', 'F', 'D', 'C', 'G', 'D', 'D', 'A']), (549, ['E', 'D', 'D', 'C', 'G', 'D', 'A']), (457, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'A']), (406, ['E', 'D', 'F', 'F', 'D', 'H', 'H', 'H', 'H', 'H', 'I', 'I', 'H', 'D', 'H', 'I', 'D', 'H', 'D', 'H', 'H', 'D', 'C', 'D', 'A']), (292, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'D', 'A']), (58, ['E', 'D', 'D', 'D', 'B', 'B', 'D', 'C', 'C', 'A']), (440, ['E', 'D', 'F', 'A']), (542, ['E', 'D', 'F', 'D', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (540, ['E', 'D', 'D', 'H', 'H', 'I', 'H', 'H', 'A']), (232, ['E', 'B', 'A']), (25, ['E', 'M', 'A']), (311, ['E', 'D', 'D', 'A']), (295, ['E', 'D', 'D', 'C', 'C', 'C', 'A']), (149, ['E', 'D', 'F', 'D', 'D', 'B', 'B', 'A']), (42, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'A']), (3, ['E', 'D', 'D', 'C', 'D', 'B', 'B', 'A']), (121, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (393, ['E', 'D', 'D', 'K', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (380, ['E', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'A']), (94, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'C', 'C', 'A']), (209, ['E', 'D', 'D', 'F', 'D', 'D', 'B', 'D', 'A']), (483, ['E', 'D', 'D', 'D', 'B', 'A']), (151, ['E', 'D', 'D', 'C', 'C', 'C', 'D', 'B', 'B', 'B', 'A']), (494, ['E', 'D', 'D', 'D', 'B', 'B', 'D', 'C', 'G', 'C', 'B', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'D', 'D', 'B', 'B', 'D', 'B', 'D', 'B', 'D', 'D', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'A']), (217, ['E', 'D', 'D', 'D', 'D', 'B', 'D', 'H', 'I', 'H', 'D', 'H', 'I', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'D', 'H', 'I', 'H', 'A']), (224, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'D', 'D', 'D', 'B', 'A']), (354, ['E', 'D', 'C', 'C', 'D', 'D', 'C', 'F', 'F', 'A']), (324, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'B', 'B', 'A']), (299, ['E', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'P', 'P', 'D', 'D', 'D', 'D', 'J', 'D', 'A']), (113, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'B', 'B', 'F', 'D', 'H', 'H', 'I', 'H', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'A']), (71, ['E', 'D', 'D', 'B', 'B', 'A']), (241, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'D', 'A']), (24, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'D', 'D', 'B', 'B', 'D', 'D', 'B', 'A']), (396, ['E', 'D', 'D', 'D', 'H', 'H', 'D', 'D', 'D', 'C', 'K', 'A']), (244, ['E', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'A']), (170, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'A']), (315, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (364, ['E', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'D', 'D', 'D', 'B', 'A']), (304, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'D', 'A']), (385, ['E', 'D', 'F', 'D', 'D', 'D', 'B', 'B', 'B', 'F', 'D', 'C', 'C', 'G', 'A']), (371, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'A']), (56, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'A']), (423, ['E', 'D', 'D', 'C', 'C', 'D', 'H', 'D', 'A']), (47, ['E', 'D', 'D', 'D', 'C', 'A']), (83, ['E', 'C', 'A']), (323, ['E', 'D', 'D', 'G', 'D', 'C', 'A']), (82, ['E', 'D', 'A'])])
log = log_5alunos_100traces
amtlog = len(log_5alunos_100traces)

# ETM_Configuration1 = col.OrderedDict({0: ('A', 'B', 'C', 'D', 'E', 'G'), 1: ('A', 'D', 'B', 'C', 'E', 'G'), 2: ('A', 'B', 'C', 'F', 'G'), 3: ('A', 'C', 'B', 'F', 'G'), 4: ('A', 'B', 'D', 'C', 'F', 'G'), 5: ('A', 'C', 'D', 'B', 'F', 'G'), 6: ('A', 'B', 'D', 'C', 'E', 'G'), 7: ('A', 'B', 'C', 'D', 'F', 'G'), 8: ('A', 'D', 'B', 'C', 'F', 'G'), 9: ('A', 'D', 'C', 'B', 'F', 'G'), 10: ('A', 'C', 'B', 'E', 'G')})
# amtlog = len(ETM_Configuration1)

# full_logfabio2m = col.OrderedDict([(0, ['E', 'D', 'D', 'C', 'D', 'D', 'A']), (1, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (2, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'D', 'A']), (3, ['E', 'M', 'P', 'P', 'P', 'D', 'D', 'C', 'D', 'C', 'D', 'A']), (4, ['E', 'D', 'D', 'D', 'D', 'B', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'A']), (5, ['E', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'A']), (6, ['E', 'D', 'N', 'A']), (7, ['E', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (8, ['E', 'D', 'D', 'A']), (9, ['E', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'B', 'B', 'A']), (10, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'C', 'D', 'C', 'C', 'D', 'B', 'B', 'B', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'A']), (11, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'A']), (12, ['E', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'O', 'D', 'A']), (13, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (14, ['E', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'A']), (15, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'A']), (16, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'A']), (17, ['E', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'D', 'A']), (18, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (19, ['E', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'A']), (20, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'C', 'A']), (21, ['E', 'D', 'D', 'D', 'A']), (22, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'A']), (23, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'A']), (24, ['E', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'A']), (25, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (26, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'A']), (27, ['E', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'D', 'A']), (28, ['E', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'A']), (29, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'A']), (30, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'A']), (31, ['E', 'D', 'D', 'D', 'C', 'D', 'A']), (32, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (33, ['E', 'D', 'A']), (34, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'J', 'J', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'A']), (35, ['E', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'A']), (36, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'C', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'C', 'A']), (37, ['E', 'D', 'C', 'C', 'D', 'D', 'C', 'D', 'B', 'D', 'A']), (38, ['E', 'D', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'H', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'A']), (39, ['E', 'D', 'D', 'D', 'D', 'A']), (40, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'A']), (41, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'A']), (42, ['E', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'A']), (43, ['E', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'Z', 'A']), (44, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'A']), (45, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'J', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'A']), (46, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'A']), (47, ['E', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'D', 'B', 'D', 'D', 'D', 'D', 'D', 'A']), (48, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'C', 'C', 'A']), (49, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (50, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'A']), (51, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'D', 'C', 'C', 'C', 'C', 'D', 'B', 'B', 'B', 'D', 'D', 'D', 'C', 'C', 'D', 'B', 'B', 'B', 'B', 'A']), (52, ['E', 'D', 'N', 'D', 'A']), (53, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (54, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'A']), (55, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (56, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'H', 'D', 'D', 'F', 'B', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'J', 'J', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'O', 'D', 'D', 'A']), (57, ['E', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'A']), (58, ['E', 'D', 'D', 'D', 'D', 'B', 'D', 'A']), (59, ['E', 'D', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'C', 'D', 'B', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'B', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'J', 'D', 'A']), (60, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'A']), (61, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (62, ['E', 'D', 'D', 'D', 'C', 'D', 'A']), (63, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'D', 'A']), (64, ['E', 'D', 'D', 'C', 'D', 'D', 'A']), (65, ['E', 'D', 'D', 'C', 'C', 'A']), (66, ['E', 'D', 'D', 'C', 'D', 'A']), (67, ['E', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'A']), (68, ['E', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'A']), (69, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'A']), (70, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'A']), (71, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (72, ['E', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (73, ['E', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'C', 'A']), (74, ['E', 'D', 'D', 'C', 'D', 'A']), (75, ['E', 'D', 'D', 'D', 'H', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'A']), (76, ['E', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'A']), (77, ['E', 'D', 'N', 'N', 'N', 'N', 'A']), (78, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A'])])
## This is the full pack used to test proM's ETMd


# full_logfabio2m = col.OrderedDict([(0, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'C', 'A']), (1, ['E', 'D', 'D', 'C', 'D', 'A']), (2, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'C', 'C', 'A']), (3, ['E', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'D', 'A']), (4, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (5, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'A']), (6, ['E', 'D', 'D', 'D', 'D', 'A']), (7, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'H', 'D', 'D', 'F', 'B', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'J', 'J', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'O', 'D', 'D', 'A']), (8, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'J', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'A']), (9, ['E', 'D', 'D', 'D', 'H', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'A'])])
# amtlog = len(full_logfabio2m)
## This one is a 10 pack used to test proM's ETMd

# full_logfabio2m = col.OrderedDict([(0, ['E', 'D', 'D', 'C', 'D', 'D', 'A']), (1, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (2, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (3, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'C', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'C', 'A']), (4, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (5, ['E', 'D', 'D', 'C', 'D', 'A']), (6, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'C', 'A']), (7, ['E', 'D', 'D', 'D', 'D', 'B', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'A']), (8, ['E', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'A']), (9, ['E', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'Z', 'A']), (10, ['E', 'D', 'D', 'D', 'C', 'D', 'A']), (11, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'A']), (12, ['E', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'D', 'B', 'D', 'D', 'D', 'D', 'D', 'A']), (13, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'J', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'A']), (14, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'H', 'D', 'D', 'F', 'B', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'J', 'J', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'O', 'D', 'D', 'A']), (15, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (16, ['E', 'D', 'D', 'D', 'D', 'A']), (17, ['E', 'D', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'H', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'A']), (18, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'D', 'A'])])
# amtlog = len(full_logfabio2m)
# This one is a 19 pack used to test proM's ETMd

# full_logfabio2m = col.OrderedDict([(0, ['E', 'D', 'D', 'D', 'D', 'A']), (1, ['E', 'D', 'D', 'D', 'D', 'B', 'B', 'B', 'D', 'D', 'C', 'C', 'C', 'C', 'D', 'B', 'B', 'B', 'D', 'D', 'D', 'C', 'C', 'D', 'B', 'B', 'B', 'B', 'A']), (2, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (3, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'C', 'A']), (4, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'A']), (5, ['E', 'D', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (6, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A']), (7, ['E', 'M', 'P', 'P', 'P', 'D', 'D', 'C', 'D', 'C', 'D', 'A']), (8, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'D', 'A']), (9, ['E', 'D', 'D', 'C', 'D', 'D', 'B', 'B', 'B', 'B', 'B', 'B', 'A']), (10, ['E', 'D', 'D', 'C', 'D', 'D', 'A']), (11, ['E', 'D', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'H', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'A']), (12, ['E', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'B', 'D', 'B', 'D', 'C', 'C', 'D', 'D', 'D', 'C', 'D', 'B', 'D', 'D', 'D', 'D', 'D', 'A']), (13, ['E', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'A']), (14, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'B', 'A']), (15, ['E', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'A']), (16, ['E', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'A']), (17, ['E', 'D', 'D', 'C', 'D', 'A']), (18, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'C', 'D', 'D', 'A']), (19, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'D', 'B', 'B', 'C', 'B', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'D', 'D', 'D', 'C', 'D', 'B', 'B', 'B', 'B', 'D', 'C', 'A']), (20, ['E', 'D', 'D', 'D', 'C', 'D', 'A']), (21, ['E', 'D', 'D', 'C', 'D', 'C', 'D', 'J', 'D', 'D', 'C', 'D', 'D', 'C', 'D', 'H', 'D', 'D', 'D', 'D', 'D', 'A']), (22, ['E', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'H', 'D', 'D', 'F', 'B', 'D', 'D', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'J', 'J', 'D', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'D', 'C', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'D', 'O', 'D', 'D', 'A']), (23, ['E', 'D', 'D', 'D', 'D', 'B', 'D', 'H', 'I', 'H', 'I', 'H', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'A']), (24, ['E', 'D', 'D', 'D', 'H', 'D', 'D', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'A']), (25, ['E', 'D', 'D', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'D', 'H', 'D', 'D', 'H', 'H', 'D', 'Z', 'A']), (26, ['E', 'D', 'A']), (27, ['E', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'A']), (28, ['E', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'D', 'A']), (29, ['E', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'D', 'D', 'C', 'D', 'C', 'D', 'C', 'C', 'D', 'D', 'D', 'D', 'C', 'C', 'D', 'C', 'C', 'C', 'A'])])
# amtlog = len(full_logfabio2m)
## This last one is a 30 pack used to test proM's ETMd
# 6-10 hours each run


# Reducing the log traces to speed up the evolution
# sublog_evc_keys = np.random.choice(list(log.keys()), amtlog, False)  # Choosing an amount of traces
# sublog_evc = {key: log[key] for key in sublog_evc_keys}  # Remounting the traces dict
# print(sublog_evc)
# Chose to keep the full rpdict
# rpdict_logfabio2m_full = {'I': {'after': {'H'}, 'before': {'H'}}, 'D': {'after': {'H', 'A', 'D', 'J', 'B', 'C', 'F', 'O', 'Z', 'N'}, 'before': {'H', 'E', 'P', 'D', 'J', 'B', 'C', 'O', 'N'}}, 'H': {'after': {'I', 'A', 'D', 'H'}, 'before': {'D', 'I', 'H'}}, 'M': {'after': {'P'}, 'before': {'E'}}, 'E': {'after': {'D', 'M'}, 'before': set()}, 'J': {'after': {'J', 'D'}, 'before': {'D', 'J', 'C'}}, 'A': {'after': set(), 'before': {'H', 'D', 'B', 'C', 'Z', 'N'}}, 'P': {'after': {'D', 'P'}, 'before': {'M', 'P'}}, 'process': {'end': {'A'}, 'start': {'E'}}, 'B': {'after': {'A', 'B', 'D', 'C'}, 'before': {'D', 'B', 'C', 'F'}}, 'C': {'after': {'D', 'A', 'J', 'C', 'B'}, 'before': {'D', 'B', 'C'}}, 'F': {'after': {'B'}, 'before': {'D'}}, 'O': {'after': {'D'}, 'before': {'D'}}, 'Z': {'after': {'A'}, 'before': {'D'}}, 'N': {'after': {'D', 'A', 'N'}, 'before': {'D', 'N'}}}
rpdict_log_evc = prc.positional_set(log.values())  # Calculating the new rpdict to the reduced log

# alpha_logfabio2m = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'M', 'N', 'O', 'P', 'Z']
alpha_subevc = set()
for trc in log.values():
    for evt in trc:
        alpha_subevc.add(evt)
alpha_subevc = list(alpha_subevc)
# Chose to keep the same alpha of the full log, to keep compatibility if i choose to change the logs

# alphabetCM28 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# logCM28 = {
#         'A': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A9'],
#         'B': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A8', 'A9'],
#         'C': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A8', 'A9'],
#         'D': ['A1', 'A2', 'A4', 'A3', 'A5', 'A6', 'A7', 'A9']}

# reference_pos_dict = {
#         'A7': {'before': {'A6'}, 'after': {'A9'}},
#         'A9': {'before': {'A7', 'A8'}, 'after': set()},
#         'A8': {'before': {'A6'}, 'after': {'A9'}},
#         'process': {'end': {'A9'}, 'start': {'A1'}},
#         'A1': {'before': set(), 'after': {'A2'}},
#         'A5': {'before': {'A4', 'A3'}, 'after': {'A6'}},
#         'A6': {'before': {'A5'}, 'after': {'A7', 'A8'}},
#         'A4': {'before': {'A3', 'A2'}, 'after': {'A3', 'A5'}},
#         'A3': {'before': {'A4', 'A2'}, 'after': {'A4', 'A5'}},
#         'A2': {'before': {'A1'}, 'after': {'A4', 'A3'}}}
# experiments = [{'comp': 1, 'prec':0, 'crosspoint':1, 'mutac':0.05, 'tax_cross':0.95},
#         {'comp': 1, 'prec': 0, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7}]
# experiments2 = [{'comp': 1, 'prec':0, 'crosspoint':1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 1, 'prec': 0, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7},
#         {'comp': 0.5, 'prec': 0.5, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95}]

# experiments3 = [{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05}]
# experiments4 = [
# {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0},
# {'comp': 0.25, 'prec': 0.75, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0},
# {'comp': 0.5, 'prec': 0.5, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0},
# {'comp': 0.75, 'prec': 0.25, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0},
# {'comp': 1, 'prec': 0, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0}]

# experiments5 = [{'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1,
#     'muta_dir': 0}]

# experiments_pt1 = [{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross': 0.7, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':0.5, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 0.5, 'muta_dir': 0.05},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism': 1, 'muta_dir': 0.3},
#                 {'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'cohab', 'elitism': 0.5, 'muta_dir': 0.05}]
bestparams = [
{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':1, 'muta_dir': 0.05},
{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':1, 'muta_dir': 0.05},
{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':1, 'muta_dir': 0.3},
{'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':1, 'muta_dir': 0.05},
{'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.3, 'tax_cross':0.7, 'pop_ex': 'cohab', 'elitism':1, 'muta_dir': 0.3},
{'comp': 0, 'prec': 1, 'crosspoint': 99, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':1, 'muta_dir': 0.3}]

bestparam = [
{'comp': 0, 'prec': 1, 'crosspoint': 1, 'mutac': 0.05, 'tax_cross':0.95, 'pop_ex': 'kill', 'elitism':1, 'muta_dir': 0.05}
]
for count in range(1):
    print('R O U N D - ' + str(count))
    for conf in bestparam:

        size_pop = 100
        pop_exchange = conf['pop_ex'] # c - cohab, k - kill ancestors
        max_generations = 4000
        weights_fit = {'comp': conf['comp'], 'prec': conf['prec']}
        crossover_setup = {'points': conf['crosspoint'], 'chance': conf['tax_cross']}
        mutation_setup = {'logic': conf['mutac'], 'complex': 0, 'taskset': conf['mutac'], 'begin-end': 0, 'directed': conf['muta_dir']}  # each key holds the percent of chance that each mutation has of taking place
        selection_setup = {'tournament': 0, 'roulette': 1}
        elitism = conf['elitism']
        # TODO ampliar o elitismo
        max_len_trace = max([len(foo) for foo in log.values()]) * 1
        set_quant = int(len(log)*0.2)
        exec_id = '22-5alunos_100traces'+str(size_pop)+'-GEN-'+str(max_generations)+'evc1-35randomtraces'+'completude-' + str(conf['comp']) + '-precisao-' + str(conf['prec']) + '-crosspoint-' + str(conf['crosspoint']) + '-mutac-' + str(conf['mutac']) + '-tax_cross-' + str(conf['tax_cross']) + '-pop_ex-' + str(conf['pop_ex']) + '-elit-' + str(conf['elitism']) + 'dir_mut' + str(conf['muta_dir']) + 'pc0exec' + str(count)
        # exec_id = 'lol1'

        result = evol.evolution_cycle(alpha_subevc, log, size_pop, pop_exchange, max_generations, weights_fit, crossover_setup, mutation_setup, selection_setup, elitism, max_len_trace, set_quant, rpdict_log_evc, exec_id)


        p.plot_evolution(result[1], exec_id)

        # # Writing stuff to a dataframe
        # df1_dict = {'Exec ID': exec_id, 'Last Best Ind': [result[0][-1]] }#, 'Fitness evolution (worst-avg-best)': result[1], 'Best Inds - all generations':result[0]}
        # df1 = pd.DataFrame(df1_dict)


        # try:
        #     writer = xlsx.load_workbook('output.xlsx')
        # except:
        #     writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
        #
        # last_row = writer.sheets
        # print(last_row)
        # exit()
        # df1.to_excel(writer, 'Main', index=False, startrow=last_row)
        # writer.save()

        # # Writing stuff on a xlsx
        # fields = [exec_id, result[0][-1], result[1], result[0]]
        # with open('param_results.xlsx', 'a', newline='') as f:
        #         writer = csv.writer(f, delimiter=',')
        #         writer.writerow(fields)
        fields = [exec_id, log, result[0][-1], result[1]]
        with open("output_5alunos_100traces_full.csv", "a", newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', delimiter=',')
            writer.writerow(fields)
            csvfile.close()

'''
import timeit

print(timeit.timeit(stmt, number=1))