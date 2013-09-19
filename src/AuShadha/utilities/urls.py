from AuShadha.settings import APP_ROOT_URL

class UrlGenerator(object):
  """ 
    Generates URL for the classes based on action, id and a parent class attribute
  """
  parented_actions = ['add','list','json','tree','sidebar','summary']
  parentless_actions = ['edit','del']

  def __init__(self,
               instance,
               parent = None):

    self.root_url = APP_ROOT_URL
    self.instance = instance

    self.instance_id = str(instance.id)
    self.urlDict = instance.urls
    self.app_label = instance._meta.app_label
    self.model_label = instance.__model_label__
    self.parent_model = instance._parent_model


    for action in self.parentless_actions:
        url = "%s%s/%s/%s/%s/" %(self.root_url,
                                  self.app_label,
                                  self.model_label,
                                  action,
                                  self.instance_id
                                )
        self.urlDict[action] = url

    for action in self.parented_actions:
        print "Received Parent: ", parent
        print "Parent is of type: ", type(parent)
        parent_label = getattr(parent,'__model_label__')
        print parent.__model_label__
        print "Parent Label generated is: ", parent_label
        parent_id = getattr(parent,'id')
        print "Parent ID is: ", parent_id

        if hasattr(instance,'_can_add_list_or_json'):
          for m in instance._can_add_list_or_json:
            self.urlDict[action] = {}
            if parent_label and parent_id:
                url = "%s%s/%s/%s/?%s_id=%s/" %(self.root_url,
                                                self.app_label,
                                                self.model_label,
                                                action,
                                                parent_label,
                                                str(parent_id)
                                          )
                self.urlDict[action][m] = url
            else:
              raise Exception("NoParentModelLabelError")

        else:
            if parent_label and parent_id:
                url = "%s%s/%s/%s/?%s_id=%s/" %(self.root_url,
                                                self.app_label,
                                                self.model_label,
                                                action,
                                                parent_label,
                                                str(parent_id)
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
