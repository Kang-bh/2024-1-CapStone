from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import action

from rest_framework.response import Response
from .models import User, RecommendResult, BaseGames, SteamGames
from rest_framework import viewsets
from .serializers import UserSerializer, RecommendResultSerializer, BaseGameSerializer, SteamGameSerializer
from rest_framework import status
import subprocess
import ast


# Create your views here.

class userViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class recommendResultViewSet(viewsets.ModelViewSet):
    serializer_class = RecommendResultSerializer
    queryset = RecommendResult.objects.all()
    basename = 'recommend-result'

    @action(detail=False, methods=['post'], url_path='content-based')
    def contentBasedFiltering(self, request, *args, **kwargs):
        print(request.data)

        title = request.data.get('steam_game_name', [])[0]
        print(title)
        try:
            print(1)
            result = subprocess.run(['python', '/Users/gangbyeongho/Desktop/kang/KHU/전공/2024-1/캡스톤디자인/2024-1-CapStone/data-processing/content-based-recommend.py', title], capture_output=True, text=True)
            print("result : ", result)
            if result.returncode == 0 :
                print(2)
                result.stdout.strip()
            else :
                print(3)
            
                return f"Error: {result.stderr.strip()}"
        except Exception as e:
            # 예외 발생 시 오류 메시지 반환
            print(4)
            print(f"Exception: {str(e)}")
            return f"Exception: {str(e)}"   

        print("result : ", result.stdout.strip())
        result_list = ast.literal_eval( result.stdout.strip())

        games = []
        
        for game_name in result_list:
            print("game name : ", game_name)
            game_info = SteamGames.objects.filter(game_name=game_name).first()
            if game_info:
                serializer = SteamGameSerializer(game_info)
                print("serializer.data : ", serializer.data)
                games.append(serializer.data)            

        # todo : change path
        print(games)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        return JsonResponse({'result': games})

    @action(detail=False, methods=['post'], url_path='collaborative')
    def collaborativeFiltering(self, request, *args, **kwargs):
        print("request : ", request)
        print("Request Data : ", request.data)

        gameIdList = request.data.get('game_id_list')
        print("gameIdList : ", gameIdList)
        try:
            print(gameIdList[0])
            print(type(gameIdList))
            # to string and in function deserialize
            result = subprocess.run(['python', '/Users/gangbyeongho/Desktop/kang/KHU/전공/2024-1/캡스톤디자인/2024-1-CapStone/data-processing/item-based-collaborative.py', str(gameIdList[0])], capture_output=True, text=True)
            print("result : ", result)
        except Exception as e :

            print(f"Exception: {str(e)}")
            return f"Exception: {str(e)}"

        result_list = result.stdout.strip()
        result_list = ast.literal_eval(result.stdout.strip())
        print("result : ", result.stdout.strip())
        print("result : ", type(result.stdout.strip()))

        games = []
        
        for game_id in result_list:
            game_info = SteamGames.objects.filter(id=game_id).first()
            if game_info:
                serializer = SteamGameSerializer(game_info)
                print("serializer.data : ", serializer.data)
                games.append(serializer.data)            


        return JsonResponse({'result': games})

        
        
class baseGamesResultViewSet(viewsets.ModelViewSet):
    serializer_class = BaseGameSerializer
    queryset = BaseGames.objects.all()
    basename = 'baseGames'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class steamGamesResultViewSet(viewsets.ModelViewSet):
    serializer_class = SteamGameSerializer
    queryset = SteamGames.objects.all()
    basename = 'steamGames'


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='likes')
    def like(self, request, pk=None):

        try:
            print("pk : ", pk)
            steamGame = SteamGames.objects.get(id=pk)
        except SteamGames.DoesNotExist:
            return Response({'error': 'Steam Game does not exist'}, status=status.HTTP_404_NOT_FOUND)

        steamGame.likes += 1
        steamGame.save()

        steamGame.likes += 1
        steamGame.save()

        return Response({'likes' : steamGame.likes})

    @action(detail=True, methods=['post'], url_path='clicks')
    def click(self, request, pk=None):
        try:
            steamGame = SteamGames.objects.get(id=pk)
        except SteamGames.DoesNotExist:
            return Response({'error': 'Steam Game does not exist'}, status=status.HTTP_404_NOT_FOUND)

        steamGame.clicks += 1
        steamGame.save()

        return Response({'clicks' : steamGame.clicks})
