FROM alpine:3.9 AS download
RUN apk add curl libarchive-tools
RUN curl -OL {{url}}
RUN bsdtar xf {{filename}}

FROM alpine:3.9 AS buildenv
RUN apk add {{builddep}}
COPY --from=download /{{archivename}} /{{archivename}}
WORKDIR /{{archivename}}
{% for one in patch %}COPY {{one}} /
RUN patch -p1 < /{{one}}
{% endfor %}
RUN mkdir build
WORKDIR /{{archivename}}/build
RUN cmake ..
RUN make -j4
RUN make install DESTDIR=/dest

FROM alpine:3.9
RUN apk add {{runtimedep}}
COPY --from=buildenv /dest /
