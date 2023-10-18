from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import TodoModel
import urllib.request
import json



def index(request):
    return HttpResponse("Hello, world. ")


# 0. todo data front에 보내주기  -> serialize 로 코드 변경 

# todo/sendtodo   -> plan에 대한 
def sendtododb(request):

    if request.method == 'POST':

        useridPayload  = json.loads(request.body)
        ThisUserId = useridPayload['UserIdtd']
        print("get_success_sendtododata")


        #due_date정렬을 여기서 관리를 해줘야할거같다.
        #button - on -> order_by().reverse() 사용
        #button - off -> order_by() 만 사용

        button = useridPayload['duedatebtn']
        print("duedate" , button)

        if button == 0:
            TodoDBing = list(TodoModel.objects.order_by('due_date').filter(user_id=ThisUserId, status = False).values_list('id','status','title','content','due_date' ))
      
        
        else :
            TodoDBing = list(TodoModel.objects.order_by('due_date').reverse().filter(user_id=ThisUserId, status = False).values_list('id','status','title','content','due_date' ))
       


        print("현재 진행중: ", TodoDBing)
    
        data = {
            'tdmaining' : TodoDBing,
        }

        return JsonResponse(data)
    
# todo/sendtodo2  -> done에 대한

def sendtododb2(request):

    if request.method == 'POST':

        useridPayload  = json.loads(request.body)
        ThisUserId = useridPayload['UserIdtd']
        print("get_success_sendtododata")


        #due_date정렬을 여기서 관리를 해줘야할거같다.
        #button - on -> order_by().reverse() 사용
        #button - off -> order_by() 만 사용

        button = useridPayload['duedatebtn']
        print("duedate" , button)

        if button == 0:
            TodoDBdone = list(TodoModel.objects.order_by('due_date').filter(user_id=ThisUserId,  status = True).values_list('id','status','title','content','due_date' ))
        
        else :
            TodoDBdone = list(TodoModel.objects.order_by('due_date').reverse().filter(user_id=ThisUserId,  status = True).values_list('id','status','title','content','due_date' ))


        print("완료 : ", TodoDBdone)

        data = {
            'tdmaindone' : TodoDBdone,
        }

        return JsonResponse(data)
    

# todo/sendtodopopup
# todopopup - 해당 id 값에 맞는 값들 전송

def sendtodopopup(request):

    if request.method == 'POST':

        print("get_success_sendpopup")

        # front에서 보낸 todo id 값 
        popupidPayload = json.loads(request.body)
        tdid = popupidPayload['tdpopupid']
        print("front에서 넘겨준 tododid: " , tdid)

        # todoDB 에서 usetdid와 동일한 값의 행 추출

        tddata = TodoModel.objects.filter(id = tdid).values()
        

        # front에 넘겨줄 data

        todocurrentdata = {
            'tdcurrentstatus' : tddata[0]['status'] ,
            'tdcurrenttitle' : tddata[0]['title'],
            'tdcurrentcontent' : tddata[0]['content'],
            'tdcurrentduedate' : tddata[0]['due_date']
        }


        print("추출된 해당 데이터:" , todocurrentdata)

        return JsonResponse(todocurrentdata)

        
        


  








# 1. 할일 생성

# todo/create

def todocreate(request):

    if request.method == 'POST':

        print("post_success_create")

        # 프론트에서 todo data 받아서 변수에 저장

        TodoPayload = json.loads(request.body)
        print("payload" , TodoPayload)

        tduserid = TodoPayload['userids']
        tdstatus = TodoPayload["tdstatus"]
        tdtitle = TodoPayload["tdtitle"]
        tdcontent = TodoPayload["tdcontent"]
        tdduedate = TodoPayload["tdduedate"]


        print("todo data: " , tduserid, tdstatus , tdtitle , tdcontent, tdduedate )


        # todo data저장

        new_todo = TodoModel.objects.create(user_id = tduserid ,status = tdstatus , title =tdtitle , content = tdcontent, due_date=tdduedate )

        print("새로운 todo저장되었습니다.")

        successdata = {
            'result' : True
        }

        return JsonResponse(successdata)
        


# 2. 할일 삭제

