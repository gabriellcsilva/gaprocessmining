def preprocess(log):
    dicionario_ativ = {
        'user logout' : 'A',
        'resource view':'B',
        'url view' : 'C',
        'course view' : 'D',
        'user login' : 'E',
        'page view' : 'F',
        'workshop view' : 'G',
        'assignment view' : 'H',
        'assignment upload' : 'I',
        'blog view' : 'J',
        'user view all' : 'K',
        'user view' : 'L',
        'user change password' : 'M',
        'data view' : 'N',
        'message write' : 'O',
        'user update' : 'P',
        'data add' : 'Q',
        'data update' : 'R',
        'blog update' : 'S',
        'blog add' : 'T',
        'forum view forum' : 'U',
        'assignment view all' : 'V',
        'data record delete' : 'X',
        'library mailer' : 'Y'}

    for i,k in enumerate(log):
        log[i] = dicionario_ativ[k]

    return