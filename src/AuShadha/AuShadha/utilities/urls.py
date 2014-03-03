################################################################################
# Project     : AuShadha
# Description : URL Generator Class for AuShadha
# Author      : Dr. Easwar T.R
# Date        : 26-09-2013
# License     : GNU-GPL Version 3, see AuShadha/LICENSE.txt 
################################################################################

"""
 Module defines the class and its factory that generates URL based on the actions an 
 object can have / actions that can be performed on an object.
 
 This is not intended to replace Django's reverse / {%url%} template tag, rather
 this was an attempt to create something that was more like Zope with each object
 being aware internally of the actions that can be done on/by it

"""


from AuShadha.settings import APP_ROOT_URL

class UrlGenerator(object):
  
  """ 
    Generates URL for the classes based on action, id and a parent class attribute
  """
  #FIXME: This needs to be converted into more elegant code with Zope like awareness built
          #into the Model class itself with options to override it at instance level
  
  #Parented actions are actions that require a relation to a higher model
  # This is to say we are adding this object under that
  # For eg: adding a Contact to the Patient , Listing contacts of a Patients
  parented_actions = ['add','list','json','tree','sidebar','summary','pane']
  
  # These are actions that act on the object themselves
  # Editing / deleting / getting the object are examples
  parentless_actions = ['edit','del','info']

  def __init__(self,
               instance,
               parent = None):

    self.urlDict = {
                    'summary':{},
                    'pane'   :{},                    
                    'tree'   :{},
                    'sidebar':{},
                    'json'   :{},
                    'list'   :{},
                    'add'    :{},
                    'edit'   :{},
                    'del'    :{},
                    'info'   :{}
                  }

    self.root_url = APP_ROOT_URL
    self.instance = instance

    self.instance_id = str(instance.id)
    self.app_label = instance._meta.app_label
    self.model_label = instance.__model_label__
    self.parent_model = instance._parent_model

    self.can_add_list_or_json = hasattr(instance,'_can_add_list_or_json')
    self.extra_url_actions = hasattr(instance,'_extra_url_actions')

    for action in self.parentless_actions:
        url = "%s%s/%s/%s/%s/" %(self.root_url,
                                  self.app_label,
                                  self.model_label,
                                  action,
                                  self.instance_id
                                )
        self.urlDict[action] = url

    for action in self.parented_actions:
        parent_label = getattr(parent,'__model_label__',None)
        parent_id = getattr(parent,'id',None)
        if parent_id: 
          parent_id = str(parent_id)

        #print "Received Parent: ", parent
        #print "Parent is of type: ", type(parent)
        #print parent.__model_label__
        #print "Parent Label generated is: ", parent_label
        #print "Parent ID is: ", parent_id

        self.urlDict[action] = {}
        if self.can_add_list_or_json:
          if action == 'add':
            for m in instance._can_add_list_or_json:
                url = "%s%s/%s/%s/" %(self.root_url,
                                              m,
                                              action,
                                              self.instance_id
                                          )
                self.urlDict[action][m] = url

          else:
            for m in instance._can_add_list_or_json:
              url = "%s%s/%s/?%s_id=%s" %(self.root_url,
                                            m,
                                            action,
                                            self.model_label,
                                            self.instance_id
                                        )
              self.urlDict[action][m] = url

        #if self.extra_url_actions:
          #self.urlDict[action] = {}
          #for m in instance._extra_url_actions:
              #url = "%s%s/%s/%s/?%s_id=%s/" %(self.root_url,
                                           #self.app_label,
                                           #self.model_label,
                                           #m,
                                           #self.model_label,
                                           #self.instance_id
                                        #)
              #self.urlDict[action][m] = url

        else:
            if parent_label and parent_id:
                if self.app_label != self.model_label:
                  url = "%s%s/%s/%s/?%s_id=%s" %(self.root_url,
                                                  self.app_label,
                                                  self.model_label,
                                                  action,
                                                  parent_label,
                                                  parent_id
                                            )
                else:
                  url = "%s%s/%s/?%s_id=%s" %(self.root_url,
                                                  self.app_label,
                                                  action,
                                                  parent_label,
                                                  parent_id
                                            )
                self.urlDict[action] = url
            else:
              raise Exception("NoParentModelLabelError")

  def __call__(self):
    return self.urlDict

  def return_urlDict(self):
    return self.urlDict


def urlgenerator_factory(instance,parent = None):
  """
    Returns the generated URL as a String
  """
  return UrlGenerator(instance,parent)()



def generic_url_maker(instance, action, id, root_object=False):

    """
      Returns the URL Pattern for any AuShadha Object
      Following the naming conventions
      instance   : an instance of a Django Model
      action     : action that URL will commit : add/edit/delete/list/
      root_object: for the list option is root_object is False, instance id will be appended to URL else no id
                   will be appended.
                   Eg:: to list all patients, under a clinic once a queryset is done
                   the id will be that of the clinic. But for the root object clinic since there is no db_relationship
                   that fetches a list of clinics, all clinics are fetched and listed.
    """
    # FIXME:: may be better to rely on django.contrib.contenttypes.ContentType
              # to do a similar thing rather than using _meta

    if not root_object:
        #url = unicode(APP_ROOT_URL) + unicode(instance._meta.app_label)+ "/" + unicode(action) +"/" + unicode(id) +"/"
        url = unicode(APP_ROOT_URL)              + \
            unicode(instance._meta.app_label)  + "/" + \
            unicode(instance.__model_label__)  + "/" + \
            unicode(action) + "/" + unicode(id) + "/"
    if root_object:
        url = unicode(APP_ROOT_URL) + unicode(
            instance._meta.app_label) + "/" + unicode(action) + "/"
    return url
