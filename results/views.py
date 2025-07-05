import datetime

import pandas as pd
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Event, Result
from registrations.models import Registration

User = get_user_model()


def upload_results_excel(request, event_id):
    """
    Handle uploading an Excel file with results and bulk-create Result objects.

    Reads an .xlsx from `request.FILES['excel_file']`, validates required
    columns, matches users by email, parses times, and either reports errors
    via Django messages or bulk-inserts all valid rows.

    Args:
        request: incoming request, must be POST with file.
        event_id: primary key of the Event for which to import results.

    Returns:
        Renders 'organizer/upload_results_excel.html' with success or error
        messages, or re-renders form on GET.
    """

    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith('.xlsx'):
            messages.error(
                request,
                "Soubor musí být ve formátu .xlsx."
            )
            return render(
                request,
                'organizer/upload_results_excel.html',
                {'event': event}
            )

        try:
            df = pd.read_excel(excel_file)
            required_columns = ['email', 'result_time', 'id_event_id', 'year']
            if not all(col in df.columns for col in required_columns):
                messages.error(
                    request,
                    f"Soubor musí obsahovat sloupce: "
                    f"{', '.join(required_columns)}."
                )
                return render(
                    request,
                    'organizer/upload_results_excel.html',
                    {'event': event}
                )

            errors = []
            results_to_create = []
            for index, row in df.iterrows():
                email = str(row['email']).strip().lower()
                event_id_row = row['id_event_id']
                result_time = row['result_time']
                year = int(row['year'])

                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    errors.append(
                        f"Řádek {index + 2}:"
                        f"Uživatel s e-mailem {email} neexistuje."
                    )
                    continue

                if event_id_row != event.id:
                    errors.append(
                        f"Řádek {index + 2}: "
                        f"ID události ({event_id_row}) "
                        f" neodpovídá aktuální události ({event.id})."
                    )
                    continue

                try:
                    if isinstance(result_time, str):
                        result_time = datetime.datetime.strptime(
                            result_time, '%H:%M:%S').time()
                    elif isinstance(result_time, pd.Timestamp):
                        result_time = result_time.time()
                except Exception:
                    errors.append(
                        f"Řádek {index + 2}:"
                        f"Chybný formát času: {result_time}"
                    )
                    continue

                results_to_create.append(
                    Result(
                        id_user=user,
                        id_event=event,
                        result_time=result_time,
                        year=year
                    )
                )

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                Result.objects.bulk_create(results_to_create)
                messages.success(
                    request,
                    f"Úspěšně nahráno {len(results_to_create)} "
                    f"výsledků."
                )

        except Exception as e:
            messages.error(
                request,
                f"Chyba při zpracování souboru: {str(e)}"
            )

    return render(
        request,
        'organizer/upload_results_excel.html',
        {'event': event}
    )


def results_list(request, event_id):
    """
    Display all results for an Event, annotate overall and category ranks.

    Fetches every Result for `event_id`, orders by `result_time`, then
    computes `overall_rank` and `category_rank`
    (based on Registration.category).

    Args:
        request: incoming request.
        event_id: ID of the Event to show results for.

    Returns:
        Renders 'results/results_list.html' with context

            - event: the Event
            - results: list of Result objects decorated with .overall_rank,
              .category, and .category_rank.

    """

    event = get_object_or_404(Event, id=event_id)
    registrations = (Registration.objects.filter(id_event=event)
                     .select_related('id_user'))
    registration_map = {r.id_user_id: r.category for r in registrations}

    results = list(
        Result.objects.filter(id_event=event)
        .select_related('id_user')
        .order_by('result_time'))

    for i, result in enumerate(results):
        result.overall_rank = i + 1
        result.category = registration_map.get(result.id_user_id, "Neznámá")

    from collections import defaultdict
    category_groups = defaultdict(list)
    for result in results:
        category_groups[result.category].append(result)

    for group in category_groups.values():
        for i, result in enumerate(sorted(group, key=lambda r: r.result_time)):
            result.category_rank = i + 1

    return render(
        request,
        'results/results_list.html',
        {'event': event,'results': results}
    )


def leaderboard_by_distance(request, distance_km):
    """
    Show a paginated leaderboard of all runners for a given distance.

    Gathers all Events at `distance_km * 1000` meters, fetches their Results
    ordered by best time, then paginates 20 per page and computes absolute
    rank.

    Args:
        request: incoming request (can include ?page=).
        distance_km: race distance in kilometers (e.g., 5, 10, 21, 42).

    Returns:
        Renders 'results/leaderboard.html' with

            - results: this page’s list of Result
            - page_obj: the Django Paginator page
            - distance_km: echo of argument

    """

    distance_m = distance_km * 1000
    events = Event.objects.filter(distance=distance_m)
    results = (Result.objects.filter(id_event__in=events)
               .select_related('id_user', 'id_event')
               .order_by('result_time'))

    paginator = Paginator(results, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for i, result in enumerate(page_obj.object_list):
        result.rank = (page_obj.start_index() - 1) + i + 1

    return render(
        request,
        'results/leaderboard.html',
        {
            'results': page_obj.object_list,
            'page_obj': page_obj,
            'distance_km': distance_km,
        }
    )


@login_required
def best_performances_by_user(request, distance_km):
    """
    Display the logged-in user’s top 10 times for each major distance.

    Iterates over [5,10,21,42] km, filters Results for that distance
    and this user, orders by `result_time` ascending, and takes top 10.

    Args:
        request: incoming request (user must be logged in).
        distance_km: echoed into template context (not used for filter).

    Returns:
        Renders 'results/best_performances.html' with

            - results_by_distance: dict distance ▶ list[Result]
            - distances: [5,10,21,42]
            - range_max_len: helper for templating columns

    """

    user = request.user
    all_results = {}
    for km in [5, 10, 21, 42]:
        events = Event.objects.filter(distance=km * 1000)
        results = Result.objects.filter(
            id_user=user, id_event__in=events).select_related(
            'id_event').order_by('result_time')[:10]
        all_results[km] = list(results)

    max_len = max(len(all_results.get(km, [])) for km in [5, 10, 21, 42])

    return render(
        request,
        'results/best_performances.html',
        {
            'results_by_distance': all_results,
            'distance_km': distance_km,
            'distances': [5, 10, 21, 42],
            'range_max_len': range(max_len)
        }
    )
