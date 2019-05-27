from OEW_CG import function_OEW_CG, function_ZCG, function_XCG

OEW_CG = function_OEW_CG()
assert OEW_CG >= 0
assert OEW_CG <= 6

XCG = function_XCG()
assert XCG >= 0
assert XCG <= 6

ZCG = function_ZCG()
assert ZCG >= 0
assert ZCG <= 2

pass
