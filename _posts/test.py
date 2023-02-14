import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./json/obungadiscordbot-firebase-adminsdk-mn0p0-3c97204428.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#=========================Account==================================
def checkUserExist(_name, _id):
    print("user.py - checkUser()")
    # DB에 없는 유저는 NameError가 발생합니다
    try:
        find_user = db.collection(u'users').document(_name)
        if _id == find_user.get().to_dict()['id']:
            return True
        else:
            return False
    except:
        return False

def signUp(_name, _id):
    print("user.py - signUp()")
    if checkUserExist(_name,_id):
        print("등록된 유저")
        return "이미 가입된 유저입니다"
    else: 
        print("미등록 유저 - 회원가입을 진행합니다")
        doc_ref = db.collection(u'users').document(_name)
        doc_ref.set({
            u'id' : _id,
            u'money' : 30000000,
            u'loss' : 0,
            u'level' : 0,
            u'exp' : 0,
            # foreignCurrency
            u'dollar' : 0,
            u'yen' : 0,
            u'yuan' : 0,
            u'euro' : 0,
            u'pound' : 0,
            u'real' : 0,
            u'ruble' : 0,
            u'rupee' : 0,
            # coin
            u'waves' : 0,
            u'btc' : 0,
            u'eth' : 0,
            u'doge' : 0,
            u'ltc' : 0,
            u'etc' : 0,
            u'lunc' : 0,
            u'sand' : 0,
            u'bnb' : 0,
            u'xrp' : 0,
            # item
            u'bait' : 0,
            u'graps' : 0,
            u'wisky' : 0,
            u'vitamin' : 0,
            u'bk' : 0,
            u'kc' : 0,
            u'rkc' : 0,
            u'ostrich' : 0
            })
        return "회원가입 성공, 등록해주셔서 감사합니다."