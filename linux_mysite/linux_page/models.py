from django import forms
from django.db import models
from modelcluster.fields import (
    ParentalKey,
    ParentalManyToManyField,
)
from wagtail.models import (
    Page,
    Orderable,
    ClusterableModel,
)
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.search import index   # Makes model searchable
from wagtail.snippets.models import register_snippet   # For reusable pieces of content which don’t exist as part of the page tree themselves
from wagtail.contrib.forms.models import (
    AbstractFormField,
    AbstractEmailForm
)
from wagtail.contrib.forms.panels import FormSubmissionsPanel


# HomePage for managing all sections together
class BlogIndexPage(Page, ClusterableModel):
    intro = RichTextField()
    navbar_model = ParentalManyToManyField('linux_page.NavbarModel', blank=True)
    footer_model = ParentalManyToManyField('linux_page.FooterModel', blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        InlinePanel('banners_section', label="Banners section"),
        InlinePanel('about_section', label="About section", max_num=1),   # Limit to one instance
        InlinePanel('design_section', label="Design section", max_num=1),
        InlinePanel('form_page', label="Forms section", max_num=2),
        MultiFieldPanel([
            FieldPanel('navbar_model', widget=forms.CheckboxSelectMultiple),
            FieldPanel('footer_model', widget=forms.CheckboxSelectMultiple),
        ], heading="Header & Footer")
    ]

# Banner section
class Banner(Orderable):
    banner_page = ParentalKey('linux_page.BlogIndexPage', related_name='banners_section', on_delete=models.SET_NULL, null=True)
    banner_title = models.CharField(max_length=200)
    banner_description = models.CharField(max_length=500, blank=False)
    banner_image = models.ImageField(upload_to='banners/')
    panels = [
        FieldPanel('banner_title'),
        FieldPanel('banner_description'),
        FieldPanel('banner_image'),
    ]

# About Us section
class AboutSection(Orderable):
    about_page = ParentalKey('linux_page.BlogIndexPage', related_name='about_section', on_delete=models.SET_NULL, null=True)
    about_title = models.CharField(max_length=200)
    about_description = models.CharField(max_length=500)
    about_image = models.ImageField(upload_to='about/')
    panels = [
        FieldPanel('about_title'),
        FieldPanel('about_description'),
        FieldPanel('about_image'),
    ]

# Design section
class DesignSection(ClusterableModel):
    design_page = ParentalKey('linux_page.BlogIndexPage', related_name='design_section', on_delete=models.SET_NULL, null=True)
    design_title = models.CharField(max_length=200)
    design_description = models.CharField(max_length=500)
    panels = [
        FieldPanel('design_title'),
        FieldPanel('design_description'),
        InlinePanel('design_items', label="Design items"),
    ]

# Design section continue
class DesignItem(Orderable):
    designitem = ParentalKey('linux_page.DesignSection', related_name='design_items', on_delete=models.SET_NULL, null=True)
    designitem_name = models.CharField(max_length=100)
    designitem_image = models.ImageField(upload_to='designs/')
    designitem_price = models.DecimalField(max_digits=6, decimal_places=2)
    panels = [
        FieldPanel('designitem_name'),
        FieldPanel('designitem_image'),
        FieldPanel('designitem_price'),
    ]

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):
    form_page = ParentalKey('linux_page.BlogIndexPage', related_name='form_page', on_delete=models.SET_NULL, null=True)
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
    ]

# Navigationbar section
@register_snippet
class NavbarModel(models.Model):
    '''
    Represents each individual item in the navbar
    '''
    nav_title = models.CharField(max_length=255)
    nav_link_url = models.URLField(blank=True)
    panels = [
        FieldPanel('nav_title'),
        FieldPanel('nav_link_url'),
    ]
    def __str__(self):
        return self.nav_title

# Footer section
@register_snippet
class FooterModel(models.Model):
    footer_title = models.CharField(max_length=200)
    footer_content = models.CharField(max_length=500)
    panels = [
        FieldPanel('footer_title'),
        FieldPanel('footer_content'),
    ]
    def __str__(self):
        return self.footer_title