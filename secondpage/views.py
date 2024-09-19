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
                    LEFT JOIN public.app_relationshipinfo relationship ON person.id = relationship.id
                    LEFT JOIN public.app_jobcategoryinfo jobcategory ON person.id = jobcategory.id
                    LEFT JOIN public.app_targetcatgoryinfo targetcatgory ON person.id = targetcatgory.id
                    LEFT JOIN public.app_registerreasoninfo registerreason ON person.id = registerreason.id
                    LEFT JOIN public.app_paymentinfo payment ON person.id = payment.id
                    LEFT JOIN public.app_decisioninfo decision ON person.id = decision.id
                    LEFT JOIN public.app_draftpersoninfo draftperson ON person.id = draftperson.id
                    LEFT JOIN public.app_kannaiinfo kannai ON person.id = kannai.id
                    LEFT JOIN public.app_rejectinfo reject ON person.id = reject.id
                    LEFT JOIN public.app_gurdianinfo gurdian ON person.id = gurdian.id
                    LEFT JOIN public.app_registerpersoninfo registerperson ON person.id = registerperson.id
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
    # person_id = request.GET.get('personID')

    # if person_id:
    #     data = load_data(person_id)
    #     if data:
    #         context = {
    #             'person_info': data
    #         }

    #         return render(request, 'SecondPage.html', context)
        
    # return render(request, 'InvalidIdPage.html', status=404)
    try:
        person_id = request.GET.get('personID')
        data = load_data(person_id)
        return render(request, 'SecondPage.html', context = {'person_info': data})
    except ValueError:
        print(f"None")
        return render(request, 'InvalidIdPage.html', status=404)
    