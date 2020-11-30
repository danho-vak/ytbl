from django.db import models

# Create your models here.
class Coordinates(models.Model):
    lot_number = models.CharField(max_length=100) # 수거함과 폐전지함 위치가 동일 한 경우를 대비해 unique는 주지 않음
    latitude = models.FloatField()
    longitude = models.FloatField()
    detail_info = models.CharField(null=True, default='', max_length=150) # 상세 위치
    type_code = models.SmallIntegerField() # type 1: 헌옷 수거함, type 2: 배터리/형광등 수거함
    is_next_to = models.SmallIntegerField() # True: 옆에 배터리/형광등도 같이 있음

    # bulk_create로 csv를 집어넣음
    # import csv
    # from ytbl.models import Coordinates
    #
    # hand = open('../../[name.csv]')
    # reader = csv.reader(hand)
    # bulk_list = []
    # for row in reader:
    #     bulk_list.append(Coordinates(lot_number=row[0],
    #                                  latitude=row[1],
    #                                  longitude=row[2],
    #                                  detail_info=row[3],
    #                                  type_code=row[4]),
    #                                  is_next_to=row[5]))
    # Coordinates.objects.bulk_create(bulk_list)


