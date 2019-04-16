FROM alpine:3.9 AS buildenv
RUN apk add python3 python3-dev gcc g++ make
RUN apk add {{ builddep }}
{% for one in packages %}
RUN pip3 install {{ one }}
{% endfor %}

FROM alpine:3.9
RUN apk add python3 bash
RUN apk add {{ runtimedep }}
COPY --from=buildenv /usr/lib/python3.6/site-packages /usr/lib/python3.6/site-packages
ADD run.sh /run.sh
ENTRYPOINT [ "/bin/bash", "/run.sh" ]
