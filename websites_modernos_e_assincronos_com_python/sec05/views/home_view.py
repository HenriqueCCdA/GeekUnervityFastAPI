from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi import status

from core.configs import settings

router = APIRouter()


@router.get('/', name='index')
async def index(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/index.html', context=context)


@router.get('/about', name='about')
async def about(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/about.html', context=context)


@router.get('/contact', name='contact')
async def contact(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/contact.html', context=context)


@router.get('/pricing', name='pricing')
async def pricing(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/pricing.html', context=context)


@router.get('/faq', name='faq')
async def faq(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/faq.html', context=context)


@router.get('/blog', name='blog')
async def blog(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/blog.html', context=context)


@router.get('/blog_post', name='blog_post')
async def blog_post(request: Request, slug: str = '')-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/blog_post.html', context=context)


@router.get('/portfolio', name='portfolio')
async def portfolio(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/portfolio.html', context=context)


@router.get('/portfolio_item', name='portfolio_item')
async def portfolio_item(request: Request)-> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse('home/portfolio_item.html', context=context)


@router.get("/login", name="get_login")
async def get_login(request: Request) -> Response:
    context = {
        "request": request
    }

    return settings.TEMPLATES.TemplateResponse("login.html", context=context)


@router.post("/login", name="post_login")
async def post_login(request: Request) -> Response:
    response = RedirectResponse(request.url_for("admin_index"), status_code=status.HTTP_302_FOUND)

    return response
