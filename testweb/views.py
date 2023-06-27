from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from testweb.models import Signup
from testweb.models import Signup1
from testweb.models import Student
from testweb.models import Result
from testweb.models import Reset
from testweb.models import Test
from datetime import date,timedelta
from testweb.models import Math
from testweb.models import MathResult
from testweb.models import Chemistry
from testweb.models import ChemistryResult
from testweb.models import Physics
from testweb.models import PhysicsResult
from testweb.models import TeacherSignup
from testweb.models import Teacher
from rest_framework import viewsets
from testweb.serializers import TestSerializer
import random
import uuid
from .email import send_forget_password_mail
import time


class TestSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    



#signup function for teachers
def signupteacher(request):
    context = {'success':False}
    if request.method == 'POST':
        name = request.POST['Name']
        email = request.POST['Email']
        password = request.POST['Pass']
        subject = request.POST['subject']
        password = make_password(password)
        
        if(len(Signup.objects.filter(srollno=email)) or len(TeacherSignup.objects.filter(empid=email))):
            print("Inside")
            context = {'success':False}
        else:
            context = {'success':True}
            teachersignup = TeacherSignup(empid=email,ename=name,epass=password,esubject=subject)
            teacher = Teacher(empid=email,ename=name,esubject=subject)
            teachersignup.save()
            teacher.save()
            print(email,subject,name)
        print("Outside") 
    return render(request,'signupteacher.html',context=context)





#signin for teacher
def signinteacher(request):
    context = {'success':False}
    if request.method == "POST":
        email = request.POST["Email"]
        password = request.POST["Pass"]
        candiate_password_from_database = ""
        if(len(TeacherSignup.objects.filter(empid = email))):
            candiate_password_from_database = TeacherSignup.objects.get(empid = email)
        else:
            return render (request,'signupteacher.html')
        
        check = check_password(password,candiate_password_from_database.epass)
        candidate = TeacherSignup.objects.filter(empid=email)
        
        if(len(TeacherSignup.objects.filter(empid = email)) and check==True):
            request.session['TeacherEmail'] = candidate[0].empid
            request.session['Pass'] = candidate[0].epass
            # print("hi")
            teacher_name = TeacherSignup.objects.get(empid=email)
            context = {'empno':request.session['TeacherEmail'],'teacher':teacher_name.ename,'subject':teacher_name.esubject}
            return render(request,'hometeacher.html',context)
        else:
            context = {'message':'Your email or password was wrong','success':True}
            return render(request,'signinteacher.html',context)

    return render(request,'signinteacher.html')







#signin for students
def signin(request):
    passs = Signup.objects.all()
    count=0
    if request.method=='POST':
        email = request.POST['Email']
        passwords = request.POST['Pass']
        candiate_password_from_database=""
        if(len(Signup.objects.filter(srollno=email))):
            candiate_password_from_database = Signup.objects.get(srollno = email)
        else:
            return render(request,'signup.html')
        # print(make_password(passwords))
        password = check_password(passwords,candiate_password_from_database.spass)
        candidate = Signup.objects.filter(srollno=email)
        if(len(Signup.objects.filter(srollno=email)) and password==True):
            request.session['Email'] = candidate[0].srollno
            request.session['Pass'] = candidate[0].spass
            student_name = Signup.objects.get(srollno=email).sname
            context = {'rollno':request.session['Email'],'studentname':student_name}
            return render(request,'home.html',context)
        else:
            count=1
            context = {'student':passs,'yes':"Wrong Password or Email",'count':count}
            return render(request,'signin.html',context)
    else:
        return render(request,'signin.html')





#signup function for students
def signup(request):
    size = Signup.objects.count()
    context = {'success':False}
    if request.method == 'POST':
        name = request.POST['Name']
        rollNo = request.POST['Email']
        password = request.POST['Pass']
        password = make_password(password)
        signup = Signup(sname = name,srollno=rollNo,spass=password)
        signup1 = Signup1(sname = name,srollno=rollNo,spass=password)
        student = Student(srollno = rollNo, sname=name)
       
        print(size)
        if len(Signup.objects.filter(srollno=rollNo)) or len(TeacherSignup.objects.filter(empid=rollNo)):
            context={'success':False}
        else:
            print(name,rollNo,password)
            signup.save()
            signup1.save()
            student.save()
            context={'success':True}
    return render(request,'signup.html',context)

  
  
  
  
  
