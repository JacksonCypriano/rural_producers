import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from .models import Farm, Crop

logger = logging.getLogger('farmers')

class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            farms = Farm.objects.all()
            crops = Crop.objects.all()

            context.update({
                "total_farms": farms.count(),
                "total_area": farms.aggregate(total=Sum("total_area"))["total"] or 0,
                "farms_by_state": farms.values("state").annotate(count=Count("id")).order_by("-count"),
                "crops_by_name": crops.values("name").annotate(count=Count("id")).order_by("-count"),
                "land_use": farms.aggregate(
                    arable_area=Sum("arable_area"),
                    vegetation_area=Sum("vegetation_area")
                ),
            })

            logger.info(f'DashboardView acessado - fazendas: {context["total_farms"]}, culturas: {crops.count()}')
        except Exception as e:
            logger.error(f'Erro ao gerar contexto do DashboardView: {e}', exc_info=True)
        return context


class DashboardAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            farms = Farm.objects.all()
            crops = Crop.objects.all()

            data = {
                "total_farms": farms.count(),
                "total_area": farms.aggregate(total=Sum("total_area"))["total"] or 0,
                "farms_by_state": list(farms.values("state").annotate(count=Count("id")).order_by("-count")),
                "crops_by_name": list(crops.values("name").annotate(count=Count("id")).order_by("-count")),
                "land_use": farms.aggregate(
                    arable_area=Sum("arable_area"),
                    vegetation_area=Sum("vegetation_area")
                )
            }

            logger.info(f'DashboardAPIView GET - fazendas: {data["total_farms"]}, culturas: {len(data["crops_by_name"])}')
            return Response(data)
        except Exception as e:
            logger.error(f'Erro no DashboardAPIView GET: {e}', exc_info=True)
            return Response({"error": "Erro ao carregar dados do dashboard."}, status=500)
