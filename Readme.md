Execute:\
`python -m pip install -r requirements.txt`\
`python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/server.proto`

Execute in different terminals:\
`python server.py`\
`python client.py`

