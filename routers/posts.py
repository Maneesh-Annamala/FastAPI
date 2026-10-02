from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter,HTTPException,status,Depends
from schemas import *
from models import *
from database import get_db
from sqlalchemy import select
from typing import Annotated
from auth import current_user

router = APIRouter(prefix="/api/posts", tags=["Posts"])

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("", response_model=list[PostResponse])
async def get_posts(db: db_dependency):
    result = await db.execute(select(Posts).options(selectinload(Posts.author)).order_by(Posts.date_posted.desc()))
    posts = result.scalars().all()
    return posts

#create post
@router.post("",response_model=PostResponse,status_code=status.HTTP_201_CREATED,)
async def create_post(post: PostCreate, db: db_dependency,current_user : current_user):
    result = await db.execute(select(Users).where(Users.id == current_user.id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found",)

    new_post = Posts(title=post.title,content=post.content,user_id=current_user.id,)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post,attribute_names=["author"])
    return new_post

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: db_dependency):
    result = await db.execute(select(Posts).options(selectinload(Posts.author)).where(Posts.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.put("/{post_id}")
async def update_post_full(post_data : PostCreate,
                           post_id: int, 
                           db: db_dependency,
                           current_user : current_user):
    result = await db.execute(select(Posts).options(selectinload(Posts.author)).where(Posts.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user didn't matched")
    post.title = post_data.title
    post.content = post_data.content
    post.user_id = current_user.id

    await db.commit()
    await db.refresh(post, attribute_names=["author"])
    return post

@router.patch("/{post_id}")
async def update_post_partial(post_data : UpdatePost,
                              post_id: int, 
                              db: db_dependency,
                              current_user : current_user):
    result = await db.execute(select(Posts).where(Posts.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User didn't Matched")

    update_post = post_data.model_dump(exclude_unset=True)
    for field,val in update_post.items():
        setattr(post,field,val)

    await db.commit()
    await db.refresh(post,attribute_names=["author"])
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user : current_user, db: db_dependency):
    result = await db.execute(select(Posts).where(Posts.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User didn't Matched")
    await db.delete(post)
    await db.commit()