from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pretty_errors
from game.models import Game, GameMovement

def indexView(request):
    user = request.user
    if user is None or request.user.username == "":
        context = {
        }

    else:
        gamesPerPage = 25
        
        # Get real user
        user = User.objects.get(username=request.user.username)

        paginator = Paginator(Game.objects.filter(user_x=None), gamesPerPage)
        openedGames= paginator.page(1)
        
        myGames = Game.objects.filter(user_o=user).order_by('-creation')[:gamesPerPage]

        context = {
            myGames: myGames,
            openedGames: openedGames
        }

    response = loader.get_template("game/templates/index.html").render(context, request)
    return HttpResponse(response)


def loginView(request):
    if request.POST.get("username", "") == "ai":
        return makeErrorView(request, "Don't mess with the dragons!")
    
    print("Trying to log in user "+request.POST.get("username", "")+"...")
    user = authenticate(username=request.POST.get("username", ""), password=request.POST.get("password", ""))

    if user is not None and user.is_active:
        print("User "+request.POST.get("username", "")+" authenticated!")
        login(request, user)
        return redirect('index')
    
    else:
        if User.objects.filter(username=request.POST.get("username", "")).exists():
            return makeErrorView(request, "Invalid username or password.")
        
        else:
            if len(request.POST.get("password", "")) < 8 or request.POST.get("password", "").find(request.POST.get("username", "")) != -1:
                return makeErrorView(request, "Password too short or too similar to username.")
            
            # Create user now
            user = User.objects.create_user(username=request.POST.get("username", ""), email='', password=request.POST.get("password", ""));
            login(request, user)
            return redirect('index')


def logoutView(request):
    logout(request)
    return redirect('index')


def createGameView(request):
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get real user
    user = User.objects.get(username=request.user.username)

    # Create game
    if request.POST.get("type", "pvp") == "pvp":
        print("Creating PVP game...")
        game = Game.objects.create(user_o=user, user_x=None, board=".........", winner=".")

    else:
        ai = getDragonAI()
        if ai is None:
            return makeErrorView(request, "Cannot create PVE game! There are no dragons in the lair at this moment...")
        
        print("Creating PVE game...")
        game = Game.objects.create(user_o=user, user_x=ai, board=".........", winner=".")

    # X=Player X movement, Y=Player Y movement, C=Game creation, etc
    print("Creating initial movement (C=creation)...")
    GameMovement.objects.create(user=user, game=game, symbol="C", movement=0)

    print("Game with ID "+str(game.id)+" created! Redirecting to play...")
    return redirect('play', id=game.id)


def playGameView(request, id):
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get game
    print("Obtaining game with ID "+str(id)+" created! Redirecting to play...")
    game = Game.objects.get(id=id)

    if game is not None:
        print("Game obtained! ", game)
        context = {
            game: game
        }

        response = loader.get_template("game/templates/game.html").render(context, request)
        return HttpResponse(response)
    
    else:
        return makeErrorView(request, "Cannot load that game!")


def makeErrorView(request, message):
    print(message)

    context = {
        "message": message
    }

    response = loader.get_template("game/templates/error.html").render(context, request)
    return HttpResponse(response)


def getDragonAI():
    dragon = None

    try:
        print("Getting dragon...")
        dragon = User.objects.get(username="ai")

    except User.DoesNotExist:
        print("Nobody is in the lair! Creating dragon now...")
        dragon = User.objects.create_user(username="ai", email="ai@tic.fake", password="drag0n");

    return dragon
    
