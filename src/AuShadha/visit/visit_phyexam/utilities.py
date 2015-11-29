

def visit_detail_has_exam(exam_obj, visit_obj):
    query = exam_obj.objects.filter(visit_detail=visit_obj)
    if query:
        return query
    else:
        return None
