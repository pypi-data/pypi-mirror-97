from invoke import task


@task
def prep_project(ctx):
    print(">> Creating virtual env")
    ctx.run("python -m venv venv")
    print(">> Updating pip")
    ctx.run("venv\\Scripts\\python.exe -m pip install pip -U")
    print(">> Installing flit")
    ctx.run("venv\\Scripts\\python.exe -m pip install flit")
    print(">> Installing flit dependencies")
    ctx.run("venv\\Scripts\\python.exe -m flit install")
