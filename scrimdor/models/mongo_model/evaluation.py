'''
collection name: profile.evaluation
description: 유저가 받은 평가 비율
field:
    user_id: 유저 고유번호
    positive: 받은 긍정평가 개수
    negative: 받은 부정평가 개수
    유저가 받은 평가항목별 개수 
    * 평가항목 p#: 긍정평가
    * 평가항목 n#: 부정평가

ex)
{
    'user_id':2,
    'positive': 2,
    'negative': 3,
    'n1':3
    'p1':3,
    'p2':10
}
'''

'''
collection name: profile.evaluation.log
description: 유저가 받은 평가 기록
field:
    user_id: 평가 받은 유저 고유번호
    평가한 사람의 고유번호: {
        evaluated_user_id: 평가 받은 유저 고유번호
        kinds: negative or positive
        contents: [평가 받은 내용]
    }

ex)
{
        "user_id": 3,
        "2": {
            "evaluated_user_id": 3,
            "kinds": "negative",
            "contents": [
                -1,
                -4,
                -5,
                "good"
            ]
        },
        "3": {
            "evaluated_user_id": 3,
            "kinds": "negative",
            "contents": [
                -1,
                0,
                0,
                "bad"
            ]
        }
    }
'''