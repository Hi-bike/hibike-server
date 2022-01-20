from scrimdor import cdn, mongo

def register_game_profile(user_id, game, nickname, server):
    doc = mongo.db.profile.game.find_one({'user_id':user_id})
    if doc and game in doc:
        # 게임에 계정 추가
        mongo.db.profile.game.update_one(
            {'user_id':user_id},
            {'$set':{
                '{}.accounts.{}'.format(game, nickname):{
                'nickname':nickname,
                'server':server,
                'account_checked':True, 
                'certified': False
            }}})
    else:
        # 최초 등록
        mongo.db.profile.game.update_one(
            {'user_id':user_id}, 
            {'$set':{
                game:{
                    'game':game,
                    'image':"{}.png".format(game),
                    'checked': True,
                    'accounts':{
                        nickname:{ 
                            'nickname':nickname,
                            'server':server,
                            'account_checked':True, 
                            'certified': False
                        }
                    }
                }
            }},
            upsert = True
        )       
    
    return True
