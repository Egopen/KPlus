using Elastic.Clients.Elasticsearch;
using Elastic.Clients.Elasticsearch.Nodes;
using KPProject.DAL.documents_db;
using KPProject.DTO.ElasticSearch;
using static System.Net.Mime.MediaTypeNames;

namespace KPProject
{
    public class ElasticSearchFillingScript
    {
        private readonly DocsDBContext _db;
        private readonly ElasticsearchClient _client;

        public ElasticSearchFillingScript(DocsDBContext db, ElasticsearchClient client)
        {
            _db = db;
            _client = client;
        }

        public async Task FillAsync()
        {
            var el_docs = await GetElasticIdsAsync();
            var docs = _db.Documents.Join(_db.DocumentContents, d => d.Id, dc => dc.DocumentId,
                (d, dc) => new ElasticDoc
                {
                    Id = d.Id,
                    Title = d.Title,
                    Content = dc.Content
                }
                );
            if (docs.Any())
            {
                foreach (var doc in docs)
                {
                    if (!el_docs.Contains(doc.Id.ToString()))
                    {
                        await AddDocumentToElasticAsync(doc);
                    }
                }
            }
        }

        private async Task<HashSet<string>> GetElasticIdsAsync()
        {
            var indexExistsResponse = await _client.Indices.ExistsAsync("documents");
            if (!indexExistsResponse.IsValidResponse)
            {
                var createResponse = await _client.Indices.CreateAsync("documents");

                if (!createResponse.IsSuccess())
                {
                    throw new Exception($"Не удалось создать индекс: {createResponse.DebugInformation}");
                }
            }
            var ids = new HashSet<string>();
            var response = await _client.SearchAsync<object>(s => s
                .Index("documents")
                .Size(10000)
                .SourceIncludes("_id")
            );
            if (response.IsSuccess()) {
                foreach (var hit in response.Hits)
                {
                    ids.Add(hit.Id);
                }
            }
            else
            {
                throw new Exception($"Ошибка при извлечении документов: {response.DebugInformation}");
            }
            return ids;

        }

        private async Task AddDocumentToElasticAsync(ElasticDoc document)
        {
            var indexName = "documents";
            var response = await _client.IndexAsync(document, idx => idx.Index(indexName).Id(document.Id.ToString()));

            if (response.IsValidResponse)
            {
                Console.WriteLine($"Index document with ID {response.Id} succeeded.");
            }
        }
    }
}