#forget password  for teacher
def forget(request):
    if request.method =='POST':
        email = request.POST['Email']
        print(email)
        # emails = request.POST['TeacherEmail']
        if(len(Signup1.objects.filter(srollno=email))):
            token = str(uuid.uuid4())
            context = {'message':"Link has been sent.",'count':1}
            reset_student_password = Reset(srollno = email,stoken=token)
            send_forget_password_mail(email,token)
            reset_student_password.save()
            return render(request,'forget.html',context)
        
        elif(len(TeacherSignup.objects.filter(empid=email))):
            token = str(uuid.uuid4())
            context = {'message':"Link has been sent.",'count':1}
            reset_teacher_password = Reset(srollno = email,stoken=token)
            send_forget_password_mail(email,token)
            reset_teacher_password.save()
            print(email)
            return render(request,'forget.html',context)
        
        else:
            return render(request,'signup.html')
    return render(request,'forget.html')
  



  

#confirm password reset  student
def confirm(request):
    object = Reset.objects.get(sid=Reset.objects.latest('sid').sid)
    
    if object.date == date.today():
        if request.method == 'POST':
            password = request.POST['Pass1']
            password1 = request.POST['Pass']
            
            if (len(Signup.objects.filter(srollno = object.srollno))) and password == password1:
                student_password_change = Signup.objects.get(srollno = object.srollno)
                student_password_change1 = Signup1.objects.get(srollno = object.srollno)
                student_password_change.spass = make_password(password)
                student_password_change1.spass = make_password(password)
                object.spass = make_password(password)
                print('changed',object.srollno)
                student_password_change.save()
                object.save()
                student_password_change1.save()
                return render(request,'confirm.html')
            
            elif (len(TeacherSignup.objects.filter(empid = object.srollno))):
                teacher_password_change = TeacherSignup.objects.get(empid = object.srollno)
                teacher_password_change.epass = make_password(password)
                object.spass = make_password(password)
                print('changed',object.srollno)
                teacher_password_change.save()
                object.save()
                return render(request,'confirm.html')
            else:
                return render(request,'notconfirm.html')
    else:
        return render(request,'linkexpired.html')







#link expired page
def linkexpired(request):
    return render(request,'linkexpired.html')








#if password not changed properly 
def notconfirm(request):
    return render(request,'notconfirm.html')
  
  
  
 
 
  
#changepassword
def changepassword(request,token):
    return render(request,'changepassword.html')
 
    
    
    
    
    
