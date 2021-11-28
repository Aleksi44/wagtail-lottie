from django.contrib import admin
from .models import LottieAnimation, LottieAnimationImage


class LottieAnimationImageInline(admin.TabularInline):
    model = LottieAnimationImage
    readonly_fields = ('image',)


@admin.register(LottieAnimation)
class LottieAnimationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'uuid')
    readonly_fields = ('name', 'json_file', 'uuid', 'created')
    exclude = ('zip_file',)
    inlines = (LottieAnimationImageInline,)
