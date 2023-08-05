def sin_a(opp, adj, hyp):
    return opp / hyp


def cos_a(opp, adj, hyp):
    return adj / hyp


def tan_a(opp, adj, hyp):
    return opp / adj


def cot_a(opp, adj, hyp):
    return adj / opp


def sec_a(opp, adj, hyp):
    return hyp / adj


def cosec_a(opp, adj, hyp):
    return hyp / opp


def sin_ang(ang):
    if ang == 0:
        return '0'
    if ang == 30:
        return '1/2'
    if ang == 45:
        return '1/√2'
    if ang == 60:
        return '√3/2'
    if ang == 90:
        return '1'


def cos_ang(ang):
    if ang == 0:
        return '1'
    if ang == 30:
        return '√3/2'
    if ang == 45:
        return '1/√2'
    if ang == 60:
        return '1/2'
    if ang == 90:
        return '0'


def tan_ang(ang):
    if ang == 0:
        return '0'
    if ang == 30:
        return '1/√3'
    if ang == 45:
        return '1'
    if ang == 60:
        return '√3'
    if ang == 90:
        return 'undefined'


def cot_ang(ang):
    if ang == 0:
        return 'undefined'
    if ang == 30:
        return '√3'
    if ang == 45:
        return '1'
    if ang == 60:
        return '1/√3'
    if ang == 90:
        return '0'


def sec_ang(ang):
    if ang == 0:
        return '1'
    if ang == 30:
        return '2/√3'
    if ang == 45:
        return '√2'
    if ang == 60:
        return '2'
    if ang == 90:
        return 'undefined'


def cosec_ang(ang):
    if ang == 0:
        return 'undefined'
    if ang == 30:
        return '2'
    if ang == 45:
        return '√2'
    if ang == 60:
        return '2/√3'
    if ang == 90:
        return '1'
    
