from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

LOAD_JQUERY = getattr(settings, 'CROPOVERRIDE_LOAD_JQUERY', True)
SHOW_THUMB = getattr(settings, 'CROPOVERRIDE_SHOW_THUMB', False)

if SHOW_THUMB:
  from sorl.thumbnail import get_thumbnail

class CropOverrideInput (forms.ClearableFileInput):
  def __init__ (self, original, aspect, attrs=None):
    self.original = original
    self.aspect = aspect
    super().__init__(attrs=attrs)

  def render (self, name, value, attrs=None, renderer=None):
    tmp = self.aspect.split('x')
    aspect = float(tmp[0]) / float(tmp[1])

    thumb = ''
    if SHOW_THUMB and value:
      im = get_thumbnail(value, '128x128')
      if hasattr(im, 'url'):
        thumb = '<img alt="" src="%s"><br>' % im.url

    html = super().render(name, value, attrs, renderer=renderer)
    jcrop = """
<div id="crop_%(name)s">
    <a href="javascript: void(0);" onclick="show_cropper('%(name)s', '%(orig)s', %(aspect).2f)">Crop From Original</a>\
    <span id="display_crop_%(name)s"></span>
    <input type="hidden" name="crop_%(name)s" id="id_crop_%(name)s" value=""/>
</div>
    """ % {'name': name, 'orig': self.original, 'aspect': aspect}

    return mark_safe(thumb + html + jcrop)

  class Media:
    css = {'all': ('cropo/js/jcrop/css/jquery.Jcrop.css', 'cropo/js/simplemodal/css/basic.css')}

    if LOAD_JQUERY:
      js = (
        'cropo/js/jquery-1.7.2.min.js',
        'cropo/js/jcrop/js/jquery.Jcrop.min.js',
        'cropo/js/simplemodal/js/jquery.simplemodal.js',
        'cropo/js/cropper.js',
      )

    else:
      js = (
        'cropo/js/jcrop/js/jquery.Jcrop.min.js',
        'cropo/js/simplemodal/js/jquery.simplemodal.js',
        'cropo/js/cropper.js',
      )

class AdminCropOverrideInput (CropOverrideInput):
  pass

class OriginalInput (forms.ClearableFileInput):
  def render (self, name, value, attrs=None, renderer=None):
    thumb = ''
    if SHOW_THUMB and value:
      im = get_thumbnail(value, '128x128')
      if hasattr(im, 'url'):
        thumb = '<img alt="" src="%s"><br>' % im.url

    html = super().render(name, value, attrs, renderer=renderer)
    jcrop = '<input type="hidden" name="orig_%s" id="id_orig_%s" value=""/>' % (name, name)
    if value and hasattr(value, "url"):
      jcrop = '<input type="hidden" name="orig_%s" id="id_orig_%s" value="%s"/>' % (name, name, value.url)

    return mark_safe(thumb + html + jcrop)

class AdminOriginalInput (OriginalInput):
  pass
