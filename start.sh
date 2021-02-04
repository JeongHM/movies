#/bin/bash


echo "\n[도커에서 사용중인 포트를 확인합니다]\n"

PORTS=$(lsof -iTCP -sTCP:LISTEN -n -P | grep -w '5050\|3030')

if [ -n "$PORTS" ]; then
  echo "[실핼중인 포트를 중지해야합니다]\n"
  lsof -iTCP -sTCP:LISTEN -n -P | grep -w '5050\|3030'

else
  DOCKERS=$(docker ps -a | grep -w 'movie-swagger\|movie-application')

  if [ -n "$DOCKERS" ]; then
    echo "[도커 컨테이너가 존재합니다. 아래와 같이 실행 시켜주셔야됩니다.]"
    echo "[1. docker stop movie-swagger]"
    echo "[2. docker stop movie-application]"
    echo "[3. docker rm movie-swagger]"
    echo "[4. docker rm movie-application]"

  else
    echo "[도커 컴포즈를 실행합니다.]\n"
    docker-compose up

  fi
fi