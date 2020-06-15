import mimetypes

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


from mimetypes import guess_type
import os
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote
import urllib




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
    mtask2 = get_object_or_404(MTask.objects.order_by('DetNum'), performance_id=pk, TNum=tnum, Dbool=1)

    mtask1_serializer = MTaskSerializer(mtask1, many=True)
    mtask2_serializer = MTaskSerializer(mtask2)
    sc = []
    mcc = []
    mcont = []
    taskteam = TaskTeam.objects.filter(performance_id=pk, TNum=tnum)
    taskteam_ser = TaskTeamSerializer(taskteam, many=True)
    participate = UserDetail.objects.filter(performance_id=pk, TNum=tnum)
    participate_ser = UserDetailSerializer(participate, many=True)
    dl = []
    delog = DetailLog.objects.filter(performance_id=pk).order_by('date')
    for i in mtask1:
        sc.append(i.SCNum)
        mcc.append(i.mcontents_id)
        dd = delog.filter(mc=i.mcontents_id)
        dl = dl +list(dd)

    dl.sort(key=lambda object: object.date)
    dl_serializer = DetailLogSerializer(dl, many=True)

    c = [x for x in zip(sc, mcc)]
    c = dict(c)
    print(c)
    for key, value in c.items():
        mcont.append(get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))

    mcont_serializer = MContentSerializer(mcont, many=True)
    #print(type(mtask_serializer))
    #userd = get_object_or_404(UserDetail, user=request.user)
    com = Comment.objects.filter(performance_id=pk, TNum=tnum).order_by('create')
    print("dddd")

    com_serializer = CommentSerializer(com, many=True)

    if request.method == 'GET': # Contents Task Read
        s=[]
        s.append(mtask2_serializer.data)
        s = s + dl_serializer.data + mtask1_serializer.data + mcont_serializer.data + com_serializer.data + taskteam_ser.data + participate_ser.data
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
        tname = con.tcontent
        t = get_object_or_404(MTask, performance_id=pk, mcontents_id=value, SCNum=key, TNum=tnum)
        if con.filetype == 1:
            if con.id == id:
                st = t.DetName + " 의 " + con.SCName + " 에 업로드된 파일입니다."
                confile = MContentsFile.objects.create(mcontents=con, storage=st, performance_id=pk)
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

                t = get_object_or_404(MTask, performance_id=pk, mcontents_id=value, SCNum=key, TNum=tnum)
                print(request.user)
                ud = get_object_or_404(UserDetail, user_id=request.user, performance_id=pk, TNum=None)
                print(ud)
                mod = t.DetName + " 의 " + con.SCName + " 에 " + " 파일이 업로드 되었습니다."
                dlog = DetailLog.objects.create(performance_id=pk, mtask=t, userdetail=ud, mc=t.mcontents_id, mod=mod,
                                                username=request.user.username)
                dlog.save()
                # dlog_serializer = DetailLogSerializer(dlog)
                #  s.append(dlog_serializer)

                return Response(confile_serializer.data,content_type=u"application/json; charset=utf-8")
            return Response(confile_serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            if con_serializer.is_valid():
                con_serializer.save()
                t = get_object_or_404(MTask, performance_id=pk, mcontents_id=value, SCNum=key, TNum=tnum)
                print(request.user)
                ud = get_object_or_404(UserDetail, user_id=request.user, performance_id=pk, TNum=None)
                print(ud)
                mod = t.DetName + " 의 " + con.SCName + " 가(이) " + tname + " 에서 " + con.tcontent + " 로 변경 되었습니다."
                dlog = DetailLog.objects.create(performance_id=pk, mtask=t, userdetail=ud, mc=t.mcontents_id,mod=mod,username=request.user.username)
                dlog.save()
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

    userd = get_object_or_404(UserDetail, user=request.user, TNum=None)

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

@api_view(['GET','PUT'])
def comment_Update(request,pk,tnum,id):
    com = get_object_or_404(Comment, performance_id=pk, TNum=tnum, id=id)
    if com.username == request.user.username:
        if request.method == 'PUT':
            com_ser = CommentSerializer(com, data=request.data)
            if com_ser.is_valid():
                com_ser.save()
                return Response(com_ser.data)
            return Response(com_ser.errors, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'No user rights.'})


@api_view(['GET', 'DELETE'])
def comment_delete(request, pk, tnum, id):
    try:
        comment = Comment.objects.get(performance_id=pk, TNum=tnum, id=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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
@api_view(['GET', 'PUT'])
def TaskMod(request,pk,tnum):
    mtask = get_object_or_404(MTask, performance_id=pk, TNum=tnum, Dbool=1)
    if request.method == "PUT":

        mt_s = MTaskSerializer(mtask, data=request.data)
        if mt_s.is_valid():
            print(mtask.Dbool)
            print(request.data)
            mt_s.save()
            print(mtask.Dbool)
            print(mt_s.data)
            return Response(mt_s.data)
        return Response(mt_s.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def TaskUserCreate(request,pk,tnum):

    if request.method == "POST":
        #u = get_object_or_404(UserDetail,)
        ud = UserDetail.objects.create(performance_id=pk, TNum=tnum)
        ud_s = UserDetailSerializer(ud,data=request.data)
        if ud_s.is_valid():
            ud_s.save()
            return Response(ud_s.data)
        return Response(ud_s.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def TaskTeamCreate(request, pk, tnum):

    if request.method == "POST":
        tt =TaskTeam.objects.create(performance_id=pk, TNum=tnum)

        tt_s = TaskTeamSerializer(tt, data=request.data)
        if tt_s.is_valid():
            tt_s.save()
            return Response(tt_s.data)
        return Response(tt_s.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def fileRead(request, pk):
    mcs= []
    mf = MContentsFile.objects.filter(performance_id=pk)

    if request.method == "GET":
        for i in mf:
            if i.name == None:
                i.name = filename(i)
                i.save()
                mcs.append(i)
                print(i)
                print("됐다")
            else:
                mcs.append(i)
                print(i)
                print("안됐다")

        mf_s =MContentFileSerializer(mcs, many=True)
        #mc_s =MContentSerializer(mcs, many=True)
        return Response(mf_s.data,content_type=u"application/json; charset=utf-8")

@api_view(['GET', 'POST'])
def filedown(request, pk, id):
    if request.method == 'GET':
        mf = get_object_or_404(MContentsFile, performance_id=pk, id=id)
        url = mf.fcontent.url[1:]
        file_url = urllib.parse.unquote(url)
        print(url)
        print(file_url)
        if os.path.exists(file_url):
            with open(file_url, 'rb') as fh:
                quote_file_url = urllib.parse.quote(file_url.encode('utf-8'))
                print(quote_file_url)
                response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
                response['Content-Disposition'] = 'attachment;fcontent*=UTF-8\'\'%s' % quote_file_url
                return response
            raise Http404

def filename(mc):
    ma = mc
    na = ma.fcontent.url[13:]
    furl = urllib.parse.unquote(na)

    return furl