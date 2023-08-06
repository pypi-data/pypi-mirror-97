# docker file to build manylinux wheels for the python bindings
FROM quay.io/pypa/manylinux2014_x86_64

RUN yum install -y zeromq-devel zlib-devel \
    && yum clean all \
    && rm -rf /var/cache/yum

# we need protobuf3 for python3
# passing -O2 dramatically reduces library and thus wheel size
RUN cd /tmp \
	&& curl -L https://github.com/protocolbuffers/protobuf/releases/download/v3.15.3/protobuf-all-3.15.3.tar.gz | tar xz \
	&& cd protobuf-3.15.3 \
	&& ./configure \
	&& make CXXFLAGS="-O2" \
	&& make install \
	&& cd / \
	&& rm -rf /tmp/protobuf-3.15.3

ADD build_wheels.sh /

RUN mkdir -p /home/wheel && chmod a+rwx /home/wheel
ENV HOME=/home/wheel
ENV PATH="/home/wheel/.local/bin:$PATH"
WORKDIR /home/wheel

CMD /build_wheels.sh
