FROM alpine:3.9 AS download
RUN apk add curl libarchive-tools
RUN curl -OL {{url}}
RUN bsdtar xf {{filename}}

FROM alpine:3.9
RUN apk add bash {{runtimedep}}
COPY --from=download /{{archivename}} /opt/{{archivename}}
{% for one in custom_deployment %}{{one}}
{% endfor %}
ADD run.sh /run.sh
ENTRYPOINT [ "/bin/bash", "/run.sh" ]
