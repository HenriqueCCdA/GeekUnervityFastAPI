from fastapi.routing import APIRouter
from fastapi.requests import Request

from core.configs import settings

router = APIRouter()


templates = settings.TEMPLATES


@router.get("/", name="index")
async def index(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/index.html", context)

@router.get("/about", name="about")
async def about(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/about.html", context=context)


@router.get('/contact', name='contact')
async def contact(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse('home/contact.html', context=context)


@router.get("/pricing", name="pricing")
async def pricing(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/pricing.html", context=context)


@router.get("/faq", name="faq")
async def faq(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/faq.html", context=context)


@router.get("/blog", name="blog")
async def blog(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/blog.html", context=context)


@router.get("/blog_post", name="blog-post")
async def blog_post(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/blog_post.html", context=context)


@router.get("/portfolio", name="portfolio")
async def portfolio(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/portfolio.html", context=context)


@router.get("/portfolio_item", name="portfolio-item")
async def portfolio_item(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("home/portfolio_item.html", context=context)
