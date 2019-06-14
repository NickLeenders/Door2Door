import numpy as np 

def BoltStress(ReactionForce_X, thickness, ult_stress_material):

	diameter = ReactionForce_X / (ult_stress_material * thickness)
	return diameter 

print BoltStress(10000, 0.005, 2.2e6)