using Elastic.Clients.Elasticsearch;
using Elastic.Transport;
using KPProject.BL;
using KPProject.BL.Logger;
using KPProject.DAL.documents_db;
using Microsoft.AspNetCore.Builder;
using Supabase;

namespace KPProject
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            try
            {
                EnvReader.Load(".env");
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }

            string elasticUrl = Environment.GetEnvironmentVariable("ELASTIC_URL");
            string elasticUser = Environment.GetEnvironmentVariable("ELASTIC_USERNAME");
            string elasticPassword = Environment.GetEnvironmentVariable("ELASTIC_PASSWORD");

            var settings = new ElasticsearchClientSettings(new Uri(elasticUrl))
                .Authentication(new BasicAuthentication(elasticUser, elasticPassword))
                .DefaultIndex("documents");

            var elasticClient = new ElasticsearchClient(settings);
            builder.Services.AddSingleton(elasticClient); 

            builder.Services.AddCors();
            builder.Services.AddControllers();
            builder.Services.AddMemoryCache();
            builder.Services.AddSingleton<LoggerService>();
            var url = Environment.GetEnvironmentVariable("SUPABASE_URL");
            var key = Environment.GetEnvironmentVariable("SUPABASE_KEY");
            var options = new SupabaseOptions
            {
                AutoRefreshToken = true,
                AutoConnectRealtime = true,
            };
            builder.Services.AddSingleton(provider => new Supabase.Client(url, key, options));
            builder.Services.AddDbContext<DocsDBContext>();
            builder.Services.AddScoped<ElasticSearchFillingScript>();
            builder.Services.AddScoped<DocsService>();
            builder.Services.AddScoped<DocsStatsService>();
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
                {
                    Title = "Employer Service API",
                    Version = "v1",
                    Description = "API "
                });

                c.AddSecurityDefinition("Bearer", new Microsoft.OpenApi.Models.OpenApiSecurityScheme
                {
                    Name = "Authorization",
                    Type = Microsoft.OpenApi.Models.SecuritySchemeType.Http,
                    Scheme = "bearer",
                    BearerFormat = "JWT",
                    Description = "¬ведите токен"
                });
                c.AddSecurityRequirement(new Microsoft.OpenApi.Models.OpenApiSecurityRequirement
                {
                    {
                        new Microsoft.OpenApi.Models.OpenApiSecurityScheme
                        {
                            Reference = new Microsoft.OpenApi.Models.OpenApiReference
                            {
                                Type = Microsoft.OpenApi.Models.ReferenceType.SecurityScheme,
                                Id = "Bearer"
                            }
                        },
                        Array.Empty<string>()
                    }
                });
                c.OrderActionsBy((apiDesc) => $"{apiDesc.HttpMethod} {apiDesc.RelativePath}");
            });

            var app = builder.Build();

            
            using (var scope = app.Services.CreateScope())
            {
                var elasticSearchFillingScript = scope.ServiceProvider.GetRequiredService<ElasticSearchFillingScript>();
                elasticSearchFillingScript.FillAsync().Wait();  
            }

            app.UseSwagger();
            app.UseSwaggerUI();

            app.UseCors(builder => builder.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod());
            app.UseHttpsRedirection();

            app.UseAuthentication();
            app.UseAuthorization();

            app.MapControllers();
            app.Run();
        }
    }
}
