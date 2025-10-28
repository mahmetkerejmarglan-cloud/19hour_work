from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter

from app import oauth2
from .. import schemas,utils,model, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, Union,List
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags = ['posts_i_creatd'])



@router.get("/",response_model = List[schemas.PostOut])
#@router.get("/")
def get_all_post(db: Session = Depends(get_db), current_user : int  = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    #  posts = cursor.fetchall()
    print(limit)
    posts =db.query(model.Post,func.count(model.Vote.post_id).label('likes')).join(
        model.Vote,model.Vote.post_id == model.Post.id,isouter=True).group_by(model.Post.id).filter(
        model.Post.title.contains(search)).limit(limit).offset(skip).all()

    #results = db.query(model.Post,func.count(model.Vote.post_id).label('likes')).join(
        #model.Vote,model.Vote.post_id == model.Post.id,isouter=True).group_by(model.Post.id).all()

    
    
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model = schemas.Post)
def cr_posts(post: schemas.PostCreate,db: Session = Depends(get_db),current_user : int  = Depends(oauth2.get_current_user)):
    #cursor.execute(
        #"""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """,
        #(post.title, post.content, post.published),
    #)
    #new_post = cursor.fetchone()
    #conn.commit()

    new_post = model.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post


@router.get("/{id}",response_model = schemas.PostOut)
def get_post_by_id(id: int,db: Session =Depends(get_db),current_user : int  = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = db.query(model.Post,func.count(model.Vote.post_id).label('likes')).join(
        model.Vote,model.Vote.post_id == model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    #post = db.query(model.Post).filter(model.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found ",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return  {'message':f"post with id: {id} was not found "}

    return post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int,db: Session = Depends(get_db),current_user : int  = Depends(oauth2.
                                                                                     get_current_user)):
    # cursor.execute("""DELETE FROM  posts WHERE id = %s returning *""", ((id),))
    # del_post = cursor.fetchone()
    # conn.commit()

    # deleting pos
    # find the index in the array
    post_query =db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist",
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"message":"post deleted"}


@router.put("/{id}",response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,db:Session = Depends(get_db),
                current_user : int  = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""",
        #(post.title, post.content, post.published,   id))
   # updated_post = cursor.fetchone()
    #conn.commit()
   post_query =  db.query(model.Post).filter(model.Post.id == id)

   post = post_query.first()


   if post ==  None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist"  )
   
   if post.owner_id != current_user.id:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                           detail = 'Not authorized to perform requested action')
   post_query.update(updated_post.dict(),synchronize_session=False)
   db.commit()
   return post_query.first()