#home page 
def home(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    else:
        print(request.session.get('Email'))
        student_name = Student.objects.get(srollno=request.session['Email'])
        context = {'rollno':request.session['Email'],'studentname':student_name.sname}
        return render(request,'home.html',context)





#home page 
def hometeacher(request):
    if 'TeacherEmail' not in request.session.keys():
        return render(request,'signinteacher.html')
    else:
        print(request.session.get('TeacherEmail'))
        teacher_name = TeacherSignup.objects.get(empid=request.session['TeacherEmail'])
        context = {'empno':request.session['TeacherEmail'],'teacher':teacher_name.ename,'subject':teacher_name.esubject}
        return render(request,'hometeacher.html',context)





#paperset for student
def paperset(request):
    if 'TeacherEmail' not in request.session.keys():
        return render(request,'signinteacher.html')
    else:
        teacher_name = TeacherSignup.objects.get(empid=request.session['TeacherEmail'])
        total_number_of_question=0
        if teacher_name.esubject.lower() == "physics":
            total_number_of_question = Physics.objects.count()+1
        elif teacher_name.esubject.lower() == "chemistry":
            total_number_of_question = Chemistry.objects.count()+1
        elif teacher_name.esubject.lower() == "math":
            total_number_of_question = Math.objects.count()+1
        elif teacher_name.esubject.lower() == "gs":
            total_number_of_question = Test.objects.count()+1
            
        if request.method == "POST":
            questionno = request.POST["Questionno"]
            question = request.POST["Question"]
            ans = request.POST["Ans"]
            ans = ans.lower()
            A = request.POST["A"]
            B = request.POST["B"]
            C = request.POST["C"]
            D = request.POST["D"]
            print(teacher_name.esubject.lower())
            if teacher_name.esubject.lower() == "physics":
                Physicsquestion = Physics(qno=questionno,qname=question, qclass=ans,a=A,b=B,c=C,d=D)
                Physicsquestion.save()
                total_number_of_question = Physics.objects.count()
                total_number_of_question = total_number_of_question+1
                print("SaveP")
                
            elif teacher_name.esubject.lower() == "chemistry":
                Chemistryquestion = Chemistry(qno=questionno,qname=question, qclass=ans,a=A,b=B,c=C,d=D)
                Chemistryquestion.save()
                total_number_of_question = Chemistry.objects.count()
                total_number_of_question = total_number_of_question+1
                print("SaveC",total_number_of_question)
                
            elif teacher_name.esubject.lower() == "math":
                Mathquestion = Math(qno=questionno,qname=question, qclass=ans,a=A,b=B,c=C,d=D)
                Mathquestion.save()
                total_number_of_question = Math.objects.count()
                total_number_of_question = total_number_of_question+1
                print("SaveM",total_number_of_question)
                
            elif teacher_name.esubject.lower() == "gs":
                Testquestion = Test(qno=questionno,qname=question, qclass=ans,a=A,b=B,c=C,d=D)
                Chemistryquestion.save()
                total_number_of_question = Test.objects.count()
                total_number_of_question = total_number_of_question+1
                print("SaveG",total_number_of_question)
                
                
        context = {'empno':request.session['TeacherEmail'],'teacher':teacher_name.ename,'subject':teacher_name.esubject,'size':total_number_of_question}
        return render(request,'paperset.html',context)






#show all question
def totalquestion(request):
    if 'TeacherEmail' not in request.session.keys():    
        return render(request,'signinteacher.html')
    else:
        teacher_name = TeacherSignup.objects.get(empid=request.session['TeacherEmail'])
        context = {}
        if teacher_name.esubject.lower() == "physics":
            physics_question = list(Physics.objects.all())
            context = {'question':physics_question}
        elif teacher_name.esubject.lower() == "chemistry":
            chemistry_question = list(Chemistry.objects.all())
            context = {'question':chemistry_question}
        elif teacher_name.esubject.lower() == "math":
            math_question = list(Math.objects.all())
            context = {'question':math_question}
        elif teacher_name.esubject.lower() == "gs":
            gs_question = list(Test.objects.all())
            context = {'question':gs_question} 
        return render(request,'totalquestion.html',context)






#marks can see by teacher also
def marks(request):
    if 'TeacherEmail' not in request.session.keys():    
        return render(request,'signinteacher.html')
    else:
        teacher_name = TeacherSignup.objects.get(empid=request.session['TeacherEmail'])
        context = {}
        if teacher_name.esubject.lower() == "physics":
            physics_question = list(PhysicsResult.objects.all())
            context = {'result':physics_question,'subject':'Physics','empid':request.session['TeacherEmail']}
        elif teacher_name.esubject.lower() == "chemistry":
            chemistry_question = list(ChemistryResult.objects.all())
            print(chemistry_question)
            context = {'result':chemistry_question,'subject':'Chemistry','empid':request.session['TeacherEmail']}
        elif teacher_name.esubject.lower() == "math":
            math_question = list(MathResult.objects.all())
            context = {'result':math_question,'subject':'Math','empid':request.session['TeacherEmail']}
        elif teacher_name.esubject.lower() == "gs":
            gs_question = list(Result.objects.all())
            context = {'result':gs_question,'subject':'GS','empid':request.session['TeacherEmail']} 
        return render(request,'marks.html',context)




#logout student user here 
def logout(request):   
    if 'Email' not in request.session.keys():    
        return render(request,'signin.html')
    del request.session['Email']
    del request.session['Pass']
    return render(request,'signin.html')




def front(request):
    return render(request,'front.html')




#logout teacher user here
def logoutteacher(request): 
    if 'TeacherEmail' not in request.session.keys():    
        return render(request,'signinteacher.html')
    del request.session['TeacherEmail']
    del request.session['Pass']
    return render(request,'signinteacher.html')





#general knowledge test
def tests(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    
    n = int(request.GET['n'])
    question = list(Test.objects.all())
    random.shuffle(question)
    question_list = question[:n]
    context = {'test':question_list,'count':n}
    return render(request,'test.html',context=context)




#chemistry test
def chemistrytest(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    
    n = int(request.GET['n'])
    question = list(Chemistry.objects.all())
    random.shuffle(question)
    question_list = question[:n]
    context = {'test':question_list,'count':n}
    return render(request,'chemistrytest.html',context=context)





#physics test
def physicstest(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    
    n = int(request.GET['n'])
    question = list(Physics.objects.all())
    random.shuffle(question)
    question_list = question[:n]
    context = {'test':question_list,'count':n}
    return render(request,'physicstest.html',context=context)





#math test
def mathtest(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    
    n = int(request.GET['n'])
    question = list(Math.objects.all())
    random.shuffle(question)
    question_list = question[:n]
    context = {'test':question_list,'count':n}
    return render(request,'mathtest.html',context=context)






#physics
def physics(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    context = {'rollno':request.session['Email']}
    return render(request,'physics.html',context=context)





#chemistry
def chemistry(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    context = {'rollno':request.session['Email']}
    return render(request,'chemistry.html',context=context)





#math
def math(request):
    if 'Email' not in request.session.keys():
       return render(request,'signin.html')
    context = {'rollno':request.session['Email']}
    return render(request,'math.html',context=context)





#gs
def gs(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    context = {'rollno':request.session['Email']}
    return render(request,'gs.html',context=context)




#calculate result gs result here
def calculate(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Test.objects.get(qno=n)
        try:
            if question.qclass == request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    if total_attempt == 0:
        points = (total_right)/10
    else:
        points = (total_right)/total_attempt*10

    # store result in result in Result table
    result = Result()
    result.username = Student.objects.get(srollno = request.session['Email'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    # update candiate table
    candidate = Student.objects.get(srollno = request.session['Email'])
    candidate.sattempt +=1
    candidate.spoints += (candidate.spoints)
    candidate.save()
    resultg = Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = "General Studies"
    context = {'result':resultg,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)






#calculate physics result here
def calculatep(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Physics.objects.get(qno=n)
        try:
            if question.qclass == request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    if total_attempt == 0:
        points = (total_right)/10
    else:
        points = (total_right)/total_attempt*10

    # store result in result in Result table
    result = PhysicsResult()
    result.username = Student.objects.get(srollno = request.session['Email'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    # update candiate table
    candidate = Student.objects.get(srollno = request.session['Email'])
    candidate.sattempt +=1
    candidate.spoints += (candidate.spoints)
    candidate.save()
    resultp = PhysicsResult.objects.filter(resultid=PhysicsResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = "Physics"
    context = {'result':resultp,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)






#calculate chemistry result here
def calculatec(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Chemistry.objects.get(qno=n)
        try:
            if question.qclass == request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    if total_attempt == 0:
        points = (total_right)/10
    else:
        points = (total_right)/total_attempt*10

    # store result in result in Result table
    result = ChemistryResult()
    result.username = Student.objects.get(srollno = request.session['Email'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    # update candiate table
    candidate = Student.objects.get(srollno = request.session['Email'])
    candidate.sattempt +=1
    candidate.spoints += (candidate.spoints)
    candidate.save()
    resultc = ChemistryResult.objects.filter(resultid=ChemistryResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = "Chemistry"
    context = {'result':resultc,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)






#calculate chemistry result here
def calculatem(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    total_attempt = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Math.objects.get(qno=n)
        try:
            if question.qclass == request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    if total_attempt == 0:
        points = (total_right)/10
    else:
        points = (total_right)/total_attempt*10

    # store result in result in Result table
    result = MathResult()
    result.username = Student.objects.get(srollno = request.session['Email'])
    result.attempt = total_attempt
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    # update candiate table
    candidate = Student.objects.get(srollno = request.session['Email'])
    candidate.sattempt +=1
    candidate.spoints += (candidate.spoints)
    candidate.save()
    resultm = MathResult.objects.filter(resultid=MathResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = "Math"
    context = {'result':resultm,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)






#current test result for gs here 
def result(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch latest result from result table
    result = Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = 'General Studies'
    context = {'result':result,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)




#current test result for chemistry here 
def resultc(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch latest result from result table
    result = ChemistryResult.objects.filter(resultid=ChemistryResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = 'Chemistry'
    context = {'result':result,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)
    




#current test result for gs here 
def resultp(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch latest result from result table
    result = PhysicsResult.objects.filter(resultid=PhysicsResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = 'Physics'
    context = {'result':result,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)





#current test result for math here 
def resultm(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch latest result from result table
    result = MathResult.objects.filter(resultid=MathResult.objects.latest('resultid').resultid,username = request.session['Email'])
    subject = 'Math'
    context = {'result':result,'rollno':request.session['Email'],'subject':subject}
    return render(request,'result.html',context)






#all results show throw this function of gs test
def results(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch all result from result table
    results = Result.objects.filter(username = request.session['Email'])
    subject = 'General Studies'
    context = {'result':results,'rollno':request.session['Email'],'subject':subject}
    return render(request,'results.html',context)





#all results show throw this function of math test
def resultsm(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch all result from result table
    results = MathResult.objects.filter(username = request.session['Email'])
    subject = 'Math'
    context = {'result':results,'rollno':request.session['Email'],'subject':subject}
    return render(request,'results.html',context)
   




#all results show throw this function of physics test
def resultsp(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch all result from result table
    results = PhysicsResult.objects.filter(username = request.session['Email'])
    subject = 'Physics'
    context = {'result':results,'rollno':request.session['Email'],'subject':subject}
    return render(request,'results.html',context)




#all results show throw this function of Chemistry test
def resultsc(request):
    if 'Email' not in request.session.keys():
        return render(request,'signin.html')
    # fetch all result from result table
    results = ChemistryResult.objects.filter(username = request.session['Email'])
    subject = 'Chemistry'
    context = {'result':results,'rollno':request.session['Email'],'subject':subject}
    return render(request,'results.html',context)

# Create your views here.
