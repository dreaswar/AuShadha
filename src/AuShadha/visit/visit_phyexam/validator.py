class Validator(object):
  """
  Validates a field for values
  """
  accepted_methods = ['is_in_range',
                      'is_greater',
                      'is_lesser',
                      'is_later',
                      'is_in_between',
                      'is_earlier',
                      'is_true_or_false',
                      'is_equal_to',
                      'is_not_equal_to',
                      'contains_text',
                      'in_list',
                      None
                     ]

  def __init__(self, 
               method,
               value_to_validate, 
               constraints = None,
               value_to_compare=None):

    if method in self.accepted_methods:
      self.method_map = {'is_in_range':self.is_in_range,
                        'is_greater':self.is_greater,
                        'is_lesser':self.is_lesser,
                        'is_later':self.is_later,
                        'is_in_between':None,
                        'is_earlier':self.is_earlier,
                        'is_true_or_false':self.is_true_or_false,
                        'is_equal_to':self.is_equal_to,
                        'is_not_equal_to':self.is_not_equal_to,
                        'contains_text':None,
                        'in_list':self.in_list,
                        None:None
                        }
      self.method_to_call = self.method_map[method]
      self.constraints = constraints
      self.value_to_validate = value_to_validate
      self.value_to_compare = value_to_compare
    else:
      print "ERROR! You have asked for validation with ", method
      raise Exception("Invalid Method. Not in accepted validator list")

  def __call__(self):
    attr = getattr(self,'method_to_call',None)
    if attr:
      return attr()
    else:
      return

  def is_in_range(self):

    if type(self.value_to_validate) == 'int':
      max_v = self.constraints['max']+1
      if self.value_to_validate in range( self.constraints['min'], max_v ):
        print "Value is in range"
        return True
      else:
        print "Value not in range"
        return False
    elif type(self.value_to_validate) == 'float':
      if (self.value_to_validate <= self.constraints['max']) and \
         (self.value_to_validate >= self.constraints['min']):
          return True
      else:
        return False

  def is_equal_to(self):
    if self.value_to_validate == self.value_to_compare:
      return True
    else:
      return False

  def is_not_equal_to(self):
    if self.value_to_validate != self.value_to_compare:
      return True
    else:
      return False

  def is_greater(self):
    if self.value_to_validate > self.value_to_compare:
      return True
    else:
      return False

  def is_lesser(self):
    if self.value_to_validate < self.value_to_compare:
      return True
    else:
      return False

  def is_earlier(self):
    if value_to_validate <value_to_compare:
      return True
    else:
      return False

  def is_later(self):
    if self.value > self.value_to_compare:
      return True
    else:
      return False

  def is_true_or_false(self):
    if self.value_to_validate == True:
      return True
    else:
      return False

  def in_list(self):
    if self.value_to_validate in self.value_to_compare:
      return True
    else:
      return False

def validator_factory(method,value,constraints=None,value_to_compare = None):
  """ Returns a instantiated Validator Class """
  return Validator(method,value,constraints,value_to_compare).__call__()


