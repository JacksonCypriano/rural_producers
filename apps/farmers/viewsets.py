import logging
from rest_framework import viewsets
from .models import Farmer, Farm, Harvest, Crop
from .serializers import FarmerSerializer, FarmSerializer, HarvestSerializer, CropSerializer

logger = logging.getLogger('farmers')

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        try:
            for param, value in self.request.query_params.items():
                if param in [field.name for field in Farmer._meta.fields]:
                    filter_params[param] = value
                elif '__' in param and param.split('__')[0] in [field.name for field in Farmer._meta.fields]:
                    filter_params[param] = value
            filtered = queryset.filter(**filter_params)
            logger.info(f'FarmerViewSet: filtros aplicados {filter_params}, resultados {filtered.count()}')
            return filtered
        except Exception as e:
            logger.error(f'FarmerViewSet: erro ao filtrar com {filter_params} - {e}', exc_info=True)
            return queryset


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        try:
            for param, value in self.request.query_params.items():
                if param in [field.name for field in Farm._meta.fields]:
                    filter_params[param] = value
                elif '__' in param and param.split('__')[0] in [field.name for field in Farm._meta.fields]:
                    filter_params[param] = value
            filtered = queryset.filter(**filter_params)
            logger.info(f'FarmViewSet: filtros aplicados {filter_params}, resultados {filtered.count()}')
            return filtered
        except Exception as e:
            logger.error(f'FarmViewSet: erro ao filtrar com {filter_params} - {e}', exc_info=True)
            return queryset


class HarvestViewSet(viewsets.ModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        try:
            for param, value in self.request.query_params.items():
                if param in [field.name for field in Harvest._meta.fields]:
                    filter_params[param] = value
                elif '__' in param and param.split('__')[0] in [field.name for field in Harvest._meta.fields]:
                    filter_params[param] = value
            filtered = queryset.filter(**filter_params)
            logger.info(f'HarvestViewSet: filtros aplicados {filter_params}, resultados {filtered.count()}')
            return filtered
        except Exception as e:
            logger.error(f'HarvestViewSet: erro ao filtrar com {filter_params} - {e}', exc_info=True)
            return queryset


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        try:
            for param, value in self.request.query_params.items():
                if param in [field.name for field in Crop._meta.fields]:
                    filter_params[param] = value
                elif '__' in param and param.split('__')[0] in [field.name for field in Crop._meta.fields]:
                    filter_params[param] = value
            filtered = queryset.filter(**filter_params)
            logger.info(f'CropViewSet: filtros aplicados {filter_params}, resultados {filtered.count()}')
            return filtered
        except Exception as e:
            logger.error(f'CropViewSet: erro ao filtrar com {filter_params} - {e}', exc_info=True)
            return queryset
