import datetime


LIST_DATA = {
    'train_movement_report': 'The PostgreSQL table provides detailed tracking information for train movements, including dates, day of the week, train unit numbers, days until next examination, start locations, availability status, repair priorities, assigned and coupled diagrams, orientations, various types of comments (unit, location, layover, other), start and end of day details like headcodes, locations, times, detailed explanations of train statuses, and maintenance windows and statuses.', 
    'diagram_plan': 'The diagram_plan dictionary outlines the specifications for diagram plans, detailing the date, day of the week, number of cars, class, energy type, service type, specific route details, diagram name, information about attachment with other diagrams, start and end locations, and the departure and arrival times. This setup helps in organizing and planning the operation and routing of trains, including whether they are attached to or separated from other trains, along with energy requirements and service status.', 
    'penalty': 'the penalty PostgreSQL for each type of train assignment violation', 
    'train_config': 'PostgreSQL configuration of each train unit, including number of cars and train class.'}

LIST_DATA_PROMPT = """Here are the list of data with data type (PostgreSQL/JSON)
\ntrain_movement_report(PostgreSQL): The table provides detailed tracking information for train movements, including dates, day of the week, train unit numbers, days until next examination, start locations, availability status, repair priorities, assigned and coupled diagrams, orientations, various types of comments (unit, location, layover, other), start and end of day details like headcodes, locations, times, detailed explanations of train statuses, and maintenance windows and statuses.
\ndiagram_plan(JSON): The diagram_plan dictionary outlines the specifications for diagram plans, detailing the date, day of the week, number of cars, class, energy type, service type, specific route details, diagram name, information about attachment with other diagrams, start and end locations, and the departure and arrival times. This setup helps in organizing and planning the operation and routing of trains, including whether they are attached to or separated from other trains, along with energy requirements and service status.
\npenalty(PostgreSQL): the penalty for each type of train assignment violation,
\ntrain_config(PostgreSQL): configuration of each train, including number of cars and train class.

\n\nPlease choose a table to get the list of fields and their meaning."""

RELEVANT_DATA_PROMPT = """Return the names of ALL the DATA AND DATA TYPE (PostgreSQL/JSON) that MIGHT be relevant to the user question. \
Remember to include ALL POTENTIALLY RELEVANT data, even if you're not sure that they're needed.

Here are the list of data with data type (PostgreSQL/JSON)
\ntrain_movement_report(PostgreSQL): The table provides detailed tracking information for train movements, including dates, day of the week, train unit numbers, days until next examination, start locations, availability status, repair priorities, assigned and coupled diagrams, orientations, various types of comments (unit, location, layover, other), start and end of day details like headcodes, locations, times, detailed explanations of train statuses, and maintenance windows and statuses, and violations.
\ndiagram_plan(JSON): The diagram_plan dictionary outlines the specifications for diagram plans, detailing the date, day of the week, number of cars, class, energy type, service type, specific route details, diagram name, information about attachment with other diagrams, start and end locations, and the departure and arrival times. This setup helps in organizing and planning the operation and routing of trains, including whether they are attached to or separated from other trains, along with energy requirements and service status.
\npenalty(PostgreSQL): the penalty for each type of train assignment violation,
\ntrain_config(PostgreSQL): configuration of each train, including number of cars and train class.

For violations:
\ntrain_movement_report(PostgreSQL): in_service_then_withdrawn; incorrect_fleet_type_allocation; category_defect; divergent_handover_location
\ndiagram_plan(JSON): uncover diagram


Example of question - relevant data pair:
1. Show me the train with repair priority from 2024-08-04 to 2024-08-09?
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}]
2. Where is usually the end destination of the diagram DN504?
[{'data_name': 'diagram_plan', 'type': 'JSON'}]
3. Show all diagrams with Bi-mode on Friday.
[{'data_name': 'diagram_plan', 'type': 'JSON'}]
4. Which train units usually run from night (10 PM) till morning (6 AM)?
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}]
5. Which trains will arrive at LDS in 2024-08-04?
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}]
6. Show me the violations on 2024-8-8
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}, {'data_name': 'diagram_plan', 'type': 'JSON'}]
7. Calculate the penalty on 2024-8-8
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}, {'data_name': 'penalty', 'type': 'PostgreSQL'}]
8. What violation occur the least?
[{'data_name': 'train_movement_report', 'type': 'PostgreSQL'}, {'data_name': 'diagram_plan', 'type': 'JSON'}]
9. List uncovered diagrams on 3/8/2024
[{'data_name': 'diagram_plan', 'type': 'JSON'}]
Answer with only a list of GetRelevantDataName with data name and data type. 
"""


