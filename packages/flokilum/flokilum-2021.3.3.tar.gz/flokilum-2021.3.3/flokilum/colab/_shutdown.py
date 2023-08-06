def shutdown():

    import IPython

    print(F"NOTICE: RESTARTING RUNTIME !!!")

    app = IPython.Application.instance()
    app.kernel.do_shutdown(True)
