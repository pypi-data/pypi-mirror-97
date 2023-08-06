from django.contrib import admin

from huscy.project_ethics import models


admin.site.register(models.Ethic)
admin.site.register(models.EthicBoard)
