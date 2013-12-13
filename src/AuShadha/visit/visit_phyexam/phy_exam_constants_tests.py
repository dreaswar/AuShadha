#! /usr/bin/python2

from phy_exam_constants import PC, validator_factory


def main():
  vital = PC['vital']
  s_bp = vital['sys_bp']
  
  s_validate  = s_bp['validator']
  s_constraints = s_bp['constraints']
  
  bp_val = 300

  v =  validator_factory(s_validate, 300, s_constraints)

  return v.__call__()




if __name__ == '__main__':
  main()
  print "Validated Successfully"


