from django.db.models.deletion import ProtectedError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ingredients.models import (
    Ingredient, IngredientCategory, IngredientDietaryTag,
    MeasurementUnit, IngredientMeasurementUnit,
)
from recipes.models import Recipe, RecipeCategory
from .mixins import IsOwnerOrModeratorOrReadOnly, ReadWriteSerializerMixin, SetTrackingUserMixin
from .serializers import (
    IngredientSerializer,
    IngredientCategorySerializer,
    IngredientDietaryTagSerializer,
    IngredientMeasurementUnitSerializer,
    IngredientMeasurementUnitListSerializer,
    MeasurementUnitWriteSerializer,
    RecipeCategorySerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
)


class ListCreateIngredientApiView(ListCreateAPIView):
    """
    GET  /api/ingredients/  → list all ingredients (anyone)
    POST /api/ingredients/  → create ingredient (authenticated users)
    """
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.select_related(
        'category', 'default_unit'
    ).prefetch_related(
        'dietary_tag', 'measurement_units__unit'
    ).all().order_by('name')


class RetrieveUpdateDestroyIngredientApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.select_related(
        'category', 'default_unit'
    ).prefetch_related(
        'dietary_tag', 'measurement_units__unit'
    ).all()


class ListCreateIngredientCategoryApiView(SetTrackingUserMixin, ListCreateAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientCategorySerializer
    queryset = IngredientCategory.objects.all().order_by('name')


class RetrieveUpdateDestroyIngredientCategoryApiView(SetTrackingUserMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientCategorySerializer
    queryset = IngredientCategory.objects.all()


class ListCreateIngredientDietaryTagApiView(SetTrackingUserMixin, ListCreateAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientDietaryTagSerializer
    queryset = IngredientDietaryTag.objects.all().order_by('name')


class RetrieveUpdateDestroyIngredientDietaryTagApiView(SetTrackingUserMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = IngredientDietaryTagSerializer
    queryset = IngredientDietaryTag.objects.all()


class ListCreateMeasurementUnitApiView(SetTrackingUserMixin, ListCreateAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = MeasurementUnitWriteSerializer
    queryset = MeasurementUnit.objects.all().order_by('code')


class RetrieveUpdateDestroyMeasurementUnitApiView(SetTrackingUserMixin, RetrieveUpdateDestroyAPIView):
    """
    DELETE relies on Ingredient.default_unit's on_delete=PROTECT — if this
    unit is any ingredient's default_unit, Django raises ProtectedError,
    which is caught here and turned into a clean 409 instead of a 500.
    No other usage checks are applied (matches HTML view behavior).
    """
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = MeasurementUnitWriteSerializer
    queryset = MeasurementUnit.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'error': 'This unit is set as the default unit for one or more ingredients and cannot be deleted.'},
                status=status.HTTP_409_CONFLICT
            )


class ListCreateRecipeCategoryApiView(SetTrackingUserMixin, ListCreateAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = RecipeCategorySerializer
    queryset = RecipeCategory.objects.all().order_by('name')


class RetrieveUpdateDestroyRecipeCategoryApiView(SetTrackingUserMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    serializer_class = RecipeCategorySerializer
    queryset = RecipeCategory.objects.all()


class ListCreateRecipeApiView(ReadWriteSerializerMixin, ListCreateAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    read_serializer = RecipeReadSerializer
    write_serializer = RecipeWriteSerializer
    queryset = Recipe.objects.select_related('category', 'created_by').prefetch_related(
        'recipe_ingredient__ingredient__dietary_tag',
        'recipe_ingredient__ingredient__category',
        'recipe_ingredient__ingredient__default_unit',
        'recipe_ingredient__unit__unit',
    ).all().order_by('name')

    def create(self, request, *args, **kwargs):
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        recipe = write_serializer.save()
        read_serializer = RecipeReadSerializer(recipe, context=self.get_serializer_context())
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateDestroyRecipeApiView(ReadWriteSerializerMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]
    read_serializer = RecipeReadSerializer
    write_serializer = RecipeWriteSerializer
    queryset = Recipe.objects.select_related('category', 'created_by').prefetch_related(
        'recipe_ingredient__ingredient__dietary_tag',
        'recipe_ingredient__ingredient__category',
        'recipe_ingredient__ingredient__default_unit',
        'recipe_ingredient__unit__unit',
    ).all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        recipe = write_serializer.save()
        read_serializer = RecipeReadSerializer(recipe, context=self.get_serializer_context())
        return Response(read_serializer.data)

class AddIngredientMeasurementUnitApiView(APIView):
    """
    GET  /api/ingredients/<id>/units/  → list all measurement units for this ingredient (anyone)
    POST /api/ingredients/<id>/units/  → add or update a measurement unit for an ingredient (owner or moderator)
    """
    permission_classes = [IsOwnerOrModeratorOrReadOnly]

    def get_ingredient(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            return None

    @extend_schema(responses={200: IngredientMeasurementUnitListSerializer(many=True)})
    def get(self, request, pk):
        ingredient = self.get_ingredient(pk)
        if not ingredient:
            return Response({'error': 'Ingredient not found.'}, status=status.HTTP_404_NOT_FOUND)

        units = ingredient.measurement_units.select_related('unit').order_by('unit__code')
        serializer = IngredientMeasurementUnitListSerializer(units, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=IngredientMeasurementUnitSerializer,
        responses={201: IngredientMeasurementUnitSerializer},
    )
    def post(self, request, pk):
        ingredient = self.get_ingredient(pk)
        if not ingredient:
            return Response({'error': 'Ingredient not found.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, ingredient)

        serializer = IngredientMeasurementUnitSerializer(data=request.data)
        if serializer.is_valid():
            imu = serializer.save(ingredient=ingredient)
            return Response({
                'ingredient': ingredient.name,
                'unit_code': imu.unit.code,
                'unit_name_singular': imu.unit.name_singular,
                'unit_name_plural': imu.unit.name_plural,
                'conversion_to_base': imu.conversion_to_base,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteIngredientMeasurementUnitApiView(APIView):
    permission_classes = [IsOwnerOrModeratorOrReadOnly]

    def delete(self, request, pk, unit_id):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            return Response({'error': 'Ingredient not found.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, ingredient)

        try:
            imu = IngredientMeasurementUnit.objects.get(pk=unit_id, ingredient=ingredient)
        except IngredientMeasurementUnit.DoesNotExist:
            return Response({'error': 'Measurement unit not found for this ingredient.'}, status=status.HTTP_404_NOT_FOUND)

        if imu.unit_id == ingredient.default_unit_id:
            return Response(
                {'error': "Cannot delete the ingredient's default unit link."},
                status=status.HTTP_409_CONFLICT
            )

        imu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)