DATA_FIELDS_PROMPT = """Return the fields and their meanings for the relevant data {related_data_name} by using the tool [get_data_fields_meaning_tool].
"""

DATA_FIELDS_MEANING = {
"train_movement_report": {
    "data_type": "PostgreSQL",
    "fields": {
        "start_datetime": "the time and date that the train unit starts running, Examples: 2024-08-03 08:59:00.000, 2024-08-04 23:52:00.000",
        "end_datetime": "the time and date that the train unit finish running, Examples: 2024-08-04 22:19:00.000, 2024-08-06 23:52:00.000",
        "week_day": "day of the week, Examples: Monday, Tuesday",
        "train_unit": "6-digit train unit number, Examples: 800201, 801206",
        "odr": "number of days remaining before examination, Examples: 22, 15",
        "unit_location": "start location of the train, Examples: BGN, NEV",
        "unit_available": "whether the train unit is available (Available, Exam, Overhaul, Repair, D&V, Tyre Turn), Examples: Available, Exam",
        "kprio": "train's repair priority, which is number of days remaining before train must stop to repair, NULL value means no priority, Examples: K1, K2, ''",
        "sod_diagram": "final diagram of the train unit in a day, Examples: DN801, DN809 at the end of the run",
        "coupled": "the train diagram which is coupled with the current train diagram, Examples: DN504, DN923",
        "orien": "orientation of the train, Examples: T, L",
        "unit_com": "violation notes on changes between specific train units, car class, or configurations, Examples: 5E vice 9E, 5E vice 5B",
        "location_com": "violation notes on false location adjustments or replacements, Examples: DON vice NEV, KGX vice BGN",
        "layover_com": "brief note at each short stop of the train, Examples: 2:59 3D12, 16:30 5D26, LAYOVER BGN",
        "other_com": "other comments on the train status concerning its Diagram, Coupled, Trailing, etc, Examples: Direct to BGN, 5Y16 1806-5S09 2255, Split/Join Diagram",
        "sod_headcode": "start of date headcode of the train unit, Examples: 5D04, 1E13",
        "sod_location": "start of date location of the train unit, Examples: BGN, INV",
        "eod_diagram": "final diagram of the train unit in a day, Examples: DN801, DN809 at the end of the run",
        "eod_coupled": "the diagram coupled with the current diagram, Examples: DN605, DN504",
        "eod_headcode": "end of date headcode of the train unit, Examples: 5S22, 5H10",
        "eod_location": "end of date location of the train unit, Examples: CRA, DON",
        "details": "explanation to details from other columns, regarding kprio, unit_available, unit_com, location_com, layover_com, other_com. Example: K2 - 800209 Software MODs (DON): Train 800209 needs repair in 2 days for software mods at location DON",
        "main_w": "maintenance window, Examples: 13:38, 07:47",
        "main_status": "maintenance status, Examples: Breach, #VALUE!",
        "swap_diagram": "original diagram ",
        "swap_coupled": "",
        "swap_headcode": "",
        "swap_location": "",
        "swap_time": "",
        "swap_comments": "",
        "fy": "fiscal year",
        "week": "week order in fiscal year",
        "in_service_then_withdrawn": "a type of  violation for train units, indicating a withdrawn from specific services due to various reasons",
        "incorrect_fleet_type_allocation": "a type of  violation for train units (e.g. True/False, True means having this violation, False means NO)",
        # "category_defect": "a type of violation for train units, indicating issues arise from unavoidable breaches or defects in maintenance, operations, or scheduling, often requiring adjustments.",
        "divergent_handover_location": "a type of violation for train units, indicating instances where handover locations differ from planned or expected due to operational adjustments or disruptions.(e.g. True/False, True means having this violation, False means NO) ",
        "maintenance_location": "location where train units undergo repairment, maintenance, or examination (e.g. True/False, True means having this violation, False means NO)"
    }
}
}