from django.shortcuts import render, get_object_or_404, redirect,get_list_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from Log.models import *
from Log.serializers import *
from .forms import *
from .models import *
from rest_framework import status,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
# Create your views here.


def show(request):
    return render(request, 'base.html')


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        username = request.data['Username']
        password = request.data['password']
        print(request.data)
        print(username)
        user = auth.authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            #us_v = {'Username':username, 'Password':password}
            #us = UserSerializer(request.data)
            #print(us)
            return Response(request.data)
        else:
            return Response({'error':'username or password is incorrect'})


@api_view(['GET', 'POST'])
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return Response({'logout'})

@api_view(['GET', 'POST'])
def PeListView(request):
    if request.method == 'GET':
        per_list = Performance.objects.all()
        perl = per_list[1:]
        print(perl)
        serializer = PerformanceSerializer(perl, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        per_list = Performance.objects.all()
        perl = per_list[1:]
        print(perl)
        serializer = PerformanceSerializer(perl, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])
def PeCreateView(request):
    if request.method == "POST":
        create_serializer = PerformanceCreateSerializer(data=request.data)
        form = PerCreateForm(request.POST, request.FILES)
        scontents = SContents.objects.order_by('id')
        if create_serializer.is_valid():
            genre = create_serializer.validated_data['genre']
            title = create_serializer.validated_data['title']
            directiont = create_serializer.validated_data['directiont']
            configurationt = create_serializer.validated_data['configurationt']
            check = create_serializer.validated_data['check']
            date = create_serializer.validated_data['date']
            place = create_serializer.validated_data['place']
            special = create_serializer.validated_data['special']
            p = Performance.objects.order_by('-id')
            l=p[0].id+1
            perfor=Performance.objects.create(pk=l,title=title)
           #new_user = UserDetail.objects.create(user=request.user, performance=perfor)
            #new_user.save()
            a=[genre,title,directiont,configurationt,check,date,place,special]
            for i in scontents:
                MContents.objects.create(performance=perfor, SCNum=i.id, SCName=i.SCName,filetype=i.filetype)
            MContents.objects.order_by('id')
            for i in range(0,8):
                mc = MContents.objects.get(performance=perfor,SCNum=scontents[i].id,SCName=scontents[i].SCName)
                mc.tcontent = a[i]
                mc.save()
            mct = MContents.objects.order_by('id')
            s = STask.objects.order_by('id')
            for i in s:
                for x in mct:
                    if i.SCNum == None:
                        if i.Dbool == 1:
                            MTask.objects.create(TNum=i.TNum, DetNum=i.DetNum, TName=i.TName, DetName=i.DetName,
                                                 SCNum=i.SCNum, objective=i.objective, category=i.category_id,
                                                 bool=i.bool,
                                                 performance=perfor, Dbool=1)
                        else:
                            MTask.objects.create(TNum=i.TNum, DetNum=i.DetNum, TName=i.TName, DetName=i.DetName,
                                                 SCNum=i.SCNum, objective=i.objective, category=i.category_id, bool=i.bool,
                                                 performance=perfor,Dbool=0)
                        break
                    elif i.SCNum == x.SCNum:
                        MTask.objects.create(TNum=i.TNum, DetNum=i.DetNum, TName=i.TName, DetName=i.DetName,
                                             SCNum=i.SCNum, objective=i.objective, category=i.category_id, bool=i.bool,
                                             performance=perfor,mcontents=x,Dbool=0)
                        break
                    else:
                        continue
            return Response(create_serializer.data, status=status.HTTP_201_CREATED)
    return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def CaTaskView(request,pk):
    if request.method == 'GET':
        category = Category.objects.all()
        category_serializer = CategorySerializer(category, many=True)
        performance = get_object_or_404(Performance, pk=pk)
        performance_serializer = PerformanceSerializer(performance)
        mtask = get_list_or_404(MTask.objects.order_by('TNum'), performance=performance,Dbool=1)
        mtask_serializer = MTaskSerializer(mtask, many=True)
        s=[]
        s.append(performance_serializer.data)
        s = s + category_serializer.data + mtask_serializer.data
        return Response(s)

