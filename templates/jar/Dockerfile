FROM alpine:3.9 AS download
RUN apk add curl libarchive-tools
RUN curl -OL {{url}}

FROM alpine:3.9
RUN apk add openjdk8-jre {{runtimedep}}
COPY --from=download /{{filename}} /opt/{{filename}}
ENV JAVA_OPTIONS -Xmx4g
RUN echo 'java ${JAVA_OPTIONS} -jar /opt/{{filename}} "${@}"' > /usr/bin/{{name}} && chmod +x /usr/bin/{{name}}
