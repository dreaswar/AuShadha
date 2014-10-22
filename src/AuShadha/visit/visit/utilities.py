from django.contrib.auth.decorators import login_required

from AuShadha.apps.ui.ui import ui as UI
#from .models import VisitDetail, VisitComplaint

PatientDetail = UI.get_module("PatientRegistration")
VisitDetail = UI.get_module("OPD_Visit")
VisitComplaint = UI.get_module("OPD_Visit_Complaint")




def get_all_complaints(visit):

    v_id = visit.id
    pat_obj  = visit.patient_detail

    visit_obj = VisitDetail.objects.filter(patient_detail = pat_obj).order_by('-visit_date')
    visit_complaint_list = []

    if visit_obj:

        for visit in visit_obj:
            visit_complaints = VisitComplaint.objects.filter( visit_detail = visit )

            if visit_complaints:
                for complaint in visit_complaints:
                    dict_to_append = {}
                    dict_to_append['complaint'] = complaint.complaint
                    dict_to_append['duration'] = complaint.duration
                    dict_to_append['visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                    dict_to_append['is_active'] = complaint.visit_detail.is_active
                    dict_to_append['visit_detail'] = complaint.visit_detail
                    dict_to_append['visit_fu'] = complaint.visit_detail.has_fu_visits()

                    visit_complaint_list.append(dict_to_append)

    return visit_complaint_list
    

####################################### PDF Render #############################

# Will be removed
# Better to rely on plain HTML
# This is lot of work and not an absolute necessity
# Add more complexity, external dependency to the project
# Cumbersome to style it with current tools
# Creates a significant additional skillset to learn with a very limited use case 

@login_required
def render_visit_pdf(request, id):
    if request.user:
        user = request.user
        try:
            id = int(id)
            visit_detail_obj = VisitDetail.objects.get(pk=id)
        except(ValueError, AttributeError, TypeError, VisitDetail.DoesNotExist):
            raise Http404(
                'Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
        pat_detail_obj = visit_detail_obj.patient_detail
        if request.method == 'GET':
            variable = RequestContext(request,
                                      {'user': user,
                                       'pat_detail_obj': pat_detail_obj,
                                       'visit_detail_obj': visit_detail_obj,
                                       }
                                      )
            return render_to_response('visit_detail/visit_pdf_template.html', variable)
        elif request.method == 'POST':
            pass
        else:
            raise Http404("Bad Request.." + str(request.method))
    else:
        return HttpResponseRedirect('/login')


@login_required
def render_patient_visits_pdf(request, id):
    if request.user:
        user = request.user
        try:
            id = int(id)
            patient_detail_obj = PatientDetail.objects.get(pk=id)
        except(ValueError, AttributeError, TypeError, PatientDetail.DoesNotExist):
            raise Http404(
                'Error!!:: AttributeError/ ValueError/ TypeError/ DoesNotExist')
        visit_detail_obj = VisitDetail.objects.filter(
            patient_detail=patient_detail_obj)
        visit_obj_list = []

        if visit_detail_obj:
            error_message = "Listing the Visits"
            for visit in visit_detail_obj:
                dict_to_append = {}
                visit_complaint_obj = VisitComplaint.objects.filter(
                    visit_detail=visit)
                visit_hpi_obj = VisitHPI.objects.filter(
                    visit_detail=visit)
                visit_ros_obj = VisitROS.objects.filter(
                    visit_detail=visit)
                if visit_ros_obj:
                    visit_ros_obj = visit_ros_obj[0]
                dict_to_append[visit] = {'complaint': visit_complaint_obj,
                                         'hpi': visit_hpi_obj,
                                         'ros': format_ros(visit_ros_obj)
                                         }
                visit_obj_list.append(dict_to_append)
        else:
            error_message = "No Visits Recorded"

        if request.method == 'GET':
            variable = RequestContext(
                request, {'user': user,
                          'visit_detail_obj': visit_detail_obj,
                          'visit_obj_list': visit_obj_list,
                          'patient_detail_obj': patient_detail_obj,
                          'error_message': error_message,
                          'pagesize': "A4"
                          })

            template = get_template(
                'visit_detail/patient_visit_pdf_template.html')
            html = template.render(variable)
            result = StringIO.StringIO()
            pdf = pisa.pisaDocument(
                StringIO.StringIO(html.encode("UTF-8")), result)

            if not pdf.err:
                return HttpResponse(result.getvalue(), mimetype='application/pdf')
            return HttpResponse("Error Generating PDF.. %s" % (html))

        else:
            raise Http404("Bad Request.." + str(request.method))
    else:
        return HttpResponseRedirect('/login')


def has_previous_visits(visit_id):
  visit_detail_obj = VisitDetail.objects.get(pk = int(visit_id) )
  patient_detail_obj = visit_detail_obj.patient_detail
  all_visits = VisitDetail.objects.get(patient_detail = patient_detail_obj).order_by('visit_date')

  for v in all_visits:
    if (v.visit_date <= visit_detail_obj.visit_date) and (v != visit_detail_obj):
      return True
    else:
      continue


#@login_required
#def visit_summary(request, patient_id = None):

    #user = request.user

    #if request.method == "GET" and request.is_ajax():
        #try:
            #if patient_id:
              #patient_id = int(patient_id)
            #else:
              #patient_id = int(request.GET.get('patient_id') )
            #print "Listing Summary for patient with ID: " + str(patient_id)
            #patient_detail_obj = PatientDetail.objects.get(pk=patient_id)
            #visit_detail_obj = VisitDetail.objects.filter(
                #patient_detail=patient_detail_obj).order_by('-visit_date')
        #except (TypeError, NameError, ValueError, AttributeError, KeyError):
            #raise Http404("Error ! Invalid Request Parameters. ")
        #except (PatientDetail.DoesNotExist):
            #raise Http404("Requested Patient Does not exist.")

        #visit_obj_list = []
        #if visit_detail_obj:
            #error_message = "Listing the Visits in ", visit_detail_obj
            #print "Listing the Visits in ", visit_detail_obj
            #for visit in visit_detail_obj:
                #dict_to_append = OrderedDict()
                #dict_to_append[visit] = None
                #print "Aggregating sub-modules in visit: ", visit
                #visit_complaint_obj = VisitComplaint.objects.filter(
                    #visit_detail=visit)
                #visit_hpi_obj = VisitHPI.objects.filter(
                    #visit_detail=visit)
                #visit_ros_obj = VisitROS.objects.filter(
                    #visit_detail=visit)
                #vital_exam_obj = VitalExam_FreeModel.objects.filter(
                    #visit_detail=visit)
                #gen_exam_obj = GenExam_FreeModel.objects.filter(
                    #visit_detail=visit)
                #sys_exam_obj = SysExam_FreeModel.objects.filter(
                    #visit_detail=visit)
                #neuro_exam_obj = PeriNeuroExam_FreeModel.objects.filter(
                    #visit_detail=visit)
                #vasc_exam_obj = VascExam_FreeModel.objects.filter(
                    #visit_detail=visit)

                #if visit_hpi_obj:
                    #visit_hpi_obj = visit_hpi_obj[0]

                #if visit_ros_obj:
                    #visit_ros_obj = visit_ros_obj[0]
                    #v_ros = visitrospresentationclass_factory(visit_ros_obj)
                #else:
                  #v_ros = "No Review of System Recorded"

                #if vital_exam_obj:
                    #vital_exam_obj = vital_exam_obj[0]
                    #vf = vitalexamobjpresentationclass_factory(vital_exam_obj)
                #else:
                    #vf = "No Vitals Recorded"

                #if gen_exam_obj:
                    #gen_exam_obj = gen_exam_obj[0]
                    #gf = genexamobjpresentationclass_factory(gen_exam_obj)
                #else:
                    #gf = "No General Examination Recorded"

                #if sys_exam_obj:
                    #sys_exam_obj = sys_exam_obj[0]
                    #sf = sysexamobjpresentationclass_factory(sys_exam_obj)
                #else:
                    #sf = "No Systemic Examination Recorded"

                #if neuro_exam_obj:
                    #neuro_exam_obj = neuro_exam_obj[0]
                    #nf = neuroexamobjpresentationclass_factory(neuro_exam_obj)
                #else:
                    #nf = "No Neurological Examination Recorded"

                #if vasc_exam_obj:
                    #vasc_f = vascexamobjpresentationclass_querysetfactory(vasc_exam_obj)
                #else:
                    #vasc_f = "No Vascular Examination Recorded"

                #d = OrderedDict()
                #d['complaint']= visit_complaint_obj
                #d['hpi']= visit_hpi_obj
                #d['ros']= v_ros
                #d['vitals']= vf
                #d['gen_exam']=gf
                #d['sys_exam']=sf
                #d['neuro_exam']=nf
                #d['vasc_exam']=vasc_f
                #dict_to_append[visit] = d
                #visit_obj_list.append(dict_to_append)
                ##print "Vascular Exam is: "
                ##print vasc_f
        #else:
            #error_message = "No Visits Recorded"
        #variable = RequestContext(
            #request, {'user': user,
                      #'visit_detail_obj': visit_detail_obj,
                      #'visit_obj_list': visit_obj_list,
                      #'patient_detail_obj': patient_detail_obj,
                      #'error_ message': error_message
                      #})
        #return render_to_response('visit_detail/summary.html', variable)
    #else:
        #raise Http404(" Error ! Unsupported Request..")