# todo/delete

def tododelete(request):

    if request.method == 'POST':

        # 삭제할 todo pk id받기
        TodoDeletePayload = json.loads(request.body)
        TodoPkId = TodoDeletePayload['todopkid']
        
        print('id:', TodoPkId)

        # 행 삭제하기

        deletetodo = TodoModel.objects.filter(id = TodoPkId)

        print("삭제될 행 추출" , deletetodo)

        GoDeleteToDo = deletetodo.delete()

        print("post_success_delete")

        data = {
            'success' : True
        }
        return JsonResponse(data)


# 3. 할일 수정

# todo/modify


def todomodify(request):

    if request.method == 'PUT':

        print("post_success_modify")

        modifyPayload = json.loads(request.body)

        print("modifypayload : ", modifyPayload)

        #  front에서 수정된 값을 비교하고 바뀌었을 경우 바뀐 값 저장 ,
        #  수정된 값이 null일 경우 -> 원래의 값으로 저장

        # 1. 해당 id에 맞는 현재 값 들
        currentToDo = TodoModel.objects.filter(id = modifyPayload['tdmdid']).values()

        # 2. 각 컬럼 (4가지 - status , title , content , due_date ) 비교

        newstatus = modifyPayload['tdmdstatus']
        newtitle = modifyPayload['tdmdtitle']
        newcontent = ''
        newduedate = ''

        # 2-1 -> status 비교             -> 수정 ok
        if modifyPayload['tdmdstatus'] == '':
            newstatus = currentToDo[0]['status'] 
            print("status is same")

        else : 
            print( "status is modify")
      
 
        # 2-2 -> title 비교      -> 수정  ok
        if modifyPayload['tdmdtitle'] == '':
            newtitle = currentToDo[0]['title']
            print("title is same")
          
        else : 
            print( "title is modify")


        # 2-3 -> content 비교   -> 수정 ok
        if modifyPayload['tdmdcontent'] :
            newcontent = modifyPayload['tdmdcontent']
           
        else :
            newcontent = currentToDo[0]['content']
            print("content is same")
         
        # 2-4 -> due date 비교   -> 수정 ok
        if modifyPayload['tdmdduedate'] == '':
            newduedate = currentToDo[0]['due_date']
            print("duedate is same")
        else :

            newduedate = modifyPayload['tdmdduedate']


        # 새로운 값으로 대체

        print("--------------------------------------------------------------------")

        print('새로운 값: ' , newstatus, newtitle,newcontent,newduedate )

        modify_todo= TodoModel.objects.filter(id = modifyPayload['tdmdid']).update(status =newstatus  , title =newtitle , content =newcontent , due_date=newduedate)

        print("변경완료되었습니다 -> " , modify_todo)


        data = {
            'resultmodify' : 0
        }

        return JsonResponse(data)

# 4. 상태 수정

# todo/statusmodify

def statusmodify(request):

    if request.method == "PUT":

        statusmodifyPayload = json.loads(request.body)

        statusmodifycurrent = TodoModel.objects.filter(id = statusmodifyPayload['statusid']).values('status')

        print("status 추출" ,statusmodifycurrent)


        # 클릭시 반대로 바꿔서 상태저장하기

        currentstatus = statusmodifycurrent[0]

        print("현상태값" ,currentstatus)

        newstatusTrue = True
        newstatusFalse = False

        data = {
            "result" : 1
        }

        
        # status 현재 상태 체크 후 반대상태로 업데이트 한 후 프론트로 응답하기
        
        if statusmodifycurrent[0]['status'] == False:
            updatestatus = TodoModel.objects.filter(id = statusmodifyPayload['statusid']).update(status = newstatusTrue)
            print("완료상태로 변경완료")
            return JsonResponse(data)
        
        else :
            print("not")

 
            

        if statusmodifycurrent[0]['status'] == True:
            updatestatus = TodoModel.objects.filter(id = statusmodifyPayload['statusid']).update(status = newstatusFalse)
            print("미완료 상태로 변경완료")
            return JsonResponse(data)
        else :
            print("not")




        # TotalDB = TodoModel.objects.all().reverse().update()

        
     

       


  
        
        











