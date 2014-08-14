from userdb import Base, user_table, candidate_table

def isKnown(name, session):
    userlist = [user[0] for user in session.query(user_table.user)]
    return (name in userlist)

def userlist(session):
    return [user[0] for user in session.query(user_table.user)]

def authenticate(name, password, session):
    plist = [p[0] for p in session.query(user_table.password).filter(user_table.user == name)]
    #print password , plist
    #print (password in plist)
    return password in plist

def adduser(name, password, session):
    newuser = user_table(name, password)
    session.add(newuser)
    session.commit()
    return

def saveresult(name, session, result):
    #try:
    #print result
    newres = [name] + result
    candidate = candidate_table(*newres)
    session.add(candidate)
    session.commit()
    #except TypeError:
        #print [type(r) for r in result ]
    return 

def QueryUserProfile(name, session):
    submitted_labels =  [l[0] for l in session.query(candidate_table.label).filter(candidate_table.user == name)]
    size = len(submitted_labels)
    return len([l for l in submitted_labels if l == 'g']), len([l for l in submitted_labels if l == 'b']), size


