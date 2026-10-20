


import re
from os import path
from os import walk


# for root, dirs, files in walk(r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\common\technologies'):

#     for file in files:
#         with open(path.join(root, file)) as f:
#             lines = f.readlines()
#             for l in lines:
#                 match = re.match('	([a-z_0-9]+) = \{', l)
#                 if not match:
#                     continue
#                 tech = match.group(1)
#                 print(f'''			set_technology = {{
# 				{tech} = 1
#             }}''')


# specs = ['air',  'land', 'nuclear', 'naval', 'radar', 'rocket']

# for s in specs:
#     p = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Hearts of Iron IV\\common\\special_projects\\projects\\' + s + '_projects.txt'
#     with open(p, mode='r') as f:
#         lines = f.readlines()
#         for l in lines:
#             match = re.match('([a-z_]+) = \{', l)
#             if not match:
#                 continue
#             tech = match.group(1)
#             #print(f'''            complete_special_project = sp:{tech}''')

categories = '''
	light_air
	medium_air
	heavy_air
	armor
	cat_light_armor
	cat_medium_armor
	cat_heavy_armor
	artillery
	cat_anti_tank
	cat_anti_air
	naval_air
	infantry_weapons
	motorized_equipment
	cat_mechanized_equipment
	naval_equipment
	rocketry
	nuclear
	industry
	electronics
	cat_fortification
	land_doctrine
	air_doctrine
	naval_doctrine
	strategic_destruction_tree
	battlefield_support_tree
	operational_integrity_tree
	jet_technology
	trade_interdiction_tree
	convoy_defense_tree
	light_fighter
	cat_heavy_fighter
	tactical_bomber
	cat_strategic_bomber
	naval_bomber
	cas_bomber
	ship_modules_tech
	dd_tech
	cl_tech
	ca_tech
	cv_tech
	bc_tech
	bb_tech
	shbb_tech
	ss_tech
	tp_tech
	synth_resources
	fleet_in_being_tree
	encryption_tech
	decryption_tech
	computing_tech
	radar_tech
	infantry_tech
	marine_tech
	construction_tech
	excavation_tech
	submarine_doctrine
	air_equipment
	cat_mobile_warfare
	cat_superior_firepower
	cat_grand_battle_plan
	cat_mass_assault
	cat_base_strike
	cat_trade_interdiction
	cat_fleet_in_being
	cat_strategic_destruction
	cat_battlefield_support
	cat_operational_integrity
	night_vision
	base_strike_main
	mot_rockets
	support_tech
	para_tech
	engineers_tech
	recon_tech
	mountaineers_tech
	military_police_tech
	hospital_tech
	logistics_tech
	signal_company_tech
	maintenance_company_tech
	naval_mines
	concentrated_industry_category
	dispersed_industry_category
	asw_tech
	naval_minesweeping
	naval_minelaying
	cat_scout_plane
	train_tech
	cat_production
	cat_synth_rubber
	cat_synth_oil
	cat_armored_cars
	cat_special_forces_generic
	cat_torpedoes
	cat_ship_light_battery
	cat_ship_medium_battery
	cat_ship_heavy_battery
	air_equipment
	plane_modules_tech
	cat_air_guns
	cat_air_engine
	cat_air_bombs
	special_forces_doctrine
	cat_maritime_patrol
	cat_mountaineers_doctrine
	cat_marines_doctrine
	cat_paratroopers_doctrine
	naval_armor
	naval_artillery
	helicopter_tech
	pykrete_tech
	transport_planes_cat
'''

counter = 0
for category in categories.split('\n'):
    counter +=1
    print(f'''
			add_tech_bonus = {{
				uses = 100
				bonus = 1
				name = CHI_oracle{counter}
				category = {category.strip()}
            }}
''')
    
while counter:
    print(f'  CHI_oracle{counter}: "Oracle {counter}"')
    counter -= 1