from django.shortcuts import render
import pandas as pd
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Event, Result
from django.db.models import Prefetch
from registrations.models import Registration

User = get_user_model()

def upload_results_excel(request, event_id):
    # TODO upravit docstrings a 79 znaků
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, "Soubor musí být ve formátu .xlsx.")
            return render(request, 
                    'organizer/upload_results_excel.html', {'event': event})

        try:
            df = pd.read_excel(excel_file)

        
            required_columns = ['email', 'result_time', 'id_event_id']
            if not all(col in df.columns for col in required_columns):
                messages.error(
                request, f"Soubor musí obsahovat sloupce: {', '.join(required_columns)}.")
                return render(request, 'organizer/upload_results_excel.html', {'event': event})

            errors = []
            results_to_create = []

            for index, row in df.iterrows():
                email = str(row['email']).strip().lower()
                event_id_row = row['id_event_id']
                result_time = row['result_time']

                # 🔍 Ověření uživatele podle e-mailu
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    errors.append(f"Řádek {index+2}: Uživatel s e-mailem {email} neexistuje.")
                    continue

                # Ověření události
                if event_id_row != event.id:
                    errors.append(f"Řádek {index+2}: ID události ({event_id_row}) neodpovídá aktuální události ({event.id}).")
                    continue

                # Čas ve správném formátu
                try:
                    if isinstance(result_time, str):
                        result_time = datetime.datetime.strptime(result_time, '%H:%M:%S').time()
                    elif isinstance(result_time, pd.Timestamp):
                        result_time = result_time.time()
                except Exception:
                    errors.append(f"Řádek {index+2}: Chybný formát času: {result_time}")
                    continue

                # Uložení výsledku
                results_to_create.append(Result(
                    id_user=user,
                    id_event=event,
                    result_time=result_time
                ))

            
            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                Result.objects.bulk_create(results_to_create)
                messages.success(request, f"Úspěšně nahráno {len(results_to_create)} výsledků.")

        except Exception as e:
            messages.error(request, f"Chyba při zpracování souboru: {str(e)}")

    return render(request, 'organizer/upload_results_excel.html', {'event': event})


def results_list(request, event_id):
    #TODO docstring + úprava 79 znaků
    event = get_object_or_404(Event, id=event_id)

    registrations = Registration.objects.filter(id_event=event).select_related('id_user')
    registration_map = {r.id_user_id: r.category for r in registrations}

    results = list(Result.objects.filter(id_event=event).select_related('id_user').order_by('result_time'))

    for i, result in enumerate(results):
        result.overall_rank = i + 1  # Celkové pořadí
        result.category = registration_map.get(result.id_user_id, "Neznámá")

    # Výpočet pořadí v kategorii
    from collections import defaultdict
    category_groups = defaultdict(list)
    for result in results:
        category_groups[result.category].append(result)

    for group in category_groups.values():
        for i, result in enumerate(sorted(group, key=lambda r: r.result_time)):
            result.category_rank = i + 1

    return render(request, 'results/results_list.html', {
        'event': event,
        'results': results
    })