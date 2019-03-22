FROM alpine:3.9 AS download
RUN apk add curl libarchive-tools
RUN curl -OL {{url}}
RUN bsdtar xf {{filename}}

FROM alpine:3.9
RUN apk add {{runtimedep}}
COPY --from=download /{{archivename}} /opt/{{archivename}}
{% for one in custom_deployment %}{{one}}
{% endfor %}