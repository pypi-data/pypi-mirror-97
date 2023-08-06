from scenario_tool_interface import ScenarioToolInterface

sti = ScenarioToolInterface(api_url="https://development-api.dance4water.org/api" )

sti.login("christian.urich@gmail.com", "rejudo01")

project_id = 30327
scenarios = sti.get_scenarios(project_id)

scenario_id = 0
for s in scenarios:
    scenario_id = s['id']
print()
sti.show_log(scenario_id)