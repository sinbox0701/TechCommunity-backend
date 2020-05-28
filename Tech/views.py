from django.shortcuts import render, get_object_or_404, redirect,get_list_or_404
from .forms import *
from .models import *

# Create your views here.


def show(request):
    return render(request, 'base.html')

def PeListView(request):
    per_list = Performance.objects.all()
    context = {'per_list':per_list}
    return render(request,'Tech/Performance_list.html',context)

def PeCreateView(request):
    if request.method == "POST":
        form = PerCreateForm(request.POST, request.FILES)
        scontents = SContents.objects.order_by('id')
        if form.is_valid():
            genre = form.cleaned_data['genre']
            title = form.cleaned_data['title']
            direction = form.cleaned_data['direction']
            construct = form.cleaned_data['construct']
            check = form.cleaned_data['check']
            date = form.cleaned_data['date']
            p = Performance.objects.order_by('-id')
            l=p[0].id+1
            perfor=Performance.objects.create(pk=l,title=title)
            a=[genre,title,'',direction,'',construct,'',check,date]
            for i in range(0, 37):
                MContents.objects.create(performance=perfor, SCNum=scontents[i].id, SCName=scontents[i].SCName)
            MContents.objects.order_by('id')
            for i in range(0,9):
                if i!=4 or i!=6 or i!=2:
                    mc = MContents.objects.get(performance=perfor,SCNum=scontents[i].id,SCName=scontents[i].SCName)
                    mc.tcontent = a[i]
                    mc.save()
            MContents.objects.order_by('id')
            s = STask.objects.order_by('id')
            for i in range(0,59):
                MTask.objects.create(TNum=s[i].TNum,DetNum=s[i].DetNum,TName=s[i].TName,DetName=s[i].DetName,
                                     SCNum=s[i].SCNum,objective=s[i].objective,category=s[i].category_id,performance=perfor)
            return redirect('Tech:list')
    else:
        form = PerCreateForm()
    context = {'form':form}
    return render(request,'Tech/Performance_create.html',context)



def PeCateView(request,pk):
    category = Category.objects.all()
    performance = get_object_or_404(Performance, pk=pk)
    mtask = get_list_or_404(MTask, performance=performance)


    mlist = []
    ml = []
    for i in mtask:
        if i.TNum not in mlist:
            mlist.append(i.TNum)
            ml.append(i)
        else:
            continue
    print(ml)
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

    print(a)
    print(act)
    print(zero)
    print(one)
    print(two)
    print(three)
    print(four)
    print(list)
    l=[]
    for i in range(0,max):
        l.append(int(i))
    print(l)
    context = {'category':category, 'performance':performance, 'mtask':mtask,'act':act,'a':a,'l':l}
    return render(request,'Tech/Category_list.html',context)

'''def TaModifyView(request,pk):
    mtask = get_object_or_404(MTask,pk=pk)
    if request.method == "POST":'''

