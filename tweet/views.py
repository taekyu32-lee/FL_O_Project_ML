from cv2 import computeECC
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article, Comment, TweetComment
from django.contrib.auth.decorators import login_required

def write(request):
    # user = authenticate(request, username = username, password = password)
    # if user:
        
        if request.method == "GET":

            return render(request, 'write.html')
        elif request.method == "POST":
            title = request.POST.get('title')
            content = request.POST.get('content')
            article = Article()
            article.image = request.FILES['image']
            
            Article.objects.create(title = title, content = content, image = article.image)
            
            
            return redirect('/tweet/community/')

def community(request):
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-create_at')
        context = {
            'articles' : articles
        }
        
        return render(request, 'community.html', context)


@login_required
def write_comment(request, id): # 댓글 작성
    if request.method =='POST':
        comment = request.POST.get('comment','')
        current_twwet = Article.objects.get(id = id)

        

def add(request, id):
    id_com = Article.objects.get(id = id) # get의 의미 db에 A필드에 B인걸 가지고 오겠따(where같은개념)  
    com = {
        'id_com' : id_com,
    }
    print(id_com.id) 
    return render(request, 'add.html', com) #render는 type는 반드시 딕셔너리만 가능하게끔 되어있다. 

def mod(request, id):
    if request.method == 'GET':
        id_sa = Article.objects.get(id = id)
        b = {
            'id_sa' : id_sa,
        }
        return render(request, 'mod.html', b)

    elif request.method == 'POST':
        id_sa = Article.objects.get(id = id)
        id_sa.title = request.POST.get('title')
        id_sa.content = request.POST.get('content')
        id_sa.save()
            
        return redirect('/tweet/community/')        
        
            



        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_twwet
        TC.save()
        
        return redirect('/write/'+str(id))
    
@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/write/'+str(current_tweet))


def post_detail(request, id):
    if request.method == 'GET':
        #todo 여기에 게시글
        return render(request, 'post_detail.html')
    
@login_required
def post_like(request, id):
    me = request.user
    click_post = Article.objects.get(id=id) #클릭된 유저
    if me in click_post.likes.all(): #라이크 한 사람들 모두 가져옴
        click_post.likes.remove(request.user) # 그 사람중에 나를 뺌
    else:
        click_post.likes.add(request.user)
    return redirect('/')