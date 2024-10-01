from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.template import loader


def load_data(person_id):
    try: 
        with connection.cursor() as cursor:
            sql = """                    
                    SELECT *
                    FROM public.app_personinfo person
                    FULL OUTER JOIN public.app_relationshipinfo relationship ON person."relationshipId" = relationship."relationshipID"
                    FULL OUTER JOIN public.app_jobcategoryinfo jobcategory ON person."jobId" = jobcategory."jobID"
                    FULL OUTER JOIN public.app_targetcatgoryinfo targetcatgory ON person."targetID" = targetcatgory."targetID"
                    FULL OUTER JOIN public.app_registerreasoninfo registerreason ON person."reReasonID" = registerreason."reReasonID"
                    FULL OUTER JOIN public.app_paymentinfo payment ON person."paymentID" = payment."paymentID"
                    FULL OUTER JOIN public.app_decisioninfo decision ON person."decisionID" = decision."decisionID"
                    FULL OUTER JOIN public.app_draftpersoninfo draftperson ON person."draftPersonID" = draftperson."draftPersonID"
                    FULL OUTER JOIN public.app_kannaiinfo kannai ON person."kannaiID" = kannai."kannaiID"
                    FULL OUTER JOIN public.app_rejectinfo reject ON person."rejectID" = reject."rejectID"
                    FULL OUTER JOIN public.app_gurdianinfo gurdian ON person."gurdianID" = gurdian."gurdianID"
                    FULL OUTER JOIN public.app_registerpersoninfo registerperson ON person."registerPersonID" = registerperson."registerPersonID"
                    WHERE "personId" = %s;
                """
            cursor.execute(sql, [person_id])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            result = []
            for row in rows:
                row_data = {}
                for col, val in zip(columns, row):
                    if val is not None:
                        row_data[col] = val
                    else:
                        row_data[col] = ''
                result.append(row_data)
            return result
    except:
        return None

def get_secondpage(request):
    person_id = request.GET.get('personID')

    if person_id:
        data = load_data(person_id)
        if data:
            context = {
                'person_info': data
            }

            return render(request, 'SecondPage.html', context)
        
    return render(request, 'InvalidIdPage.html', status=404)
    # try:
    #     person_id = request.GET.get('personID')
    #     data = load_data(person_id)
    #     return render(request, 'SecondPage.html', context = {'person_info': data})
    # except ValueError:
    #     print(f"None")
    #     return render(request, 'InvalidIdPage.html', status=404)
    