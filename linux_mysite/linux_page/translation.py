from modeltranslation.translator import translator, TranslationOptions
from .models import BlogIndexPage

class BlogIndexPageTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

translator.register(BlogIndexPage, BlogIndexPageTranslationOptions)