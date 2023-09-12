from rest_framework import serializers
from .models import Advocate, Company


class CompanySerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'

    def get_employee_count(self, obj):
        count = obj.advocate_set.all().count()
        return count


class AdvocateSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Advocate
        fields = [
            'username',
            'bio',
            'company',
        ]
