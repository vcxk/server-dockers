FROM debian:rc-buggy

RUN apt-get update && apt-get install -y curl wget

RUN curl -L https://mirrors.host900.com/https://github.com/snail007/goproxy/blob/master/install_auto.sh | bash

ENTRYPOINT ["proxy"]
CMD [""]