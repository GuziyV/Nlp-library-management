from pyswip import *

prolog = Prolog()
prolog.assertz("likes(john,'charles dickens christmas carol')")
prolog.assertz("likes(ben,'victor hugo les miserables')")
prolog.assertz("likes(peter,'ernest hemingway the old man and the sea')")
prolog.assertz("likes(edvard,'shakespeare hamlet')")
prolog.assertz("likes(oliver,' Goethe The Sorrows of Young Werther')")
prolog.assertz("likes(frank,'jerome k jerome three in a boat')")
prolog.assertz("friend(frank,kate)")
prolog.assertz("friend(ben,david)")
prolog.assertz("friend(edvard,jeremy)")
prolog.assertz("friend(jeremy,michael)")
prolog.assertz("friend(steve,john)")
prolog.assertz("friend(mark,kate)")
prolog.assertz("friend(emily,mark)")
prolog.assertz("get_friend(A,B):- friend(A,B);friend(B,A)")
prolog.assertz("get_book(A,B):- likes(A,B);get_friend(A,C),likes(C,B);get_friend(A,C),get_friend(C,D),likes(D,B);get_friend(A,C),get_friend(C,D),get_friend(D,F),likes(F,B)")


def getBook(name):
    l1 =  list(prolog.query("get_book(%s,X)"%name))[0]['X']
    return l1