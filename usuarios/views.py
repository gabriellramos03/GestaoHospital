from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django, logout as logout_django
from .models import Medico
from django.urls import reverse
from django.core.paginator import Paginator

def login(request):
    if request.method == "GET":
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(username = username, password = senha)

        if user:
            login_django(request, user)
            return render(request, 'usuarios/home.html')
        else:
            return HttpResponse('E-mail ou senha inválidos!')
        
def logout(request):
    if request.user.is_authenticated:
        logout_django(request)
        return render(request, 'usuarios/login.html')
    else:
        #return HttpResponse("Você não acessou sua conta!")
        return render(request, 'usuarios/login.html')

def cadastro(request):
    if request.method =="GET":
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        first_name = request.POST.get('nome')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse("Usuário já existente!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
            user.save()

            return render(request, 'usuarios/login.html')
        
def home(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/home.html')
    else:
        #return HttpResponse("Faça o login para acessar!")
        return render(request, 'usuarios/login.html')

def lancar(request):
    if request.method =='GET':
        if request.user.is_authenticated:
            return render(request, 'usuarios/lancar.html')
        else:
            #return HttpResponse("Faça o login para acessar!")
            return render(request, 'usuarios/login.html')
    else:
        medico = Medico()
        medico.nome_medico = request.POST.get('nome_medico')
        medico.especializacao = request.POST.get('especializacao')
        medico.crm = request.POST.get('crm')
        medico.email = request.POST.get('email')
        medico.telefone = request.POST.get('telefone')

        medico_verificado = Medico.objects.filter(nome_medico=medico.nome_medico).first()

        if medico_verificado:
            return HttpResponse("Já possui cadastro desse médico!")
        else:
            medico.save()
            return render(request, 'usuarios/home.html')

def alterar(request):
    if request.method =="GET":
        if request.user.is_authenticated:
            lista_medicos = Medico.objects.all()
            dicionario_medicos = {'lista_medicos':lista_medicos}
            return render(request, 'usuarios/alterar.html', dicionario_medicos)
        else:
            #return HttpResponse("Faça login para acessar!")
            return render(request, 'usuarios/login.html')

#def visualizar(request):
#    if request.method == "GET":
#        if request.user.is_authenticated:
#            lista_medicos = Medico.objects.all()
#            dicionario_medicos = {'lista_medicos':lista_medicos}
#            return render(request, 'usuarios/visualizar.html', dicionario_medicos)
#        else:
#            return HttpResponse("Fala o login para acessar!")
#    else:
#        especializacao = request.POST.get('especializacao')
#        if especializacao == "Todas as epecializações":
#            lista_medicos = Medico.objects.all()
#            dicionario_medicos = {'lista_medicos':lista_medicos}
#            return render(request, 'usuarios/visualizar.html', dicionario_medicos)
#        else:
#            lista_medicos = Medico.objects.filter(especializacao=especializacao)
#            dicionario_especial_filtradas = {'lista_medicos':lista_medicos}
#            return render(request, 'usuarios/visualizar.html', dicionario_especial_filtradas)

#def visualizar_medicos(request):
#    especializacao_selecionada = request.POST.get('especializacao', '')
#    if especializacao_selecionada:
#        lista_medicos = Medico.objects.filter(especializacao=especializacao_selecionada)
#    else:
#        lista_medicos = Medico.objects.all()
#    
#    lista_especializacoes = Medico.objects.values_list('especializacao', flat=True).distinct()
#
#    return render(request, 'usuarios/visualizar.html', {
#        'lista_medicos': lista_medicos,
#        'lista_especializacoes': lista_especializacoes,
#        'especializacao_selecionada': especializacao_selecionada
#    })

def visualizar_medicos(request): 
    especializacao_selecionada = request.POST.get('especializacao', '') 
    if especializacao_selecionada: 
        lista_medicos = Medico.objects.filter(especializacao=especializacao_selecionada) 
    else: 
        lista_medicos = Medico.objects.all() 

    # Paginação
    paginator = Paginator(lista_medicos, 8)  # Exibe 8 médicos por página
    page_number = request.GET.get('page')
    lista_medicos = paginator.get_page(page_number)

    lista_especializacoes = Medico.objects.values_list('especializacao', flat=True).distinct() 

    return render(request, 'usuarios/visualizar.html', { 
        'lista_medicos': lista_medicos, 
        'lista_especializacoes': lista_especializacoes, 
        'especializacao_selecionada': especializacao_selecionada 
    })


def excluir_verificacao(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            lista_medicos = Medico.objects.get(pk=pk)
            dicionario_medicos = {'lista_medicos':lista_medicos}
            return render(request, 'usuarios/excluir.html', dicionario_medicos)
        else:
            return HttpResponse("Fala o login para acessar!")
        
def excluir(request, pk):
    if request.method =="GET":
        if request.user.is_authenticated:
            medico_selecionado = Medico.objects.get(pk=pk)
            medico_selecionado.delete()
            return HttpResponseRedirect(reverse('alterar'))
        else:
            #return HttpResponse("Faça o login para acessar!")
            return render(request, 'usuarios/login.html')
        
def editar_verificacao(request, pk):
    if request.method =="GET":
        if request.user.is_authenticated:
            lista_medicos = Medico.objects.get(pk=pk)
            dicionario_medico = {'lista_medicos':lista_medicos}
            return render(request, 'usuarios/editar.html', dicionario_medico)
        else:
            return HttpResponse("Fala o login para acessar!")
        
def editar(request, pk):
    if request.method =="POST":
        if request.user.is_authenticated:
            nome_medico = request.POST.get('nome_medico')
            especializacao = request.POST.get('especializacao')
            crm = request.POST.get('crm')
            email = request.POST.get('email')
            telefone = request.POST.get('telefone')
            Medico.objects.filter(pk=pk).update(nome_medico=nome_medico, especializacao=especializacao, crm=crm, email=email, telefone=telefone)
            return HttpResponseRedirect(reverse('alterar'))
        else:
            #return HttpResponse("Faça o login para acessar!")
            return render(request, 'usuarios/login.html')
        
def sobre(request):
    if request.user.is_authenticated:
        return render(request, 'sobre.html')
    else:
        return render(request, 'usuarios/login.html')  # Ou redirecione para a página de login

def contatos(request):
    if request.user.is_authenticated:
        return render(request, 'contatos.html')
    else:
        return render(request, 'usuarios/login.html')