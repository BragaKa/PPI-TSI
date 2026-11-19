from api.serializers import FundoImobiliarioSerializer
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from api.models import FundoImobiliario
from django_filters.rest_framework import DjangoFilterBackend


class FundoImobiliarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet que fornece automaticamente as ações padrão de um CRUD completo
    (Create, Read, Update, Delete) para o modelo FundoImobiliario.

    Equivale ao "sanduíche pronto do McDonald's": com pouquíssimas linhas,
    o DRF monta e disponibiliza todos os endpoints necessários.
    """
     
    # 1. Consulta ao Banco (Queryset):
    # Define quais registros do banco serão expostos por este ViewSet.
    # .all() traz todos os fundos imobiliários cadastrados.
    queryset = FundoImobiliario.objects.all()

    # 2. Transformador de Dados (Serializer):
    # Indica qual serializer será usado para validar e converter os dados (JSON <-> Model).
    serializer_class = FundoImobiliarioSerializer

    # 3. Controle de Acesso (Permissions):
    # Restringe o acesso aos endpoints. Neste caso, apenas usuários autenticados
    # (logados) podem visualizar, criar, editar ou excluir os dados.
    permission_classes = [permissions.IsAuthenticated]

    # 4. Backends de Filtro, Busca e Ordenação:
    # Lista, em ordem, os "motores" que o DRF aplica sobre o queryset a cada
    # requisição GET de listagem. Cada backend lê seus próprios parâmetros da URL:
    #   - DjangoFilterBackend -> filtros exatos por campo   (?codigo=HGLG11&setor=logistica)
    #   - SearchFilter        -> busca textual              (?search=hglg)
    #   - OrderingFilter      -> ordenação dos resultados   (?ordering=-dividend_yield_medio_12m)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 4.1 Filtros (DjangoFilterBackend):
    # Campos que podem ser usados como filtro de igualdade exata na URL.
    # Ex.: /api/v1/fundos?setor=logistica  ou  /api/v1/fundos?codigo=HGLG11
    # Os filtros podem ser combinados: /api/v1/fundos?setor=logistica&codigo=HGLG11
    filterset_fields = ['codigo', 'setor']

        # 4.2 Busca textual (SearchFilter):
    # Campos em que o parâmetro ?search= procura o texto informado.
    # Por padrão a busca é "contém", sem diferenciar maiúsculas de minúsculas
    # (icontains) e é aplicada em cada um dos campos abaixo (resultado = união).
    # Ex.: /api/v1/fundos?search=hglg  ou  /api/v1/fundos?search=lajes
    search_fields = ['codigo', 'setor']

    # 4.3 Ordenação (OrderingFilter):
    # Whitelist dos campos que o cliente pode usar em ?ordering=. Campos fora
    # desta lista são ignorados (evita ordenar por colunas não previstas).
    # Prefixo "-" inverte para ordem decrescente: ?ordering=-dividend_yield_medio_12m
    # Vários campos separados por vírgula: ?ordering=setor,-dividend_yield_medio_12m
    ordering_fields = [
        'codigo',
        'setor',
        'dividend_yield_medio_12m',
        'vacancia_financeira',
        'vacancia_fisica',
        'quantidade_ativos',
    ]

    # Ordenação padrão: usada quando a requisição NÃO envia ?ordering=.
    # Também garante uma ordem estável entre as páginas da paginação
    # (sem ela o banco pode devolver registros em ordem arbitrária e o DRF
    # emite o aviso UnorderedObjectListWarning).
    ordering = ['codigo']