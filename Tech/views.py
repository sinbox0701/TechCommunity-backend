from django.shortcuts import render, get_object_or_404, redirect,get_list_or_404
from .forms import *
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
# Create your views here.


def show(request):
    return render(request, 'base.html')

@api_view(['GET', 'POST'])
def PeListView(request):
    if request.method == 'GET':
        per_list = Performance.objects.all()
        serializer = PerformanceSerializer(per_list, many=True)
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
            a=[genre,title,directiont,configurationt,check,date,place,special]
            for i in scontents:
                MContents.objects.create(performance=perfor, SCNum=i.id, SCName=i.SCName)
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
                        MTask.objects.create(TNum=i.TNum, DetNum=i.DetNum, TName=i.TName, DetName=i.DetName,
                                             SCNum=i.SCNum, objective=i.objective, category=i.category_id, bool=i.bool,
                                             performance=perfor)
                        break
                    elif i.SCNum == x.SCNum:
                        MTask.objects.create(TNum=i.TNum, DetNum=i.DetNum, TName=i.TName, DetName=i.DetName,
                                             SCNum=i.SCNum, objective=i.objective, category=i.category_id, bool=i.bool,
                                             performance=perfor,mcontents=x)
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
        mtask = get_list_or_404(MTask, performance=performance)
        mtask_serializer = MTaskSerializer(mtask, many=True)
        s=[]
        s.append(performance_serializer.data)
        s = s + category_serializer.data + mtask_serializer.data
        return Response(s)

@api_view(['GET', 'DELETE'])
def PeDeleteView(request,pk):
    try:
        performance = Performance.objects.get(pk=pk)
    except Performance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        performance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def TaskContentView(request, pk, tnum):
    mtask = get_list_or_404(MTask, performance_id=pk, TNum=tnum)
    mtask_serializer = MTaskSerializer(mtask, many=True)
    sc = []
    mc = []
    mcont = []
    for i in mtask:
        sc.append(i.SCNum)
        mc.append(i.mcontents_id)

    c = [x for x in zip(sc, mc)]
    c = dict(c)

    for key, value in c.items():
        mcont.append(get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
    mcont_serializer = MContentSerializer(mcont, many=True)
    print(type(mtask_serializer))

    if request.method == 'GET':
        s = mtask_serializer.data + mcont_serializer.data
        return Response(s)

@api_view(['GET', 'PUT'])
def ContentsUpdateView(request,pk,tnum,id):
    mtask = get_list_or_404(MTask, performance_id=pk, TNum=tnum)
    sc = []
    mc = []
    for i in mtask:
        sc.append(i.SCNum)
        mc.append(i.mcontents_id)

    c = [x for x in zip(sc, mc)]
    c = dict(c)
    for key, value in c.items():
        con = (get_object_or_404(MContents, performance_id=pk, pk=value, SCNum=key))
        if con.id == id:
            con_serializer = MContentSerializer(con,request.data)
            break
    if request.method == 'PUT':
        if con_serializer.is_valid():
            con_serializer.save()
            return Response(con_serializer.data)
        return Response(con_serializer.errors, status.HTTP_400_BAD_REQUEST)



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