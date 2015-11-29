from .models import VisitDetail, VisitComplaint


def get_all_complaints(visit):

    v_id = visit.id
    pat_obj = visit.patient_detail

    visit_obj = VisitDetail.objects.filter(
        patient_detail=pat_obj).order_by('-visit_date')
    visit_complaint_list = []

    if visit_obj:

        for visit in visit_obj:
            visit_complaints = VisitComplaint.objects.filter(
                visit_detail=visit)

            if visit_complaints:
                for complaint in visit_complaints:
                    dict_to_append = {}
                    dict_to_append['complaint'] = complaint.complaint
                    dict_to_append['duration'] = complaint.duration
                    dict_to_append[
                        'visit_date'] = complaint.visit_detail.visit_date.date().isoformat()
                    dict_to_append[
                        'is_active'] = complaint.visit_detail.is_active
                    dict_to_append['visit_detail'] = complaint.visit_detail
                    dict_to_append[
                        'visit_fu'] = complaint.visit_detail.has_fu_visits()

                    visit_complaint_list.append(dict_to_append)

    return visit_complaint_list
