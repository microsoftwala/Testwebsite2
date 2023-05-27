from django.contrib import admin
from django.urls import path,include
from testweb.views import TestSet
from rest_framework import routers
from testweb import views

app_name = 'testweb'


router = routers.DefaultRouter()
router.register(r'tests',TestSet)


urlpatterns = [
    path('/',include(router.urls)),
    path('signup',views.signup,name='Signup'),
    path('',views.front,name='Front'),
    path('signin',views.signin,name='Signin'),
    path('signinteacher',views.signinteacher,name='Signinteacher'),
    path('forget',views.forget,name='Forget'),
    path('home',views.home,name='Home'),
    path('hometeacher',views.hometeacher,name='Hometeacher'),
    path('signup',views.signup,name='Signupstudent'),
    path('signupteacher',views.signupteacher,name='Signupteacher'),
    path('logout',views.logout,name='logout'),
    path('logoutteacher',views.logoutteacher,name='logoutteacher'),
    path('tests',views.tests,name='tests'),
    path('paperset',views.paperset,name='paperset'),
    path('totalquestion',views.totalquestion,name='totalquestion'),
    path('marks',views.marks,name='marks'),
    path('calculate',views.calculate,name='calculate'),
    path('calculatep',views.calculatep,name='calculatep'),
    path('calculatec',views.calculatec,name='calculatec'),
    path('calculatem',views.calculatem,name='calculatem'),
    path('result',views.result,name='result'),
    path('resultp',views.resultp,name='resultp'),
    path('resultc',views.resultc,name='resultc'),
    path('resultm',views.resultm,name='resultm'),
    path('results',views.results,name='results'),
    path('resultsp',views.resultsp,name='resultsp'),
    path('resultsc',views.resultsc,name='resultsc'),
    path('resultsm',views.resultsm,name='resultsm'),
    path('changepassword/<token>/',views.changepassword,name='Changepassword'),
    path('confirm',views.confirm,name='confirm'),
    path('notconfirm',views.notconfirm,name='notconfirm'),
    path('physics',views.physics,name='physics'),
    path('chemistry',views.chemistry,name='chemistry'),
    path('gs',views.gs,name='gs'),
    path('mathtest',views.mathtest,name='mathtest'),
    path('physicstest',views.physicstest,name='physicstest'),
    path('chemistrytest',views.chemistrytest,name='chemistrytest'),
    path('math',views.math,name='math'),
    path('linkexpired',views.linkexpired,name='linkexpired'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
