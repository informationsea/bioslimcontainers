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
RUN make -j4
{% for one in artifacts %}RUN install -D -t /dest/{{one.dest}} {{one.file}}
{% endfor %}

FROM alpine:3.9
RUN apk add bash {{runtimedep}}
COPY --from=buildenv /dest /
ADD run.sh /run.sh
ENTRYPOINT [ "/bin/bash", "/run.sh" ]