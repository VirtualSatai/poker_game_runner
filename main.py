import json
from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot, fbl_bot


bots = [fbl_bot, fbl_bot, randombot, randombot, fbl_bot, fbl_bot, randombot, randombot, fbl_bot, fbl_bot]
bot_instances = [b.Bot() for b in bots]

res, details = play_tournament_table(bot_instances, 500, 
                (BlindScheduleElement(20, 5,10,0),
                BlindScheduleElement(40, 10,20,0),     
                BlindScheduleElement(60, 15,30,0),
                BlindScheduleElement(80, 20,40,0),
                BlindScheduleElement(100, 25,50,0),
                BlindScheduleElement(110, 35,70,0),
                BlindScheduleElement(120, 50,100,0),
                BlindScheduleElement(130, 75,150,0),
                BlindScheduleElement(140, 100,200,0),
                BlindScheduleElement(150, 150,300,0),
                BlindScheduleElement(160, 200,400,0),
                BlindScheduleElement(170, 300,600,0),
                BlindScheduleElement(180, 400,800,0),
                BlindScheduleElement(190, 500,1000,0),
                BlindScheduleElement(200, 750,1500,0),
                BlindScheduleElement(210, 1000,2000,0),
                BlindScheduleElement(220, 1500,3000,0),
                BlindScheduleElement(230, 2000,4000,0),
                BlindScheduleElement(250, 3000,6000,0),
                BlindScheduleElement(-1, 4000,8000,0)))
print(res)

with open('output.json', 'w') as file:
    json.dump(details, file)



