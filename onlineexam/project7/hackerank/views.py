from django.shortcuts import render
from hackerank.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Profile
from .models import Exam, Question, UserAnswer
from django.contrib.auth.decorators import login_required




# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    user_type = request.GET.get('type', 'practice')
    heading = "Register as Developer" if user_type == 'practice' else "Register as Employer"

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Manually create profile
            Profile.objects.create(user=user, user_type=form.cleaned_data['user_type'])
            messages.success(request, "Registration successful! You can login now.")
            return redirect('login')
    else:
        form = CustomUserForm(initial={'user_type': user_type})

    return render(request, 'register.html', {'form': form, 'heading': heading})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
    return render(request, 'login.html')


def logout_view(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Loged out Successfully")
  return redirect("/")


def user_confirm(request):
    return render(request,'user_confirm.html')


@login_required
def create_exam(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        duration = request.POST['duration']
        exam = Exam.objects.create(
            name=name, description=description, duration=duration, created_by=request.user
        )
        # questions create ചെയ്യാനും POST data ഉപയോഗിച്ച് loop നടത്താം
        return redirect('exam_detail', exam_id=exam.id)
    return render(request, 'create_exam.html')

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    if request.method == 'POST':
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer:
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'selected_answer': answer}
                )
        return redirect('exam_result', exam_id=exam.id)

    return render(request, 'take_exam.html', {'exam': exam, 'questions': questions})

@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__exam=exam)
    return render(request, 'exam_result.html', {'exam': exam, 'user_answers': user_answers})


def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam_list.html', {'exams': exams})




    