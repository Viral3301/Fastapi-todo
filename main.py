from fastapi import FastAPI,Request,Depends,Form
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import date
from database import session, engine
from schemas import Formdata
import starlette.status as status
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = session()
    try: 
        yield db
    finally:
        db.close()


@app.get("/")
async def home(request: Request,db: session = Depends(get_db)):
    all_todos = db.query(models.Post).all()
    return templates.TemplateResponse('home.html',{'request':request,'todo_list':all_todos})

@app.get("/create")
async def createview(request: Request,db: session = Depends(get_db)):
    return templates.TemplateResponse('task_create.html',{'request':request,})

@app.post("/create")
async def create(request: Request,form: Formdata = Depends(Formdata.as_form),db: session = Depends(get_db)):
    new_todo = models.Post(task_title=form.task_title,task_body=form.task_body)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER)


@app.get("/task/{todo_id}")
async def detail(request: Request,todo_id : int,db: session = Depends(get_db)):
    todo = db.query(models.Post).filter(models.Post.id == todo_id)
    return templates.TemplateResponse('task_detail.html',{'request':request,'todo':todo})



@app.get("/task/update/{todo_id}")
async def updateview(request: Request,todo_id : int,db: session = Depends(get_db)):
    return templates.TemplateResponse('task_update.html',{'request':request,'todo_id':todo_id})

@app.post("/task/update/{todo_id}")
async def update(request: Request,todo_id : int,form: Formdata = Depends(Formdata.as_form),db: session = Depends(get_db)):
    todo = db.query(models.Post).filter(models.Post.id == todo_id)
    todo.update({'task_title': form.task_title,'task_body': form.task_body}) 
    db.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER)

@app.get("/task/delete/{todo_id}")
async def create(request: Request,todo_id: int,db: session = Depends(get_db)):
    todo = db.query(models.Post).filter(models.Post.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url,status_code=status.HTTP_303_SEE_OTHER)

