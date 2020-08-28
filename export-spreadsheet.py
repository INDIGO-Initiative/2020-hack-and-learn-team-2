import requests
import csv
import jsonpointer

BASE_URL = "https://golab-indigo-data-store.herokuapp.com"


def go():
    r1 = requests.get(BASE_URL + '/app/api1/project')


    with open('out.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Project: ID",
            "Project: Name",
            "Project: Delivery Location Countries",
            "Project: Intervention",
            "Project: Target population",
            "Project: Policy Sector",
            "Outcome: ID",
            "Outcome: Outcome Definition",
            "Outcome: Target Population",
            "Outcome: Targeted number of service users Or beneficiaries (total)",
            "Outcome: Unit type of targeted Service users or beneficiaries",
            "Outcome: Unit description of Service user or beneficiaries",
            "Outcome: Outcome metric target",
            "Outcome: Other target for Meeting outcome metric target",
            "Outcome: Outcome validation Method",
            "Outcome: Data source for Outcome validation",
            "Outcome: Policy sector",
            "Outcome: Primary SDG goal",
            "Outcome: Secondary SDG goals",
            "Outcome: Primary SDG target",
            "Outcome: Secondary SDG targets",
            "Outcome: Notes",
        ])

        project_ids = [d.get('id') for d in r1.json().get('projects') if d.get('public')]
        project_ids.sort()

        for project_id in project_ids:
                print(project_id)
                request_project =  requests.get(BASE_URL + '/app/api1/project/' + project_id)
                project_data = request_project.json()

                delivery_location_countries_string = ""
                delivery_locations_list = jsonpointer.resolve_pointer(project_data, "/project/data/delivery_locations", [])
                if isinstance(delivery_locations_list, list):
                    delivery_location_countries = [
                        jsonpointer.resolve_pointer(d, '/location_country/value', '') for d in delivery_locations_list
                    ]
                    delivery_location_countries_string = ', '.join(
                        list(set([ i for i in delivery_location_countries if i ]))
                    )

                for outcome_metric_data in jsonpointer.resolve_pointer(project_data, "/project/data/outcome_metrics", []):

                    row = [
                        jsonpointer.resolve_pointer(project_data, "/project/id"),
                        jsonpointer.resolve_pointer(project_data, "/project/data/name/value", ''),
                        delivery_location_countries_string,
                        jsonpointer.resolve_pointer(project_data, "/project/data/purpose_and_classifications/intervention/value", ''),
                        jsonpointer.resolve_pointer(project_data, "/project/data/service_and_beneficiaries/target_population/value", ''),
                        jsonpointer.resolve_pointer(project_data, "/project/data/purpose_and_classifications/policy_sector/value", ''),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/id"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/definition/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/target_population/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/targeted_number_of_service_users_or_beneficiaries_total/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/unit_type_of_targeted_service_users_or_beneficiaries/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/unit_description_of_service_user_or_beneficiaries/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/outcome_metric_target/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/other_target_for_meeting_outcome_metric_target/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/outcome_validation_method/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/data_source_for_outcome_validation/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/policy_sector/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/primary_sdg_goal/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/secondary_sdg_goals/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/primary_sdg_target/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/secondary_sdg_targets/value"),
                        jsonpointer.resolve_pointer(outcome_metric_data, "/notes"),

                    ]

                    writer.writerow(row)




if __name__ == "__main__":
    go()
