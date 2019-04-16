FROM alpine:3.9 AS download
RUN apk add curl libarchive-tools
RUN curl -OL {{url}}

FROM alpine:3.9
RUN apk add openjdk8-jre bash {{runtimedep}}
COPY --from=download /{{filename}} /opt/{{filename}}
ENV JAVA_OPTIONS -Xmx4g
RUN echo 'java ${JAVA_OPTIONS} -jar /opt/{{filename}} "${@}"' > /usr/bin/{{name}} && chmod +x /usr/bin/{{name}}
{% for one in custom_deployment %}{{one}}
{% endfor %}
ADD run.sh /run.sh
ENTRYPOINT [ "/bin/bash", "/run.sh" ]