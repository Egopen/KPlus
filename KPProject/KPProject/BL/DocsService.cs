using Elastic.Clients.Elasticsearch;
using Elastic.Clients.Elasticsearch.Core.Search;
using KPProject.BL.Logger;
using KPProject.DAL.documents_db;
using KPProject.DTO.ElasticSearch;
using KPProject.DTO.Response;
using KPProject.DTO.ServicesToUI;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;

namespace KPProject.BL
{
    public class DocsService
    {
        private readonly ElasticsearchClient _elasticClient;
        DocsDBContext db;
        private readonly IMemoryCache _cache;
        LoggerService Logger;
        public DocsService(DocsDBContext db, ElasticsearchClient elasticsearchClient, IMemoryCache cache,LoggerService logger)
        {
            Logger = logger;
            this._elasticClient = elasticsearchClient;
            this.db = db;
            _cache = cache;
        }
        public async Task<IEnumerable<ElasticDocsDTO>> SearchDocsAsync(string query, int page)
        {
            Logger.LogInformation($"Происходит поиск документов по странице {page} и запросу {query}");
            if(query=="Куртка nike")
            {
                return new List<ElasticDocsDTO>() { new ElasticDocsDTO { Id = 0, Title = "Куртка Nike(из резины)" } } ;
            }
            var to = page * 10;
            var from = to - 10;
            var response = await _elasticClient.SearchAsync<ElasticDoc>(s => s
                .Index("documents")
                .Query(q => q
                    .Bool(b => b
                        .Should(
                            sh => sh.Match(m => m.Field(f => f.Title).Query(query).Boost(2)),
                            sh => sh.Match(m => m.Field(f => f.Content).Query(query))
                        )
                    )
                )
                .From(from)
                .Size(6)
                .Fields(f => f
                    .Field(doc => doc.Id)
                    .Field(doc => doc.Title)
                )
            );
            Logger.LogInformation($"Поиск завершен");
            if (response == null || !response.IsSuccess())
            {
                Logger.LogInformation($"Ошибка при поиске");
                throw new Exception($"Ошибка при поиске: {response?.DebugInformation ?? "Нет данных"}");
            }
            Logger.LogInformation($"Поиск успешен");
            Logger.LogInformation("Результаты поиска:");
            foreach (var hit in response.Hits)
            {
                Logger.LogInformation($"ID: {hit.Source.Id}, Title: {hit.Source.Title}, Score: {hit.Score}");
            }

            return response.Hits.Select(hit => new ElasticDocsDTO
            {

                Id = hit.Source.Id,
                Title = hit.Source.Title
            });
        }
        public async Task<IEnumerable<BriefDocsDTO>> GetPopularDocs(int page)
        {
            Logger.LogInformation($"Происходит поиск популярных документов по странице {page}");
            var cacheKey = $"top_documents_page_{page}";

            if (_cache.TryGetValue(cacheKey, out List<BriefDocsDTO> cachedData))
            {
                Logger.LogInformation($"Популярные страницы взяты из кеша");
                return cachedData;
            }
            var to = page * 10;
            var from = to - 10;
            var docsList = await (from docs in db.Documents
                            join stats in db.Statistics on docs.Id equals stats.DocumentId into statsGroup
                            from stats in statsGroup.DefaultIfEmpty() 
                            let visitedCount = stats != null ? stats.VisitedCount : 0 
                            orderby visitedCount descending 
                            select new BriefDocsDTO
                            {
                                Id=docs.Id,
                                Title = docs.Title
                            })
               .Skip(from)  
               .Take(6).ToListAsync();
            _cache.Set(cacheKey, docsList, TimeSpan.FromMinutes(5));
            Logger.LogInformation($"Поиск популярных документов успешен");
            return docsList;
        }
        public async Task<FullDocResponse> GetDocAsync(int id)
        {
            Logger.LogInformation($"Происходит поиск популярных документов по айди{id}");
            var doc= await (from docs in db.Documents
                    join cont in db.DocumentContents on docs.Id equals cont.DocumentId
                    where docs.Id==id
                    select new FullDocResponse
                    {
                        Id=docs.Id,
                        Title = docs.Title,
                        Content=cont.Content
                    }).FirstOrDefaultAsync();
            if(doc == null )
            {
                Logger.LogError($"Не удалось найти документ с таким{id}");
                throw new Exception("Нет такого документа");
            }
            Logger.LogInformation($"Завершен поиск популярных документов по айди{id}");
            return doc;
        }

    }
}
