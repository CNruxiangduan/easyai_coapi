FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./app /app
COPY ./package /package
ADD sources.list /etc/apt/
RUN apt-get update -y && apt install libx11-xcb1 -y && apt-get install libgl1 -y

# RUN pip install /package/torch-1.13.1+cpu-cp38-cp38-linux_x86_64.whl
# RUN pip install /package/opencv_python-4.7.0.72-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN pip install  -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com/simple ultralytics --extra-index-url https://download.pytorch.org/whl/cpu
ENV PATH="/root/.local/bin:${PATH}"