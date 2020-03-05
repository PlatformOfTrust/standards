FROM library/alpine

ARG standards_version=v1
ENV standards_version=$standards_version

ENV LC_ALL=C.UTF-8 \
	LANG=C.UTF-8



ADD app /var/public
ADD v1 /var/public/${standards_version}
ADD docker-entrypoint.sh /opt/

RUN apk add --update --no-cache nginx \
    && mkdir -p /run/nginx \
    && adduser -D -g 'www' www \
    && chown -R www:www /var/lib/nginx \
    && rm -f /etc/nginx/nginx.conf \
    && rm -rf /etc/nginx/conf.d \
    && chown -R www:www /var/public \
    && chmod +x /opt/docker-entrypoint.sh


RUN ln -sf /dev/stdout /var/log/nginx/error.log \
	&& ln -sf /dev/stdout /var/log/nginx/access.log

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/opt/docker-entrypoint.sh"]

EXPOSE 80 443
