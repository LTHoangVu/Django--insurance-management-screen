from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.template import loader


def format_data(columns, rows):
    try:
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
        print("Can't not format")        

def replace_asterisk(menu_item):
    return [
        tuple("" if value == "**" else value for value in row)
        for row in menu_item
    ]

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

            result = format_data(columns, rows)
            return result
    except:
        return None

def load_drop_down_item(menu_type):
    try: 
        with connection.cursor() as cursor:
            match menu_type:
                case 'relationship':
                    sql = """
                        SELECT "relationshipID", "relationshipType" FROM app_relationshipinfo 
                        ORDER BY "relationshipID" ASC;
                    """
                case 'jobcategory':
                    sql = """
                        SELECT "jobID", "jobType" FROM app_jobcategoryinfo
                        ORDER BY "jobID" ASC;
                    """
                case 'targetcategory':
                    sql = """
                        SELECT "targetID", "targetName" FROM app_targetcatgoryinfo
                        ORDER BY "targetID" ASC;
                    """
                case 'registerreason':
                    sql = """
                        SELECT "reReasonID", "reReasonName" FROM app_registerreasoninfo
                        ORDER BY "reReasonID" ASC;
                    """
                case 'payment':
                    sql = """
                        SELECT "paymentID", "paymentType" FROM app_paymentinfo
                        ORDER BY "paymentID" ASC;
                    """
                case 'decision':
                    sql = """
                        SELECT "decisionID", "decisionType" FROM app_decisioninfo
                        ORDER BY "decisionID" ASC;
                    """
                case 'reject':
                    sql = """
                        SELECT "rejectID", "rejectType" FROM app_rejectinfo
                        ORDER BY "rejectID" ASC;
                    """
                case 'draft':
                    sql = """
                        SELECT "draftPersonID", "draftPersonName" FROM app_draftpersoninfo 
                        ORDER BY "draftPersonID" ASC
                    """
                case 'kannai': 
                    sql = """
                        SELECT "kannaiID", "kannaiType" FROM app_kannaiinfo
                        ORDER BY 
                            CASE 
                                WHEN "kannaiID" ~ '^[0-9]+$' THEN CAST("kannaiID" AS INTEGER)
                                ELSE 1
                            END ASC, 
                            "kannaiID" ASC;
                    """
                case 'registerperson': 
                    sql = """
                        SELECT "registerPersonID", "registerPersonName" FROM app_registerpersoninfo
                        ORDER BY "registerPersonID" ASC
                    """
                case _:
                    return []

            cursor.execute(sql)
            menu_item = cursor.fetchall()
            formatted_items = replace_asterisk(menu_item)
            
            return formatted_items
    except:
        print("ERROR FOR LOADING ITEM")
        return {}

def get_secondpage(request):
    try: 
        person_id = request.GET.get('personID')
        data = load_data(person_id)
        menu_types = ['relationship', 'jobcategory', 'registerreason', 'targetcategory', 'payment', 'decision', 'reject', 'draft', 'kannai', 'registerperson']
        menu_item = {}

        for menu_type in menu_types:
            menu_item[menu_type] = load_drop_down_item(menu_type)

        if not data:
            raise ValueError("No data found")
            
        context = {
                    'person_info': data,
                    'menu_item': menu_item
                }
        return render(request, 'SecondPage.html', context)

    except:    
        return render(request, 'InvalidIdPage.html', status=404)