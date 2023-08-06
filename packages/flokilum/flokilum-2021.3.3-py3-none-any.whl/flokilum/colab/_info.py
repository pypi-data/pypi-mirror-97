def info():

	from datetime import date
	from os import environ
	from platform import python_version

	## date
	_date = date.today()
	print(F"{'date'.rjust(50)} : {_date}")

	## python version
	_python = python_version()
	print(F"{'python'.rjust(50)} : {_python}")

	## shell
	_shell = environ.get("SHELL")
	print(F"{'shell'.rjust(50)} : {_shell}")

	## cuda
	## _cuda = environ.get("CUDA_VERSION")
	## print(F"{'cuda'.rjust(50)} : {_cuda}")

	## cudnn
	## _cudnn = environ.get("CUDNN_VERSION")
	## print(F"{'cudnn'.rjust(50)} : {_cudnn}")

	print(F"{'=========='.rjust(50)} : ==========")