'''@api_view(['GET','POST','DELETE'])
def DepCreateView(request,pk):
    performance = get_object_or_404(Performance, pk=pk)

    if request.method == 'GET':
        dep = Department.objects.filter(performance=performance)
        dep_ser = DepartSerializer(dep, many=True)
        return Response(dep_ser.data)

    elif request.method == 'POST':
        dep_ser = DepartSerializer(data=request.data)
        if dep_ser.is_valid():
            name = dep_ser.validated_data['name']
            dep = Department.objects.create(performance=performance,name=name)
            team = Team.objects.create(performance=performance,name=name)
            de_ser = DepartSerializer(dep)
            team_ser = TeamSerializer(team)
            d=[]
            d.append(de_ser.data)
            d.append(team_ser.data)
            return Response(d, status=status.HTTP_201_CREATED)

    return Response(dep_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
@api_view(['GET', 'DELETE'])
def PeDeleteView(request,pk):
    try:
        performance = Performance.objects.get(pk=pk)
    except Performance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        performance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST','PUT'])
def TaskContentView(request, pk, tnum):
    mtask1 = get_list_or_404(MTask.objects.order_by('DetNum'), performance_id=pk, TNum=tnum, Dbool=0)
    print(mtask1)
    mtask2 = get_object_or_404(MTask.objects.order_by('DetNum'), performance_id=pk, TNum=tnum, Dbool=1)

    mtask1_serializer = MTaskSerializer(mtask1, many=True)
    mtask2_serializer = MTaskSerializer(mtask2)
    sc = []
    mcc = []
    mcont = []
    dl = []
    delog = DetailLog.objects.filter(performance_id=pk).order_by('date')
    for i in mtask1:
        sc.append(i.SCNum)
        mcc.append(i.mcontents_id)
        dd = delog.filter(mc=i.mcontents_id)
        dl = dl +list(dd)
        print(dd)
        print(dl)

    dl.sort(key=lambda object: object.date)
    dl_serializer = DetailLogSerializer(dl, many=True)

    c = [x for x in zip(sc, mcc)]
    c = dict(c)
    print(c)
    for key, value in c.items():
        mcont.append(get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
    mcont_serializer = MContentSerializer(mcont, many=True)
    #print(type(mtask_serializer))
    userd = get_object_or_404(UserDetail, user=request.user)
    com = get_list_or_404(Comment.objects.order_by('create'), performance_id=pk, TNum=tnum)
    com_serializer = CommentSerializer(com, many=True)

    if request.method == 'GET': # Contents Task Read
        s=[]
        s.append(mtask2_serializer.data)
        s = s + dl_serializer.data + mtask1_serializer.data + mcont_serializer.data + com_serializer.data
        return Response(s)

    elif request.method == 'PUT': # Task Update
        mtask3_serializer = MTaskSerializer(mtask2,data=request.data)
        if mtask3_serializer.is_valid():
            mtask3_serializer.save()
            return Response(mtask3_serializer.data)
        return Response(mtask3_serializer.errors, status.HTTP_400_BAD_REQUEST)

'''
@api_view(['GET', 'POST'])
def DetailCreateView(request, pk, tnum):
    mtask1 = get_list_or_404(MTask.objects.order_by('DetNum'), performance_id=pk, TNum=tnum, Dbool=0)
    detn = mtask1[0].DetNum
    mt1 = get_list_or_404(MTask.objects.order_by('id'),performance_id=pk, DetNum=detn ,Dbool=0)
    sc=[]
    mcc=[]
    for i in mtask1:
        sc.append(i.SCNum)
        mcc.append(i.mcontents_id)

    c = [x for x in zip(sc, mcc)]
    c = dict(c)
    mcont=[]
    for key, value in c.items():
        mcont.append(get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
    mc = get_list_or_404(MContents.objects.order_by('SCNum'), performance_id=pk)
    mc1 = mc[-1].SCNum
    x=1
    mc2 =[]
    mt2=[]
    if request.method == 'POST':
        for i in mcont:
            mc2.append(MContents.objects.create(performance_id=pk, SCNum=mc1+x, SCName=i.SCName, filetype=i.filetype))
            mt2.append(MTask.objects.create(performance_id=pk, TNum=tnum, ,SCNum=mc2[x-1].SCNum, mcontents=))
'''

@api_view(['GET', 'PUT'])
def ContentsUpdateView(request,pk,tnum,id):
    mtask = get_list_or_404(MTask, performance_id=pk, TNum=tnum,Dbool=0)
    sc = []
    mc = []
    for i in mtask:
        sc.append(i.SCNum)
        mc.append(i.mcontents_id)

    c = [x for x in zip(sc, mc)]
    c = dict(c)
    for key, value in c.items():
        con = (get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
        if con.filetype == 1:
            confile = MContentsFile.objects.create(mcontents=con)
            if con.id == id:
                con_serializer = MContentSerializer(con, data=request.data)
                confile_serializer = MContentFileSerializer(confile, data=request.data)
                break
        else:
            if con.id == id:
                con_serializer = MContentSerializer(con, data=request.data)
                break

    if request.method == 'PUT': # Contents Update
        print(con.filetype)
        if con.filetype == 1:
            if confile_serializer.is_valid():
                confile_serializer.save()
                if con_serializer.is_valid():
                    con_serializer.save()
                    t = get_object_or_404(MTask, performance_id=pk, mcontents_id=value, SCNum=key, TNum=tnum)
                    print(request.user)
                    ud = get_object_or_404(UserDetail, user_id=request.user, performance_id=pk, TNum=None)
                    print(ud)
                    dlog = DetailLog.objects.create(performance_id=pk, mtask=t, userdetail=ud, mc=t.mcontents_id)
                    dlog.save()
                   # dlog_serializer = DetailLogSerializer(dlog)
                    s=[]
                    s.append(con_serializer.data)
                    s.append(confile_serializer.data)
                  #  s.append(dlog_serializer)
                    return Response(s)
                return Response(confile_serializer.data)
            return Response(confile_serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            if con_serializer.is_valid():
                con_serializer.save()
                return Response(con_serializer.data)
            return Response(con_serializer.errors, status.HTTP_400_BAD_REQUEST)
    #if request.method == 'POST':
     #   confile = MContentsFile.objects.create(mcontents=con)


#@api_view(['GET', 'PUT'])
#def TaskUpdateView(request,pk,tnum,):


@api_view(['GET','POST'])
def comment(request,pk,tnum):
    #mtask = get_object_or_404(MTask, performance_id=pk, TNum=tnum, Dbool=1)
    #comment = Comment.objects.filter(TNum=mtask.TNum)
    userd = get_object_or_404(UserDetail, user=request.user)

    if request.method == 'POST':
        comment = Comment.objects.create(performance_id=pk, TNum=tnum, userdetail=userd, username=request.user.username)
        print(request.user.username)
        print('dddddddddd')
        comment_serializer = CommentSerializer(comment, data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        return Response(comment_serializer.errors,status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def comment_reply(request,pk,tnum,id):
    userd = UserDetail.objects.get(user=request.user)
    if request.method == 'POST':
        comment = Comment.objects.create(performance_id=pk, TNum=tnum, userdetail=userd, parent_id=id, username=request.user.username)
        comment_serializer = CommentSerializer(comment, data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data)
        return Response(comment_serializer.errors, status.HTTP_400_BAD_REQUEST)


'''
@api_view(['GET', 'POST', 'PUT'])
def fileupload(request,pk, tnum, id):
    mtask = get_list_or_404(MTask, performance_id=pk, TNum=tnum, Dbool=0)
    sc = []
    mc = []
    for i in mtask:
        sc.append(i.SCNum)
        mc.append(i.mcontents_id)
    c = [x for x in zip(sc, mc)]
    for key, value in c.items():
        con = (get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
        confile = get_object_or_404(MContentsFile, mcontents=con)
        if con.id == id:
            confile_serializer = MContentSerializer(confile, data=request.data)
            break
    if request.method == 'PUT':  # Contents Update
        if confile_serializer.is_valid():
            confile_serializer.save()
            return Response(confile_serializer.data)
        return Response(confile_serializer.errors, status.HTTP_400_BAD_REQUEST)
'''

'''def TaModifyView(request,pk):
    mtask = get_object_or_404(MTask,pk=pk)
    if request.method == "POST":'''

'''mlist = []
       ml = []
       for i in mtask_serializer:
           if i.TNum not in mlist:
               mlist.append(i.TNum)
               ml.append(i)
           else:
               continue
       max=0
       zero =[]
       one=[]
       two=[]
       three=[]
       four=[]

       for i in ml:
           if i.category == category[0].id:
               zero.append(i)
           elif i.category == category[1].id:
               one.append(i)
           elif i.category == category[2].id:
               two.append(i)
           elif i.category == category[3].id:
               three.append(i)
           elif i.category == category[4].id:
               four.append(i)
       list = []
       list.append(len(zero))
       list.append(len(one))
       list.append(len(two))
       list.append(len(three))
       list.append(len(four))

       for i in range(0,5):
           if max < list[i]:
               max = list[i]
       list.append(int(max))
       act=[]
       for i in range(0,max):
           if i >= len(zero):
               act.append('')
           else:
               act.append(zero[i])
           if i >= len(one):
               act.append('')
           else:
               act.append(one[i])
           if i >= len(two):
               act.append('')
           else:
               act.append(two[i])
           if i >= len(three):
               act.append('')
           else:
               act.append(three[i])
           if i >= len(four):
               act.append('')
           else:
               act.append(four[i])

       a=[act[i*5:(i+1)*5] for i in range((len(act)+4)//5)]
       l=[]
       for i in range(0,max):
           l.append(int(i))

       context = {'category':category, 'performance':performance, 'mtask':mtask,'act':act,'a':a,'l':l}'''