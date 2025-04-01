
using KPProject.BL.Logger;
using KPProject.DAL.documents_db;
using KPProject.DAL.documents_db.Models;
using KPProject.DTO.Request;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using Supabase.Interfaces;

namespace KPProject.BL
{
    public class DocsStatsService
    {
        DocsDBContext db;
        LoggerService Logger;
        private readonly Supabase.Client _supabaseClient;
        public DocsStatsService(DocsDBContext db,LoggerService logger, Supabase.Client supabaseClient)
        {
            Logger= logger;
            this.db = db;
            _supabaseClient = supabaseClient;
        }
        public async Task<bool> AddStatsToDocsAsync(AddStatsToDocsDTO stats)
        {
            try
            {
                Logger.LogInformation($"Попытка добавить статистику к документу с id {stats.Id}, время {stats.SpentTime}");
                var statsField = await db.Statistics.FirstOrDefaultAsync((d) => d.DocumentId == stats.Id);
                if (statsField != null)
                {
                    Logger.LogInformation($"Создание новой записи статистики");
                    statsField.VisitedCount++;
                    statsField.AvrTime = (statsField.AvrTime * (statsField.VisitedCount - 1) + stats.SpentTime) / statsField.VisitedCount;
                }
                else
                {
                    Logger.LogInformation($"Запись в уже существующую статистику");
                    Statistic statistic = new Statistic { DocumentId = stats.Id, AvrTime = stats.SpentTime, VisitedCount = 1 };
                    await db.AddAsync(statistic);

                }
                await db.SaveChangesAsync();
            }
            catch (Exception ex) {
                Logger.LogError($"произошла ошибка при попытку добавления статистики: {ex.Message}");
                return false;
            }
            Logger.LogInformation($"Добавление статистики к документу успешно");
            return true;

        }
        public async Task<bool> AddStatsAsync(AddStatsDTO stats)
        {
            var existingStats = await _supabaseClient
                .From<Stats>()
                .Where(s => s.StatName == stats.StatName)
                .Get();

            if (existingStats.Models.Any())
            {
                var stat = existingStats.Models.First();
                stat.Count += stats.Count; 
                var updateResponse = await _supabaseClient
                    .From<Stats>()
                    .Update(stat);

                return updateResponse.Models.Any();
            }
            else
            {
                var newStat = new Stats
                {
                    StatName = stats.StatName,
                    Count = stats.Count,
                    CreatedAt = DateTime.UtcNow 
                };

                var insertResponse = await _supabaseClient
                    .From<Stats>()
                    .Insert(newStat);

                return insertResponse.Models.Any();
            }
        }
    }
}
